#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import re
import shelve
import codecs
import socket
import urllib2
from json import dumps
import json
from urllib import urlencode
from retry_decorator import retry
from org_info_parser import OrgInformation


data_URL = 'http://oid.nat.gov.tw/infobox1/showdata.jsp'
time_str = time.strftime("%Y%m%dT%H%M%S", time.localtime())


def save_to_json(file_name, data):
    """ Save data to json format, this will use file_name to save
    """
    with codecs.open(file_name, 'w', 'utf-8') as f:
        f.write(dumps(data, ensure_ascii = False, indent=4))


def get_response_data(response):
    """
    Check response is big5 or not.
    Than call decode method.
    """
    info = response.info()
    if _is_big5_charset(info.plist):
        raw_data = response.read().decode('big5')
    else:
        raw_data = response.read()

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
    param_pat = re.compile(r'showdata\(\'(?P<PARAM>\S*)\'\)')

    for match in re.finditer(param_pat, data):
        return match.group('PARAM')


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
        if info[u'機關 DN'] == name.decode('utf-8'):
            return info

    return None


def walk_oid(d, output, oid_data, level):
    """ walking l in d
    """
    for i in d.keys():
        param = collect_showdata_param(eval(i)[1])
        if param:
            info = find_info(oid_data, param)
            if info:
                name = info[u'機關名稱']
                oid = info[u'機關 OID']

                if __debug__:
                    print "\t" * level + "%s %s" % (name, oid)

                children = []

                walk_oid(d[i], children, oid_data, level+1)

                data = {}
                data.setdefault('name',name)
                data.setdefault('oid',oid)
                if len(children) is not 0:
                    data.setdefault('children',children)

                output.append(data)


def main(db_path, oid_path):
    oid = shelve.open(db_path)['oid']
    raw_data_list = []
    oid_data = json.load(open(oid_path))

    walk_oid(oid, raw_data_list, oid_data, 0)

    roc = { 'name' : u'中華民國政府',
            'oid' : u'2.16.886.101',
            'children' : raw_data_list }
    save_to_json(file_name = "../raw_data/oid.all.tree_%s.json" %(time_str),
                 data = roc)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ./%s <oid_shelve file> <oid_raw_data.js>" % (sys.argv[0])
        sys.exit(-1)

    main(sys.argv[1],sys.argv[2])
