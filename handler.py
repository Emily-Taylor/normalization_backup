# -*- coding: utf-8 -*-
import base64
from collections import defaultdict
import copy
import json
import logging
import os
import sys
import re
from lambda_decorators import dump_json_body, json_http_resp
import yaml
import common as c
import normalization as n

from functions import adjust_structure, adjust_structure_minimal, MAPPING

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


#def norm_handler_kinesis(event: dict, *args):
#    if 'Records' in event:
#        for rec in event['Records']:
#            message = parse_record(rec)
#
#    elif 'parts' in event:
#        message = event
#    else:
#        logging.error("no Records found in event")
#        print(event)

#    output = {'parts': []}
#    if 'parts' in message:
#        if 'source' in message:
#            source = message['source']
#            timestamp = message['ts']
#        else:
#            logging.warning("could not find source (distributor) in message")
#            return False
#        for part in message['parts']:
#            part_properties = list(part.keys())
#            missing_keys = list(
#                map(lambda v: v in MAPPING[source], part_properties))
#            missing_keys = [not i for i in missing_keys]
#            missing_keys = [int(i) for i in missing_keys]
#            missing_keys = sum(missing_keys)
#            if missing_keys > 0:
#                missing_keys_list = []
#                for v in part.keys():
#                    if v not in MAPPING[source]:
#                        missing_keys_list.append(v)
#                logging.warning("there are {1} missing keys: {0}".format(missing_keys_list,missing_keys))
#            if 'categories' in part:
#                category = str(part['categories'])
#                category = re.sub('\', \'', '\',\'', category)
#                category_exists = '' 
#                if source != 'mouser':
#                    if category in n.categories[source]:
#                        category_exists = True
#                    elif category not in n.categories[source]:
#                        category_exists = False
#            else:
#                # failed to find category in part...
#                category_exists = False
#
#            # we only normlize and process digikey and mouser.
#            # we also only normlize categories we mapped and tested.
#            # # if we can't normalize it
#            if source not in MAPPING or missing_keys > 0 or category_exists is False:
#                # we can't handle it this part because it's from a distributor we don't know.
#                logging.warning("missing keys, mappings or new source. running minimal normalization")
#                part = adjust_structure_minimal(part, source, timestamp)
#                output['parts'].append(part)
#            elif source in MAPPING:
#                part = adjust_structure(part, source, timestamp)
#                output['parts'].append(part)
#
#    c.publish_kinesis_single(output)
#    return True


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
    if 'parts' in message:

        if 'source' in message:
            source = message['source']
            timestamp = message['ts']
        else:
            logging.warning("could not find source (distributor) in message")
            return False
        for part in message['parts']:
            part_properties = list(part.keys())
            missing_keys = list(
                map(lambda v: v in MAPPING[source], part_properties))
            missing_keys = [not i for i in missing_keys]
            missing_keys = [int(i) for i in missing_keys]
            missing_keys = sum(missing_keys)
            if missing_keys > 0:
                missing_keys_list = []
                for v in part.keys():
                    if v not in MAPPING[source]:
                        missing_keys_list.append(v)
                logging.warning("there are {1} missing keys: {0}".format(missing_keys_list,missing_keys))
            if 'categories' in part:
                category = str(part['categories'])
                category = re.sub('\', \'', '\',\'', category)
                category_exists = '' 
                if source != 'mouser':
                    if category in n.categories[source]:
                        category_exists = True
                    elif category not in n.categories[source]:
                        category_exists = False
            else:
                # failed to find category in part...
                category_exists = False

            # we only normlize and process digikey and mouser.
            # we also only normlize categories we mapped and tested.
            # # if we can't normalize it
            if source not in MAPPING or missing_keys > 0 or category_exists is False:
                # we can't handle it this part because it's from a distributor we don't know.
                logging.warning("missing keys, mappings or new source. running minimal normalization")
                part = adjust_structure_minimal(part, source, timestamp)
                output['parts'].append(part)
            elif source in MAPPING:
                part = adjust_structure(part, source, timestamp)
                output['parts'].append(part)
    return output
