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


# Create sample dataframe to test normalization functions

df = {'id': ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10'],
      'col1': ['1, 1','2','4','6, a','5','6','6, b','8, 11','12','16'],
      'col2': ['  ',np.nan,'-','-','*',np.nan,np.nan,'-','*',np.nan],
      'col3': ['12 C','1 C','4 C','-',np.nan,'9 C','11 C','12 C',np.nan,np.nan],
      'col4': ['Abs (new)','Abc (old)','Abd (new)','Afs (out)','bds (old)','mbd (new)','Abs (new)','nmsd (old)','Abs (out)','ccs (new)'],
      'col5': ['10 nm to 100 nm','12 nm to 20 cm','34 mm to 100 mm','0.6 mm','33 cm',np.nan,np.nan,'1 mm to 22 cm',np.nan,'22 mm to 100 cm'],
      'col6': ['1 Hz','3 kHz','4 MHz','1 kHz','0.9 Hz','33 kHz','12 MHz',np.nan,np.nan,'1.34 kHz']}

d = pd.DataFrame(data=df)


class TestNorm(unittest.TestCase):

    def test_changename(self):

        result = normalization.changename(
            d, header='col1', new_name='col_new')

        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(d.columns), len(result.columns))
        self.assertFalse('col1' in result.columns)
        self.assertTrue('col_new' in result.columns)


    def test_cleanblank(self):
        
        result = normalization.cleanblank(d)
        
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(d.columns), len(result.columns))
        self.assertEqual(result.col2.isnull().sum(), len(result))


    def test_convercatext(self):
        
        result = normalization.convertcatext(d, header='col4', ext=' .*')
        
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(d.columns), len(result.columns))
        self.assertEqual(result['col4'].str.contains(" .*").sum(), 0)
        
    def test_remempty(self):
        
        result = normalization.remempty(normalization.cleanblank(d))
        
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(d.columns), len(result.columns)+1)
        self.assertFalse('col2' in result.columns)
        
    
    def test_convertnumext(self):
        
        result = normalization.convertnumext(d, header='col3', ext='C')
        
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(d.columns), len(result.columns))
        self.assertFalse('col3' in result.columns)
        self.assertTrue('col3_C' in result.columns)
        self.assertTrue(np.issubdtype(result['col3_C'].dtype, np.number))
        
        
    def test_sepheader(self):
        
        result = normalization.sepheader(d, header='col5', separator = ' to ')
        
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(d.columns), len(result.columns))
        self.assertTrue('col5' in result.columns)
        self.assertTrue('col5_min' in result.columns)
        self.assertTrue('col5_max' in result.columns)
        self.assertEqual(result['col5_min'].str.contains(" to ").sum(), 0)
        self.assertEqual(result['col5_max'].str.contains(" to ").sum(), 0)
        self.assertTrue(result.col5_min.isnull().sum() <= len(result))
        self.assertTrue(result.col5_max.isnull().sum() <= len(result))


    def test_convertmixedext(self):
        
        result = normalization.convertMixedExt(
        d, header='col6', ext=[" Hz", " kHz", " MHz"], scaling_factor=[1, 1000, 1000000])
    
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(len(d.columns), len(result.columns))
        self.assertTrue('col6_normalized' in result.columns)
        self.assertTrue(np.issubdtype(result['col6_normalized'].dtype, np.number))
        self.assertTrue(result.col6_normalized.isnull().sum() <= len(result))
    
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

if __name__ == '__main__':
    unittest.main()
