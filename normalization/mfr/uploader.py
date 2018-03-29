import json
# aiohttp doesn't work nicely with aws v4 signed request
import asyncio
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, as_completed
import requests
from requests_aws_sign import AWSV4Sign
from boto3 import session
#from tqdm import tqdm
import os,sys
import threading

# Establish credentials
session = session.Session()
credentials = session.get_credentials()
region = session.region_name or 'eu-central-1'

def post_data(data):
    uri =  "https://app-dev.sourcingbot.com/entity/manufacturer"
    headers={"Content-Type":"application/json"}
    service = 'execute-api'
    auth=AWSV4Sign(credentials, region, service)
    response = requests.post(uri, auth=auth, headers=headers,json=data)
    return response


def process(data):
    #print("original data: " str(data))
    response = []
    if len(data) ==1:
        data  = { "name": data[0], "alias": data[0]}
        #print(json.dumps(data))
        response.append(post_data(data))

    elif  len(data) >1:
        first = data[0]
        for name in data:
            #print("name: {0}".format(name))
            #print("data: {0}".format(str(data)))
            data  = { "name":first, "alias": name}
            #print(json.dumps(data))
            response.append(post_data(data))
    return response

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "companies-clean-array.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

async def main():
   with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                process, 
                i
            )
            for i in data
        ]
        for response in await asyncio.gather(*futures):
            print(response)




executor = concurrent.futures.ThreadPoolExecutor(64)

loop = asyncio.get_event_loop()
#loop.run_until_complete(tqdm_parallel_map(executor,process,data[0:100]))
loop.run_until_complete(main())
