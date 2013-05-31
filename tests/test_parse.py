
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

        #fname, date1, date2, data_frame = parse.parse_form_13f(test_file_one)
        form = parse.parse_form_13f(test_file_one)

        self.assertEqual(
            form.data_frame.ix['ITAU UNIBANCO HLDG SA']['MARKET VALUE'],
            int(lines[580][60:63].strip())
        )

    def test_parse_form_two(self):
        # pick another file, check some data
        test_file_two = os.path.join(DATA_DIR, '0000909012-12-000274.txt')

        with open(test_file_two) as f:
            lines = f.readlines()

        form = parse.parse_form_13f(test_file_two)

        self.assertEqual(
            form.data_frame.ix['AKAMAI TECHNOLOGIES INC']['SHRS OR PRN AMT'],
            int(lines[36][68:73].strip())
        )

    def test_market_value_sums(self):
        """use sum of market value as a checksum, see ./solo/filing/data/odf/.
        for OpenDocument spreadsheets used to calc these values"""

        # OpenOffice Calc values
        # filename, sum of market value column
        file_one = ['0000909012-12-000274.txt', 667757]

        file_two = ['0000909012-12-000357.txt', 769056]

        file_three = ['0000909012-12-000436.txt', 692743]

        file_four = ['0000909012-13-000071.txt', 831365]

        fixture_data_set = [file_one, file_two, file_three, file_four]

        data_set = parse.parse_all_files()

        for form, fixture_data in zip(data_set, fixture_data_set):

            # assert filename the same (discard path for algo data)
            self.assertEqual(os.path.basename(form.file_name), fixture_data[0])

            self.assertEqual(form.data_frame['MARKET VALUE'].sum(),
                             fixture_data[1])


if __name__ == '__main__':
    unittest.main()
