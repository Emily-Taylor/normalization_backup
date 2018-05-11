# -*- coding: utf-8 -*-
import base64
from collections import defaultdict
import copy
import json
import logging
import os
import sys
from lambda_decorators import dump_json_body, json_http_resp
import yaml
import common as c
import normalization as n

from functions import adjust_structure

c.init()


@dump_json_body
def ping(event, context):
    """
        This endpdoints always returns 200.
    """
    return {
        "statusCode": 200,
        "body": {
            "message": "Pong!"
        },
    }


def parse_record(rec):
    if 'kinesis' in rec:
        if 'data' in rec['kinesis']:
            try:
                val = json.loads(base64.b64decode(rec['kinesis']['data']))
            except BaseException:
                logging.error(
                    "couldn't parse base64 or json from records arriving from kinesis")
    return val


def norm_handler_kinesis(event: dict, *args):
            # print(event)
    if 'Records' in event:
        for rec in event['Records']:
            message = parse_record(rec)

    elif 'parts' in event:
        message = event
    else:
        logging.error("no Records found in event")
        print(event)


    output = {'parts': []}

    if 'parts' in message:
        if 'source' in message:
            source = message['source']
            timestamp = message['ts']
        else:
            logging.warning(
                "could not find source (distributor) in message kinesis")
            logging.warning(message)
            #return False
        for part in message['parts']:
            # this is where the magic happens
            part = adjust_structure(part, source, timestamp)
            output['parts'].append(part)
            # if not rest_call:
            #	print(c.publish_data(part))
    #final_out =json.dumps(output)
    c.publish_kinesis_single(output)
    #print("length of payload: {}".format(len(output.encode("utf8"))))
    return True


@json_http_resp
@dump_json_body
def norm_handler_http(event, *args):
    if len(args) > 0:
        context = args[0]
        if context.function_name == 'Fake':
            print("found Fake in context, we are in testing")
            message = event
        if 'httpMethod' in event:
            try:
                message = json.loads(event['body'])
            except BaseException:
                print(event['body'])
                print("failed to load json from http request")
    output = {'parts': []}
    #print(  message)
    #print( 'parts' in message )
    #print(  len(message.get('parts', 0)))   

    if 'parts' in message:
        
        if 'source' in message:
            source = message['source']
            timestamp = message['ts']
            print(source,timestamp)
        else:
            logging.warning("could not find source (distributor) in message")
            #return False
        for part in message['parts']:
            # this is where the magic happens
            #print("magic!")
            #
            # print(part.keys())
            part = adjust_structure(part, source, timestamp)
            output['parts'].append(part)

    return output
