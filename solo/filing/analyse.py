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


def total_market_value_of_COM(data_frame):
    
    title_of_class = parse.COLUMN_NAMES[1]
    market_value = parse.COLUMN_NAMES[3]

    # filter TITLE OF CLASS = COM
    filter = data_frame[title_of_class] == 'COM'
    # apply filter
    data_frame = data_frame[filter]

    return data_frame[market_value].sum()


def question_2_a(data_set):
    """a) What was the total value of all common stock positions in the fund
    for each quarter? Did the fund grow or fall in value with respect to its
    common stock positions over the 4 quarters?

    Answer return as tuple
    """

    total_values = []
    for fname, conformed_period, filed_date, df in data_set:
        total_values.append((fname, conformed_period, filed_date,
                             total_market_value_of_COM(df)))

    first_quarter_total = total_values[0][3]
    last_quarter_total = total_values[-1][3]

    return total_values, first_quarter_total < last_quarter_total


def analyse_all():
    quarters = parse.parse_all_files()

    assert len(quarters) == 4, 'Wrong number of quarters'

    return question_2_a(quarters)
