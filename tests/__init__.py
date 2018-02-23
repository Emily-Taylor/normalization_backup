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
        
    def test_split_l_w(self):
        output = (7.00,5.50)
        d = '0.276" L x 0.217" W (7.00mm x 5.50mm)'
        result = normalization.split_l_w(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
        
        
    def test_inductance(self):
        output = (5.3e-07)
        d = '530nH'
        result = normalization.inductance(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)
              
    def test_current(self):
        output = (5.3e-07)
        d = '530nA'
        result = normalization.current(d)
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
