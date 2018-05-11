import os
from collections import defaultdict
import yaml
import boto3
import json
import random
from datetime import datetime
here = os.path.dirname(os.path.realpath(__file__))


# this is deprecated
with open(os.path.join(here,'config.yml'), 'r') as f:
  config = yaml.load(f)

stage =os.environ.get('stage', "dev")
REGION_NAME = os.getenv('REGION_NAME','eu-central-1')
OUTGOING_KINESIS_TOPIC = os.getenv('OUTGOING_KINESIS_TOPIC','arn:aws:kinesis:eu-central-1:202439666482:stream/norm-new-item-dev')
INCOMING_SNS_TOPIC = os.getenv('INCOMING_SNS_TOPIC','arn:aws:sns:eu-central-1:202439666482:crawler-new-item')
MISSING_QUEUE_NAME = os.getenv('MISSING_QUEUE_NAME','missing-mapping')



class Records:
  def __init__(self, init_items =[]):
    self.items = init_items

  def add_item(self, item):
    self.items.append(item) 
    
def build_records(data: dict):
  obj = json.dumps(data)
  output = {	'Data': obj,
          'PartitionKey': "normalized_data"
        }
  return output

# invoke kinesis single records
client_kinesis = boto3.client('kinesis', region_name=REGION_NAME)

# invoke kinesis multiple records
def publish_kinsis_records(RecordKinesis):
  response = client_kinesis.put_records(
    StreamName=OUTGOING_KINESIS_TOPIC,
    Records=RecordKinesis
  )
  return response

# invoke kinesis single records
def publish_kinesis_single(record: dict):
  obj = json.dumps(record)
  response = client_kinesis.put_record(
    StreamName=OUTGOING_KINESIS_TOPIC,
    Data=obj,
    PartitionKey="normalized_data"
  )
  return response


# Get the service resource
sqs = boto3.resource('sqs', region_name=REGION_NAME)

# Get the queue
queue = sqs.get_queue_by_name(QueueName=MISSING_QUEUE_NAME)

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
stage =os.environ.get('stage', "dev")


# Establish credentials using boto3
session = session.Session()
credentials = session.get_credentials()
region = session.region_name or REGION_NAME

#set urls for the two functions
uri_alias = "https://app-{stage}.sourcingbot.com/entity/manufacturer/alias/{name}"
uri_full = "https://app-{stage}.sourcingbot.com/entity/manufacturer/{name}"
headers={"Content-Type":"application/json"}
service = 'execute-api'
auth=AWSV4Sign(credentials, region, service)

#start caching requests 
requests_cache.install_cache(backend='memory')

def get_alias(mfr: str):
  if isinstance(mfr, string_types):
    #turn to lower case
    mfr = mfr.lower()
    url = uri_alias.format_map({"name":mfr, "stage":stage})
    response= requests.get(url, auth=auth, headers=headers)
    if response.ok:
      logger.info('result from cache {0}'.format(response.from_cache))
      data = response.json()
      try:
        name =  data['data']['name']
        return name
      except:
        logger.error("couldn't parse name out of the respone: \"{}\".".format(data))
    elif response.status_code == 404:
      logger.error("mfr mapping not found for \"{}\".".format(mfr))
      return mfr
    else:
      return mfr
  else:
    logger.error('alias is not a string')
    return mfr

def get_full(mfr):
  if isinstance(mfr, string_types):
    url = uri_full.format_map({"name":mfr, "stage":stage})
    response= requests.get(url, auth=auth, headers=headers)
    if response.ok:
      data = response.json()
      return data
    else:
      return False
  else:
    logger.error('alias is not a string')
    return False

with open('../normalization/mfr/array.json', 'r') as f:
    mapping = json.load(f)
mapping_dict = {}
for i in mapping:
    if len(i) == 1:
        mapping_dict[i[0].lower()] = i[0].lower()
    if len(i) >1:
        for name in i:
            mapping_dict[name.lower()] = i[0].lower()
# this is the static file version of mfr mapping
def get_mfr_mapping(mfr):
    mfr = mfr.lower()
    if mfr in mapping_dict:
        return mapping_dict[mfr]
    else:
        print('error - missing mfr mapping for: "{}"'.format(mfr))
        return mfr 
class MissingMappingResults:
  """
  Description : Aggregator for items
  """

  def __init__(self, init_items = defaultdict(dict)):
    self.items = init_items

  def add_category(self, item):
    cat = item['categories']
    key = item['key']
    source = item['source']
    normalized_key = cat
    
    if normalized_key not in self.items:
      self.items[normalized_key] = {}
    if key not in self.items[normalized_key]:
      self.items[normalized_key][key] = 0
    self.items[normalized_key][key] += 1
  def add_item(self, item):
    cat = item['categories']
    key = item['key']
    source = item['source']
    normalized_key = source+"/"+"__".join(cat).replace(" ","_").lower()
    if normalized_key not in self.items:
      self.items[normalized_key] = {}
    if key not in self.items[normalized_key]:
      self.items[normalized_key][key] = 0
    self.items[normalized_key][key] += 1

def init():
  global agg
  agg = MissingMappingResults()


def now():
  d = datetime.now()
  #return d.isoformat()
  return int(d.strftime("%s%f")[:-3])
