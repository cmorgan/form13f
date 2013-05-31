
import os
import unittest
import datetime

from solo.filing import analyse, parse

from pprint import pprint 


class TestAnalyse(unittest.TestCase):
    """Used for ensuring the we maintain the correct answer when refactoring
    analyse.py. It is not intended to test the sum function of
    panadas.DataFrame"""

    @property
    def data(self):
        return parse.parse_all_files()

    def test_question_2_a(self):

        total_values, fund_growth = analyse.question_2_a(self.data)

        self.assertTrue(fund_growth)

        # file_name, conformed_date, report_date, com_value
        file_one = ['0000909012-12-000274.txt',
                    datetime.date(2012, 3, 31),
                    datetime.date(2012, 5, 15),
                    583849.0]

        file_two = ['0000909012-12-000357.txt',
                    datetime.date(2012, 6, 30),
                    datetime.date(2012, 8, 14),
                    656620.0]

        file_three = ['0000909012-12-000436.txt',
                     datetime.date(2012, 9, 30),
                     datetime.date(2012, 11, 9),
                     602253.0]

        file_four = ['0000909012-13-000071.txt',
                     datetime.date(2012, 12, 31),
                     datetime.date(2013, 2, 13),
                     725498.0]

        fixtures = [file_one, file_two, file_three, file_four]

        # assert algo gives fixture data
        for (form, com_value), fixture in zip(total_values, fixtures):
            self.assertEqual(os.path.basename(form.file_name), fixture[0])
            self.assertEqual(form.conformed_period, fixture[1])
            self.assertEqual(form.submit_date, fixture[2])
            self.assertEqual(com_value, fixture[3])

    def test_question_2_b_exchange_open(self):
        # the market is closed, return no stocks
        self.assertFalse(bool(analyse.question_2_b(self.data)))

    def test_is_nyse_open(self):
        open_monday = datetime.date(2013, 5, 20)
        self.assertTrue(analyse.is_nyse_open(open_monday))

    def test_is_nyse_closed(self):
        independence_day = datetime.date(2013, 7, 4)
        self.assertFalse(analyse.is_nyse_open(independence_day))

    def test_question_2_c(self):
        answer = analyse.question_2_c(self.data)

        fixture_answer_index = sorted(['DISCOVER FINL SVCS',
                                       'GENERAL ELECTRIC CO',
                                       'FRANKLIN RES INC'])

        self.assertEqual(sorted(list(answer)), fixture_answer_index)


if __name__ == '__main__':
    unittest.main()
