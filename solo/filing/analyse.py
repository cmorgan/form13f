"""
Analyses datastructure ./data/solo-filing.pkl calculating metrics given in brief:
"Data Exercise for IM Developer Role.docx"

From brief:

2. Retrieve the following information (for all of these tasks assume common
stock is classified as "COM" in the Title of Class field):

a) What was the total value of all common stock positions in the fund for each
quarter? Did the fund grow or fall in value with respect to its common stock
positions over the 4 quarters?

b) What would have been the 5 largest holdings of common stock that were
publically available on 12 August 2012 for the fund manager? 

c) As at 12/31/2012, what were the fund's 3 biggest new common stock positions
(stocks it had not held in the previous quarter)?
"""

from .import parse
import datetime


def get_common_stocks(data_frame):
    print data_frame
    title_of_class = parse.COLUMN_NAMES[1]
    # filter TITLE OF CLASS = COM
    filter = data_frame[title_of_class] == 'COM'
    # apply pandas filter on columns
    return data_frame[filter]


def total_market_value_of_COM(data_frame):

    data_frame = get_common_stocks(data_frame)
    # string identifying market value
    market_value = parse.COLUMN_NAMES[3]

    return data_frame[market_value].sum()


def question_2_a(data_set):
    """a) What was the total value of all common stock positions in the fund
    for each quarter? Did the fund grow or fall in value with respect to its
    common stock positions over the 4 quarters?

    Answer return as tuple
    """

    total_values = []
    for fname, conformed_period, filed_date, df in data_set:
        total_values.append(
            (fname, conformed_period, filed_date,
             total_market_value_of_COM(df))
        )

    first_quarter_total = total_values[0][3]
    last_quarter_total = total_values[-1][3]

    return total_values, first_quarter_total < last_quarter_total


def get_new_stocks(data_frame1, data_frame2):
    """return data_frame containing COM stock positions that are in data_frame1
    but not in data_frame2"""

    data_frame1, data_frame2 = map(get_common_stocks,
                                   [data_frame1, data_frame2])

    new_stocks = data_frame1.index - data_frame2.index

    # apply a pandas filter on the index
    return data_frame1.ix[new_stocks]


def get_top_market_value(data_frame, n):
    "return top n holdings from a data_frame"

    # sort by market value
    df_by_market_value = data_frame.sort(parse.COLUMN_NAMES[3], ascending=False)
    return df_by_market_value[0: n]


def get_closest_data(data_set, target_date):
    """given set of data return that which has closest conformed period to
    target date"""

    date_diffs = []

    for i, data in enumerate(data_set):
        report_date = data[1]
        # report_date must be greater than target to be of interest
        if report_date > target_date:
            date_diffs.append((i, report_date - target_date))

    # sort by date diff ascending
    sorted_diffs = sorted(date_diffs, key=lambda x: x[1])

    return data_set[sorted_diffs[0][0]]


def question_2_b(data_set):
    """b) What would have been the 5 largest holdings of common stock that were
    publically available on 12 August 2012 for the fund manager?"""
    target_date = datetime.datetime(2012, 8, 12)

    _, _, _, data_frame = get_closest_data(data_set, target_date)

    # assuming 'largest holdings' means by market value not no. of shares
    return get_top_market_value(data_frame, 5)


def question_2_c(data_set):
    """c) As at 12/31/2012, what were the fund's 3 biggest new common stock
    positions (stocks it had not held in the previous quarter)?"""

    target_conformed_date = datetime.datetime(2012, 12, 31)

    # order data by conformed (just in case)
    sorted_data_set = sorted(data_set, key=lambda d: d[1])

    # check the last conformed data equals target
    assert sorted_data_set[-1][1] == target_conformed_date, 'Got wrong date'

    target_data_frame = sorted_data_set[-1][3]
    previous_data_frame = sorted_data_set[-2][3]

    new_stocks = get_new_stocks(target_data_frame, previous_data_frame)

    # assuming 'biggest new common stock...' means by market value
    top_holdings = get_top_market_value(new_stocks, 3)

    return top_holdings


def analyse_all():

    quarters = parse.parse_all_files()
    assert len(quarters) == 4, 'Wrong number of quarters'

    print question_2_a(quarters)
    print question_2_b(quarters)
    print question_2_c(quarters)
