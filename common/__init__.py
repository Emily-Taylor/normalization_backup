import os
import yaml
import boto3

here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here,'config.yml'), 'r') as f:
    config = yaml.load(f)

# Get the service resource
sqs = boto3.resource('sqs', region_name=config['region_name'])

# Get the queue
queue = sqs.get_queue_by_name(QueueName=config['missing_queue_name'])

def send_msg(msg):
    response = queue.send_message(
    MessageBody=msg
    )
    # message ID and MD5
    return(response.get('MessageId'),response.get('MD5OfMessageBody'))


# stuff related to sending signed requests to  mfr service
import requests
from requests_aws_sign import AWSV4Sign
import requests_cache
from boto3 import session
from six import string_types
import logging as logger

#get running enviroment  - necessariy for URL
env =os.environ.get('ENV', "dev")


# Establish credentials using boto3
session = session.Session()
credentials = session.get_credentials()
region = session.region_name or 'eu-central-1'

#set urls for the two functions
uri_alias =  "https://app-{env}.sourcingbot.com/entity/manufacturer/alias/{name}"
uri_full =  "https://app-{env}.sourcingbot.com/entity/manufacturer/{name}"
headers={"Content-Type":"application/json"}
service = 'execute-api'
auth=AWSV4Sign(credentials, region, service)

#start caching requests 
requests_cache.install_cache(backend='memory')

def get_alias(mfr):
    if isinstance(mfr, string_types):
        #turn to lower case
        mfr = mfr.lower()
        url = uri_alias.format_map({"name":mfr, "env":env})
        response= requests.get(url, auth=auth, headers=headers)
        if response.ok:
            logger.info('result from cache {0}'.format(response.from_cache))
            data = response.json()
            return data
        else:
            return False
    else:
        logger.error('alias is not a string')
        return False

def get_full(mfr):
    if isinstance(mfr, string_types):
        url = uri_full.format_map({"name":mfr, "env":env})
        response= requests.get(url, auth=auth, headers=headers)
        if response.ok:
            data = response.json()
            return data
        else:
            return False
    else:
        logger.error('alias is not a string')
        return False

def normalize_mfr(mfr: str):
    data = {"mfr": { "main":"","aliases":[]}}
    if isinstance(mfr, string_types):
        alias = get_alias((mfr))
        if alias:
            if 'data' in alias and 'parent' in alias['data']:
                main = alias['data']['parent']
                data['mfr']['main'] = main
                alias2 =  get_full(main)
                if 'data' in alias2 and 'alias' in alias2['data']:
                    data['mfr']['aliases'] = alias2['data']['alias']
            return data
        elif not alias:
            logger.error("mfr mapping not found. normalization wasn't done.")
            data['mfr']['main'] = mfr.lower()
            return data
    else:
        logger.error('bad mfr mapping received')
        data['mfr']['main'] = mfr.lower()
        return data