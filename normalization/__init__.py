# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:08:54 2017

@author: HindolRakshit

Collection of normalization functions

"""
import logging
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
    
def tempcoeff(d):
    """turns temp coefficients into number"""
    symbols = ['±','°C','ppm', ' PPM / C']
    if isinstance(d, str):
        if any(x in d for x in symbols):
            d = d.replace(' PPM / C', '')
            d = d.replace('±', '')
            d = d.replace('ppm/°C', '')
            d = d.replace(' ', '')
            
            try:
                d = float(d)
                return d
            except ValueError:
                logging.warning("value: \"{0}\" doesn't cannot be converted to float".format(d))
                return d
        else:
            logging.warning("value: \"{0}\" doesn't match expected pattern".format(d))
            return d
    else:
        logging.warning("during coeff type conversion got a non-string")

def extract_num(d):
    """turns strings with ANY unit into numbers"""
    if isinstance(d, str):
        
        if (len(d) > 0):
            
            d = d.replace('µ','u')
            d = d.replace(' %', '')
            d = re.sub(r'\(.*\)', '', d)
            d = d.replace(' ', '')
            d = d.replace(' Max','')
            d = d.replace('±', '')
            d = d.replace('ppm/°C', '')
            d = float(Quantity(d,''))
            return d
        else:
            logging.warning("during coversion got an empty string")
            return d
    else:
        logging.warning("during type conversion got a non-string")     
        
def inductance(d):
    """ turns inducance string to numeric"""
    if isinstance(d, str):
        d = d.replace('µ','u')
        d = float(Quantity(d,'H'))
        return d
    else:
        logging.warning("during inductance type conversion got a non-string")
        return d

def voltage(d):
    """ turns voltage string to numeric"""
    if isinstance(d, str):
        d = d.replace('µ','u')
        d = float(Quantity(d,'V'))
        return d
    else:
        logging.warning("during voltage type conversion got a non-string")
        return d
    
def tolerance(d):
    """ turns tolerance into number """
    if isinstance(d, str):
        d = d.replace('±', '')
        d = d.replace('%', '')
        return int(d)
    else:
        logging.warning("during tolerance type conversion got a non-string")
    

    
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
    
def resistance(d):
    
    """ turns resistance based strings into numeric"""
    
    if isinstance(d, str):
        
        ## unit to consider: Ohm
        d = d.replace('µ','u')
        d = d.replace('s', '')
        d = d.replace(' Max','')
        d = float(Quantity(d,'Ohm'))
        return d
    else:
        logging.warning("during resistance type conversion got a non-string")
        return d
    
def resistance_addunit(d):
    """add Ohm extension whenever it's not there"""
    d = d + 'Ohm'
    return d

def power(d):
    
    """ turns power based strings into numeric"""
    
    if isinstance(d, str):
        
        ## unit to consider: W
        d = d.replace('µ','u')
        d = d.replace('s', '')
        d = d.replace(' Max','')
        d = float(Quantity(d,'W'))
        return d
    else:
        logging.warning("during power type conversion got a non-string")
        return d    
    
def capacitance(d):
    
    """ turns capacitance based strings into numeric"""
    
    if isinstance(d, str):
        
        ## unit to consider: F
        d = d.replace('µ','u')
        d = d.replace(' Max','')
        d = float(Quantity(d,'F'))
        return d
    else:
        logging.warning("during capacitance type conversion got a non-string")
        return d

def frequency(d):
    
    """ turns frequency based strings into numeric"""
    
    if isinstance(d, str):
        
        ## unit to consider: Hz
        d = d.replace('µ','u')
        d = d.replace(' Max','')
        d = float(Quantity(d,'Hz'))
        return d
    else:
        logging.warning("during frequency type conversion got a non-string")
        return d
    

def parse_dimensions(d):
    """splits Lenght and Width from strings
    example: '0.276" L x 0.217" W (7.00mm x 5.50mm)'
    ignoring inches, focusing on millimeters
    """
    regexp =re.compile('([\d\.]+mm)')
    res = regexp.findall(d)
    if len(res) == 2:
        l,w = res[0],res[1] 
        l = float(Quantity(l,scale='mm'))
        w = float(Quantity(w,scale='mm'))
        return l,w
    if len(res) == 1:
        dim = float(Quantity(res[0],scale='mm'))
        return (dim,)

def split_temp(d):
    
    """ splits temperature columns into min and max"""
    
    t_min, t_max = d.split(' ~ ')
    
    temp_min = float(Quantity(t_min))
    temp_max = float(Quantity(t_max))
    
    return (temp_min, temp_max)

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

def split_at(d):
    """split strings which are presented
    in the format: ... @ ...
    """
    if isinstance(d, str):
        n1, n2 = d.split('@')
        n1 = n1.strip(" ")
        n2 = n2.strip(" ")
        n1  = float(Quantity(n1))
        n2  = float(Quantity(n2))
        return(n1, n2)
    else:
        logging.warning("during type conversion got a non-string")
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

def split_rc(d):
    """split a rc string with @ into two values
    input looks like  "ripple_current_@_low_frequency": "28mA @ 120Hz"
    output should look like
    c = 0,028
    freq = 120
    """
    c,freq = d.split('@')
    c = c.strip(" ")
    c = float(Quantity(c))
    freq = freq.strip(" ")
    freq  = float(Quantity(freq))
    return(c,freq) 

def split_esr(d):
    """split esr string into r and freq
    input looks like: '520 mOhm @ 100kHz'
    output should look like
    r = 0.52
    freq = 100000
    """
    r, freq = d.split('@')
    r = r.strip(" ")
    r = float(Quantity(r))
    freq = freq.strip(" ")
    freq = float(Quantity(freq))
    return(r,freq)

def split_lifetime(d):
    """split esr string into r and freq
    input looks like: '2000 Hrs @ 85°C'
    output should look like
    t = 2000
    c = 85
    """
    t, c = d.split('@')
    t = t.strip(" ")
    t = float(Quantity(t))
    c = c.strip(" ")
    c = float(Quantity(c))
    return(t,c)

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
    if  isinstance(d, (str)):
        return int(d)  
    else:
        raise TypeError('cannot cast {0} into float as it\'s not a string'.format(d))

def to_float(d):
    """turns a string into decimal"""
    if  isinstance(d, str):
        return float(d)
    else:
        raise TypeError('cannot cast {0} into float as it\'s not a string'.format(d))
