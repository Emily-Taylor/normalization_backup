import json
# aiohttp doesn't work nicely with aws v4 signed request
import requests
from requests_aws_sign import AWSV4Sign
from boto3 import session
#from tqdm import tqdm
from multiprocessing import Pool
import tqdm
import os,sys
import threading


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Establish credentials
session = session.Session()
credentials = session.get_credentials()
region = session.region_name or 'eu-central-1'

# set filename and load all data
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, "companies-clean-array-v2.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# call entity storage service
def post_data(data):
    uri =  "https://app-dev.sourcingbot.com/entity/manufacturer"
#    uri =  "http://localhost:3000/entity/manufacturer"

    headers={"Content-Type":"application/json"}
    service = 'execute-api'
    auth=AWSV4Sign(credentials, region, service)
    response = requests.post(uri, auth=auth, headers=headers,json=data)
    return response


def process(data):
    response = []
    if len(data) ==1:
        data  = { "name": data[0], "alias": data[0]}
        response.append(post_data(data))

    elif  len(data) >1:
        first = data[0]
        for name in data:
            data  = { "name":first, "alias": name}
            response.append(post_data(data))
    return response


if __name__ == '__main__':
   with Pool(250) as p:
      r = list(tqdm.tqdm(p.imap(process, data), total=len(data)))
      print(r)
