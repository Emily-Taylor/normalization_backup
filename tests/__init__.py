# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:15:43 2017

@author: HindolRakshit

Unit tests for normalization functions

"""

import unittest
import pandas as pd
import numpy as np
import normalization
import numbers
# import preprocess


class TestNorm(unittest.TestCase):
       
    def test_split_Q(self):
        output = (72.0,100000000.0)
        d = "72 @ 100MHz"
        result = normalization.split_q(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
       
    def test_split_rc(self):
       output = (0.028,120)
       d = "28mA @ 120Hz"
       result = normalization.split_rc(d)
       self.assertTrue(isinstance(result[0], numbers.Real))
       self.assertTrue(isinstance(result[1], numbers.Real))
       self.assertEqual(result, output)
       
    def test_split_l_w(self):
        output = (7.00,5.50)
        d = '0.276" L x 0.217" W (7.00mm x 5.50mm)'
        result = normalization.parse_dimensions(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
    
    def test_split_dia(self):
        output = (7.62,)
        d = '0.300" Dia (7.62mm)'
        result = normalization.parse_dimensions(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertEqual(result, output)
       
    def test_extract_num(self):
       output1 = (5.3e-07)
       output2 = (20.0)
       d1 = '530nH'
       d2 = '530nW'
       d3 = '530nHz'
       d4 = '530nA'
       d5 = '530nW'
       d6 = '530nF'
       d7 = '530nOhm'
       d8 = '±20ppm/°C'
       
       result1 = normalization.extract_num(d1)
       result2 = normalization.extract_num(d2)
       result3 = normalization.extract_num(d3)
       result4 = normalization.extract_num(d4)
       result5 = normalization.extract_num(d5)
       result6 = normalization.extract_num(d6)
       result7 = normalization.extract_num(d7)
       result8 = normalization.extract_num(d8)
       
       self.assertTrue(isinstance(result1, numbers.Real))
       self.assertTrue(isinstance(result2, numbers.Real))
       self.assertTrue(isinstance(result3, numbers.Real))
       self.assertTrue(isinstance(result4, numbers.Real))
       self.assertTrue(isinstance(result5, numbers.Real))
       self.assertTrue(isinstance(result6, numbers.Real))
       self.assertTrue(isinstance(result7, numbers.Real))
       self.assertTrue(isinstance(result8, numbers.Real))
       self.assertEqual(result1, output1)
       self.assertEqual(result2, output1)
       self.assertEqual(result3, output1)
       self.assertEqual(result4, output1)
       self.assertEqual(result5, output1)
       self.assertEqual(result6, output1)
       self.assertEqual(result7, output1)
       self.assertEqual(result8, output2)
       
    def test_capacitance(self):
        output = (5.3e-07)
        d = '530nF'
        result = normalization.capacitance(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output) 
              
    def test_tempcoeff(self):
       output = (260)
       d = '±260ppm/°C'
       result = normalization.tempcoeff(d)
       self.assertTrue(isinstance(result, numbers.Real))
       self.assertEqual(result, output)
       
    def test_inductance(self):
        output = (5.3e-07)
        d = '530nH'
        result = normalization.inductance(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)
              
    def test_power(self):
        output = (5.3e-07)
        d = '530nW'
        result = normalization.power(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output) 
              
    def test_tolerance(self):
       output = (20)
       d = '±20%'
       result = normalization.tolerance(d)
       self.assertTrue(isinstance(result, numbers.Real))
       self.assertEqual(result, output)
       
    def test_voltage(self):
        output = (5.3e-07)
        d = '530nV'
        result = normalization.voltage(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)  
              
    def test_current(self):
        output = (5.3e-07)
        d = '530nA'
        result = normalization.current(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)
              
    def test_resistance(self):
        output = (5.3e-07)
        d = '530nOhm'
        result = normalization.resistance(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)
     
    def test_frequency(self):
        output = (5.3e-07)
        d = '530nHz'
        result = normalization.frequency(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)

    def test_height(self):
        d = '0.512" (13.00mm)'
        output = 13.0
        result = normalization.parse_dimension(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)

if __name__ == '__main__':
    unittest.main()
