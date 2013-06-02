"""
Parses ./data/*.txt, constrcuts Form13F objects

From brief:

1. Store the fields from the complete submission text files (including Name
of Issuer, Title of Class, CUSIP, etc) in a data structure. Be sure to include
the "period of report" and the "filed as of date" as fields.
"""

import os
import datetime

import pandas


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(THIS_DIR, 'data')


class Form13F:
    column_names = ['NAME OF ISSUER', 'TITLE OF CLASS', 'CUSIP',
                    'MARKET VALUE', 'SHRS OR PRN AMT', 'SH/ PUT/ PRN CALL',
                    'INVESTMENT DESCRETION', 'VOTING AUTHORITY SOLE',
                    'VOTING AUTHORITY SHARED', 'VOTING AUTHORITY NONE']

    def __init__(self, fname, conformed_period, submit_date, data_frame):
        self.file_name = fname
        self.conformed_period = conformed_period
        self.submit_date = submit_date
        self.data_frame = data_frame


def get_files():
    for fname in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, fname)
        if os.path.isfile(fpath):
            yield fpath


def parse_form_13f_date(date_string):
    # remove tabs, newlines and spaces
    date_string = date_string.strip()
    # No Exception handling here as the date is used as an index
    return datetime.datetime.strptime(date_string, '%Y%m%d').date()


def parse_form_13f_head(fname):
    """extract 'confirmed period of report' and 'filed as of date' from head of
    Form 13F and number of declared columns (<C>)"""

    conformed_period_of_report = None
    filed_as_of_date = None
    no_of_columns = None

    with open(fname, 'r') as f:
        # give readlines a small buffer as we expect the head data in the first
        # few lines
        for line in f:
            if 'CONFORMED PERIOD OF REPORT' in line:
                title, conformed_period_of_report = line.split(':')
                conformed_period_of_report = parse_form_13f_date(
                    conformed_period_of_report)

            if 'FILED AS OF DATE' in line:
                title, filed_as_of_date = line.split(':')
                filed_as_of_date = parse_form_13f_date(filed_as_of_date)

            if '<S>' in line:
                # count the <S> column in the column count
                no_of_columns = line.count('<C>') + 1
                return conformed_period_of_report, filed_as_of_date, \
                    no_of_columns

    return conformed_period_of_report, filed_as_of_date, no_of_columns


def parse_form_13f(fname):

    # note 'OTHER MANAGERS' field is absent from the fixed width column
    # definitions presumably because the no data is present in these documents
    # for this field.
    # The assertion will pick up if we get unexpected no. of columns
    conformed_period_of_report, filed_as_of_date, no_of_columns = \
            parse_form_13f_head(fname)

    assert no_of_columns == len(Form13F.column_names), \
        'Not enough column_names/columns'

    # construct pandas.DataFrame from fixed with file, use the 0th column as
    # the label for the row (security)
    data_frame = pandas.read_fwf(
        fname,
        # ranges of the fixed width columns
        colspecs=[(0, 29), (29, 45), (45, 57), (57, 64), (64, 73), (73, 79),
                  (79, 92), (92, 112), (112, 123), (123, 132)],
        skiprows=[0, 1, 2, 3, 4],
        index_col=0,
        names=Form13F.column_names,
    )

    # drop label if all values in row are Na
    data_frame = data_frame.dropna(how='all')

    # for each column apply a function on each of the rows which strips strings
    # of tabs, newlines and spaces
    data_frame = data_frame.apply(lambda x: x.apply(
        lambda x: x.strip() if isinstance(x, str) else x)
    )

    return Form13F(fname, conformed_period_of_report, filed_as_of_date,
                   data_frame)


def sort_forms(data_set):
    "sorts data_set by conformed date"
    return sorted(data_set, key=lambda d: d.conformed_period)


def parse_all_files():
    """returns Form13F objects"""
    return sort_forms(
        map(parse_form_13f, get_files())
    )
