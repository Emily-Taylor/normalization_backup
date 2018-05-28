# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:15:43 2017

@author: HindolRakshit

Unit tests for normalization functions

"""

import unittest
import normalization
import numbers
# import preprocess


class TestNorm(unittest.TestCase):

    def test_split_at(self):

        d1 = "72 @ 100MHz"
        d2 = "28mA @ 120Hz"
        d3 = "520 mOhm @ 100kHz"
        d4 = "2000 Hrs @ 85°C"
        output1 = (72.0, 100000000.0)
        output2 = (0.028, 120)
        output3 = (0.52, 100000.0)
        output4 = (2000.0, 85.0)

        result1 = normalization.split_at(d1)
        result2 = normalization.split_at(d2)
        result3 = normalization.split_at(d3)
        result4 = normalization.split_at(d4)

        self.assertTrue(isinstance(result1[0], numbers.Real))
        self.assertTrue(isinstance(result1[1], numbers.Real))
        self.assertEqual(result1, output1)
        self.assertTrue(isinstance(result2[0], numbers.Real))
        self.assertTrue(isinstance(result2[1], numbers.Real))
        self.assertEqual(result2, output2)
        self.assertTrue(isinstance(result3[0], numbers.Real))
        self.assertTrue(isinstance(result3[1], numbers.Real))
        self.assertEqual(result3, output3)
        self.assertTrue(isinstance(result4[0], numbers.Real))
        self.assertTrue(isinstance(result4[1], numbers.Real))
        self.assertEqual(result4, output4)

    def test_split_temp(self):
        # this test only covers a single, abnormal edge case. more testing need for ranges like (-10 - 80) etc.
        d = "105°C (TA)"
        output = (0.0, 105.0)
        result = normalization.split_temp(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
        # "operating_temperature": "-40°C ~ 85°C (TA)",
        d = "-40°C ~ 85°C (TA)"
        output = (-40.0, 85.0)
        result = normalization.split_temp(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)

    def test_split_to(self):
        d = '1000 F to 330000 F'
        output = (1000, 330000)
        result = normalization.split_to(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)

    def test_split_Q(self):
        output = (72.0, 100000000.0)
        d = "72 @ 100MHz"
        result = normalization.split_q(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)

    def test_inchtomm(self):
        output = (25.4)
        d = 1
        result = normalization.inchtomm(d)
        self.assertTrue(isinstance(result, numbers.Real))
        self.assertEqual(result, output)

    def test_split_rc(self):
        output = (0.028, 120)
        d = "28mA @ 120Hz"
        result = normalization.split_rc(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)

    def test_split_esr(self):
        output = (0.52, 100000.0)
        d = "520 mOhm @ 100kHz"
        result = normalization.split_esr(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)

    def test_split_lifetime(self):
        output = (2000.0, 85.0)
        d = '2000 Hrs @ 85°C'
        result = normalization.split_lifetime(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)

    def test_split_l_w(self):
        output = (7.00, 5.50, 0.0)
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
        output3 = (4.0)
        output4 = (0.5)

        d1 = '530nH'
        d2 = '530nW'
        d3 = '530nHz'
        d4 = '530nA'
        d5 = '530nW'
        d6 = '530nF'
        d7 = '530nOhm'
        d8 = '±20ppm/°C'
        d9 = '3/0.75Ohms'
        d10 = '1/2A'

        result1 = normalization.extract_num(d1)
        result2 = normalization.extract_num(d2)
        result3 = normalization.extract_num(d3)
        result4 = normalization.extract_num(d4)
        result5 = normalization.extract_num(d5)
        result6 = normalization.extract_num(d6)
        result7 = normalization.extract_num(d7)
        result8 = normalization.extract_num(d8)
        result9 = normalization.extract_num(d9)
        result10 = normalization.extract_num(d10)

        self.assertTrue(isinstance(result1, numbers.Real))
        self.assertTrue(isinstance(result2, numbers.Real))
        self.assertTrue(isinstance(result3, numbers.Real))
        self.assertTrue(isinstance(result4, numbers.Real))
        self.assertTrue(isinstance(result5, numbers.Real))
        self.assertTrue(isinstance(result6, numbers.Real))
        self.assertTrue(isinstance(result7, numbers.Real))
        self.assertTrue(isinstance(result8, numbers.Real))
        self.assertTrue(isinstance(result9, numbers.Real))
        self.assertTrue(isinstance(result10, numbers.Real))
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output1)
        self.assertEqual(result3, output1)
        self.assertEqual(result4, output1)
        self.assertEqual(result5, output1)
        self.assertEqual(result6, output1)
        self.assertEqual(result7, output1)
        self.assertEqual(result8, output2)
        self.assertEqual(result9, output3)
        self.assertEqual(result10, output4)

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
		
	def test_mpn(self):
		mpn1 = '123456'
		mpn2 = '123-456'
		mpn3 = 'aA*bcc-X'
		mpn4 = 'aAbccX'
		
		out1 = normalization.create_id(mpn1, 'abc')
		out2 = normalization.create_id(mpn2, 'abc')
		out3 = normalization.create_id(mpn3, 'abc')
		out4 = normalization.create_id(mpn4, 'abc')
		
		self.assertTrue(isinstance(out1, str))
		self.assertTrue(isinstance(out2, str))
		self.assertTrue(isinstance(out3, str))
		self.assertTrue(isinstance(out4, str))
		
		self.assertTrue(out1 == out2)
		self.assertTrue(out3 == out4)
		
    def test_height(self):
        # supposed to work with input like this:	'0.039" (1.00mm)'
        d1 = '0.512" (13.00mm)'
        d2 = '22 mm (0.875)'
        output1 = 13.0
        output2 = 22.0
        result1 = normalization.parse_dimension(d1)
        result2 = normalization.parse_dimension(d2)
        self.assertTrue(isinstance(result1, numbers.Real))
        self.assertTrue(isinstance(result2, numbers.Real))
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
    def test_height_v(self):
          # supposed to work with input like this:	'0.039\" (13.00mm)'
        d1 = '0.512\\" (13.00mm)'
        output1 = 13.0
        result1 = normalization.parse_dimension(d1)
        self.assertTrue(isinstance(result1, numbers.Real))
        self.assertEqual(result1, output1)

    def test_split_timing(self):
        d1 = '1023 s'
        output1 = (1023.0, 1023.0)
        d2 = '1 m to 100 m'
        output2 = (60.0, 6000.0)
        d3 = 'Fixed 3m'
        output3 = (180.0, 180.0)
        d4 = '0.1 s to 100 m'
        output4 = (0.1, 6000.0)
        d5 = '1 s to 1023 s'
        output5 = (1.0, 1023.0)
        d6 = '0.1 s to 10 d'
        output6 = (0.1, 864000.0)

        result1 = normalization.split_timing(d1)
        result2 = normalization.split_timing(d2)
        result3 = normalization.split_timing(d3)
        result4 = normalization.split_timing(d4)
        result5 = normalization.split_timing(d5)
        result6 = normalization.split_timing(d6)

        self.assertTrue(isinstance(result1[0], numbers.Real))
        self.assertTrue(isinstance(result1[1], numbers.Real))
        self.assertTrue(isinstance(result2[0], numbers.Real))
        self.assertTrue(isinstance(result2[1], numbers.Real))
        self.assertTrue(isinstance(result3[0], numbers.Real))
        self.assertTrue(isinstance(result3[1], numbers.Real))
        self.assertTrue(isinstance(result4[0], numbers.Real))
        self.assertTrue(isinstance(result4[1], numbers.Real))
        self.assertTrue(isinstance(result5[0], numbers.Real))
        self.assertTrue(isinstance(result5[1], numbers.Real))
        self.assertTrue(isinstance(result6[0], numbers.Real))
        self.assertTrue(isinstance(result6[1], numbers.Real))
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)


if __name__ == '__main__':
    unittest.main()
