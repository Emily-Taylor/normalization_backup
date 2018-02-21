import asyncio
import aiohttp
import json
URL  =  'https://6q9kqpdeof.execute-api.eu-central-1.amazonaws.com/production/entity/parts'
import yaml
import os
import normalization_service.normalization as n
import logging 

here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here,'mapping.yml'), 'r') as f:
    mapping = yaml.load(f)

@asyncio.coroutine
async def post_data(data):
	async with aiohttp.ClientSession() as session:
		async with session.post(url=URL,json=data) as resp:
			return resp


async def norm_handler(message, *args):
	if 'parts' in message:
		if 'source' in message:
			source = message['source']
		else:
			logging.warning("could not find source (distributor) in message")
			return False
		for part in message['parts']:
			for key in list(part): 
				# apply norm
					if key in mapping[source]:
						try:
							#attempt to apply functions
							if 'actions' in mapping[source][key]:
								functions = mapping[source][key]['actions']
								for f in functions:
									part[key] = eval("n."+f+"({})".format("part['"+key+"']"))
						except:
							raise ValueError("something wrong with functions") 

						#check for new keys name
						if isinstance(mapping[source][key]['output_key'],list):
							t_res =  dict(zip(mapping[source][key]['output_key'], part[key]))
							for k in t_res.keys():
								part[k] = t_res[k]
							if part[key] != mapping[source][key]['output_key']:
								part.pop(key)
						else:
							new_key = mapping[source][key]['output_key']
							part[new_key] =part.pop(key)
					else:
						print("{0} not in mapping".format(key))
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

			# post data after normalization
			result = await post_data(part)
			print(result)				
	return True


async def error_handler(exc_type, message):
	print('exception {} received'.format(exc_type))
	# do not delete the message that originated the error
	return  False
