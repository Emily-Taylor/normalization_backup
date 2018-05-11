
# coding: utf-8

# In[7]:


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import jsonlines
import lambda_decorators
import handler
from functions import adjust_structure
import boto3
import random
import string
import time
import fire


from collections import defaultdict

import yaml, json
import jsonlines
import gzip

from boto3 import session
from six import string_types
import logging 

#from tqdm import tqdm
from tqdm import tqdm_notebook as tqdm


# In[16]:


filename = '/home/username/projects/sourcingbot/normalization_service/data-full/digikey/inductor_digikey.ndjson.gz'
#filename =  '/home/username/projects/sourcingbot/normalization_service/data/1000inductors.ndjson.gz'
#filename =  '/home/username/projects/sourcingbot/normalization_service/data/100inductors.ndjson.gz'
output_filename ='normalized_inductors.json'


# In[ ]:





# In[14]:






class Context:
    def __init__(self):
        self.function_name = 'Fake'

context = Context()

large_list = []
def handle_parts(obj):
    res = handler.norm_handler_http(obj, context)
    #large_list.append(json.loads(res['body']))
    return json.loads(res['body'])
        


# In[10]:


start = time.time()
# read mapping file
def process(filename):
  here = os.path.dirname(os.getcwd())
  with jsonlines.Reader(gzip.open(os.path.join(here, filename))) as reader:
    global temp_obj
    temp_obj = []
    tqdm.monitor_interval = 0
    for obj in tqdm (reader):
      res = handle_parts(obj)
      large_list.append(res)

    end = time.time()
    print(end - start)


# In[11]:


process(filename)


# In[15]:


import multiprocessing as mp
#from multiprocessing import Process, Value, Array

pool = mp.Pool(processes=64)
with jsonlines.Reader(gzip.open(filename)) as reader:
    tqdm.monitor_interval = 0
    results = [pool.apply(handle_parts, args=(obj,)) for obj in tqdm (reader)]


# In[42]:


print(len(results))


# In[45]:


if output_filename:
    # Writing JSON data
    with open(output_filename, 'w') as f:
        json.dump(results, f)

