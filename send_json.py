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
# stage = os.environ.get('stage', "dev")
# STREAM_NAME = os.environ.get('STREAM_NAME', 'crawler-data-raw-dev')

# set logger
logger = logging.getLogger('replay-raw')
hdlr = logging.FileHandler('/var/tmp/replay-raw.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)


# set SQS parameters

REGION_NAME = os.getenv('REGION_NAME','eu-central-1')
test_queue_name = os.getenv('test_queue_name','testQ')
sqs = boto3.resource('sqs', region_name=REGION_NAME)

# Get the queue
queue = sqs.get_queue_by_name(QueueName=test_queue_name)

def publish_sqs_single(output):
    """
    Pushes each batch of parts (25 max) at a time in SQS
    """
    try:
        response = queue.send_message(MessageBody=json.dumps(output))
        return response
    except ClientError as err:
        print(err)
        return err
    

def send_file_sqs(filename):
    """
    Send data to SQS, one record at a time
    Pushes each batch of parts in publish_sqs_single, which processes
    and publishes data in queue
    """
    here = os.path.dirname(os.path.realpath(__file__))
    with jsonlines.Reader(gzip.open(os.path.join(here, filename))) as reader:
        tqdm.monitor_interval = 0
        for obj in tqdm(reader):
            output = []
            for part in obj['parts']:
                part_normed = adjust_structure(part, obj['source'], obj['ts'])
                output.append(part_normed)
            res = publish_sqs_single(output)
            if res['ResponseMetadata']['HTTPStatusCode'] != 200:
                print(res)

                
if __name__ == '__main__':
    fire.Fire()
