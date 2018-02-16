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

def parse_height(d):
    """
    parse out the height in mm from string
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

def cleanblank(d):
    """Cleans blank spaces and special characters"""
    d = d.replace('', np.nan)
    d = d.replace(u'  ', np.nan)
    d = d.replace('-', np.nan)
    d = d.replace('*', np.nan)
    return d

def remempty(d):
    """Removes entirely empty headers"""

    d = d.dropna(axis=1, how='all')

    return d


def changename(d, header, new_name):
    """Changes name of a header"""

    if header in d.columns:

        d = d.rename(index=str, columns={header: new_name})

        return d

    else:

        # ERROR HANDLING

        raise NameError('Invalid header name.')

def to_int(d):
    """turns a string into integer"""
    if  isinstance(d, (string)):
        return int(d)  
    else:
        raise TypeError('cannot cast {0} into float as it\'s not a string'.format(d))

def to_float(d):
    """turns a string into decimal"""
    if  isinstance(d, (string)):
        return float(d)
    else:
        raise TypeError('cannot cast {0} into float as it\'s not a string'.format(d))

def rescale(d, scaling_factor):
    """Rescales numerical fields"""

    if isinstance(d, (int, float)) and isinstance(scaling_factor, (int, float)):
            d = d * scaling_factor
            return d
    else:
        # ERROR HANDLING
        raise TypeError('Non-numerical headers or factors cannot be processed. if {0} and {1} look like a numbers, you may want to cast them first'.format(d,scaling_factor))


def convertnumext(d, header, ext):
    """Converts unit extensions and adjusts header names"""

    if header in d.columns:

        if np.issubdtype(d[header].dtype, np.number) == False:

            # convert header to numeric

            d[header] = d[header].str.extract('([\d\.]+)', expand=True)
            d[header] = pd.to_numeric(d[header], errors='coerce')

            # rename header usig assigned extension

            new_name = header + '_' + ext

            d = d.rename(index=str, columns={header: new_name})

            return d

        else:

            # ERROR HANDLING

            raise TypeError('Numerical headers cannot be processed.')

    else:

        # ERROR HANDLING

        raise NameError('Invalid header name.')


def convertcatext(d, header, ext):
    """Removes specified string extensions"""

    if header in d.columns:

        if np.issubdtype(d[header].dtype, np.number) == False:

            d[header] = pd.Series(d[header]).str.replace(ext, '')

            return d

        else:

            # ERROR HANDLING

            raise TypeError('Numerical headers cannot be processed.')

    else:

        # ERROR HANDLING

        raise NameError('Invalid header name.')


def sepheader(d, header, separator):
    """Separates range headers to min/max headers"""

    if header in d.columns:

        if np.issubdtype(d[header].dtype, np.number) == False:

            header_min = header + '_' + 'min'
            header_max = header + '_' + 'max'

            sep_min = separator + '.*'
            sep_max = '.*' + separator

            d[header_min] = pd.Series(d[header]).str.replace(sep_min, '')
            d[header_max] = pd.Series(d[header]).str.replace(sep_max, '')

            return d

        else:

             # ERROR HANDLING

            raise TypeError('Numerical headers cannot be processed.')

    else:

        # ERROR HANDLING

        raise NameError('Invalid header name.')


def convertMixedExt(d, header, ext, scaling_factor):
    """Normalizes mixed units headers"""

    if header in d.columns:

        if np.issubdtype(d[header].dtype, np.number) == False:

            if len(ext) == len(scaling_factor):

                # Initiate new header with extracted numerical values

                newHeader = header + '_' + 'normalized'

                d[newHeader] = d[header].str.extract('([\d\.]+)', expand=True)
                d[newHeader] = pd.to_numeric(d[newHeader], errors='coerce')

                # Multiply values with suitable scaling factor

                # Define `which()` analogue in python

                def which(lst): return list(np.where(lst)[0])

                # Turn off 'SettingWithCopyWarning'

                pd.options.mode.chained_assignment = None

                # Iteratively find out locations, and rescale

                for i in range(len(ext)):

                    temp = which(pd.Series(d[header]).str.contains(ext[i], case=True))

                    d[newHeader][temp] = d[newHeader][temp] * scaling_factor[i]

                return d

            else:

                # ERROR HANDLING

                raise ValueError('Length of \'ext\' and \'scaling_factor\' do not match.')
        else:

            # ERROR HANDLING

            raise TypeError('Numerical headers cannot be processed.')

    else:

        # ERROR HANDLING

        raise NameError('Invalid header name.')
