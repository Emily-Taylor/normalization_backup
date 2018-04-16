from lambda_decorators import dump_json_body
import yaml
import json
import common as c 
import normalization as n
import os

@dump_json_body
def ping(event, context):
	 return {
		  "statusCode": 200,
		  "body": {
				"message": "Pong!"
		  },
	 }


import logging 
from collections import defaultdict
from hashlib import sha1


here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here,'mapping.yml'), 'r') as f:
	 mapping = yaml.load(f)




def deep_set(part,value,keys):
	 d = part
	 for key in keys[:-1]:
		  d = d[key]
	 d[keys[-1]] = value

@dump_json_body

def norm_handler(event, *args):
	if 'Records' in event:
		if event['Records'][0]['EventSource'] == 'aws:sns':
			print("we're doing sns")
			message = event['Records'][0]['Sns']['Message']
	if len(args)> 0:
		context = args[0]
		print("we're probs doing REST")
	if context.function_name =='Fake':
		print("found Fake in context, we are in testing")
		if context.function_name =='Fake':
			rest_call = True
			message = event
	# we aren't supposed to have context in sns
	elif context:
		rest_call = True
		message = event
	output = {'parts':[]}
	if 'parts' in message:
		if 'source' in message:
			source = message['source']
		else:
			logging.warning("could not find source (distributor) in message")
			return False
		for part in message['parts']:
			part = defaultdict(dict,part)
			#fix mfr before everything
			if 'mfr' in part:
				mfr = c.normalize_mfr(part['mfr'])
				part['mfr'] =mfr['mfr']
			#keep desciprtion
			if 'description' in part:
				raw_desc = part['description']
				part['description_raw'] = {}
				part['description_raw'][source] = raw_desc
			#fix category before normalization
			if 'categories' in part:
				raw_categories = part['categories']
				part['categories_raw'] = {}
				part['categories_raw'][source] = raw_categories
			#remove availablity and pricing, minimum_quantity
			part.pop('availability', None)
			part.pop('pricing', None)
			part.pop('minimum_quantity', None)
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
			#fix lifecycle/life
			if 'life' in part:
				new_life = part.pop('life')
				part['life'] = {}
				part['life'][source] = new_life
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
			#generate IDs
			if 'mpn' in part and 'mfr' in part:
				id = (part['mpn']+part['mfr']['main']).lower().replace(" ","")
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
			# last big modification of the structure of the json
			# we want to stuff everything but [mfr, mpn, category, sku, links, description, lifecycle] as nested properties.
			main_keys = ['mfr', 'mpn', 'categories','categories_raw', 'sku', 'links', 'description', 'lifecycle','properties','id']
			part['properties'] = {}
			for k in list(part):
				if k not in main_keys:
					#print("{0} not in main_keys".format(k))
					part['properties'][k] = part.pop(k, None)
		output['parts'].append(part)
	#print("length of payload: {}".format(len(json.dumps(output).encode("utf8"))))
	if not rest_call:
		print(c.publish_data(output))
	return output
