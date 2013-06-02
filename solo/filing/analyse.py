# -*- coding: utf-8 -*-
"""
Analyses parse.Form13F calculating metrics given in brief: "Data Exercise for
IM Developer Role.docx"

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

from .import parse


def is_nyse_open(dt):
    nyse_holiday_list_2013 = [
        datetime.date(2013, 1, 1),
        datetime.date(2013, 1, 21),
        datetime.date(2013, 2, 18),
        datetime.date(2013, 3, 29),
        datetime.date(2013, 5, 27),
        datetime.date(2013, 7, 4),
        datetime.date(2013, 9, 2),
        datetime.date(2013, 11, 28),
        datetime.date(2013, 12, 25)
    ]
    # monday = 0, sunday = 6
    if dt.weekday() < 5 and dt not in nyse_holiday_list_2013:
        return True
    return False


def get_new_stocks(form1, form2):
    """return data_frame containing COM stock positions that are in form1 but
    not in form2"""

    new_stocks = form1.common_stocks.index - form2.common_stocks.index

    # apply a pandas filter on the index
    return form1.data_frame.ix[new_stocks]


def get_top_by_column(data_frame, n, column):
    "return top n holdings from a data_frame"

    # sort by market value
    df_by_market_value = data_frame.sort(column, ascending=False)
    return df_by_market_value[0: n]


def get_closest_form(forms, target_date):
    """given forms return form with conformed period closest to target date"""

    date_diffs = []
    for i, form in enumerate(forms):
        # conformed_period must be greater than target to be of interest
        if form.conformed_period > target_date:
            date_diffs.append((i, form.conformed_period - target_date))

    # sort by date diff ascending
    sorted_diffs = sorted(date_diffs, key=lambda x: x[1])

    return forms[sorted_diffs[0][0]]


def question_2_a(forms):
    """Question a) What was the total value of all common stock positions in
    the fund for each quarter? Did the fund grow or fall in value with respect
    to its common stock positions over the 4 quarters?  """

    total_values = []
    for form in forms:
        total_values.append((form, form.total_market_value_of_COM))

    first_quarter_total = total_values[0][1]
    last_quarter_total = total_values[-1][1]

    return total_values, first_quarter_total < last_quarter_total


def question_2_b(forms):
    """Question b) What would have been the 5 largest holdings of common stock
    that were publically available on 12 August 2012 for the fund manager?"""

    target_date = datetime.date(2012, 8, 12)

    # to be publically available, an exchange must be open
    if not is_nyse_open(target_date):
        return []

    form = get_closest_form(forms, target_date)

    common_stocks = form.common_stocks

    market_value = form.column_names[3]
    # assuming 'largest holdings' means by market value not no. of shares
    return list(get_top_by_column(common_stocks, 5, market_value).index)


def question_2_c(forms):
    """Question c) As at 12/31/2012, what were the fund's 3 biggest new common
    stock positions (stocks it had not held in the previous quarter)?"""

    forms = parse.sort_forms(forms)
    target_conformed_period = datetime.date(2012, 12, 31)

    # check the last conformed data equals target
    assert forms[-1].conformed_period == target_conformed_period, \
        'Got wrong date'

    target_form = forms[-1]
    previous_form = forms[-2]

    new_stocks = get_new_stocks(target_form, previous_form)

    market_value = target_form.column_names[3]
    # assuming 'biggest new common stock...' means by market value
    top_holdings = get_top_by_column(new_stocks, 3, market_value)

    return list(top_holdings.index)


def check_number_of_forms(forms):
    assert len(forms) == 4, 'Wrong number of forms.'


def verbose_answer_all():
    forms = parse.parse_all_files()

    print('\n' + question_2_a.__doc__)

    total_values, fund_growth = question_2_a(forms)
    value_string = 'The value of the fund in conformed period %s was £%sk'

    all_value_string = '\n'.join(
        [value_string % (form.conformed_period, fund_value) for form,
         fund_value in total_values]
    )

    print('Answer:\n%s.\nThe fund %s grow with respect to its %s positions '
          'over the 4 quarters.\n' % (
              all_value_string,
              'did' if fund_growth else 'did not', parse.Form13F.com_regex)
          )

    print(question_2_b.__doc__)
    print('Answer:\n5 largest holdings of common stock that were availble to '
          'the public as of 12/08/12 were: %s\n' % ', '.join(
              question_2_b(forms) or ['None (is exchange open?)'])
          )

    print(question_2_c.__doc__)
    print('Answer:\nThe 3 biggest mew %s positions as of 12/31/2012 are: %s\n'
        % (parse.Form13F.com_regex, ', '.join(question_2_c(forms))))
