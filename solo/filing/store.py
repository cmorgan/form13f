"""
Parses ./data/*.txt, creates queryable datastructure, saves as pickle
solo-filing.pkl


From brief:

1. Store the fields from the complete submission text files (including Name
of Issuer, Title of Class, CUSIP, etc) in a data structure. Be sure to include
the "period of report" and the "filed as of date" as fields. 
"""

import os

import pandas


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(THIS_DIR, 'data')

f = 'data/0000909012-12-000274.txt'


def get_files():
    for fname in os.listdir(DATA_DIR):
        if os.path.isfile(fname):
            yield os.path.join(DATA_DIR, fname)


def parse_file(fname):
    #return pandas.read_csv(fname, sep='\s', header=2, skiprows=0)
    #return pandas.read_csv(fname, sep='\w', skipinitialspace=True, skiprows=5)
    return pandas.read_csv(fname, delim_whitespace=True, skipinitialspace=True, skiprows=5)
    


def simple_parse(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    return lines
