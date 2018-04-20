import os
import yaml
import boto3
import json
here = os.path.dirname(os.path.realpath(__file__))

# this is deprecated
with open(os.path.join(here,'config.yml'), 'r') as f:
	config = yaml.load(f)

REGION_NAME = os.getenv('REGION_NAME')
OUTGOING_SNS_TOPIC = os.getenv('OUTGOING_SNS_TOPIC')
INCOMING_SNS_TOPIC = os.getenv('INCOMING_SNS_TOPIC')
MISSING_QUEUE_NAME = os.getenv('MISSING_QUEUE_NAME')


client = boto3.client('sns', region_name=REGION_NAME)

#post to sns
def publish_data(data: dict):
	response = client.publish(
	TopicArn=OUTGOING_SNS_TOPIC,
	Message=json.dumps(data),
	Subject='normalized-data')
	return response

#post to sns
def publish_data_test(data: dict):
	response = client.publish(
	TopicArn=INCOMING_SNS_TOPIC,
	Message=json.dumps(data),
	Subject='crawler-data')
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