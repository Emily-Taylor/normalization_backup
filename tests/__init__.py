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
        d5 = '37 mOhms'
        d6 = '11 mm'
        d7 = '1.22 A'
        d8 = '21 mOHms'
        d9 = '3 ohms'
        d10 = '55 mohms'
        d11 = '2500V @ 1 Second'
        d12 = '120/240VAC'
        d13 = '1500VRMS @ 1 Minute'
        d14 = '100VRMS'
        d15 = '25V, 70V'
        d16 = 'Parallel 21.6µH @ 10kHz, Series 778µH @ 10kHz'
        d17 = '1V @ 2mA (Min)'
        d18 = '1V @ 2µA (Min)'
        d19 = '1V @ 2mA (Typ)'
        d20 = '1V @ 2µA (Typ)'
        d21 = '1mV @ 2µA (Min)'
        d22 = '1mV @ 2mA (Min)'
        d23 = '30pF @ 10V (VGS)'
        
        output1 = (72.0, 100000000.0)
        output2 = (0.028, 120)
        output3 = (0.52, 100000.0)
        output4 = (7200000.0, 85.0)
        output5 = (0.037, 'n/a')
        output6 = (0.011, 'n/a')
        output7 = (1.22, 'n/a')
        output8 = (0.021, 'n/a')
        output9 = (3.0, 'n/a')
        output10 = (0.055, 'n/a')
        output11 = (2500.0, 1.0)
        output12 = (120.0, 'n/a')
        output13 = (1500.0, 60.0)
        output14 = (100.0, 'n/a')
        output15 = (25.0, 'n/a')
        output16 = (2.16e-05, 10000.0)
        output17 = (1.0, 0.002)
        output18 = (1.0, 2e-06)
        output19 = (1.0, 0.002)
        output20 = (1.0, 2e-06)
        output21 = (0.001, 2e-06)
        output22 = (0.001, 0.002)
        output23 = (3e-11, 10.0)

        result1 = normalization.split_at(d1)
        result2 = normalization.split_at(d2)
        result3 = normalization.split_at(d3)
        result4 = normalization.split_at(d4)
        result5 = normalization.split_at(d5)
        result6 = normalization.split_at(d6)
        result7 = normalization.split_at(d7)
        result8 = normalization.split_at(d8)
        result9 = normalization.split_at(d9)
        result10 = normalization.split_at(d10)
        result11 = normalization.split_at(d11)
        result12 = normalization.split_at(d12)
        result13 = normalization.split_at(d13)
        result14 = normalization.split_at(d14)
        result15 = normalization.split_at(d15)
        result16 = normalization.split_at(d16)
        result17 = normalization.split_at(d17)
        result18 = normalization.split_at(d18)
        result19 = normalization.split_at(d19)
        result20 = normalization.split_at(d20)
        result21 = normalization.split_at(d21)
        result22 = normalization.split_at(d22)
        result23 = normalization.split_at(d23)

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
        
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
        self.assertEqual(result8, output8)
        self.assertEqual(result9, output9)
        self.assertEqual(result10, output10)
        self.assertEqual(result11, output11)
        self.assertEqual(result12, output12)
        self.assertEqual(result13, output13)
        self.assertEqual(result14, output14)
        self.assertEqual(result15, output15)
        self.assertEqual(result16, output16)
        self.assertEqual(result17, output17)
        self.assertEqual(result18, output18)
        self.assertEqual(result19, output19)
        self.assertEqual(result20, output20)
        self.assertEqual(result21, output21)
        self.assertEqual(result22, output22)
        self.assertEqual(result23, output23)

    def test_split_temp(self):
        # this test only covers a single, abnormal edge case. more testing need for ranges like (-10 - 80) etc.
        d = "105°C (TA)"
        output = (105.0, 'n/a')
        result = normalization.split_temp(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        # self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
        # "operating_temperature": "-40°C ~ 85°C (TA)",
        d = "-40°C ~ 85°C (TA)"
        output = (-40.0, 85.0)
        result = normalization.split_temp(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
        
        d1 = "50/60Hz"
        d2 = '881.5/1960.0MHz'
        d3 = "1.843/1.96GHz"
        d4 = "763/793MHz"
        d5 = "769/860.5MHz"
        d6 = "1V NPN, 2V N Channel"
        d7 = "1V NPN, 2V N-Channel"
        d8 = "1V PNP, 2V N Channel"
        d9 = "1V PNP, 2V N-Channel"
        d10 = "1V PNP, 2V P-Channel"
        d11 = "1V PNP, 2 N-Channel"
        d12 = "1V NPN, 2V P-Channel"
        d13 = "1V NPN, 2V NPN"
        
        output1 = (50.0, 60.0)
        output2 = (881500000.0, 1960000000.0)
        output3 = (1843000000.0, 1960000000.0)
        output4 = (763000000.0, 793000000.0)
        output5 = (769000000.0, 860500000.0)
        output6 = (1.0, 2.0)
        
        result1 = normalization.split_temp(d1)
        result2 = normalization.split_temp(d2)
        result3 = normalization.split_temp(d3)
        result4 = normalization.split_temp(d4)
        result5 = normalization.split_temp(d5)
        result6 = normalization.split_temp(d6)
        result7 = normalization.split_temp(d7)
        result8 = normalization.split_temp(d8)
        result9 = normalization.split_temp(d9)
        result10 = normalization.split_temp(d10)
        result11 = normalization.split_temp(d11)
        result12 = normalization.split_temp(d12)
        result13 = normalization.split_temp(d13)
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output6)
        self.assertEqual(result8, output6)
        self.assertEqual(result9, output6)
        self.assertEqual(result10, output6)
        self.assertEqual(result11, output6)
        self.assertEqual(result12, output6)
        self.assertEqual(result13, output6)

    def test_split_to(self):
        d = '1000 F to 330000 F'
        output = (1000, 330000)
        result = normalization.split_to(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
        
        d1 = '2.4GHz ~ 2.483.5GHz, 4.9GHz ~ 5.9GHz'
        d2 = '2.4GHz ~ 2.483.5GHz'
        d3 = '0.47 ÂµH'
        d4 = '0.3 uH to 0.55 uH and 0.8 uH'
        d5 = '250kHz Min'
        d6 = 'Custom'
        d7 = '- 8 V'
        d8 = '- 1 V, 2 V'
        d9 = '+/- 8 V'
        d10 = '1.8 VDC to 3.3 VDC'
        d11 = '2.5 V, 3.3 V, 5 V'
        d12 = '+/- 2.5 V, +/- 3.3 V, +/- 5 V'
        d13 = '+/- 2.5 V, +/- 2.75 V'
        d14 = '5 V, 9 V, 12 V, 15 V'
        d15 = '200 VAC, VDC 200'
        d16 = '120/240 VAC/VDC'
        d17 = '900 mVDCo 1.4 VDC'
        d18 = '1.8 V/2.5 V/3.3 V'
        
        output1 = (2400000000.0, 2483000000.0)
        output2 = (2400000000.0, 2483000000.0)
        output3 = (4.7e-07, 'n/a')
        output4 = (3e-07, 5.5e-07)
        output5 = (250000.0, 'n/a')
        output6 = ('n/a', 'n/a')
        output7 = (-8.0, 'n/a')
        output8 = (-1.0, 2.0)
        output9 = (-8.0, 8.0)
        output10 = (1.8, 3.3)
        output11 = (2.5, 5.0)
        output12 = (2.5, 5.0)
        output13 = (2.5, 2.75)
        output14 = (5.0, 15.0)
        output15 = (200.0, 200.0)
        output16 = (120.0, 240.0)
        output17 = (0.9, 1.4)
        output18 = (1.8, 3.3)
        
        result1 = normalization.split_to(d1)
        result2 = normalization.split_to(d2)
        result3 = normalization.split_to(d3)
        result4 = normalization.split_to(d4)
        result5 = normalization.split_to(d5)
        result6 = normalization.split_to(d6)
        result7 = normalization.split_to(d7)
        result8 = normalization.split_to(d8)
        result9 = normalization.split_to(d9)
        result10 = normalization.split_to(d10)
        result11 = normalization.split_to(d11)
        result12 = normalization.split_to(d12)
        result13 = normalization.split_to(d13)
        result14 = normalization.split_to(d14)
        result15 = normalization.split_to(d15)
        result16 = normalization.split_to(d16)
        result17 = normalization.split_to(d17)
        result18 = normalization.split_to(d18)
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
        self.assertEqual(result8, output8)
        self.assertEqual(result9, output9)
        self.assertEqual(result10, output10)
        self.assertEqual(result11, output11)
        self.assertEqual(result12, output12)
        self.assertEqual(result13, output13)
        self.assertEqual(result14, output14)
        self.assertEqual(result15, output15)
        self.assertEqual(result16, output16)
        self.assertEqual(result17, output17)
        self.assertEqual(result18, output18)

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
        output = (7.00, 5.50, 'n/a')
        d = '0.276" L x 0.217" W (7.00mm x 5.50mm)'
        result = normalization.parse_dimensions(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertTrue(isinstance(result[1], numbers.Real))
        self.assertEqual(result, output)
        
    def test_parse_dimensions(self):
        result1 = normalization.parse_dimensions("39 x 20 x 13")
        result2 = normalization.parse_dimensions('32 x 30')
        result3 = normalization.parse_dimensions('PS 30.5 x 10.2')
        result4 = normalization.parse_dimensions('PM 62 x 49')
        result5 = normalization.parse_dimensions('13 x 7 x 4 (EF 12.6)')
        result6 = normalization.parse_dimensions('RM 10')
        result7 = normalization.parse_dimensions('E 5')
        result8 = normalization.parse_dimensions('RM 6')
        result9 = normalization.parse_dimensions('25.4 x 10 x 7 (EF 20)')
        result10 = normalization.parse_dimensions('ETD 34')
        result11 = normalization.parse_dimensions("EP 7")
        result12 = normalization.parse_dimensions("P 26 x 16")
        result13 = normalization.parse_dimensions("PQ 26 x 25")
        result14 = normalization.parse_dimensions("28.5 x 16.9 x")
        result15 = normalization.parse_dimensions("15 x 12-1")
        result16 = normalization.parse_dimensions("EPO 13")
        result17 = normalization.parse_dimensions("EPX 10")
        result18 = normalization.parse_dimensions("Ep 7")
        result19 = normalization.parse_dimensions("35 X 9")
        result20 = normalization.parse_dimensions("12 x 3 x12")
        result21 = normalization.parse_dimensions("EPO 13")
        result22 = normalization.parse_dimensions("RMR 6")
        result23 = normalization.parse_dimensions("ER 11")
        result24 = normalization.parse_dimensions("EV 30")
        result25 = normalization.parse_dimensions("EFD 10")
        result26 = normalization.parse_dimensions("EF 16")
        result27 = normalization.parse_dimensions("ETD 59 (EER 60)")
        
        output1 = (39.0, 20.0, 13.0)
        output2 = (32.0, 30.0, 'n/a')
        output3 = (30.5, 10.2, 'n/a')
        output4 = (62.0, 49.0, 'n/a')
        output5 = (13.0, 7.0, 4.0)
        output6 = (10.0, 'n/a', 'n/a')
        output7 = (5.0, 'n/a', 'n/a')
        output8 = (6.0, 'n/a', 'n/a')
        output9 = (25.4, 10.0, 7.0)
        output10 = (34.0, 'n/a', 'n/a')
        output11 = (7.0, 'n/a', 'n/a')
        output12 = (26.0, 16.0, 'n/a')
        output13 = (26.0, 25.0, 'n/a')
        output14 = (28.5, 16.9, 'n/a')
        output15 = (15.0, 12.0, 'n/a')
        output16 = (13.0, 'n/a', 'n/a')
        output17 = (10.0, 'n/a', 'n/a')
        output18 = (7.0, 'n/a', 'n/a')
        output19 = (35.0, 9.0, 'n/a')
        output20 = (12.0, 3.0, 12.0)
        output21 = (13.0, 'n/a', 'n/a')
        output22 = (6.0, 'n/a', 'n/a')
        output23 = (11.0, 'n/a', 'n/a')
        output24 = (30.0, 'n/a', 'n/a')
        output25 = (10.0, 'n/a', 'n/a')
        output26 = (16.0, 'n/a', 'n/a')
        output27 = (59.0, 'n/a', 'n/a')
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
        self.assertEqual(result8, output8)
        self.assertEqual(result9, output9)
        self.assertEqual(result10, output10)
        self.assertEqual(result11, output11)
        self.assertEqual(result12, output12)
        self.assertEqual(result13, output13)
        self.assertEqual(result14, output14)
        self.assertEqual(result15, output15)
        self.assertEqual(result16, output16)
        self.assertEqual(result17, output17)
        self.assertEqual(result18, output18)
        self.assertEqual(result19, output19)
        self.assertEqual(result20, output20)
        self.assertEqual(result21, output21)
        self.assertEqual(result22, output22)
        self.assertEqual(result23, output23)
        self.assertEqual(result24, output24)
        self.assertEqual(result25, output25)
        self.assertEqual(result26, output26)
        self.assertEqual(result27, output27)
        
    def test_split_current(self):
        result1 = normalization.split_current('600V, 6.3V, 5V')
        result2 = normalization.split_current('5V, ±12V')
        result3 = normalization.split_current('Parallel 18V, Series 36V')
        result4 = normalization.split_current('12.6V')
        result5 = normalization.split_current('600V, 6.3V, 5V, 2.5V, 2.5V')
        result6 = normalization.split_current('230mA, 6A, 3A')
        result7 = normalization.split_current('230mA, 6A, 3A, 2.5A, 2.5A')
        result8 = normalization.split_current('120V, 12/12V')
        
        output1 = (600.0, 6.3)
        output2 = (5.0, 12.0)
        output3 = (18.0, 36.0)
        output4 = (12.6, 12.6)
        output5 = (600.0, 6.3)
        output6 = (0.23, 6.0)
        output7 = (0.23, 6.0)
        output8 = (120.0, 12.0)
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
        self.assertEqual(result8, output8)
        
    def test_split_spread(self):
        result1 = normalization.split_spread('±0.25%, Center Spread')
        result2 = normalization.split_spread('-0.50%, Down Spread')
        result3 = normalization.split_spread('±0.25% ~ ±2% Center Spread, -0.5% ~ -4% Down Spread')
        
        output1 = (0.25, 0.25, 'n/a', 'n/a')
        output2 = ('n/a', 'n/a', 0.5, 0.5)
        output3 = (0.25, 2.0, 0.5, 4.0)
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)

    def test_split_dia(self):
        output = (7.62, 'n/a', 'n/a')
        d = '0.300" Dia (7.62mm)'
        result = normalization.parse_dimensions(d)
        self.assertTrue(isinstance(result[0], numbers.Real))
        self.assertEqual(result, output)

    def test_extract_num(self):
        output1 = (5.3e-07)
        output2 = (20.0)
        output3 = (3.0)
        output4 = (1.0)
        output5 = (1.4)
        output7 = (1.1)
        output8 = 'n/a'
        output9 = (8.0)
        output10 = (0.0)
        output11 = (5.3)
        output12 = (5.0)

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
        d11 = '1.4 Ohms/350 mOhms'
        d12 = '1.1 Ohms and 1.7 Ohms'
        d13 = '1dB @ 2GHz'
        d14 = '1dB @ 2MHz'
        d15 = 'Clamped'
        d16 = '1 dB at 2 GHz'
        d17 = '-/+ 8 V'
        d18 = 'DC'
        d19 = '+ / - 5.3 V'
        d20 = '0.197" (5.00mm) ~ 0.200" (5.08mm)'

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
        result11 = normalization.extract_num(d11)
        result12 = normalization.extract_num(d12)
        result13 = normalization.extract_num(d13)
        result14 = normalization.extract_num(d14)
        result15 = normalization.extract_num(d15)
        result16 = normalization.extract_num(d16)
        result17 = normalization.extract_num(d17)
        result18 = normalization.extract_num(d18)
        result19 = normalization.extract_num(d19)
        result20 = normalization.extract_num(d20)

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
        self.assertEqual(result11, output5)
        self.assertEqual(result12, output7)
        self.assertEqual(result13, output4)
        self.assertEqual(result14, output4)
        self.assertEqual(result15, output8)
        self.assertEqual(result16, output4)
        self.assertEqual(result17, output9)
        self.assertEqual(result18, output10)
        self.assertEqual(result19, output11)
        self.assertEqual(result20, output12)

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
        output1 = (20, 'n/a')
        output2 = (5.0, 'n/a')
        output3 = (0.1, 'n/a')
        output4 = (20.0, 'n/a')
        output5 = (50.0, 'n/a')
        output6 = (50.0, 'n/a')
        output7 = (50.0, 'n/a')
        output8 = ('n/a', 3e-10)
        output9 = (20.0, 'n/a')
        output10 = ('n/a', 'n/a')
        output11 = ('n/a', 'n/a')
        output12 = ('n/a', 1e-10)
        output13 = ('n/a', 3e-05)
        output14 = ('n/a', 'n/a')
        output15 = ('n/a', 3e-10)
        
        d1 = '±20%'
        d2 = "±5%"
        d3 = "0.1 %"
        d4 = "-15%, +20%"
        d5 = "+ 50 %, - 30 %"
        d6 = "- 30 % / + 50 %"
        d7 = "- 30 %, + 50 %"
        d8 = "0.3 nH, 0.2 nH"
        d9 = "20 %"
        d10 = "5 Ohms"
        d11 = "-0.5/+0.1 nS"
        d12 = "0.1 nH"
        d13 = "30 uH"
        d14 = "±0.28nS"
        d15 = "±0.3nH"
        
        result1 = normalization.split_tolerance(d1)
        result2 = normalization.split_tolerance(d2)
        result3 = normalization.split_tolerance(d3)
        result4 = normalization.split_tolerance(d4)
        result5 = normalization.split_tolerance(d5)
        result6 = normalization.split_tolerance(d6)
        result7 = normalization.split_tolerance(d7)
        result8 = normalization.split_tolerance(d8)
        result9 = normalization.split_tolerance(d9)
        result10 = normalization.split_tolerance(d10)
        result11 = normalization.split_tolerance(d11)
        result12 = normalization.split_tolerance(d12)
        result13 = normalization.split_tolerance(d13)
        result14 = normalization.split_tolerance(d14)
        result15 = normalization.split_tolerance(d15)
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
        self.assertEqual(result8, output8)
        self.assertEqual(result9, output9)
        self.assertEqual(result10, output10)
        self.assertEqual(result11, output11)
        self.assertEqual(result12, output12)
        self.assertEqual(result13, output13)
        self.assertEqual(result14, output14)
        self.assertEqual(result15, output15)

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
        
    def test_attenuation(self):
        d1 = '25dB @ 1.71 ~ 1.91GHz, 30dB @ 880 ~ 960MHz'
        output1 = (25.0, 1710000000.0, 1910000000.0)
        d2 = '25dB @ 900 MHz ~ 1000 MHz'
        output2 = (25.0, 900000000.0, 1000000000.0)
        d3 = '35dB @ 800MHz ~ 2.7GHz, 40dB @ 1GHz'
        output3 = (35.0, 800000000.0, 2700000000.0)
        d4 = '-25dB @ 900MHz'
        output4 = (-25.0, 900000000.0, 900000000.0)
        d5 = '50dB @ 100MHz'
        output5 = (50.0, 100000000.0, 100000000.0)
        
        result1 = normalization.attenuation(d1)
        result2 = normalization.attenuation(d2)
        result3 = normalization.attenuation(d3)
        result4 = normalization.attenuation(d4)
        result5 = normalization.attenuation(d5)
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)

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
    
    def test_split_comma(self):
        
        result1 = normalization.split_comma('2.5V, 4V')
        result2 = normalization.split_comma('11.3V')
        result3 = normalization.split_comma('1.8 V, 5V')
        result4 = normalization.split_comma('-0.35V')
        
        output1 = (2.5, 4.0)
        output2 = (11.3, 'n/a')
        output3 = (1.8, 5.0)
        output4 = (-0.35, 'n/a')
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
    
    def test_split_slash(self):
        
        result1 = normalization.split_slash('8ns/8ns')
        result2 = normalization.split_slash('8ns/8Âµs')
        result3 = normalization.split_slash('8Âµs/8Âµs')
        result4 = normalization.split_slash('8Âµs/-')
        result5 = normalization.split_slash('8ns/-')
        result6 = normalization.split_slash('-/8Âµs')
        result7 = normalization.split_slash('-/8ns')
        
        output1 = (8e-09, 8e-09)
        output2 = (8e-09, 8e-06)
        output3 = (8e-06, 8e-06)
        output4 = (8e-06, 'n/a')
        output5 = (8e-09, 'n/a')
        output6 = ('n/a', 8e-06)
        output7 = ('n/a', 8e-09)
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
    
    def test_split_three(self):
        
        result1 = normalization.split_three('8 Ohm @ 8mA, 8V')
        result2 = normalization.split_three('1 mOhm @ 2mA, 3A')
        result3 = normalization.split_three('1 mOhm @ 2V, 3A')
        result4 = normalization.split_three('8 Ohm @ 8ÂµA, 8V')
        result5 = normalization.split_three('1 Ohm')
        result6 = normalization.split_three('1 Ohm @ 3V')
        result7 = normalization.split_three('1 mOhm @ 2A, 3V, 8 mOhm @ 8A, 8V')
        result8 = normalization.split_three('1 mOhm @ 2A')
        result9 = normalization.split_three('1 mOhm @ 3V')
        result10 = normalization.split_three('1 mOhm @ 2A, 3V, 8 Ohm @ 8A, 8V')
        result11 = normalization.split_three('8mV @ 8mA, 8mA / 8mV @ 8ÂµA, 8mA')
        result12 = normalization.split_three('1 @ 2V, 3MA')
        result13 = normalization.split_three('8 @ 8MA, 8MA')
        result14 = normalization.split_three('8V @ 8V, 8A (Typ')
        result15 = normalization.split_three('1 @ 2ma, 3V')
        result16 = normalization.split_three('0.3pF @ 150mV, -')
        
        output1 = (8.0, 0.008, 8.0)
        output2 = (0.001, 0.002, 3.0)
        output3 = (0.001, 3.0, 2.0)
        output4 = (8.0, 8e-06, 8.0)
        output5 = (1.0, 'n/a', 'n/a')
        output6 = (1.0, 'n/a', 3.0)
        output7 = (0.001, 2.0, 3.0)
        output8 = (0.001, 2.0, 'n/a')
        output9 = (0.001, 'n/a', 3.0)
        output10 = (0.001, 2.0, 3.0)
        output11 = (0.008, 0.008, 0.008)
        output12 = (1.0, 0.003, 2.0)
        output13 = (8.0, 0.008, 0.008)
        output14 = (8.0, 8.0, 8.0)
        output15 = (1.0, 0.002, 3.0)
        output16 = (3e-13, 0.15, 'n/a')
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
        self.assertEqual(result8, output8)
        self.assertEqual(result9, output9)
        self.assertEqual(result10, output10)
        self.assertEqual(result11, output11)
        self.assertEqual(result12, output12)
        self.assertEqual(result13, output13)
        self.assertEqual(result14, output14)
        self.assertEqual(result15, output15)
        self.assertEqual(result16, output16)
    
    def test_split_percent_value(self):
        result1 = normalization.split_percent_value('8 mV/C')
        result2 = normalization.split_percent_value('8 %/K')
        result3 = normalization.split_percent_value('8 mV/K')
        result4 = normalization.split_percent_value('- 8 mV/C')
        result5 = normalization.split_percent_value('8 %/C')
        result6 = normalization.split_percent_value('+ / - 8 %/C')
        result7 = normalization.split_percent_value('+ 8 %/C')
        result8 = normalization.split_percent_value('8 %/C to 8 %/C')
        result9 = normalization.split_percent_value('- 8 %/C')
        result10 = normalization.split_percent_value('8 uV/C')
        result11 = normalization.split_percent_value('- 8 mV/K')
        result12 = normalization.split_percent_value('- 8 uV/C')
        result13 = normalization.split_percent_value('8 mV / C')
        result14 = normalization.split_percent_value('8 mV/C')
        result15 = normalization.split_percent_value('- 8 mV/C')
        result16 = normalization.split_percent_value('- 8 % / C')
        result17 = normalization.split_percent_value('8 uV/K')
        result18 = normalization.split_percent_value('8 % / C')
        result19 = normalization.split_percent_value('-8 %/C')
        result20 = normalization.split_percent_value('8 mV/deg C')
        result21 = normalization.split_percent_value('- 8 mV/deg C')
        result22 = normalization.split_percent_value('8 %/deg C')
        result23 = normalization.split_percent_value('+ / - 8 %/C')
        result24 = normalization.split_percent_value('+ 8 mV/K')
        result25 = normalization.split_percent_value('8 mW/K')
        result26 = normalization.split_percent_value('+/- 8 %/C')
        result27 = normalization.split_percent_value('- 8 %/deg C')
        result28 = normalization.split_percent_value('- 1 mV/K to - 2 mV/K')
        result29 = normalization.split_percent_value('- 1 %/K to 2 %/K')
        result30 = normalization.split_percent_value('- 1 %/C, 2 %/C')
        result31 = normalization.split_percent_value('- 1 %/C , + 2 %/C')
        result32 = normalization.split_percent_value('- 1 %/C , - 2 %/C')
        result33 = normalization.split_percent_value('1 mV/C to 2 mV/C')
        result34 = normalization.split_percent_value('- 1 mV/C to 2 mV/C')
        result35 = normalization.split_percent_value('1 mV/ C to 2 mV/C')
        result36 = normalization.split_percent_value('1 %/K to 2 %/K')
        result37 = normalization.split_percent_value('- 1 mV/K to 2 mV/K')
        result38 = normalization.split_percent_value('1 mV/K to 2 mV/K')
        result39 = normalization.split_percent_value('+ 1 %/C to + 2 %/C')
        result40 = normalization.split_percent_value('8')
        result41 = normalization.split_percent_value('#NAME?')
        result42 = normalization.split_percent_value('+ 8 C')
        result43 = normalization.split_percent_value('8 V')
        result44 = normalization.split_percent_value('- 8 mV / k')
        result45 = normalization.split_percent_value('8/C')
        result46 = normalization.split_percent_value(14.4)
        result47 = normalization.split_percent_value('30 mv/C')
        result48 = normalization.split_percent_value('24.4 mv/C')
        
        self.assertEqual(result1, ('n/a', 0.008))
        self.assertEqual(result2, (8.0, 'n/a'))
        self.assertEqual(result3, ('n/a', 0.008))
        self.assertEqual(result4, ('n/a', 0.008))
        self.assertEqual(result5, (8.0, 'n/a'))
        self.assertEqual(result6, (8.0, 'n/a'))
        self.assertEqual(result7, (8.0, 'n/a'))
        self.assertEqual(result8, (8.0, 'n/a'))
        self.assertEqual(result9, (8.0, 'n/a'))
        self.assertEqual(result10, ('n/a', 8e-06))
        self.assertEqual(result11, ('n/a', 0.008))
        self.assertEqual(result12, ('n/a', 8e-06))
        self.assertEqual(result13, ('n/a', 0.008))
        self.assertEqual(result14, ('n/a', 0.008))
        self.assertEqual(result15, ('n/a', 0.008))
        self.assertEqual(result16, (8.0, 'n/a'))
        self.assertEqual(result17, ('n/a', 8e-06))
        self.assertEqual(result18, (8.0, 'n/a'))
        self.assertEqual(result19, (8.0, 'n/a'))
        self.assertEqual(result20, ('n/a', 0.008))
        self.assertEqual(result21, ('n/a', 0.008))
        self.assertEqual(result22, (8.0, 'n/a'))
        self.assertEqual(result23, (8.0, 'n/a'))
        self.assertEqual(result24, ('n/a', 0.008))
        self.assertEqual(result25, ('n/a', 'n/a'))
        self.assertEqual(result26, (8.0, 'n/a'))
        self.assertEqual(result27, (8.0, 'n/a'))
        self.assertEqual(result28, ('n/a', 0.001))
        self.assertEqual(result29, (1.0, 'n/a'))
        self.assertEqual(result30, (1.0, 'n/a'))
        self.assertEqual(result31, (1.0, 'n/a'))
        self.assertEqual(result32, (1.0, 'n/a'))
        self.assertEqual(result33, ('n/a', 0.001))
        self.assertEqual(result34, ('n/a', 0.001))
        self.assertEqual(result35, ('n/a', 0.001))
        self.assertEqual(result36, (1.0, 'n/a'))
        self.assertEqual(result37, ('n/a', 0.001))
        self.assertEqual(result38, ('n/a', 0.001))
        self.assertEqual(result39, (1.0, 'n/a'))
        self.assertEqual(result40, ('n/a', 'n/a'))
        self.assertEqual(result41, ('n/a', 'n/a'))
        self.assertEqual(result42, ('n/a', 'n/a'))
        self.assertEqual(result43, ('n/a', 'n/a'))
        self.assertEqual(result44, ('n/a', 0.008))
        self.assertEqual(result45, (8.0, 'n/a'))
        self.assertEqual(result46, (14.4, 14.4))
        self.assertEqual(result47, ('n/a', 0.03))
        self.assertEqual(result48, ('n/a', 0.024399999999999998))
        
    def test_parse_dimension(self):
        result1 = normalization.parse_dimension('1 1/2')
        result2 = normalization.parse_dimension('1 3/8')
        result3 = normalization.parse_dimension('2 in')
        result4 = normalization.parse_dimension('33 mm)')
        result5 = normalization.parse_dimension('0.512" (13.00mm)')
        result6 = normalization.parse_dimension('0.512\" (13.00mm)')
        result7 = normalization.parse_dimension('22 mm (0.875)')
        result8 = normalization.parse_dimension('12.7 mm (0.5 in)')
        result9 = normalization.parse_dimension('7.6m (25 ft)')
        result10 = normalization.parse_dimension('25 ft')
        result11 = normalization.parse_dimension('19.69µin (0.50µm)')
        result12 = normalization.parse_dimension('Flash')
        result13 = normalization.parse_dimension('Custom')
        result14 = normalization.parse_dimension('83.500" (212.09cm)')
        result15 = normalization.parse_dimension('50 cm')
        result16 = normalization.parse_dimension("12' (3.65m) 4 yds")
        result17 = normalization.parse_dimension('6 ft 8 in')
        result18 = normalization.parse_dimension('1 M')
        result19 = normalization.parse_dimension('100 um')
        result20 = normalization.parse_dimension('CG')
        
        output1 = 38.1
        output2 = 34.925
        output3 = 50.8
        output4 = 33.0
        output5 = 13.0
        output6 = 13.0
        output7 = 22.0
        output8 = 12.7
        output9 = 7620.0
        output10 = 7620.0
        output11 = 0.0005
        output12 = 'n/a'
        output13 = 'n/a'
        output14 = 2120.9
        output15 = 500.0
        output16 = 3650.0
        output17 = 2032.0000000000002
        output18 = 1000.0
        output19 = 0.1
        output20 = 'n/a'
        
        self.assertEqual(result1, output1)
        self.assertEqual(result2, output2)
        self.assertEqual(result3, output3)
        self.assertEqual(result4, output4)
        self.assertEqual(result5, output5)
        self.assertEqual(result6, output6)
        self.assertEqual(result7, output7)
        self.assertEqual(result8, output8)
        self.assertEqual(result9, output9)
        self.assertEqual(result10, output10)
        self.assertEqual(result11, output11)
        self.assertEqual(result12, output12)
        self.assertEqual(result13, output13)
        self.assertEqual(result14, output14)
        self.assertEqual(result15, output15)
        self.assertEqual(result16, output16)
        self.assertEqual(result17, output17)
        self.assertEqual(result18, output18)
        self.assertEqual(result19, output19)
        self.assertEqual(result20, output20)


if __name__ == '__main__':
    unittest.main()
