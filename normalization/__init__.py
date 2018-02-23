# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:08:54 2017

@author: HindolRakshit

Collection of normalization functions

"""
import logging
import numpy as np
import pandas as pd
from quantiphy import Quantity
import re
import yaml
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'categories.yml'), 'r') as f:
    categories = yaml.load(f)

def reverse(d):
    d = d[::-1] 
    return d

def lower(d):
    if isinstance(d,str):
        d = d.lower()
        return d
    else:
        return d

def inductance(d):
    """ turns inducance string to numeric"""
    if isinstance(d, str):
        d = d.replace('µ','u')
        d = float(Quantity(d,'H'))
        return d
    else:
        logging.warning("during inductance type conversion got a non-string")
        return d

 
def current(d):
    
    """ turns current based strings into numeric"""
    
    if isinstance(d, str):
        
        ## unit to consider: A
        d = d.replace('µ','u')
        d = float(Quantity(d,'A'))
        return d
    else:
        logging.warning("during current type conversion got a non-string")
        return d


def split_l_w(d):
    """splits Lenght and Width from strings
    example: '0.276" L x 0.217" W (7.00mm x 5.50mm)'
    ignoring inches, focusing on millimeters
    """
    regexp =re.compile('\((.*) x (.*)\)')
    res = regexp.findall(d)[0]
    if len(res) == 2:
        l,w = res[0],res[1] 
        l = float(Quantity(l,scale='mm'))
        w = float(Quantity(w,scale='mm'))
        return l,w

def parse_dimension(d):
    """
    parse out any dimension in mm from string
    '0.512" (13.00mm)'
    """
    regexp =re.compile('\((.*)mm\)')
    res = regexp.findall(d)
    if len(res) >0:
        if res[0] is not None:
            d = float(Quantity(res[0], "mm"))
    else:
        return d
    return d

def split_q(d):
    """split a Q string with @ into two values
    input looks like  "q_@_freq": "72 @ 100MHz"
    output should look like
    q = 72
    freq_hz = 100000000
    """
    q,freq = d.split('@')
    q = q.strip(" ")
    q = float(q)
    freq = freq.strip(" ")
    freq  = float(Quantity(freq))
    return(q,freq) 

def category_normalize_digikey(d):
    """
    For categories, instead of changing the name
    """
    for n, i in enumerate(d):
        if i in categories['digikey']:
            d[n] = categories['digikey'][i]
        else:
            logging.warning("missing mapping for {0}".format(i))
    return d


def to_int(d):
    """turns a string into integer"""
    if  isinstance(d, str):
        return int(d)  
    else:
        raise TypeError('cannot cast {0} into float as it\'s not a string'.format(d))

def to_float(d):
    """turns a string into decimal"""
    if  isinstance(d, str):
        return float(d)
    else:
        raise TypeError('cannot cast {0} into float as it\'s not a string'.format(d))
