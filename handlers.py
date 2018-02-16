import asyncio
import aiohttp
import json
URL  =  'https://6q9kqpdeof.execute-api.eu-central-1.amazonaws.com/production/entity/parts'

@asyncio.coroutine
async def post_data(data):
	async with aiohttp.ClientSession() as session:
		async with session.post(url=URL,json=data) as resp:
			return resp


async def norm_handler(message, *args):
	print('message is {}'.format(message))
	print('args is {}'.format(args))
	if 'parts' in message:
		print("found parts")
		for part in message['parts']:
			#part['id'] = part.pop('mpn')
				for key in list(part): 
				# apply norm
					if key in mapping['digikey']:
						try:
							if 'actions' in mapping['digikey'][key]:
								functions = mapping['digikey'][key]['actions']
								for f in functions:
								#
									new_val = eval("n."+f+"({})".format("part['"+key+"']"))
									part[key] = eval("n."+f+"({})".format("part['"+key+"']"))
									

						except:
							raise ValueError("something wrong with functions") 
						#check for new keys name
						if isinstance(mapping['digikey'][key]['output_key'],list):
							t_res =  dict(zip(mapping['digikey'][key]['output_key'], part[key]))
							for k in t_res.keys():
								part[k] = t_res[k]
							part.pop(key)
						else:
							new_key = mapping['digikey'][key]['output_key']
							part[new_key] =part.pop(key)

		else:
			print("{0} not in mapping".format(i))
		
		part['id'] = part.pop('mpn')
		result = await post_data(part)
		print(result)
	return True


async def error_handler(exc_type, message):
	print('exception {} received'.format(exc_type))
	# do not delete the message that originated the error
	return  False
