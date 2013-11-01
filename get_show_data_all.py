#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import re
import shelve
import codecs
import socket
import urllib2
import json
import uniout
from urllib import urlencode
from retry_decorator import retry
from org_info_parser import OrgInformation
# grequest


SHOW_DATA = 1

SHOW_DATA_PATTERN = re.compile(
    r"""
        show(Unit)?data
        \('
        (?P<PARAM>[^']*)
        '\)
    """,
    re.VERBOSE
)

data_URL = 'http://oid.nat.gov.tw/infobox1/showdata.jsp'
time_str = time.strftime("%Y%m%dT%H%M%S", time.localtime())

def save_to_json(file_name, data):
    """ Save data to json format, this will use file_name to save
    """
    with codecs.open(file_name, 'w', 'utf-8') as f:
        f.write(json.dumps(data, ensure_ascii = False, indent=4))

def get_response_data(response):
    """
    Check response is big5 or not.
    Than call decode method.
    """
    info = response.info()
    raw_data = response.read()

    if not _is_big5_charset(info.plist):
        return raw_data

    try:
        big5_data = raw_data.decode('big5')
        return big5_data
    except UnicodeDecodeError:
        return raw_data

def _is_big5_charset(plist):
    """
    Check charset is big5 or not in header
    """
    assert isinstance(plist, list)

    big5_set_list = ['big5', 'ms950', 'cp950']
    re_pat = re.compile('charset=(?P<CODE>\S*)')

    for item in plist:
        m = re_pat.match(item)
        if not m:
            continue

        if m.group('CODE').lower() not in big5_set_list:
            continue

        return True
    return False


def collect_showdata_param(data):
    """ find request param in showdata
    this will find special param, like "javascript:showdata(<PARAM>)"
    """
    m = SHOW_DATA_PATTERN.search(data)
    if m:
        return m.group('PARAM')

    # error
    if __debug__:
        print 'error: cannot parse showdata -- [%s]' % data
    return ''


def collect_goverment(data):
    g = re.compile(r'[ol]=(?P<GOVERNMENT>\S*),c=TW')

    for match in re.finditer(g, data):
        return match.group('GOVERNMENT')

@retry((socket.timeout))
def showdata(data_URL, param):
    """ request show_data on data_URL with param
    """
    request = urllib2.Request(data_URL, param)
    response = urllib2.urlopen(request)
    return get_response_data(response)

def find_info(oid_data, name):
    """ find info in oid_data for name
    """
    for info in oid_data:
        if info[u'機關DN'] == name.decode('utf-8'):
            return info

    return None


def walk_oid(d, output, check_source, level):
    for i in d.keys():
        show_data = eval(i)[SHOW_DATA]
        param = collect_showdata_param(show_data)
        if param:
            gov = collect_goverment(param)

            if not find_info(check_source, param):

                if __debug__:
                    print '\t'*level + "sSdn : %s" % (param)

                try:
                    encode_param = urlencode({'sSdn':param.decode('utf-8').encode('big5')})
                    output.setdefault('success_decode',[]).append(encode_param)
                except UnicodeDecodeError:
                    output.setdefault('failed_decode',[]).append(param)

                walk_oid(d[i], output, check_source, level+1)

def main(db_file, append_source):
    oid = shelve.open(db_file)['oid']
    raw_data_list = {}
    append_oid = json.load(open(append_source))

    walk_oid(oid, raw_data_list, append_oid, 0)

    org_info = OrgInformation()
    for encode_param in raw_data_list['success_decode']:
        raw_data = showdata(data_URL, encode_param)
        org_info.parse_data(raw_data)

    # Get org_info data iter
    for info in org_info.get_info_iter():
        append_oid.append(info)

    save_to_json(file_name = "raw_data/oid.nat.gov.tw_%s.json" %(time_str),
                 data = append_oid)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ./%s <oid_shelve_db> <append_source>" % (sys.argv[0])
        sys.exit(-1)

    main(sys.argv[1], sys.argv[2])
