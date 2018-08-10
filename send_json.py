import logging
import os
import inspect
import sys
import json
import gzip
import fire
import jsonlines
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm
from functions import adjust_structure

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# get running enviroment  - necessariy for URL
stage = os.environ.get('stage', "dev")
STREAM_NAME = os.environ.get('STREAM_NAME', 'crawler-data-raw-dev')

# invoke kinesis single records
# client_kinesis = boto3.client('kinesis')


logger = logging.getLogger('replay-raw')
hdlr = logging.FileHandler('/var/tmp/replay-raw.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

import time

# set SQS parameters

REGION_NAME = os.getenv('REGION_NAME','eu-central-1')
test_queue_name = os.getenv('test_queue_name','testQ')
sqs = boto3.resource('sqs', region_name=REGION_NAME)

# Get the queue
queue = sqs.get_queue_by_name(QueueName=test_queue_name)

def publish_sqs_single(part, source, ts):
    """
    Pushes each part at a time in SQS
    """
    
    try:
        part_normed = adjust_structure(part, source, ts)
        response = queue.send_message(MessageBody=json.dumps(part_normed))
        return response
    except ClientError as err:
        print(err)
        time.sleep(1)
        return err

def send_file_sqs(filename):
    """
    Send data to SQS, one record at a time
    Pushes each part in publish_sqs_single, which processes
    and publishes data in queue
    """
    here = os.path.dirname(os.path.realpath(__file__))
    with jsonlines.Reader(gzip.open(os.path.join(here, filename))) as reader:
        tqdm.monitor_interval = 0
        for obj in tqdm(reader):
            for part in obj['parts']:
                res = publish_sqs_single(part, obj['source'], obj['ts'])
                if res['ResponseMetadata']['HTTPStatusCode'] != 200:
                    print(res)


if __name__ == '__main__':
    fire.Fire()
