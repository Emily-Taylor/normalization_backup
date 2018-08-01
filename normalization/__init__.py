# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:08:54 2017

@author: HindolRakshit

Collection of normalization functions

"""
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import common as c
import json
from quantiphy import Quantity
import re
import yaml
import os
import typing
from fractions import Fraction
from hashlib import sha1

# define function to get constant

CONST_NA = 'n/a';

def multiple_replace(text: str, adict: dict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'categories.yml'), 'r') as f:
    categories = yaml.load(f)

def attenuation(d: str) -> typing.Tuple[float, float, float]:
   """splits attenuation header into 3 keys"""
   if isinstance(d, str):
       d = re.sub(',.*', '', d)
       v_str, r_str = d.split(' @ ')
       if ' ~ ' in r_str:
           
           if len(re.findall('\d+.\d+ ~ \d+.\d+[a-zA-Z]+', r_str)) == 0:
               r1_str, r2_str = r_str.split(' ~ ')
               v = float(Quantity(v_str, ''))
               r1 = float(Quantity(r1_str, ''))
               r2 = float(Quantity(r2_str, ''))
               return (v, r1, r2)
           else:
               r1_str, r2_str = r_str.split(' ~ ')
               v = float(Quantity(v_str, ''))
               
               unit = re.findall('[a-zA-Z]+', r2_str)[0]
               r1_str = r1_str + unit
               
               r1 = float(Quantity(r1_str, ''))
               r2 = float(Quantity(r2_str, ''))
               return (v, r1, r2)
               
       else:
           v = float(Quantity(v_str, ''))
           r1 = float(Quantity(r_str, ''))
           r2 = float(Quantity(r_str, ''))
           return (v, r1, r2)
   else:
       print('during type conversion got a non-string')
       return (0.0, 0.0, 0.0)

def parse_resolution(d):
    try:
        val = int(d)
        return d
    except ValueError:
        return CONST_NA
    
def reverse(d: str):
    d = d[::-1]
    return d


def lower(d: str):
    if isinstance(d, str):
        d = d.lower()
        return d
    else:
        return d

def create_id(mpn, mfr):
    
    mpn = re.sub('[^0-9a-zA-Z]+', '', mpn)
    id = (mpn + mfr).lower().replace(" ", "")
    hash_object = sha1(id.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    
    return hex_dig

def tempcoeff(d: str) -> float:
    """turns temp coefficients into number"""
    symbols = ['±', '°C', 'ppm', ' PPM / C']
    if isinstance(d, str):
        if any(x in d for x in symbols):
            d = d.replace(' PPM / C', '')
            d = d.replace('±', '')
            d = d.replace('ppm/°C', '')
            d = d.replace(' ', '')
            try:
                d_float = float(d)
                return d_float
            except ValueError:
                print(
                    "value: \"{0}\" doesn't cannot be converted to float".format(d))
                return 0.0
        else:
            print(
                "value: \"{0}\" doesn't match expected pattern".format(d))
            return 0.0
    else:
        print("during coeff type conversion got a non-string")


def extract_num(d):
    """turns strings with ANY unit into numbers"""
    adict = {'µ': 'u', ' %': '', ' ': '', 'Max': '',
             '±': '', 'ppm/°C': '', ' (Cutoff)': '', 'ppm': '', ' (Typ)': '', 'AC/DC': '', '<': '', '+/- ': ''}

    if isinstance(d, str):

        if (len(d) > 0):
            if 'mm)' in d:
                d = d.split('(')[1]
                d = re.sub(', Full', '', d)
                d = re.sub(', Half', '', d)
                d_float = float(re.sub('mm\)', '', d))
                return d_float
            
            d = re.sub(r'\(.*\)', '', d)
            d = d.split(',', 1)[0]
            d = d.split('~', 1)[0]
            d = re.sub('Wire Wound Inductors', '0', d)
            
            
            if 'dBi @' in d:
                d = d.split('dBi', 1)[0]
                d_float = float(Quantity(d))
                return d_float
            elif 'N/A' in d or d == 'CMOS' or d == 'HCMOS' or d == 'HCMOS, TTL' or d == 'Variable' or d == 'No' or d == 'Yes':
               d_float = CONST_NA
               return d_float
            elif ' and ' in d:
               d = d.split(' and ')[0]
               d_float = float(Quantity(d, ''))
               return d_float
            elif 'Parallel @ ' in d:
               d = re.sub('Parallel @ ', '', d)
               d_float = float(Quantity(d))
               return d_float
            else:
                d = multiple_replace(d, adict)
                d = d.split('/', 1)[0]
                
                if ('@1Minute' in d) or ('@30Seconds' in d) or ('PSI' in d) or ('Pole' in d) or ('Output' in d) or ('Position' in d):
                    d_float = parse_any_number(d)[0]
                    return d_float
                elif d == 'Continuous':
                    d_float = 360.0
                    return d_float
                elif d in ['Adjustable', 'Programmable', 'Jumper', 'Ohms', 'Multiturn', 'Series', 'GMV', 'Varies']:
                    return 0.0
            #elif '/' in d:
                # d = re.sub('/.*', '', d)
                # d_float = float(Quantity(d))
                # return d_float
                elif 'mOhms/' in d:
                    d = d.split('/')[0]
                    d_float = float(Quantity(d, ''))
                    return d_float
                elif 'to' in d:
                    if 'Posiiton' in d:
                        d_float = parse_any_number(d)[0]
                        return d_float
                    else:
                        d = re.sub('.*to', '', d)
                        d = re.sub(' ', '', d)
                        d_float = float(Quantity(d, ''))
                        return d_float
                elif '/' in d:
                    if 'A' in d:
                        d_float = convert_to_float(re.sub('A', '', d))
                        return d_float
                    elif 'Ohms' in d:
                        d_float = convert_to_float(re.sub('Ohms', '', d))
                        return d_float
                    else:
                        d_float = parse_any_number(d)[0]
                        return d_float
                else:
                    d_float = float(Quantity(d, ''))
                    return d_float
        else:
            print("during conversion got an empty string")
            return 0.0
    else:
        print("during type conversion got a non-string")
        return d


def extract_torque(d):
    """
    Extracts torque in Nm (SI unit)
    """
    if isinstance(d, str):
        if ',' in d:

            d = d.split(',')[0]

        if 'Nm' in d:
            d_float = parse_any_number(d)[0]
            return(d_float)
        elif 'kg' in d:
            d_float = d_float = parse_any_number(d)[0]
            return(d_float)
        elif (('oz-in' in d) or ('/' in d)):
            d_float = d_float = parse_any_number(d)[0]
            d_float = d_float / 141.732
            return(d_float)
    else:
        print('during type conversion got a non-string.')
        return 0.0


def split_spread(d):
   """
   splits `spread_spectrum_bandwidth` specifically
   """

   if isinstance(d, str):

       center, down = d.split(', ')

       if ' ~ ' in center:
           # normalize center range
           center = re.sub(' Center Spread|±|%', '', center)
           center_min, center_max = center.split(' ~ ')
           center_min_float = abs(float(center_min))
           center_max_float = abs(float(center_max))
       else:
           center = re.sub('%', '', center)
           center = re.sub('±', '', center)
           center = re.sub('-', '', center)
           if down == 'Center Spread':
               center_min_float = abs(float(center))
               center_max_float = abs(float(center))
               down_min_float = CONST_NA
               down_max_float = CONST_NA
           if down == 'Down Spread':
               center_min_float = CONST_NA
               center_max_float = CONST_NA
               down_min_float = abs(float(center))
               down_max_float = abs(float(center))

       if ' ~ ' in down:
           down = re.sub(' Down Spread|±|%', '', down)
           down_min, down_max = down.split(' ~ ')
           down_min_float = abs(float(down_min))
           down_max_float = abs(float(down_max))


       return (center_min_float, center_max_float, down_min_float, down_max_float)
   else:
       print('during type conversion got a non-string.')
       return (0.0, 0.0, 0.0, 0.0)


def parse_any_number(d: str):
    """
    parse out any number from string

    """
    # this is just floats
    # regexp =re.compile(r'\d+\.\d+')
    # this is just integers
    # regexp =re.compile(r'\d+')
    # this one only works for positive numbers
    # regexp =re.compile(r'(\d+(\.\d+)?)')
    # this one works for negative numbers too.
    regexp = re.compile(r'([+-]?(\d+)(\.(\d+))?)')
    res = regexp.findall(d)
    if len(res) > 0:
        for k, v in enumerate(res):
            res[k] = float(v[0])
        return res
    else:
        return d
    return d


def parse_dimension3d(d: str):
    """
    extracts w, h, d from 3d entries
    """
    if isinstance(d, str):
        d_float = parse_any_number(d)
        w = d_float[0]
        h = d_float[1]
        d = d_float[2]
        return(w, h, d)
    else:
        print('during type conversion got a non-string.')
        return (0.0, 0.0, 0.0)


def inductance(d: str):
    """ turns inducance string to numeric"""
    if isinstance(d, str):
        d = d.replace('µ', 'u')
        d_float = float(Quantity(d, 'H'))
        return d_float
    else:
        print("during inductance type conversion got a non-string")
        return d


def voltage(d: str):
    """ turns voltage string to numeric"""
    if isinstance(d, str):
        d = d.replace('µ', 'u')
        d_float = float(Quantity(d, 'V'))
        return d_float
    else:
        print("during voltage type conversion got a non-string")
        return 0.0

def split_tolerance(d):
    """ turns tolerance into number """
    if isinstance(d, str):
        d = d.replace(' ', '')
        if 'nS' in d or 'Ohms' in d or 'Jumper' in d or 'GMV' in d:
            return (CONST_NA, CONST_NA)
        elif 'PPM' in d:
            d = re.sub('PPM', '', d)
            if ',' in d:
                a,b = d.split(',')
                if float(a) > float(b):
                    d_float = float(a)/1000000
                else:
                    d_float = float(b)/1000000
            else:
                d_float = float(d)/1000000
            return(d_float,CONST_NA)
        elif 'Ohm' in d:
            d = d.replace('%', '')
            d = d.replace('±', '')
            d = d.replace('Ohm', '')
            if (',') in d:
                a,b = d.split(',')
                d_float1 = float(Quantity(b))
                d_float2 = float(Quantity(a))
                return (d_float1, d_float2)
            else:
                d = d.replace('Ohm', '')
                d_float = float(d)
                return (CONST_NA, d_float)
        elif ',' in d:
            if len(d.split(',')) == 4:
                d = d.replace('%', '')
                a,b,c,d = d.split(',')
                a = float(a)
                b = float(b)
                c = float(c)
                d = float(d)
                d_float = min(a,b,c,d)
                return (CONST_NA, d_float)
                
            elif len(d.split(',')) == 3:
                a,b,c = d.split(',')
                a = a.replace('%', '')
                b = b.replace('%', '')
                c = c.replace('%', '')
                a = a.replace('±', '')
                b = b.replace('±', '')
                c = c.replace('±', '')
                if float(Quantity(a)) > float(Quantity(b)) and float(Quantity(a)) > float(Quantity(c)):
                    d_float = float(Quantity(a))
                    return (d_float, CONST_NA)
                elif float(Quantity(b)) > float(Quantity(a)) and float(Quantity(b)) > float(Quantity(c)):
                    d_float = float(Quantity(b))
                    return (d_float, CONST_NA)
                elif float(Quantity(c)) > float(Quantity(b)) and float(Quantity(c)) > float(Quantity(a)):
                    d_float = float(Quantity(c))
                    return (d_float, CONST_NA)
            elif len(d.split(',')) == 2:
                a,b = d.split(',')
                if '%' in a and '%' in b:
                    a = a.replace('%', '')
                    b = b.replace('%', '')
                    a = a.replace('±', '')
                    b = b.replace('±', '')
                    if float(Quantity(a)) > float(Quantity(b)):
                        d_float = float(Quantity(a))
                    else:
                        d_float = float(Quantity(b))
                    return (d_float, CONST_NA)
                elif 'H' in d:
                    if float(Quantity(a)) > float(Quantity(b)):
                        d_float = float(Quantity(a))
                    else:
                        d_float = float(Quantity(b))
                    return (CONST_NA, d_float)
        elif 'to' in d:
            a, b = d.split('to')
            if '%' in a and '%' in b:
                a = a.replace('%', '')
                b = b.replace('%', '')
                if float(Quantity(a)) > float(Quantity(b)):
                    d_float = float(Quantity(a))
                else:
                    d_float = float(Quantity(b))
                return (d_float, CONST_NA)
        elif '/' in d:
            a, b = d.split('/')
            if '%' in a and '%' in b:
                a = a.replace('%', '')
                b = b.replace('%', '')
                if float(Quantity(a)) > float(Quantity(b)):
                    d_float = float(Quantity(a))
                else:
                    d_float = float(Quantity(b))
                return (d_float, CONST_NA)
        else:
            d = d.replace('±', '')
            d = d.replace('+', '')
            d = d.replace('-', '')
            if '%' in d:
                d = d.replace('%', '')
                d_float = float(d)
                return (d_float, CONST_NA)
            elif 'H' in d or 'C' in d or 'F' in d:
                d_float = float(Quantity(d))
                return (CONST_NA, d_float)
    else:
        print("during tolerance type conversion got a non-string")
        return (d, CONST_NA)


def current(d: str):
    """ turns current based strings into numeric"""

    if isinstance(d, str):

        # unit to consider: A
        d = d.replace('µ', 'u')
        d_float = float(Quantity(d, 'A'))
        return d_float
    else:
        print("during current type conversion got a non-string")
        return d


def resistance(d: str):
    """ turns resistance based strings into numeric"""

    if isinstance(d, str):

        # unit to consider: Ohm
        d = d.replace('µ', 'u')
        d = d.replace('s', '')
        d = d.replace(' Max', '')
        d_float = float(Quantity(d, 'Ohm'))
        return d_float
    else:
        print("during resistance type conversion got a non-string")
        return 0.0


def resistance_addunit(d: str):
    """add Ohm extension whenever it's not there"""
    d = d + 'Ohm'
    return d


def power(d: str):
    """ turns power based strings into numeric"""

    if isinstance(d, str):

        # unit to consider: W
        d = d.replace('µ', 'u')
        d = d.replace('s', '')
        d = d.replace(' Max', '')
        d_float = float(Quantity(d, 'W'))
        return d_float
    else:
        print("during power type conversion got a non-string")
        return 0.0


def capacitance(d: str):
    """turns capacitance based strings into numeric"""

    if isinstance(d, str):

        # unit to consider: F
        d = d.replace('µ', 'u')
        d = d.replace(' Max', '')
        d_float = float(Quantity(d, 'F'))
        return d_float
    else:
        print("during capacitance type conversion got a non-string")
        return d


def frequency(d: str):
    """ turns frequency based strings into numeric"""

    if isinstance(d, str):

        # unit to consider: Hz
        d = d.replace('µ', 'u')
        d = d.replace(' Max', '')
        d_float = float(Quantity(d, 'Hz'))
        return d_float
    else:
        print("during frequency type conversion got a non-string")
        return 0.0


def parse_dimensions(d):
    """splits Lenght and Width from strings
    example: '0.276" L x 0.217" W (7.00mm x 5.50mm)'
    ignoring inches, focusing on millimeters
    """
    if isinstance(d, str):
        if 'PM ' in d:
            d = re.sub('PM ', '', d)
        if ' (EER ' in d:
            d = re.sub('\ \(EER\ \d\d?\.?\d?\)', '', d)
        if ' (EF ' in d:
            d = re.sub('\ \(EF\ \d\d?\.?\d?\)','',d)
        if 'PS ' in d:
            d = re.sub('PS ', '', d)
        if 'RM ' in d:
            d = re.sub('RM ', '', d)
        if 'E ' in d:
            d = re.sub('E ', '', d)
        if 'EP ' in d:
            d = re.sub('EP ', '', d)
        if 'Ep ' in d:
            d = re.sub('Ep ', '', d)
        if 'ER ' in d:
            d = re.sub('ER ', '', d)
        if 'EV ' in d:
            d = re.sub('EV ', '', d)
        if 'EF ' in d:
            d = re.sub('EF ', '', d)
        if 'P ' in d:
            d = re.sub('P ', '', d)
        if 'PQ ' in d:
            d = re.sub('PQ ', '', d)
        if 'RMR ' in d:
            d = re.sub('RMR ', '', d)
        if 'EPO ' in d:
            d = re.sub('EPO ', '', d)
        if 'EPX ' in d:
            d = re.sub('EPX ', '', d)
        if 'ETD ' in d:
            d = re.sub('ETD ', '', d)
        if 'EFD ' in d:
            d = re.sub('EFD ', '', d)
        if 'X' in d:
            d = re.sub('X', 'x', d)
        if (d.endswith(' x') == True):
            k = d.rfind(" x")
            d = d[:k] + "" + d[k+2:]
        if d.endswith('-1'):
            d = re.sub('-1', '', d)
        
        if 'mm' not in d:
            if 'x' in d:
                d_list = d.split('x')
                d_list = [w.replace(' ', '') for w in d_list]
                if len(d_list) == 2:
                    return (float(d_list[0]),float(d_list[1]), CONST_NA)
                elif len(d_list) == 3:
                    return (float(d_list[0]),float(d_list[1]),float(d_list[2]))
            elif 'x' not in d:
                return (float(d), CONST_NA, CONST_NA)
        else:
            regexp = re.compile(r'([\d\.*]+[\ ]?mm)')
            res = regexp.findall(d)
            if len(res) == 2:
                l, w = res[0], res[1]
                l = float(Quantity(l, scale='mm'))
                w = float(Quantity(w, scale='mm'))
                return (l, w, CONST_NA)
            elif len(res) == 3:
                l, w, h = res[0], res[1], res[2]
                l = float(Quantity(l, scale='mm'))
                w = float(Quantity(w, scale='mm'))
                h = float(Quantity(h, scale='mm'))
                return (l, w, h)
            elif len(res) == 1:
                dim = float(Quantity(res[0], scale='mm'))
                return (dim, CONST_NA, CONST_NA)
    else:
        return (d, CONST_NA, CONST_NA)


def split_band(d: str):
    """
    Splits attenuation bands into min and max
    """
    if isinstance(d, str):
        if ' / ' in d:

            band_min, band_max = d.split(' / ')
            if band_max == '-':
                band_max_float = 0
            else:
                band_max_float = parse_any_number(band_max)[0]

            band_min_float = parse_any_number(band_min)[0]
            band_typ = 0
            return(band_min_float, band_max_float, band_typ)
        else:
            band_typ = parse_any_number(d)[0]
            band_min_float = 0
            band_max_float = 0
            return(band_min_float, band_max_float, band_typ)
    else:
        print('During type conversion got a non-string.')
        return(0.0, 0.0, 0.0)



def split_temp(d):
    """ splits temperature (or similar) columns into min and max"""
    if isinstance(d, str):
        
        if 'µ' in d:
            d = re.sub('µ', 'u', d)
        
        if '°C' in d:
            d = re.sub('°C', '', d)
        
        if ((' (' in d) and (')' in d)):
            d = re.sub(' \(.*', '', d)
        
        if d == 'Self Powered' or d == 'DC' or d == "Multi-Voltage" or d == "Multiple":
            return (CONST_NA, CONST_NA)
        
        if '±' in d:
            d = re.sub('±', '', d)
        
        if ', ' not in d:
            if '~' in d:
                t_min, t_max = d.split('~')
                t_min = re.sub(' ', '', t_min)
                t_max = re.sub(' ', '', t_max)

                if (t_min.endswith('k')):
                    t_min = re.sub('k', '000', t_min)
                elif (t_min.endswith('M')):
                    t_min = re.sub('M', '000000', t_min)

                if (t_max.endswith('k')):
                    t_max = re.sub('k', '000', t_max)
                elif (t_max.endswith('M')):
                    t_max = re.sub('M', '000000', t_max)

                if t_min == 'DC':
                    t_min_float = 0.0
                    t_min_float1 = float(Quantity(t_min_float))
                    t_max_float1 = float(Quantity(t_max))
                    return (t_min_float1, t_max_float1)
                else:
                    parsed_t_min = parse_any_number(t_min)[0]
                    parsed_t_max = parse_any_number(t_max)[0]
                    t_min_float2 = float(Quantity(t_min))
                    t_max_float2 = float(Quantity(t_max))
                    return (t_min_float2, t_max_float2)
            elif len(parse_any_number(d)) == 1:
                parsed_temp = float(Quantity(d))
                # changed here: 4yy9p
                t_min_float3 = parsed_temp
                t_max_float3 = CONST_NA
                return (t_min_float3, t_max_float3)
            elif ' to ' in d:
                t_min, t_max = d.split(' to ')
                t_min = re.sub(' ', '', t_min)
                t_max = re.sub(' ', '', t_max)

                if t_min == 'DC':
                    t_min_float = 0.0
                    t_min_float4 = float(Quantity(t_min_float))
                    t_max_float4 = float(Quantity(t_max))
                    return (t_min_float4, t_max_float4)
                else:
                    parsed_t_min = parse_any_number(t_min)[0]
                    parsed_t_max = parse_any_number(t_max)[0]
                    t_min_float5 = float(Quantity(parsed_t_min))
                    t_max_float5 = float(Quantity(parsed_t_max))
                    return (t_min_float5, t_max_float5)
            elif '/' in d and 'Hz' in d:
                
                unit_list = re.findall('[a-zA_Za-zA-Z](?!\d+\/\d+)', d)
                unit = ''.join(unit_list)
                
                h_min, h_max = parse_any_number(d)
                h_min = str(h_min) + unit
                h_max = str(h_max) + unit
                
                h_min_float = extract_num(h_min)
                h_max_float = extract_num(h_max)
                return (h_min_float, h_max_float)
            
            elif '/' in d and 'VAC' in d:
                d = re.sub('VAC', '', d)
                a,b = d.split('/')
                d_float1 = float(a)
                d_float2 = float(b)
                return (d_float1, d_float2)
                
            else:
                # changed here: 4yy9p
                t_min_float6 = float(Quantity(d, ''))
                t_max_float6 = CONST_NA
                return (t_min_float6, t_max_float6)

        elif ', ' in d:
            d = d.split(', ')[0]
            if ' ~ ' in d:
                t_min, t_max = d.split(' ~ ')
                t_min = re.sub(' ', '', t_min)
                t_max = re.sub(' ', '', t_max)
                if t_min == 'DC':
                    t_min_float = 0.0
                    t_min_float7 = float(Quantity(t_min_float))
                    t_max_float7 = float(Quantity(t_max))
                    return (t_min_float7, t_max_float7)
                else:
                    t_min_float8 = float(Quantity(t_min))
                    t_max_float8 = float(Quantity(t_max))
                    return (t_min_float8, t_max_float8)
            elif ' to ' in d:
                t_min, t_max = d.split(' to ')
                t_min = re.sub(' ', '', t_min)
                t_max = re.sub(' ', '', t_max)
                if t_min == 'DC':
                    t_min_float = 0.0
                    t_min_float9 = float(Quantity(t_min_float))
                    t_max_float9 = float(Quantity(t_max))
                    return (t_min_float9, t_max_float9)
                else:
                    t_min_float10 = float(Quantity(t_min))
                    t_max_float10 = float(Quantity(t_max))
                    return (t_min_float10, t_max_float10)
            else:
                # changed here: 4yy9p
                t_min_float11 = float(Quantity(d, ''))
                t_max_float11 = CONST_NA
                return (t_min_float11, t_max_float11)

        else:
            print(
                "no commas were found while search for one. couldn't split temp")
            return(0.0, 0.0)

    else:
        print("during type conversion got a non-string")
        return(d, CONST_NA)

def parse_dimension(d):
    """
    parse dimensions from strings.
    works with using the following formats:
        1 1/2
        1 3/8
        2 in
        33 mm)
        mm x111
        Swagelok™,111
        22 mm (0.875)
        0.512" (13.00mm)
        0.512\" (13.00mm)
        12.7 mm (0.5 in)
        83.500" (212.09cm)
        118.11µin (3.00µm)
        7.6 m (25 ft)
        25 ft
        15' (4.6m) 5 yds
        50 cm
    """
    #print("going to parse dimensions for input: {0}".format(d))
    
    if isinstance(d, int) or isinstance(d, float):
        return d
    elif d == 0.0:
        return 0.0
    elif d == 'n/a':
        return d
    elif "°" in d:
        d_float = parse_any_number(d)[0]
        return d_float
    elif d == 'No Shaft' or d == 'Flush' or d == 'Swagelok™,111' or d == '1/4, 15/32' or d == '15/32 -32' or d == '10-48' or d == 'M6' or d == 'Flash' or d == 'Custom' or d == 'mm x111' or d == 'CG' or d == 'DG' or d == '1/4-40' or d == 'M12' or d == '15/32-32' or d == '11/16-28' or d == 'M6P' or d == 'M5' or d == 'M15' or d == 'M18' or d == 'M10' or d == '40-48' or d == '15/32':
        return CONST_NA
    elif d == '0.0':
        return 0.0
    elif d == '1 1/2' or d == '1 1/2"' or d == '1 1/2\"' or d == '1 1/2 in':
        d_float = 38.1
        return d_float
    elif d == '6 uF':
        d_float = 6.0
        return d_float
    elif d == '1/4"':
        d_float = 6.35
        return d_float
    elif d == '1 3/8':
        d_float = 34.925
        return d_float
    elif ' ft' in d and ' in' in d:
       list = d.split()
       ft_str = float(list[0])
       in_str = float(list[2])
       d_float = ft_str*304.8 + in_str*25.4
       return d_float
    elif ' in Flatted' in d:
        if 'to' in d:
            a,b = d.split(' in Flatted to ')
            if convert_to_float(Quantity(a)) < convert_to_float(Quantity(b)):
                d_float = convert_to_float(a) * 25.4
            else:
                d_float = convert_to_float(b) * 25.4
        else:
            d = re.sub(' in Flatted', '', d)
            d_float = convert_to_float(d) * 25.4
        return d_float
    elif ' Flatted to M' in d:
        d_float = float(d.split(' Flatted to M')[1])
        return d_float
    elif ' in D-Shaft' in d:
        d = re.sub(' in D-Shaft', '', d)
        d_float = convert_to_float(d) * 25.4
        return d_float
    elif ' mm D-Shaft' in d:
        d = re.sub(' mm D-Shaft', '', d)
        d_float = convert_to_float(d)
        return d_float
    elif '-' in d:
        a = d.split('-')[0]
        a = a.strip(' ')
        a = re.sub('in', '', a)
        d_float = convert_to_float(a) * 25.4
        return d_float
    elif len(re.findall('T\d+', d)) == 1:
        d_float = float(re.sub('T', '', d))
        return d_float
    elif (len(re.findall(' in$', d)) != 0):
        d = re.sub(' in', '', d)
        if ', ' in d:
            a,b = d.split(', ')
            if convert_to_float(Quantity(a)) < convert_to_float(Quantity(b)):
                d_float = convert_to_float(a) * 25.4
            else:
                d_float = convert_to_float(b) * 25.4
        else:
            d_float = convert_to_float(d) * 25.4
        return d_float
    elif (len(re.findall('(\d+.\d)+m\)$', d)) != 0):
        d_float = float(re.findall('(\d+.\d)+m\)$', d)[0]) * 1000
        return d_float
    elif (len(re.findall('(\d+)m\)$', d)) != 0):
        d_float = float(re.findall('(\d+)m\)$', d)[0]) * 1000
        return d_float
    elif (len(re.findall('(\d+.\d+)m\)', d)) != 0):
       d_float = float(re.findall('(\d+.\d+)m\)', d)[0]) * 1000
       return d_float
    elif (len(re.findall('(\d+)m\)', d)) != 0):
       d_float = float(re.findall('(\d+)m\)', d)[0]) * 1000
       return d_float
    elif 'cm)' in d:
        d = re.findall('\d+.\d+cm', d)[0]
        d_float = parse_any_number(d)[0]
        d_float = d_float * 10
        return d_float
    elif 'µm)' in d:
        d = re.findall('\d+.\d+µm', d)[0]
        d_float = parse_any_number(d)[0]
        d_float = d_float * 0.001
        return d_float
    elif 'um' in d:
        d = re.findall('\d+ um', d)[0]
        d_float = parse_any_number(d)[0]
        d_float = d_float * 0.001
        return d_float
    elif ' ft' in d:
        d_float = parse_any_number(re.findall('\d+ ft', d)[0])[0]
        d_float = d_float * 304.8
        return d_float
    elif ' in' in d:
        
        if 'mm (' in d:
            d_float = parse_any_number(d)[0]
            return d_float
        elif 'mm)' in d:
            d_float = parse_any_number(d)[1]
            return d_float
        else:
            # TODO: test this. what happens if you have both mm and inches? in the same string
            d = re.sub(' in', '', d)
            d_float = float(Fraction(re.sub(' in', '', d))) * 25.4
            return d_float
    elif (len(re.findall(' m$', d)) != 0):
        d_float = parse_any_number(d)[0] * 1000
        return d_float
    elif (len(re.findall(' M$', d)) != 0):
       d_float = parse_any_number(d)[0] * 1000
       return d_float
    elif (len(re.findall(' mm$', d)) != 0):
        d_float = parse_any_number(d)[0]
        return d_float
    elif (len(re.findall(' cm$', d)) != 0):
        d_float = parse_any_number(d)[0] * 10
        return d_float
    if 'mm' in d:
        #regexp = re.compile(r'[\()]?(.*)[\s]?mm')
        """
        this regexp tries  to capture both patterns:
        22 mm (0.875)
        0.512" (13.00mm)
        the
        """
        regexp = re.compile(r'[\s]?([\d\.]+)[\s]?mm')
        try:
            res = regexp.findall(d)
        except:
            print("couldn't run regepxt on input {0}".format(d))
        if len(res) > 0:
            try:
                if res[0] is not None:
                    res1 = re.sub('mm x.*', '', res[0])
                    res2 = re.sub('Swagelok™,.*', '', res1)
                    d_float = float(Quantity(res2, "mm"))
                    return d_float
                else:
                    func_name = inspect.stack()[0][3]
                    print('function "{0}" could not find any of the patters it knows under "res[0]". found type{1} containing: {2}.'.format(
                        func_name, type(d), repr(d)))
                    return d
            except:
                print("can't handle these special cases")
        else:
            func_name = inspect.stack()[0][3]
            print('function "{0}" could not find any of the patters it knows under "mm". found type{1} containing: {2}.'.format(
                func_name, type(d), repr(d)))
            return d
    else:
        # inspect.currentframe().f_code.co_name
        func_name = inspect.stack()[0][3]
        print('function "{0}" could not find any of the patterns it knows to handle. found type{1} containing: {2}.'.format(
            func_name, type(d), repr(d)))
        d = parse_any_number(d)[0]
        return d


def split_at(d):
    """split strings which are presented
    in the format: ... @ ...
    """
    if isinstance(d, str):

        d = re.sub('µ', 'u', d)
        d = re.sub(',.*', '', d)
        if ('@' in d):
            n1, n2 = d.split('@')
            n1 = re.sub('Parallel ', '', n1)
            n2 = re.sub('Series ', '', n2)
            n1 = n1.strip(" ")
            n2 = n2.strip(" ")
            if (' Minute' in n2):
                n1 = float(Quantity(n1))
                n2 = float(n2[0]) * 60
            elif (' Hrs' in n1):
                n1 = float(Quantity(n1)) * 3600
                n2 = float(Quantity(n2))
            elif 'VAC/DC' in n2:
                n1 = re.sub('VA', '', n1)
                n1 = float(re.sub('A', '', n1))
                n2 = float(re.sub('VAC/DC', '', n2))
            elif 'VAC' in n2:
                n1 = float(Quantity(n1))
                n2 = re.sub('VAC', '', n2)
                n2 = re.sub('VDC', '', n2)
                if '/' in n2:
                    
                    a,b = n2.split('/')
                    if float(a) > float(b):
                        n2 = float(a)
                    else:
                        n2 = float(b)
                else:
                    n2 = float(n2)
            else:
                n1 = float(Quantity(n1))
                n2 = float(Quantity(n2))
            return(n1, n2)
        elif ('@' not in d):
            if ('/' in d):
                n1 = float(Quantity(d.split('/')[0]))
                n2 = CONST_NA
                return (n1, n2)
            elif ('Ohm' in d):
                n1 = float(Quantity(d))
                n2 = CONST_NA
                return(n1, n2)
            elif ('V' in d):
                n1 = float(Quantity(d))
                n2 = CONST_NA
                return(n1, n2)
            elif (('mm' in d) or ('A' in d) or ('ohm' in d) or ('OHm' in d)):
                n1 = float(Quantity(d))
                n2 = CONST_NA
                return (n1, n2)
            else:
                #print(
                    #"recheck splitting symbol and update function accordingly. Pattern: ", d)
                return(0.0, 0.0)

    else:
        print("during type conversion got a non-string")
        return(d, 0.0)


def split_to(d):
    """split headers with extension 'to'
    in the format: 1000 pF to 330000 pF
    """
    if isinstance(d, str):
        
        if ('N' in d):
            if ('N cm' in d):
                d = re.sub('N ', '', d)
                d_float = float(Quantity(d))
                return (d_float, CONST_NA)
            elif ('N m' in d):
                d = re.sub('N ', '', d)
                d_float = float(Quantity(d))*1000
                return (d_float, CONST_NA)
            elif ('+/-' in d):
                if ('mN' in d):
                    d = re.sub('\+/\-', '', d)
                    a = d.split('mN')[0]
                    b = d.split('mN')[1]
                    a = re.sub(' ', '', a)
                    b = re.sub(' ', '', b)
                    a_float = float(a)
                    b_float = float(b)
                    d_float1 = (a_float - b_float)/1000
                    d_float2 = (a_float + b_float)/1000
                    return (d_float1, d_float2)
                else:
                    d = re.sub('\+/\-', '', d)
                    a = d.split('N')[0]
                    b = d.split('N')[1]
                    a = re.sub(' ', '', a)
                    b = re.sub(' ', '', b)
                    a_float = float(a)
                    b_float = float(b)
                    d_float1 = (a_float - b_float)
                    d_float2 = (a_float + b_float)
                    return (d_float1, d_float2)
            elif ('lb' in d):
                a = d.split('N')[0]
                a = re.sub(' ', '', a)
                d_float = float(a)
                return (d_float, CONST_NA)
            elif ('g' in d):
                a = d.split('N')[0]
                a = re.sub(' ', '', a)
                d_float = float(a)
                return (d_float, CONST_NA)
            elif ('cN' in d):
                a = d.split('G')[1]
                a = re.sub(' ', '', a)
                a = re.sub('cN', '', a)
                d_float = float(a)/100
                return (d_float, CONST_NA)
            elif ('to' in d and 'oz' in d):
                if '(' in d:
                    d = d.split('(')[0]
                    a,b = d.split(' to ')
                    a = re.sub('N', '', a)
                    b = re.sub('N', '', b)
                    a = re.sub(' ', '', a)
                    b = re.sub(' ', '', b)
                    d_float1 = float(a)
                    d_float2 = float(b)
                    return (d_float1, d_float2)
                elif '/' in d:
                    d_float1 = parse_any_number(d)[1]
                    d_float2 = parse_any_number(d)[3]
                    return (d_float1, d_float2)
            elif ' to ' in d:
                a,b = d.split(' to ')
                d_float1 = float(Quantity(a))
                d_float2 = float(Quantity(b))
                return (d_float1, d_float2)
            else:
                if (d.count('N') == 1):
                    # changed here: 4yyma
                    d_float1 = float(Quantity(d))
                    d_float2 = CONST_NA
                    return (d_float1, d_float2)
                elif ', ' in d:
                    # changed here: 4yyma
                    d = d.split(', ')[0]
                    d_float1 = float(Quantity(d))
                    d_float2 = CONST_NA
                    return (d_float1, d_float2)
                else:
                    a = d.split('N')[0]
                    b = d.split('N')[1]
                    a = re.sub(' ', '', a)
                    b = re.sub(' ', '', b)
                    d_float1 = float(a) - float(b)
                    d_float2 = float(a) + float(b)
                    return (d_float1, d_float2)
        elif ('oz' in d):
            if ( ' + ' in d and ' - ' in d):
                a = d.split('oz')[0]
                b = d.split('oz')[1]
                c = d.split('oz')[2]
                a = re.sub(' ', '', a)
                b = re.sub(' ', '', b)
                c = re.sub(' ', '', c)
                a_float = float(a)
                b_float = float(b)
                c_float = float(c)
                d_float1 = (a_float + c_float)/3.6
                d_float2 = (a_float + b_float)/3.6
                return (d_float1, d_float2)
            elif ('+/-' in d):
                d = re.sub('\+/\-', '', d)
                a = d.split('oz')[0]
                b = d.split('oz')[1]
                a = re.sub(' ', '', a)
                b = re.sub(' ', '', b)
                a_float = float(a)
                b_float = float(b)
                d_float1 = (a_float - b_float) / 3.6
                d_float2 = (a_float + b_float) / 3.6
                return (d_float1, d_float2)
            elif ('+' in d):
                d = re.sub('\+', '', d)
                a = d.split('oz')[0]
                b = d.split('oz')[1]
                a = re.sub(' ', '', a)
                b = re.sub(' ', '', b)
                a_float = float(a)
                b_float = float(b)
                d_float1 = (a_float - b_float) / 3.6
                d_float2 = (a_float + b_float) / 3.6
                return (d_float1, d_float2)
        elif (' in lb' in d):
            d = re.sub(' in lb', '', d)
            d_float = float(d) * 4.44
            return (d_float, CONST_NA)
            
        
        d = re.sub('µ', 'u', d)
        d = re.sub('Â', '', d)

        if (', ' in d):
            d = d.split(',', 1)[0]
        
        if ('< ' in d):
            d = re.sub('< ', '0 to ', d)
        
        if (' + Jumper' in d):
            d = re.sub(' \+ Jumper', '', d)
        
        if ('+/- ' in d):
            d = re.sub('\+/\- ', '', d)

        if ('/' in d):
            d = d.split('/')[0]
            
        if (' x 2' in d):
            d = re.sub(' x 2', '', d)
        
        if ('ÂµH' in d):
            d = re.sub('ÂµH', 'uH', d)

        if ('DC' in d):
            d = re.sub('DC', '0', d)
            
        if ('2.483.5GHz' in d):
            d = re.sub('.5', '', d)
        
        if (' and ' in d):
            d = d.split(' and ')[0]
            
        if d == 'Custom' or d == 'Programmable' or d == 'Variable':
            n1_float = CONST_NA
            n2_float = CONST_NA
            return (n1_float, n2_float)

        if ('to' in d):
            n1, n2 = d.split('to')
            n1 = n1.strip(" ")
            n1 = re.sub("kHz Hz", "kHz", n1)
            n2 = n2.strip(" ")
            n1 = re.sub('\- ', '-', n1)
            n1 = re.sub('\+ ', '+', n1)
            n2 = re.sub('\- ', '-', n2)
            n2 = re.sub('\+ ', '+', n2)
            if ',' in n2:
                n2 = re.sub(',', '.', n2)
            
            n1_float = float(Quantity(n1))
            n2_float = float(Quantity(n2))
            return(n1_float, n2_float)
        elif (' ~ ' in d):
            n1, n2 = d.split(' ~ ')
            n1 = n1.strip(" ")
            n2 = n2.strip(" ")
            n1_float = float(Quantity(n1))
            n2_float = float(Quantity(n2))
            return(n1_float, n2_float)
        elif (' - ' in d):
            n1, n2 = d.split(' - ')
            n1 = n1.strip(" ")
            n2 = n2.strip(" ")
            n1_float = float(Quantity(n1))
            n2_float = float(Quantity(n2))
            return(n1_float, n2_float)
        elif '-' in d and 'Hz' in d:
                
            unit_list = re.findall('[a-zA_Za-zA-Z](?!\d+\-\d+)', d)
            unit = ''.join(unit_list)
                
            h_min, h_max = parse_any_number(d)
            h_min = str(h_min) + unit
            h_max = abs(h_max)
            h_max = str(h_max) + unit
                
            h_min_float = extract_num(h_min)
            h_max_float = extract_num(h_max)
            return (h_min_float, h_max_float)

        elif (' Max' in d):
            d = re.sub(' Max', '', d)
            n1_float = CONST_NA
            n2_float = float(Quantity(d, ''))
            return(n1_float, n2_float)
        elif (' Min' in d):
            d = re.sub(' Min', '', d)
            n1_float = float(Quantity(d, ''))
            n2_float = CONST_NA
            return (n1_float, n2_float)
        elif (' mV0o' in d):
            d = re.sub(' mV0o', 'mV', d)
            d = re.sub(' V0', 'V', d)
            a,b = d.split(' ')
            n1_float = float(Quantity(a, ''))
            n2_float = float(Quantity(b, ''))
            return (n1_float, n2_float)
        else:
            # changed here: 4yyma
            n1_float = float(Quantity(d, ''))
            n2_float = CONST_NA
            return(n1_float, n2_float)

    else:
        print("during type conversion got a non-string")
        return(d, d)


def split_q(d: str)-> typing.Tuple[float, float]:
    """split a Q string with @ into two values
    input looks like  "q_@_freq": "72 @ 100MHz"
    output should look like
    q = 72
    freq_hz = 100000000
    """
    q, freq = d.split('@')
    q = q.strip(" ")
    q_float = float(q)
    freq = freq.strip(" ")
    freq_float = float(Quantity(freq))
    return (q_float, freq_float)


def split_rc(d: str) -> typing.Tuple[float, float]:
    """split a rc string with @ into two values
    input looks like  "ripple_current_@_low_frequency": "28mA @ 120Hz"
    output should look like
    c = 0,028
    freq = 120
    """
    c, freq = d.split('@')
    c = c.strip(" ")
    c_float = float(Quantity(c))
    freq = freq.strip(" ")
    freq_float = float(Quantity(freq))
    return(c_float, freq_float)


def split_esr(d: str) -> typing.Tuple[float, float]:
    """split esr string into r and freq
    input looks like: '520 mOhm @ 100kHz'
    output should look like
    r = 0.52
    freq = 100000
    """
    r, freq = d.split('@')
    r = r.strip(" ")
    r_float = float(Quantity(r))
    freq = freq.strip(" ")
    freq_float = float(Quantity(freq))
    return(r_float, freq_float)


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
    return(t, c)


def category_normalize_digikey(d: dict):
    """
    For categories, instead of changing the name
    """
    for n, i in enumerate(d):
        if i in categories['digikey']:
            d[n] = categories['digikey'][i]
        else:
            #print("missing mapping for category name: {0}".format(i))
            #common.send_msg(json.dumps({"source": 'digikey', "categories": d, "key": "missing_category_mapping"}))
            try:
                c.agg.add_category({"source": 'digikey', "categories": (
                    "digikey/" + "__".join(d).replace(" ", "_")).lower(), "key": "missing_category_mapping"})
            except:
                print(
                    "missing mapping for category name: {0}".format(i))
                pass

    return d


def cat_normalize_digikey(d: list):
    d_str = str(d)
    d_str = re.sub('\', \'', '\',\'', d_str)

    if d_str in categories['digikey']:
        result_str = categories['digikey'][d_str]
        result = eval(result_str)
        return result
    else:
        print("missing mapping for category name: {0}".format(d))
        return d


def to_int(d: str):
    """turns a string into integer"""
    if isinstance(d, (str)):
        return int(d)
    else:
        raise TypeError(
            'cannot cast {0} into float as it\'s not a string'.format(d))

def inchtomm(d: str):
    """turns inch into mm"""
    if isinstance(d, str):
        d_float = parse_any_number(d)[0]
        d_float = d_float * 25.4
        return d_float
    else:
        if isinstance(d, int):
            d_float = d * 25.4
            return d_float
        func_name = inspect.currentframe().f_code.co_name
        print('found an error in function "{0}" during type conversion found type{1} containing: {2}.'.format(
            func_name, type(d), repr(d)))
        return 0.0

def to_float(d: str):
    """turns a string into decimal"""
    if isinstance(d, str):
        return float(d)
    else:
        raise TypeError(
            'cannot cast {0} into float as it\'s not a string'.format(d))


def split_double(d: str):

    if isinstance(d, str):
        if ' / ' in d:
            low, high = d.split(' / ')
            low_min, low_max = split_temp(low)
            high_min, high_max = split_temp(high)
            return(low_min, low_max, high_min, high_max)
        else:
            print(
                'Range separator is different than noted. Please update.')
            return(0.0, 0.0, 0.0, 0.0)
    else:
        print('during type conversion got a non-string.')
        return(0.0, 0.0, 0.0, 0.0)


def split_current(d: str):

    if isinstance(d, str):

        if (', ' in d):
            
            res = d.split(', ')
            p = res[0]
            s = res[1]
            p = re.sub('Parallel ', '', p)
            s = re.sub('Series ', '', s)
            p = re.sub('±', '', p)
            s = re.sub('±', '', s)
            if ('/' in p):
                p = p.split('/')[0]
            if ('/' in s):
                s = s.split('/')[0]
            p_float = float(Quantity(p, ''))
            s_float = float(Quantity(s, ''))
            return (p_float, s_float)
        else:
            p_float = float(Quantity(d, ''))
            s_float = p_float
            return (p_float, s_float)
    else:
        print('during type conversion got a non-string.')
        return (0.0, 0.0)


def split_resistance(d: str):

    if isinstance(d, str):

        if (', ' in d):
            
            if 'Max' in d:
                d = re.sub('Max', '', d)
                d = re.sub(' ', '', d)

            p, s = d.split(',')
            p = re.sub(' Primary', '', p)
            s = re.sub(' Secondary', '', s)
            p_float = float(Quantity(p, ''))
            s_float = float(Quantity(s, ''))
            return (p_float, s_float)
        elif (' Max' in d):
            d = re.sub(' Max', '', d)
            p_float = float(Quantity(d, ''))
            s_float = p_float
            return (p_float, s_float)
        else:
            p_float = extract_num(d)
            s_float = p_float
            return (p_float, s_float)
    else:
        print('during type conversion got a non-string.')
        return (0.0, 0.0)


def split_sensitivity(d: str):

    if isinstance(d, str):

        if ('±' in d):

            sen, rest = d.split('±')
            sen_float = extract_num(sen)

            if ('@' in rest):

                tol, cond = rest.split('@')
                tol_float = extract_num(tol)
                cond_float = extract_num(cond)
            else:
                tol_float = extract_num(rest)
                cond_float = 0.0
            return(sen_float, tol_float, cond_float)
        else:
            d_float = parse_any_number(d)[0]
            return (d_float, 0.0, 0.0)
    else:
        print('during type conversion got a non-string.')
        return (0.0, 0.0, 0.0)


def split_spl(d: str):

    if isinstance(d, str):
        if '@' in d:
            
            volume = d.split('@')[0]
            volume_float = extract_num(volume)

            v_d = d.split('@')[1]

            voltage = v_d.split(',')[0]
            distance = v_d.split(',')[1]

            voltage_float = extract_num(voltage)
            distance_float = extract_num(distance)

            return (volume_float, voltage_float, distance_float)
        else:
            volume_float = extract_num(d)
            return (volume_float, CONST_NA, CONST_NA)
    else:
        print('during type conversion got a non-string.')
        return (d, CONST_NA, CONST_NA)


def split_timing(d: str):

    if isinstance(d, str):

        if 'Fixed, ' in d:
            d = re.sub('Fixed, ', '', d)

        if 'Fixed' in d:
            d = re.sub('Fixed', '', d)

        if ', ' in d:

            d = re.sub(', .*', '', d)

        if '~' in d:
            d = re.sub('~', 'to', d)
        
        if 'FPM' in d or 'Cyc' in d:
            return (CONST_NA, CONST_NA)

        if 'to' in d:
            # split min and max from range
            t1, t2 = d.split('to')

            # edit t1

            if 'd' in t1:
                t1_float = parse_any_number(t1)[0] * 86400
            elif (('h' in t1) or ('hr' in t1) or ('Hrs' in t1)):
                t1_float = parse_any_number(t1)[0] * 3600
            elif (('m' in t1) or ('min' in t1) or ('Min' in t1)):
                t1_float = parse_any_number(t1)[0] * 60
            elif (('s' in t1) or ('Sec' in t1)):
                t1_float = parse_any_number(t1)[0]

            # edit t2

            if 'd' in t2:
                t2_float = parse_any_number(t2)[0] * 86400
            elif (('h' in t2) or ('hr' in t2) or ('Hrs' in t2) or ('Hr' in t2)):
                t2_float = parse_any_number(t2)[0] * 3600
            elif (('m' in t2) or ('min' in t2) or ('Min' in t2)):
                t2_float = parse_any_number(t2)[0] * 60
            elif (('s' in t2) or ('Sec' in t2) or ('S' in t2)):
                t2_float = parse_any_number(t2)[0]
            elif (('y' in t2) or ('Year' in t2)):
                t2_float = parse_any_number(t2)[0] * 31536000
            elif (('Week' in t2)):
                t2_float = parse_any_number(t2)[0] * 604800

            return (t1_float, t2_float)
        else:
            if 'd' in d:
                t1_float = parse_any_number(d)[0] * 86400
            elif (('h' in d) or ('hr' in d) or ('Hrs' in d)):
                t1_float = parse_any_number(d)[0] * 3600
            elif (('m' in d) or ('min' in d) or ('Min' in d)):
                t1_float = parse_any_number(d)[0] * 60
            elif (('s' in d) or ('Sec' in d)):
                t1_float = parse_any_number(d)[0]

            t2_float = t1_float

            return (t1_float, t2_float)
    else:
        print('during type conversion got a non-string.')
        return (0.0, 0.0)


def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


def split_contact(d):
    if isinstance(d, str):

        if ',' in d:
            d = d.split(',')[0]
        if ' or ' in d:
            d = d.split(' or ')[0]

        if ' to ' in d:
            if ' at ' in d:
                d,v = d.split(' at ')
                v = v.split(' to ')[0]
                v_float = float(Quantity(v))
            else:
                v_float = CONST_NA
            
            if ' to ' in d:
                
                d_min, d_max = d.split(' to ')
                d_min_float = float(Quantity(d_min))
                d_max_float = float(Quantity(d_max))
                return (d_min_float, d_max_float, v_float)
            else:
                d_min_float = float(Quantity(d))
                d_max_float = d_min_float
                return (d_min_float, d_max_float, v_float)
        elif ' at ' in d:
            if ' to ' in d:
                d = d.split(' to ')[0]
                
                d_min, v = d.split(' at ')
                d_min_float = float(Quantity(d_min))
                d_max_float = d_min_float
                v_float = float(Quantity(v))
                return (d_min_float, d_max_float, v_float)
            else:
                d_min, v = d.split(' at ')
                d_min_float = float(Quantity(d_min))
                d_max_float = d_min_float
                v_float = float(Quantity(v))
                return (d_min_float, d_max_float, v_float)
        elif d == "Tin":
            return (CONST_NA, CONST_NA, CONST_NA)
        elif ' - ' in d:
            d_min, d_max = d.split(' - ')
            d_min_float = float(Quantity(d_min))
            d_max_float = float(Quantity(d_max))
            return (d_min_float, d_max_float, CONST_NA)
        else:
            d_min_float = float(Quantity(d))
            d_max_float = d_min_float
            return (d_min_float, d_max_float, CONST_NA)
    else:
        print('during type conversion got a non-string.')
        return (d, d, CONST_NA)

def split_comma(d):
    """
    splits values by comma into float range
    """
    
    if isinstance(d, str):
        
        if ',' in d:
            
            d_min, d_max = d.split(',')
            
            d_min_float = float(Quantity(d_min))
            d_max_float = float(Quantity(d_max))
            
            return (d_min_float, d_max_float)
        
        else:
            
            d_float = float(Quantity(d))
            return (d_float, CONST_NA)
    else:
        print('during type conversion got a non-string.')
        return (d, CONST_NA)

def split_slash(d):
    """
    splits valye by / into float range
    """
    
    if isinstance(d, str):
        
        d = re.sub('Â', '', d)
        d = re.sub('µ', 'u', d)
        
        d_min, d_max = d.split('/')
        
        if d_min != '-':
            
            d_min_float = float(Quantity(d_min))
        
        else:
            
            d_min_float = CONST_NA
        
        if d_max != '-':
            
            d_max_float = float(Quantity(d_max))
        
        else:
            
            d_max_float = CONST_NA
        
        return (d_min_float, d_max_float)
    
    else:
        
        print('during type conversion got a non-string.')
        return (d, CONST_NA)

def split_three(d):
    """
    splits headers with three entries into a float range
    """
    if isinstance(d, str):
        d = re.sub('Â', '', d)
        d = re.sub('µ', 'u', d)
        d = re.sub(' ', '', d)
        d = re.sub('/.*', '', d)
        d = re.sub('M', 'm', d)
        d = re.sub('\(Typ\)', '', d)
        if '@' not in d: 
            d1_float = float(Quantity(d))
            return (d1_float, CONST_NA, CONST_NA)
        else:
            if ',' in d:    
                d1 = d.split(',')[0]
                d2 = d.split(',')[1]    
                if '@' in d1:
                    d1_1, d1_2 = d1.split('@')
                    d1_1_float = float(Quantity(d1_1))
                    
                    if 'A' in d1_2:
                        d1_2_float = float(Quantity(d1_2))
                        d2_float = float(Quantity(d2))
                    elif 'V' in d1_2:
                        d2_float = float(Quantity(d1_2))
                        d1_2_float = float(Quantity(d2))
                return (d1_1_float, d1_2_float, d2_float)
            else:
                d1, d2 = d.split('@')
                d1_float = float(Quantity(d1))
                d2_float = float(Quantity(d2))
                
                if 'V' in d2:    
                    return (d1_float, CONST_NA, d2_float)
                else:
                    return (d1_float, d2_float, CONST_NA)
    else:
        print('during type conversion got a non-string.')
        return (d, CONST_NA, CONST_NA)
    
def split_voltage(d: str):
    if isinstance(d, str):
        if ('- Max' in d):
            d = re.sub('- Max', '', d)
            if (',' in d):
                d1, d2 = d.split(',')
                if 'VAC' in d1:
                    d_vac_max = float(Quantity(d1))
                    d_vdc_max = float(Quantity(d2))
                    return(d_vac_max, d_vdc_max, 0.0, 0.0)
                elif 'VDC' in d1:
                    d_vac_max = float(Quantity(d2))
                    d_vdc_max = float(Quantity(d1))
                    return(d_vac_max, d_vdc_max, 0.0, 0.0)
            else:
                if 'VAC' in d:
                    d_vac_max = float(Quantity(d))
                    d_vdc_max = 0.0
                    return(d_vac_max, d_vdc_max, 0.0, 0.0)
                elif 'VDC' in d:
                    d_vdc_max = float(Quantity(d))
                    d_vac_max = 0.0
                    return(d_vac_max, d_vdc_max, 0.0, 0.0)
        elif (' - Nom' in d):
            d = re.sub('- Nom', '', d)
            if (',' in d):
                d1, d2 = d.split(',')
                if 'VAC' in d1:
                    d_vac_nom = float(Quantity(d1))
                    d_vdc_nom = float(Quantity(d2))
                    return (0.0, 0.0, d_vac_nom, d_vdc_nom)
                elif 'VDC' in d1:
                    d_vac_nom = float(Quantity(d2))
                    d_vdc_nom = float(Quantity(d1))
                    return (0.0, 0.0, d_vac_nom, d_vdc_nom)
            else:
                if 'VAC' in d:
                    d_vac_nom = float(Quantity(d))
                    d_vdc_nom = 0.0
                    return (0.0, 0.0, d_vac_nom, d_vdc_nom)
                elif 'VDC' in d:
                    d_vdc_nom = float(Quantity(d))
                    d_vac_nom = 0.0
                    return (0.0, 0.0, d_vac_nom, d_vdc_nom)
        else:
            print('New pattern found: %s', d)
            return (0.0, 0.0, 0.0, 0.0)
    else:
        print('during type conversion got a non-string.')
        return (0.0, 0.0, 0.0, 0.0)
