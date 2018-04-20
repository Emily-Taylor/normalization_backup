# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:08:54 2017

@author: HindolRakshit

Collection of normalization functions

"""
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import common

import json
import logging
from quantiphy import Quantity
import re
import yaml
import os
import typing
from fractions import Fraction
# import numpy as np


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
				v_str, r_str = d.split(' @ ')
				r1_str, r2_str = r_str.split(' ~ ')

				v = float(Quantity(v_str, ''))
				r1 = float(Quantity(r1_str, ''))
				r2 = float(Quantity(r2_str, ''))

				return(v, r1, r2)
		else:
				logging.warning('during type conversion got a non-string')


def reverse(d: str):
		d = d[::-1]
		return d


def lower(d: str):
		if isinstance(d, str):
				d = d.lower()
				return d
		else:
				return d


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
								logging.warning(
										"value: \"{0}\" doesn't cannot be converted to float".format(d))
								return 0.0
				else:
						logging.warning(
								"value: \"{0}\" doesn't match expected pattern".format(d))
						return 0.0
		else:
				logging.warning("during coeff type conversion got a non-string")


def extract_num(d: str) -> float:
		"""turns strings with ANY unit into numbers"""
		adict = {'µ': 'u', ' %': '', ' ': '', 'Max': '',
						 '±': '', 'ppm/°C': '', ' (Cutoff)': '', 'ppm': '', ' (Typ)': ''}

		if isinstance(d, str):

				if (len(d) > 0):
						d = re.sub(r'\(.*\)', '', d)
						d = d.split(',', 1)[0]
						d = multiple_replace(d, adict)

						if '@1Minute' in d:
								d_float = parse_any_number(d)[0]
								return d_float
						elif '@30Seconds' in d:
								d_float = parse_any_number(d)[0]
								return d_float
						elif 'PSI' in d:
								d_float = parse_any_number(d)[0]
								return d_float
						elif 'Pole' in d:
								d_float = parse_any_number(d)[0]
								return d_float
						elif 'Output' in d:
								d_float = parse_any_number(d)[0]
								return d_float
						elif 'Position' in d:
								d_float = parse_any_number(d)[0]
								return d_float
						else:
								d_float = float(Quantity(d, ''))
								return d_float
				else:
						logging.warning("during coversion got an empty string")
						return 0.0
		else:
				logging.warning("during type conversion got a non-string")


def split_spread(d: str):
		"""
		splits `spread_spectrum_bandwidth` specifically
		"""

		if isinstance(d, str):

				center, down = d.split(', ')

				# normalize center range
				center = re.sub(' Center Spread|±|%', '', center)
				center_min, center_max = center.split(' ~ ')
				center_min_float = abs(float(center_min))
				center_max_float = abs(float(center_max))

				# normalize down range
				down = re.sub(' Down Spread|±|%', '', down)
				down_min, down_max = down.split(' ~ ')
				down_min_float = abs(float(down_min))
				down_max_float = abs(float(down_max))
				return(center_min_float, center_max_float, down_min_float, down_max_float)
		else:
				logging.warning('during type conversion got a non-string.')
				return(0.0, 0.0, 0.0, 0.0)


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


def inductance(d: str):
		""" turns inducance string to numeric"""
		if isinstance(d, str):
				d = d.replace('µ', 'u')
				d_float = float(Quantity(d, 'H'))
				return d_float
		else:
				logging.warning("during inductance type conversion got a non-string")
				return d


def voltage(d: str):
		""" turns voltage string to numeric"""
		if isinstance(d, str):
				d = d.replace('µ', 'u')
				d_float = float(Quantity(d, 'V'))
				return d_float
		else:
				logging.warning("during voltage type conversion got a non-string")
				return 0.0


def tolerance(d: str):
		""" turns tolerance into number """
		if isinstance(d, str):
				d = d.replace('±', '')
				d = d.replace('%', '')
				return int(d)
		else:
				logging.warning("during tolerance type conversion got a non-string")


def current(d: str):
		""" turns current based strings into numeric"""

		if isinstance(d, str):

				# unit to consider: A
				d = d.replace('µ', 'u')
				d_float = float(Quantity(d, 'A'))
				return d_float
		else:
				logging.warning("during current type conversion got a non-string")
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
				logging.warning("during resistance type conversion got a non-string")
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
				logging.warning("during power type conversion got a non-string")
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
				logging.warning("during capacitance type conversion got a non-string")
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
				logging.warning("during frequency type conversion got a non-string")
				return 0.0


def parse_dimensions(d: str):
		"""splits Lenght and Width from strings
		example: '0.276" L x 0.217" W (7.00mm x 5.50mm)'
		ignoring inches, focusing on millimeters
		"""
		regexp = re.compile(r'([\d\.]+mm)')
		res = regexp.findall(d)
		if len(res) == 2:
				l, w = res[0], res[1]
				l = float(Quantity(l, scale='mm'))
				w = float(Quantity(w, scale='mm'))
				return l, w
		if len(res) == 1:
				dim = float(Quantity(res[0], scale='mm'))
				return (dim,)


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
				logging.warning('During type conversion got a non-string.')
				return(0.0, 0.0, 0.0)


def split_temp(d: str) -> typing.Tuple[float, float]:
		""" splits temperature (or similar) columns into min and max"""
		if isinstance(d, str):
				if ', ' not in d:
						if ' ~ ' in d:
								t_min, t_max = d.split(' ~ ')
								if t_min == 'DC':
										t_min_float = 0.0
										t_min_float = float(Quantity(t_min_float))
										t_max_float = float(Quantity(t_max))
										return (t_min_float, t_max_float)
								else:
										t_min_float = float(Quantity(t_min))
										t_max_float = float(Quantity(t_max))
										return (t_min_float, t_max_float)
						else:
								t_min_float = float(Quantity(d, ''))
								t_max_float = t_min_float
								return (t_min_float, t_max_float)

				elif ', ' in d:
						d = d.split(', ')[0]
						if ' ~ ' in d:
								t_min, t_max = d.split(' ~ ')
								if t_min == 'DC':
										t_min_float = 0.0
										t_min_float = float(Quantity(t_min_float))
										t_max_float = float(Quantity(t_max))
										return (t_min_float, t_max_float)
								else:
										t_min_float = float(Quantity(t_min_float))
										t_max_float = float(Quantity(t_max))
										return (t_min_float, t_max_float)

						else:
								t_min_float = float(Quantity(d, ''))
								t_max_float = t_min_float
								return (t_min_float, t_max_float)

				else:
						logging.warning(
								"no commas were found while search for one. couldn't split temp")
						return(0.0, 0.0)

		else:
				logging.warning("during type conversion got a non-string")
				return(0.0, 0.0)


def parse_dimension(d: str):

		if ' in' in d:
				d = re.sub(' in', '', d)
				d_float = float(Fraction(re.sub(' in', '', d))) * 25.4
				return(d_float)

		if 'mm)' in d:
				regexp = re.compile(r'\((.*)mm\)')
				res = regexp.findall(d)

				if len(res) > 0:
						if res[0] is not None:
								d_float = float(Quantity(res[0], "mm"))
								return(d_float)
						else:
								logging.warning("no given value to be extracted.")
								return(0.0)
				else:
						logging.warning("something went wrong.")
						return(0.0)
		else:
				d = parse_any_number(d)[0]
				return(d)


def split_at(d):
		"""split strings which are presented
		in the format: ... @ ...
		"""
		if isinstance(d, str):

				d = re.sub('µ', 'u', d)
				if ('@' in d):
						n1, n2 = d.split('@')
						n1 = n1.strip(" ")
						n2 = n2.strip(" ")
						n1 = float(Quantity(n1))
						n2 = float(Quantity(n2))
						return(n1, n2)
				elif ('@' not in d):
						if (' Ohms' in d):
								n1 = float(Quantity(d))
								n2 = 0
								return(n1, n2)
						elif ('V' in d):
								n1 = float(Quantity(d))
								n2 = 0
								return(n1, n2)
						else:
								logging.warning(
										"recheck splitting symbol and update function accordingly")
								return(0.0, 0.0)

		else:
				logging.warning("during type conversion got a non-string")
				return(0.0, 0.0)


def split_to(d: str):
		"""split headers with extension 'to'
		in the format: 1000 pF to 330000 pF
		"""
		if isinstance(d, str):

				if (', ' in d):
						d = d.split(',', 1)[0]

				if (' to ' in d):
						n1, n2 = d.split(' to ')
						n1 = n1.strip(" ")
						n2 = n2.strip(" ")
						if ' m' in n1:
								n1_float = parse_any_number(n1)[0]
						else:
								n1_float = float(Quantity(n1))
						if ' m' in n2:
								n2_float = parse_any_number(n2)[0]
						else:
								n2_float = float(Quantity(n2))
						return(n1_float, n2_float)
				elif (' ~ ' in d):
						n1, n2 = d.split(' ~ ')
						n1 = n1.strip(" ")
						n2 = n2.strip(" ")
						n1_float = float(Quantity(n1))
						n2_float = float(Quantity(n2))
						return(n1_float, n2_float)
				elif (' Max' in d):
						d = re.sub(' Max', '', d)
						n1_float = 0
						n2_float = float(Quantity(d, ''))
						return(n1_float, n2_float)
				else:
						n1_float = float(Quantity(d, ''))
						n2_float = float(Quantity(d, ''))
						return(n1_float, n2_float)

		else:
				logging.warning("during type conversion got a non-string")
				return(0.0, 0.0)


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
		return(q_float, freq_float)


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
						#logging.warning("missing mapping for category name: {0}".format(i))
						common.send_msg(json.dumps(
								{"source": 'digikey', "categories": d, "key": "missing_category_mapping"}))
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
		if isinstance(d, int):
				d = d * 25.4
				return d
		else:
				logging.warning('during type conversion met a string.')


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
						logging.warning(
								'Range separator is different than noted. Please update.')
						return(0.0, 0.0, 0.0, 0.0)
		else:
				logging.warning('during type conversion got a non-string.')
				return(0.0, 0.0, 0.0, 0.0)


def split_current(d: str):

		if isinstance(d, str):

				if (', ' in d):

						p, s = d.split(', ')
						p = re.sub('Parallel ', '', p)
						s = re.sub('Series ', '', s)
						p_float = float(Quantity(p, ''))
						s_float = float(Quantity(s, ''))
						return (p_float, s_float)
				else:
						logging.warning('Splitting symbol is different. Please update.')
						return (0.0, 0.0)
		else:
				logging.warning('during type conversion got a non-string.')
				return (0.0, 0.0)


def split_resistance(d: str):

		if isinstance(d, str):

				if (', ' in d):

						p, s = d.split(', ')
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
						logging.warning('Splitting symbol is different. Please update.')
						return (0.0, 0.0)
		else:
				logging.warning('during type conversion got a non-string.')
				return (0.0, 0.0)


def split_timing(d: str):

		if isinstance(d, str):

				if ', ' in d:

						d = re.sub(', .*', '', d)

				if ' to ' in d:
						# split min and max from range
						t1, t2 = d.split(' to ')

						# edit t1

						if ' s' in t1:
								t1_float = parse_any_number(t1)[0]
						elif ' h' in t1:
								t1_float = parse_any_number(t1)[0] * 3600
						elif ' hr' in t1:
								t1_float = parse_any_number(t1)[0] * 3600
						elif ' m' in t1:
								t1_float = parse_any_number(t1)[0] * 60
						elif ' min' in t1:
								t1_float = parse_any_number(t1)[0] * 60

						# edit t2

						if ' s' in t2:
								t2_float = parse_any_number(t2)[0]
						elif ' h' in t2:
								t2_float = parse_any_number(t2)[0] * 3600
						elif ' hr' in t2:
								t2_float = parse_any_number(t2)[0] * 3600
						elif ' m' in t2:
								t2_float = parse_any_number(t2)[0] * 60
						elif ' min' in t2:
								t2_float = parse_any_number(t2)[0] * 60

						return (t1_float, t2_float)
				else:
						if ' s' in d:
								t1_float = parse_any_number(d)[0]
						elif ' h' in d:
								t1_float = parse_any_number(d)[0] * 3600
						elif ' hr' in d:
								t1_float = parse_any_number(d)[0] * 3600
						elif ' m' in d:
								t1_float = parse_any_number(d)[0] * 60
						elif ' min' in d:
								t1_float = parse_any_number(d)[0] * 60

						t2_float = t1_float

						return (t1_float, t2_float)
		else:
				logging.warning('during type conversion got a non-string.')
				return (0.0, 0.0)
