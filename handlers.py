import asyncio
import aiohttp
import json
URL  =  'https://6q9kqpdeof.execute-api.eu-central-1.amazonaws.com/production/entity/parts'
import yaml
import os
import normalization_service.normalization as n
import normalization_service.common as c

import logging 
from collections import defaultdict
from hashlib import sha1


here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here,'mapping.yml'), 'r') as f:
    mapping = yaml.load(f)

@asyncio.coroutine
async def post_data(data):
	async with aiohttp.ClientSession() as session:
		async with session.post(url=URL,json=data) as resp:
			return resp


def deep_set(part,value,keys):
    d = part
    for key in keys[:-1]:
        d = d[key]
    d[keys[-1]] = value


async def norm_handler(message, *args):
	if 'parts' in message:

		if 'source' in message:
			source = message['source']
		else:
			logging.warning("could not find source (distributor) in message")
			return False
		for part in message['parts']:
			part = defaultdict(dict,part)
			for key in list(part): 
				# apply norm
					if key in mapping[source]:
						try:
							#attempt to apply functions
							if 'actions' in mapping[source][key]:
								functions = mapping[source][key]['actions']
								for f in functions:
									#print(f,key)
									new_val = eval("n."+f+"({})".format("part['"+key+"']"))
									part[key] = new_val
						except:
							raise ValueError("something wrong with functions") 

						#check for new keys name
						if isinstance(mapping[source][key]['output_key'],list):
							t_res =  dict(zip(mapping[source][key]['output_key'], part[key]))
							#print(t_res.keys()	)
							for k in t_res.keys():
								if '.' not in k:
									#print("handling double key, no nesting")
									part[k] = t_res[k]
								else:
									#print("handling double key, with nesting")
									keys = k.split('.')
									#print(k,keys,part[key])
									deep_set(part,t_res[k],keys)
									if key in part:
										part.pop(key)
							if part[key] != mapping[source][key]['output_key']:
								part.pop(key)
						else:
							if '.' not in mapping[source][key]['output_key']:
								#print("handling single key, no nesting")
								new_key = mapping[source][key]['output_key']
								part[new_key] =part.pop(key)
							else:
								#print("handling single key, with nesting")
								keys = mapping[source][key]['output_key'].split('.')
								deep_set(part,part[key],keys) 
								#finish the job
								part.pop(key)

					else:
						print("{0} not in mapping".format(key))
						#call missing-mapping queue with the source, categories and missing mapping key.
						c.send_msg(json.dumps({"source":source, "categories":part['categories'],"key":key}))
						# we are going to continue in order to prevent writing json that's not fully mapped
						continue
			#fix pricing
			if 'pricing' in part:
				new_pricing = part.pop('pricing')
				part['pricing'] = {}
				part['pricing'][source] = new_pricing
			#fix SKU
			if 'sku' in part:
				new_sku = part.pop('sku')
				part['sku'] = {}
				part['sku'][source] = new_sku
			#fix links
			if 'links' in part:
				new_links = part.pop('links')
				part['links'] = {}
				part['links'][source] = new_links
			#fix availablity
			if 'availability' in part:
				new_availability = part.pop('availability')
				#part['availability'] = {}
				part['availability'][source] = new_availability
			#generate IDs
			if 'mpn' in part and 'mfr' in part:
				
				
				id = (part['mpn']+part['mfr']).lower().replace(" ","")
				hash_object = sha1(id.encode('utf-8'))
				hex_dig = hash_object.hexdigest()
				part['id'] = hex_dig
				#print(part['id'])
			elif 'mpn' in part:
				id = part['mpn'].lower().replace(" ","")
				hash_object = sha1(id.encode('utf-8'))
				hex_dig = hash_object.hexdigest()
				part['id'] = hex_dig
				#print(part['id'])
			else:
				logging.error("can't find MPN on part!")
				return False 
			
			# post data after normalization
			
			#print("going to post part:\n")
			#print(part)
			result = await post_data(part)
			print(result)				
	return True


async def error_handler(exc_type, message):
	print('exception {} received'.format(exc_type))
	# do not delete the message that originated the error
	return  False
