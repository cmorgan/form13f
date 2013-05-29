
import unittest

import os
from solo.filing import parse


THIS_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(THIS_DIR, '..', 'solo', 'filing', 'data')


class TestParse(unittest.TestCase):

    def test_parse_form_one(self):
        # pick a file, check some data
        test_file_one = os.path.join(DATA_DIR, '0000909012-12-000357.txt')

        with open(test_file_one) as f:
            lines = f.readlines()

        fname, date1, date2, data_frame = parse.parse_form_13f(test_file_one)

        self.assertEqual(
            data_frame.ix['ITAU UNIBANCO HLDG SA']['MARKET VALUE'], 
                         int(lines[580][60:63].strip())
        )

    def test_parse_form_two(self):
        # pick another file, check some data
        test_file_two = os.path.join(DATA_DIR, '0000909012-12-000274.txt')

        with open(test_file_two) as f:
            lines = f.readlines()

        fname, date1, date2, data_frame = parse.parse_form_13f(test_file_two)

        self.assertEqual(
            data_frame.ix['AKAMAI TECHNOLOGIES INC']['SHRS OR PRN AMT'], 
                         int(lines[36][68:73].strip())
        )


if __name__ == '__main__':
    unittest.main()
