"""
Parses ./data/*.txt Form 13 F files (http://www.sec.gov/answers/form13f.htm),
creates queryable datastructure, saves as pickle solo-filing.pkl


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

f = '/home/chris/dev/other/solo/solo/filing/data/0000909012-12-000357.txt'
f2 = '/home/chris/dev/other/solo/solo/filing/data/0000909012-12-000436.txt'

# TODO: this could be a nicer datastruct like collections.namedtuple so we
# access it as an object by attribute
COLUMN_NAMES = ['NAME OF ISSUER', 'TITLE OF CLASS', 'CUSIP', 
                'MARKET VALUE', 'SHRS OR PRN AMT', 'SH/ PUT/ PRN CALL',
                'INVESTMENT DESCRETION', 'VOTING AUTHORITY SOLE',
                'VOTING AUTHORITY SHARED', 'VOTING AUTHORITY NONE']


def get_files():
    for fname in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, fname)
        if os.path.isfile(fpath):
            yield fpath


def parse_form_13f_date(date_string):
    # remove tabs, newlines and spaces
    date_string = date_string.strip()
    # No Exception handling here as the date is used as an index
    return datetime.datetime.strptime(date_string, '%Y%m%d')


def parse_form_13f_head(fname):
    """extract 'confirmed period of report' and 'filed as of date' from head of
    Form 13F and number of declared columns (<C>)"""

    conformed_period_of_report = None
    filed_as_of_date = None
    no_of_columns = None

    with open(fname, 'r') as f:
        # give readlines a small buffer as we expect the head data in the first
        # few lines
        for line in f.readlines(20):
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
                return conformed_period_of_report, filed_as_of_date, no_of_columns

    return conformed_period_of_report, file_as_of_date, no_of_columns


def parse_form_13f(fname):

    # note 'OTHER MANAGERS' field is absent from the fixed width column definitions
    # presumably because the no data is present in these documents for this field.
    # The assertion will pick up if/when the column count comes to 13
    conformed_period_of_report, filed_as_of_date, no_of_columns = \
            parse_form_13f_head(fname)

    assert no_of_columns == len(COLUMN_NAMES), 'Not enough column_names/columns'

    # construct pandas.DataFrame from fixed with file, use the 0th column as
    # the label for the row (security)
    data_frame = pandas.read_fwf(
        fname,
        # ranges of the fixed width columns
        colspecs = [(0, 29), (29, 45), (45, 57), (57, 64), (64, 73), (73, 79),
                    (79, 92), (92, 112), (112, 123), (123, 132)],
        skiprows=[0,1,2,3,4],
        index_col=0,
        names=COLUMN_NAMES,
    )

    # drop label if all values in row are Na
    data_frame = data_frame.dropna(how='all')

    # for each column apply a function on each of the rows which strips string
    # data of tabs, newlines and spaces
    data_frame = data_frame.apply(lambda x: x.apply(
        lambda x: x.strip() if isinstance(x, basestring) else x)
    )

    return fname, conformed_period_of_report, filed_as_of_date, data_frame


def parse_all_files():
    """returns data_set, [(fname, conformed_period_of_report, filed_as_of_date,
    data_frame), ...]"""
    return map(parse_form_13f, get_files())
