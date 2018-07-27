# -*- coding: utf-8 -*-
from hashlib import sha1
from copy import deepcopy
from collections import defaultdict
import json
import logging
import os
import yaml
import re

import normalization as n
import common as c
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# load key-mapping file
with open(os.path.join(CURRENT_DIR, 'key-mapping.yml'), 'r') as f:
    MAPPING = yaml.load(f)

# load mpn_mapping file
with open(os.path.join(CURRENT_DIR, 'mpn_mapping.json'), 'r') as f:
    MPN_MAPPING = json.load(f)
    
# load pkg_mapping file
with open(os.path.join(CURRENT_DIR, 'pkg_mapping.json'), 'r') as f:
    PKG_MAPPING = json.load(f)
    
# create function to map mpn
    
# def set_mpn(MPN_MAPPING: dict, m: str):
    # for key, value in MPN_MAPPING.items():
        # if m in value:
            # return key
        # else:
            # return m

def set_mpn(MPN_MAPPING: dict, m: str):
    
    sim_vec = []
    
    for i in range(len(list(MPN_MAPPING.values()))):
        if m in list(MPN_MAPPING.values())[i]:
            sim_vec.append(1)
        else:
            sim_vec.append(0)
        
    if 1 in sim_vec:
        m_index = sim_vec.index(1)
        return list(MPN_MAPPING.keys())[m_index]
    else:
        return m
        
# create function to map pkg
            
def set_pkg(PKG_MAPPING: dict, p: list):
    
    if len(p) != 0:
        p_str = p[0].lower()
        sim_vec = []
    
        for i in range(len(list(PKG_MAPPING.values()))):
            if p_str in list(PKG_MAPPING.values())[i]:
                sim_vec.append(1)
            else:
                sim_vec.append(0)
    
        if 1 in sim_vec:
            p_index = sim_vec.index(1)
            return [list(PKG_MAPPING.keys())[p_index]]
        else:
            return p
    else:
        return p
    
def mpn_norm(m: str):
    
    """
    normalizes mpn
    """
    
    m_final = re.sub('[# /.,=_%]', '-', m.upper())
    m_final = re.sub('--', '-', m_final)
                       
    return m_final
    
def deep_set(part, value, keys):
    data = part
    for key in keys[:-1]:
        data = data[key]
        data[keys[-1]] = value


def adjust_structure(part: dict, source: str, ts: int):

    part = defaultdict(dict, part)
    # fix mfr before everything
    if 'mfr' in part:
        # mfr = c.get_alias(part['mfr'])
        mfr_raw = deepcopy(part['mfr'])
        part['mfr_raw'] = {}
        part['mfr_raw'][source] = mfr_raw
        mfr = c.get_mfr_mapping(part['mfr'])
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
        # save raw mpn before normalizing
    if 'mpn' in part:
        part['mpn'] = set_mpn(MPN_MAPPING, part['mpn'])
        raw_mpn = deepcopy(part['mpn'])
        part['mpn_raw'] = {}
        part['mpn_raw'][source] = raw_mpn
    if 'packaging' in part:
        raw_pack = deepcopy(part['packaging'])
        part['packaging_raw'] = {}
        part['packaging_raw'][source] = raw_pack
        part['packaging'] = set_pkg(PKG_MAPPING, part['packaging'])
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
                print('Caught this error: ' + repr(error) + ' during processing of function '
                      + func
                      + " and key: "
                      + repr(key)
                      + " and value: "
                      + repr(part[key])
                      )

            # check for new keys name
            if isinstance(MAPPING[source][key]['output_key'], list) and isinstance(part[key], tuple):
                t_res = dict(
                    zip(MAPPING[source][key]['output_key'], part[key]))
                for k in list(t_res.keys()):
                    if part[key] != MAPPING[source][key]['output_key']:
                        part[k] = t_res[k]
                        part.pop(key)
                    else:
                        part[k] = t_res[k]
            elif isinstance(MAPPING[source][key]['output_key'], str) and isinstance(part[key], tuple):
                print("handling single output key")
                output_key = MAPPING[source][key]['output_key']
                part[output_key] = part.pop(key)
            elif isinstance(MAPPING[source][key]['output_key'], str):
                output_key = MAPPING[source][key]['output_key']
                part[output_key] = part.pop(key)
            else:
                new_keys = MAPPING[source][key]['output_key']
                print("couldn't assign new key. for old key {0}, new_keys: {2}, data: {1}".format(
                    str(key), str(part[key]), str(new_keys)))

        else:
            # call missing-mapping queue with the source, categories and
            # missing mapping key.
            # print("missing mapping")
            #c.send_msg(json.dumps(
            #    {"source": source, "categories": part['categories'], "key": key}))
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
        # part['sku'] = {}
        # part['sku'][source] = new_sku
    # fix links
    if 'links' in part:
        new_links = part.pop('links')
        part['sku'] = {}
        part['sku'][source] = {}
        part['sku'][source][new_sku[0]] = {}
        part['sku'][source][new_sku[0]]['links'] = new_links
        part['sku'][source][new_sku[0]]['packaging'] = part.pop(
            'packaging', None)

    # generate IDs
    if 'mpn' in part and 'mfr' in part:
        part['mpn'] = mpn_norm(part['mpn'])
        id = (part['mpn'] + part['mfr']).lower().replace(" ", "")
        hash_object = sha1(id.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        part['id'] = hex_dig
    # print(part['id'])
    elif 'mpn' in part:
        part['mpn'] = mpn_norm(part['mpn'])
        id = part['mpn'].lower().replace(" ", "")
        hash_object = sha1(id.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        part['id'] = hex_dig
    # print(part['id'])
    else:
        logging.debug("can't find MPN on part!")
        print("can't find MPN on part!")
        return False

    # trim category to maxmium 2 levels:
    if part['categories']:
        if len(part['categories']) >2:
            part['categories'] = part['categories'][0:2]
    # adding timestamp ts of the normalization
    part['ts_norm'] = c.now()
    # adding timestamp ts of the crawler-
    part['ts_crawler'] = ts
    # last big modification of the structure of the json
    # we want to stuff everything but [mfr, mpn, category, sku, links,
    # description, lifecycle] as nested properties.
    main_keys = [
        'mfr',
		'mfr_raw',
        'mpn',
        'packaging_raw',
        'categories',
        'categories_raw',
        'sku',
        'description',
        'description_raw',
        'lifecycle',
        'properties',
        'id',
        'ts',
        'ts_norm',
        'ts_crawler',
        'mpn_raw',
	'series']
    part['properties'] = {}
    for k in list(part):
        if k not in main_keys:
            # print("{0} not in main_keys".format(k))
            part['properties'][k] = part.pop(k, None)
    return part


def adjust_structure_minimal(part: dict, source: str, ts: int):

    part = defaultdict(dict, part)
    # fix mfr before everything
    if 'mfr' in part:
        # mfr = c.get_alias(part['mfr'])
        mfr_raw = deepcopy(part['mfr'])
        part['mfr_raw'] = {}
        part['mfr_raw'][source] = mfr_raw
        mfr = c.get_mfr_mapping(part['mfr'])
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
        # save raw mpn before normalizing
    if 'mpn' in part:
        part['mpn'] = set_mpn(MPN_MAPPING, part['mpn'])
        raw_mpn = deepcopy(part['mpn'])
        part['mpn_raw'] = {}
        part['mpn_raw'][source] = raw_mpn
    if 'packaging' in part:
        raw_pack = deepcopy(part['packaging'])
        part['packaging_raw'] = {}
        part['packaging_raw'][source] = raw_pack
        part['packaging'] = set_pkg(PKG_MAPPING, part['packaging'])
    # remove availablity and pricing, minimum_quantity and packagecase
    part.pop('availability', None)
    part.pop('pricing', None)
    part.pop('packagecase', None)
    part.pop('minimum_quantity', None)
    # fix lifecycle/life
    if 'lifecycle' in part:
        new_life = part.pop('lifecycle')
        part['lifecycle'] = {}
        part['lifecycle'][source] = new_life
    # fix SKU
    if 'sku' in part:
        new_sku = part.pop('sku')
        # part['sku'] = {}
        # part['sku'][source] = new_sku
    # fix links
    if 'links' in part:
        new_links = part.pop('links')
        part['sku'] = {}
        part['sku'][source] = {}
        part['sku'][source][new_sku[0]] = {}
        part['sku'][source][new_sku[0]]['links'] = new_links
        part['sku'][source][new_sku[0]]['packaging'] = part.pop(
            'packaging', None)

    # generate IDs
    if 'mpn' in part and 'mfr' in part:
        part['mpn'] = mpn_norm(part['mpn'])
        id = (part['mpn'] + part['mfr']).lower().replace(" ", "")
        hash_object = sha1(id.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        part['id'] = hex_dig
    # print(part['id'])
    elif 'mpn' in part:
        part['mpn'] = mpn_norm(part['mpn'])
        id = part['mpn'].lower().replace(" ", "")
        hash_object = sha1(id.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        part['id'] = hex_dig
    # print(part['id'])
    else:
        logging.debug("can't find MPN on part!")
        print("can't find MPN on part!")
        return False

    # adding timestamp ts of the normalization
    part['ts_norm'] = c.now()
    # adding timestamp ts of the crawler-
    part['ts_crawler'] = ts
    # last big modification of the structure of the json
    # we want to stuff everything but [mfr, mpn, category, sku, links,
    # description, lifecycle] as nested properties.


    main_keys = [
        'mfr',
		'mfr_raw',
        'mpn',
        'categories',
        'packaging_raw',
        'categories_raw',
        'sku',
        'description',
        'description_raw',
        'lifecycle',
        'properties',
        'id',
        'ts',
        'ts_norm',
        'ts_crawler',
        'mpn_raw',
    	'series']
    for k in list(part):
        if k not in main_keys:
            part.pop(k, None)
    return part
