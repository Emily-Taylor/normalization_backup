import os,sys,inspect
from collections import defaultdict
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import common as c
import normalization as n
c.init()

import yaml, json
import jsonlines
import gzip
from hashlib import sha1
import tabulate
import requests
from requests_aws_sign import AWSV4Sign
import requests_cache
from boto3 import session
from six import string_types
import logging 
logger = logging.getLogger('missing-mapping-processor')
hdlr = logging.FileHandler('/var/tmp/missing-mapping.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

from tqdm import tqdm
import asyncio  


SLACK_URL = 'https://hooks.slack.com/services/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'
REGION_NAME = os.getenv('REGION_NAME','eu-central-1')
OUTGOING_SNS_TOPIC = os.getenv('OUTGOING_SNS_TOPIC','arn:aws:sns:eu-central-1:202439666482:norm-new-item-dev')
INCOMING_SNS_TOPIC = os.getenv('INCOMING_SNS_TOPIC','arn:aws:sns:eu-central-1:202439666482:crawler-new-item')
MISSING_QUEUE_NAME = os.getenv('MISSING_QUEUE_NAME','missing-mapping')

here = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here, "../normalization/mfr/companies-clean-array-v2.json"), "r", encoding="utf-8") as ff:
    mfr_data = json.load(ff)

mfr_name = {}
def process_mfr_data(data):
	global mfr_name
	if len(data) ==1:
		mfr_name[data[0]] = data[0]

	elif  len(data) >1:
		first = data[0]
		for name in data:
			mfr_name[name] = first

for l in mfr_data:
	process_mfr_data(l)


def dict_to_table(res: dict) -> str:
    table = []
    for v in res:
        for vv in res[v]:
            table.append([v,vv,res[v][vv]])
    
    return (tabulate.tabulate(table,headers=["Category","Missing Mapping", "Occurrences"]))


def sent_to_slack(body: dict):
	#data = json.dumps(body)
	response = requests.post(
		
			SLACK_URL, json={"text": "```"+dict_to_table(body)+"```",
			"username": "mapping-bot", "icon_emoji": ":monkey_face:"
			},
			headers={'Content-Type': 'application/json'}
		)
	if response.status_code != 200:
		raise ValueError(
			'Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text)
	)
	return response.status_code


def deep_set(part, value, keys):
		d = part
		for key in keys[:-1]:
				d = d[key]
		d[keys[-1]] = value





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


def get_alias_local(mfr: str, source):
	global mfr_data
	mfr = mfr.lower()
	if mfr in mfr_name:
		new_mfr =  mfr_name.get(mfr.lower())
		return new_mfr
		
	else:
		c.agg.add_category({ "categories": "mfr normalization missing", "key": mfr, "source": source})
		return mfr


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
				return (True,name)
			except:
				logger.error("couldn't parse name out of the respone: \"{}\".".format(data))
		elif response.status_code == 404:
			#logger.error("mfr mapping not found for \"{}\".".format(mfr))
			return (False,mfr)
		else:
			return (False,mfr)
	else:
		logger.error('alias is not a string')
		return mfr

async def check_mappging(part: dict, source: str, ts: int, mapping: dict)):
	if 'mfr' in part:
		mfr = part['mfr']
		mfr.lower()
	if mfr in mfr_name:
		new_mfr =  mfr_name.get(mfr.lower())
		return new_mfr
		
	else:
		c.agg.add_category({ "categories": "mfr normalization missing", "key": mfr, "source": source})
		return mfr
	yield missing_mapping



async def adjust_structure(part: dict, source: str, ts: int, mapping: dict): 
		part = defaultdict(dict, part)
		# fix mfr before everything
		if 'mfr' in part:
				mfr = part['mfr']
				#print(mfr,source)
				part['mfr'] = get_alias_local(mfr, source)
				#print(part['mfr'])	
				#found, mfr = get_alias(part['mfr'])
				#if found:
				#	part['mfr'] = mfr
				#elif not found:
				#	part['mfr'] = mfr
				#	agg.add_item({"categories":"mfr_normalization_missing","key":mfr, "source": source})
		# keep desciprtion
		if 'description' in part:
				raw_desc = part['description']
				part['description_raw'] = {}
				part['description_raw'][source] = raw_desc
		# fix category before normalization
		if 'categories' in part:
				raw_categories = part['categories']
				part['categories_raw'] = {}
				part['categories_raw'][source] = raw_categories
		# remove availablity and pricing, minimum_quantity and packagecase
		part.pop('availability', None)
		part.pop('pricing', None)
		part.pop('packagecase', None)
		part.pop('minimum_quantity', None)
		for key in list(part):
				# apply norm
				if key in mapping[source]:
						try:
								# attempt to apply functions
								if 'actions' in mapping[source][key]:
										functions = mapping[source][key]['actions']
										for f in functions:
												# print(f,key)
												new_val = eval(
														"n." + f + "({})".format("part['" + key + "']"))
												part[key] = new_val
						except BaseException:
								raise ValueError("something wrong with functions")

						# check for new keys name
						if isinstance(mapping[source][key]['output_key'], list):
								t_res = dict(
										zip(mapping[source][key]['output_key'], part[key]))
								# print(t_res.keys()	)
								for k in t_res.keys():
										if '.' not in k:
												#print("handling double key, no nesting")
												part[k] = t_res[k]
										else:
												#print("handling double key, with nesting")
												keys = k.split('.')
												# print(k,keys,part[key])
												deep_set(part, t_res[k], keys)
												if key in part:
														part.pop(key)
								if part[key] != mapping[source][key]['output_key']:
										part.pop(key)
						else:
								if '.' not in mapping[source][key]['output_key']:
										#print("handling single key, no nesting")
										new_key = mapping[source][key]['output_key']
										part[new_key] = part.pop(key)
								else:
										#print("handling single key, with nesting")
										keys = mapping[source][key]['output_key'].split('.')
										deep_set(part, part[key], keys)
										# finish the job
										part.pop(key)

				else:
						#print("{0} not in mapping".format(key))
						# call missing-mapping queue with the source, categories and
						# missing mapping key.
						#c.send_msg(json.dumps({"source": source, "categories": part['categories'], "key": key}))
						c.agg.add_category({"categories": ("digikey/"+"__".join(part['categories']).replace(" ","_")).lower() ,"key":key, "source": source})
						#print(json.dumps({"source": source, "categories": part['categories'], "key": key}))
						# we are going to continue in order to prevent writing json that's
						# not fully mapped
						continue
		# fix lifecycle/life
		if 'life' in part:
				new_life = part.pop('life')
				part['life'] = {}
				part['life'][source] = new_life
		# fix SKU
		if 'sku' in part:
				new_sku = part.pop('sku')
				part['sku'] = {}
				part['sku'][source] = new_sku
		# fix links
		if 'links' in part:
				new_links = part.pop('links')
				part['links'] = {}
				part['links'][source] = new_links
		# generate IDs
		if 'mpn' in part and 'mfr' in part:
				id = (part['mpn'] + part['mfr']).lower().replace(" ", "")
				hash_object = sha1(id.encode('utf-8'))
				hex_dig = hash_object.hexdigest()
				part['id'] = hex_dig
				# print(part['id'])
		elif 'mpn' in part:
				id = part['mpn'].lower().replace(" ", "")
				hash_object = sha1(id.encode('utf-8'))
				hex_dig = hash_object.hexdigest()
				part['id'] = hex_dig
				# print(part['id'])
		else:
				logger.error("can't find MPN on part!")
				return False
		
				#adding timestamp ts.
		part['ts'] = ts
		# last big modification of the structure of the json
		# we want to stuff everything but [mfr, mpn, category, sku, links,
		# description, lifecycle] as nested properties.
		main_keys = [
				'mfr',
				'mpn',
				'categories',
				'categories_raw',
				'sku',
				'links',
				'description',
				'lifecycle',
				'properties',
				'id',
				'ts']
		part['properties'] = {}
		for k in list(part):
				if k not in main_keys:
						#print("{0} not in main_keys".format(k))
						part['properties'][k] = part.pop(k, None)
		return part


# read mapping file
async def processs_everything():
	here = os.path.dirname(os.path.realpath(__file__))
	with open(os.path.join(here, '../key-mapping.yml'), 'r') as f, jsonlines.Reader(gzip.open(os.path.join(here, '../data-full/digikey/large_digikey.ndjson.gz'))) as reader:
		mapping = yaml.load(f)
		for obj in tqdm(reader):
			ts = obj['ts']
			source = obj['source']
			for part in obj['parts']:
				#print(part.keys())
				 part = await adjust_structure(part, source, ts, mapping)
		
loop = asyncio.get_event_loop()
loop.run_until_complete(processs_everything())

#print tabluar output
print(dict_to_table(c.agg.items))
sent_to_slack(c.agg.items)
loop.close()
