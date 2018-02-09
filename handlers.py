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
			part['id'] = part.pop('mpn')
			result = await post_data(part)
			print(result)
	return True


async def error_handler(exc_type, message):
	print('exception {} received'.format(exc_type))
	# do not delete the message that originated the error
	return  False
