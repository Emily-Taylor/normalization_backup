# -*- coding: utf-8 -*-
from hashlib import sha1
from copy import deepcopy
from collections import defaultdict
from json import dumps
import logging
import os
import yaml

import normalization as n
import common as c
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(CURRENT_DIR, 'mapping.yml'), 'r') as f:
  MAPPING = yaml.load(f)



def deep_set(part, value, keys):
    data = part
    for key in keys[:-1]:
        data = data[key]
        data[keys[-1]] = value


def adjust_structure(part: dict, source: str, ts: int):
  
    part = defaultdict(dict, part)
    # fix mfr before everything
    if 'mfr' in part:
        mfr = c.get_alias(part['mfr'])
        part['mfr'] = mfr
    # keep desciprtion
    if 'description' in part:
        raw_desc = deepcopy(part['description'])
        part['description_raw'] = {}
        part['description_raw'][source] = raw_desc
        # fix category before normalization
    if 'categories' in part:
        raw_categories = deepcopy(part['categories'])
        part['categories_raw'] = {}
        part['categories_raw'][source] = raw_categories
    # remove availablity and pricing, minimum_quantity and packagecase
    part.pop('availability', None)
    part.pop('pricing', None)
    part.pop('packagecase', None)
    part.pop('minimum_quantity', None)
    for key in list(part):
    # apply norm
        if key in MAPPING[source]:
            try:
                # attempt to apply functions
                if 'actions' in MAPPING[source][key]:
                    functions = MAPPING[source][key]['actions']
                    for func in functions:
                    # print(f,key)
                        new_val = eval(
                            "n." + func + "({})".format("part['" + key + "']"))
                    part[key] = new_val
            except Exception as error:
                print('Caught this error: '+ repr(error)+' during processing of function '
                      +func
                      +" and key "
                      +repr(key)
                     )
            #raise error

                #raise ValueError("something wrong with functions: {0}".format(BaseException))

            # check for new keys name
            if isinstance(MAPPING[source][key]['output_key'], list)\
              and isinstance(part[key], tuple):
                #print("going to zip: "+str(mapping[source][key]['output_key'])+" "+str(part[key]))
                t_res = dict(zip(MAPPING[source][key]['output_key'], part[key]))
                #print(t_res.keys())
                for k in t_res.keys():
                    if '.' not in k:
                        #print("handling double key, no nesting")
                        part[k] = t_res[k]
                    else:
                        #print("handling double key, with nesting")
                        keys = k.split('.')
                        # print(k,keys,part[key])
                        deep_set(part, t_res[k], keys)
                    if key in part:
                        part.pop(key)
                if part[key] != MAPPING[source][key]['output_key']:
                    part.pop(key)
                else:
                        if '.' not in MAPPING[source][key]['output_key']:
                            #print("handling single key, no nesting")
                            new_key = MAPPING[source][key]['output_key']
                            try:
                                part[new_key] = part.pop(key)
                            except Exception as error:
                                print("couldn't assign new key. for old key {0}, new key: {1}, data: {2}".format(str(key),str(new_key), str(part[key])))
                                print('Caught this error: ' + repr(error))
                        else:
                            #print("handling single key, with nesting")
                            keys = MAPPING[source][key]['output_key'].split('.')
                            deep_set(part, part[key], keys)
                            # finish the job
                            part.pop(key)

        else:
            # call missing-mapping queue with the source, categories and
            # missing mapping key.
            #print("missing mapping")
            c.send_msg(dumps(
                {"source": source, "categories": part['categories'], "key": key}))
            # we are going to continue in order to prevent writing json that's
            # not fully mapped
            continue
    # fix lifecycle/life
    if 'lifecycle' in part:
        new_life = part.pop('lifecycle')
        part['lifecycle'] = {}
        part['lifecycle'][source] = new_life
    # fix SKU
    if 'sku' in part:
        new_sku = part.pop('sku')
        #part['sku'] = {}
        #part['sku'][source] = new_sku
    # fix links
    if 'links' in part:
        new_links = part.pop('links')
        part['sku'] = {}
        part['sku'][source] = {}
        part['sku'][source][new_sku[0]] = {}
        part['sku'][source][new_sku[0]]['links'] = new_links
        part['sku'][source][new_sku[0]]['packaging'] = part.pop('packaging', None)

    # generate IDs
    if 'mpn' in part and 'mfr' in part:
        id = (part['mpn'] + part['mfr']).lower().replace(" ", "")
        hash_object = sha1(id.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        part['id'] = hex_dig
    # print(part['id'])
    elif 'mpn' in part:
        id = part['mpn'].lower().replace(" ", "")
        hash_object = sha1(id.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        part['id'] = hex_dig
    # print(part['id'])
    else:
        logging.error("can't find MPN on part!")
        print("can't find MPN on part!")
        return False 

    #adding timestamp ts of the normalization
    part['ts_norm'] = c.now()
    #adding timestamp ts of the crawler-
    part['ts_crawler'] = ts
    # last big modification of the structure of the json
    # we want to stuff everything but [mfr, mpn, category, sku, links,
    # description, lifecycle] as nested properties.
    main_keys = [
        'mfr',
        'mpn',
        'categories',
        'categories_raw',
        'sku',
        'links',
        'description',
        'description_raw',
        'lifecycle',
        'properties',
        'id',
        'ts_norm',
        'ts_crawler']
    part['properties'] = {}
    for k in list(part):
        if k not in main_keys:
            #print("{0} not in main_keys".format(k))
            part['properties'][k] = part.pop(k, None)
    return part
