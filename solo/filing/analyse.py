"""
Analyses datastructure ./data/solo-filing.pkl calculating metrics given in
brief: "Data Exercise for IM Developer Role.docx"

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

import datetime
from pprint import pprint

from .import parse


def get_common_stocks(data_frame):
    title_of_class = parse.Form13F.column_names[1]
    # boolean array indicating match of COM followed by 0 or more whitespace
    filter = data_frame[title_of_class].str.contains('^COM\w*')
    # apply pandas filter on columns
    return data_frame[filter]


def total_market_value_of_COM(data_frame):

    data_frame = get_common_stocks(data_frame)
    # string identifying market value
    market_value = parse.Form13F.column_names[3]

    return data_frame[market_value].sum()


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
    df_by_market_value = data_frame.sort(parse.Form13F.column_names[3],
                                         ascending=False)
    return df_by_market_value[0: n]


def get_closest_form(forms, target_date):
    """given set of data return that which has closest conformed period to
    target date"""

    date_diffs = []
    for i, form in enumerate(forms):
        # conformed_period must be greater than target to be of interest
        if form.conformed_period > target_date:
            date_diffs.append((i, form.conformed_period - target_date))

    # sort by date diff ascending
    sorted_diffs = sorted(date_diffs, key=lambda x: x[1])

    return data_set[sorted_diffs[0][0]]


def question_2_a(forms):
    """a) What was the total value of all common stock positions in the fund
    for each quarter? Did the fund grow or fall in value with respect to its
    common stock positions over the 4 quarters?
    """

    total_values = []
    for form in forms:
        total_values.append(
            (form, total_market_value_of_COM(form.data_frame))
        )

    first_quarter_total = total_values[0][1]
    last_quarter_total = total_values[-1][1]

    return total_values, first_quarter_total < last_quarter_total


def question_2_b(forms):
    """b) What would have been the 5 largest holdings of common stock that were
    publically available on 12 August 2012 for the fund manager?"""
    target_date = datetime.datetime(2012, 8, 12)

    form = get_closest_form(forms, target_date)

    # assuming 'largest holdings' means by market value not no. of shares
    return get_top_market_value(form.data_frame, 5)


def question_2_c(forms):
    """c) As at 12/31/2012, what were the fund's 3 biggest new common stock
    positions (stocks it had not held in the previous quarter)?"""

    target_conformed_period = datetime.datetime(2012, 12, 31)

    # check the last conformed data equals target
    assert forms[-1].conformed_period == target_conformed_period, \
            'Got wrong date'

    target_data_frame = forms[-1].data_frame
    previous_data_frame = forms[-2].data_frame

    new_stocks = get_new_stocks(target_data_frame, previous_data_frame)

    # assuming 'biggest new common stock...' means by market value
    top_holdings = get_top_market_value(new_stocks, 3)

    return top_holdings


def verbose_answer_all():
    forms = parse.parse_all_files()
    print question_2_a.__doc__
    total_values, fund_growth = question_2_a(forms)
    print ('Answer: The fund %s grow with respect to its COM.* positions '
           'over the 4 quarters' % 'did' if fund_growth else 'did not')

    print question_2_b.__doc__
    print ('Answer: 5 largest holdings of common stock that were vailble to '
           'the public as of 12/08/12 were: %s' % question_2_b(forms))

    print question_2_c.__doc__
    print 'Answer: The 3 biggest mew COM.* positions as of 12/31/2012 are: %s'\
            % ', '.join(list(question_2_c(forms).index))


def analyse_all():

    quarters = parse.parse_all_files()
    assert len(quarters) == 4, 'Wrong number of quarters'

    print question_2_a(quarters)
    print question_2_b(quarters)

    print question_2_c(quarters)
