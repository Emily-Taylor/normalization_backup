# coding: utf-8

import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import jsonlines
import ndjson
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
import logging 
from tqdm import tqdm

import multiprocessing as mp

#filename = '/home/username/projects/sourcingbot/normalization_service/data-full/digikey/inductor_digikey.ndjson.gz'
#filename =  '/home/username/projects/sourcingbot/normalization_service/data/1000inductors.ndjson.gz'
#filename =  '/home/username/projects/sourcingbot/normalization_service/data/100inductors.ndjson.gz'
#output_filename ='normalized_inductors.json'



class Context:
    def __init__(self):
        self.function_name = 'Fake'

context = Context()

large_list = []

def handle_parts(obj):
    res = handler.norm_handler_http(obj, context)
    #large_list.append(json.loads(res['body']))
    return json.loads(res['body'])
        
def process_file(input_filename,output_filename):
    pool = mp.Pool(processes=8)
    with jsonlines.Reader(gzip.open(input_filename)) as reader:
        tqdm.monitor_interval = 0
        results = [pool.apply(handle_parts, args=(obj,)) for obj in tqdm (reader)]
    if output_filename:
        # Writing JSON data
        #with open(output_filename, 'w') as f:
        #    json.dump(results, f)
        with gzip.GzipFile(output_filename, 'w') as f:
            f.write(json.dumps(results).encode('utf-8'))


def process_file_new(input_filename,output_filename):
    #pool = mp.Pool(processes=8)
    if 'digikey' in input_filename:
        src = 'digikey'
    elif 'mouser' in input_filename:
        src = 'mouser'
    
    contents = open(input_filename, "r", encoding='utf-8').read()
    obj = {'parts': []}
    for item in tqdm(contents.strip().split('\n')):
        s = json.loads(str(item))
        obj['parts'].append(s)
    
    results = handler.norm_handler_new(obj, src)

    norm_parts  = [json.dumps(record) for record in results['parts']]
        
    if output_filename:
        # Writing JSON data
        #with open(output_filename, 'w') as f:
        #    json.dump(results, f)
        #Write compressed json file
#        with gzip.GzipFile(output_filename, 'w') as f:
#            f.write(json.dumps(results).encode('utf-8'))
#          

#    Writing ndjson 
        with open(output_filename, 'w') as f:
            for i in norm_parts:
                results_ndjson = f.write(i+'\n')
#            ndjson.dump(results_ndjson, f)       
        

if __name__ == '__main__':
    fire.Fire()

