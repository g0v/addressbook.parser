#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import pprint
import urllib2

# 3-party modules
import uniout

# in-project modules
import oid_org_map


OID_TREE_JSON = '../raw_data/oid.tree.lite.json'

# year, code, amount, name, topname, depname, depcat, cat, ref
# 0     1     2       3     4        5        6       7    8

BUDGET_CSV = [
    {  # 2014
        #'csv_file': 'budget_data/tw2014ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2014ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2013
        #'csv_file': 'budget_data/tw2013ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2013ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2012
        #'csv_file': 'budget_data/tw2012ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2012ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2011
        #'csv_file': 'budget_data/tw2011ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2011ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2010
        #'csv_file': 'budget_data/tw2010ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2010ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2009
        #'csv_file': 'budget_data/tw2009ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2009ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2008
        #'csv_file': 'budget_data/tw2008ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2008ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2007
        #'csv_file': 'budget_data/tw2007ap.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/tw2007ap.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
    {  # 2013ap-proposed
        #'csv_file': 'budget_data/2013ap-proposed.csv',  # for local test
        'csv_url': 'https://raw.github.com/g0v/twbudget/master/app/assets/data/2013ap-proposed.csv',
        'row_skip': [0],
        'column_year': 0,
        'column_org_name': 5,
    },
]

# match status
MATCH = 'MATCH'
PARTIAL_MATCH = 'PARTIAL'
MISMATCH = 'MISS'


class IMatcher(object):
    def add(self, obj):
        raise NotImplementedError

    def is_match(self):
        raise NotImplementedError


class ExactMatcher(IMatcher):
    def __init__(self):
        self._match_objs = set()

    def add(self, obj):
        self._match_objs.add(obj)

    def match(self, obj):
        if obj in self._match_objs:
            return MATCH
        else:
            return MISMATCH


# helper functions
def get_budget(budget_row_data, column_id):
    assert 0 <= column_id < len(budget_row_data)
    return budget_row_data[column_id]


def get_budget_fp(budget):
    # try to open local file
    if 'csv_file' in budget:
        print 'OPEN     %s' % budget['csv_file']
        try:
            return open(budget['csv_file'])
        except IOError, e:
            print 'FAILED   %s' % e

    # download from web
    if 'csv_url' in budget:
        print 'OPEN     %s' % budget['csv_url']
        try:
            return urllib2.urlopen(budget['csv_url'])
        except urllib2.HTTPError, e:
            print 'FAILED   %s' % e

    # error
    print 'SKIP     Cannot get budget CSV'
    return None


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    """ ref : http://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python """
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def check_budget_org(budget, org_matcher):
    assert isinstance(org_matcher, ExactMatcher)

    check_result = []

    fp = get_budget_fp(budget)
    if not fp:
        return check_result

    csv_reader = unicode_csv_reader(fp)
    for i, row in enumerate(csv_reader):
        if i in budget['row_skip']:
            continue

        org_name = get_budget(row, budget['column_org_name'])

        check_result.append({
            'row': row,
            'line': i,
            'match_status': org_matcher.match(org_name),
        })

    return check_result


def show_check_result(budget, check_result):
    for data in check_result:
        row = data['row']
        line = data['line']
        org_name = get_budget(row, budget['column_org_name'])
        year = get_budget(row, budget['column_year'])

        if data['match_status'] == MATCH:
            print 'MATCH    %s' % org_name.encode('utf-8')
        elif data['match_status'] == PARTIAL_MATCH:
            print 'PARTIAL  %s' % org_name.encode('utf-8')
        else:
            print 'MISS     %s  (year:%s, line:%s)' % (org_name.encode('utf-8'), year.encode('utf-8'), line)


def main():
    oo_map = oid_org_map.build_oid_org_map(OID_TREE_JSON)
    assert isinstance(oo_map, oid_org_map.OidOrgMap)

    org_matcher = ExactMatcher()
    for name in oo_map.iter_org_names():
        org_matcher.add(name)

    for budget in BUDGET_CSV:
        result = check_budget_org(budget, org_matcher)
        show_check_result(budget, result)


if __name__ == '__main__':
    main()
