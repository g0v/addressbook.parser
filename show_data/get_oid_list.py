#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
grab entire oid list and save them with python shelve
"""

import socket
import urllib2
import urllib
import re
import shelve
import time
from retry_decorator import retry
from BeautifulSoup import BeautifulSoup

socket.setdefaulttimeout(10)

url = 'http://oid.nat.gov.tw/infobox1/personmain.jsp'

head = {'sLevel': '1',
    'sTitle': '中華民國政府'.decode('utf8').encode('big5'),
    'sDn': 'c=TW'.decode('utf8').encode('big5')}

# head = {'sLevel': '2',
    # 'sTitle': '總統府'.decode('utf8').encode('big5'),
    # 'sDn': 'o=總統府,c=TW'.decode('utf8').encode('big5')}

time_str = time.strftime("%Y%m%dT%H%M%S", time.localtime())
oid_shelve = shelve.open('../raw_data/oid_shelve_%s.db' % time_str)
oid = {}

@retry((urllib2.URLError,socket.timeout))
def get_page(d = None):
    req = urllib2.Request(url = url, data = d)
    resp = urllib2.urlopen(req)
    return resp.read()

def walk(child, items):
    """go thru entire leaf node"""

    for i in xrange(len(items)/2):
        NextLevel = items[2*i]
        ShowData = items[2*i+1]

        nl = re.search('NextLevel\((.*)\)', NextLevel).group(0)
        sd = re.search('show(Unit)?data\((.*)\)', ShowData).group(0)
        print nl

        node = repr((nl, sd)) # shelve don't allow tupe
        child.setdefault(node, {})

        sDn, sLevel, sTitle = re.search('NextLevel\(\'(.*)\',(\d),\'(.*)\'\)', nl).groups()
        d = urllib.urlencode({'sLevel': sLevel,
            'sTitle': sTitle.decode('utf8').encode('big5'),
            'sDn': sDn.decode('utf8').encode('big5')})
        raw = get_page(d)
        pg = BeautifulSoup(str(raw).decode('big5', 'ignore'))
        sub_items = [str(i).replace('\n', '') for i in pg.findAll('a') if 'span' not in str(i)]

        if not sub_items: continue

        walk(child[node], sub_items)

def main():
    d = urllib.urlencode({'sLevel': head['sLevel'], 'sTitle': head['sTitle'], 'sDn': head['sDn']})
    raw = get_page(d)
    pg = BeautifulSoup(str(raw).decode('big5', 'ignore'))
    items = [str(i).replace('\n', '') for i in pg.findAll('a') if 'span' not in str(i)]

    walk(oid, items)

    oid_shelve['oid'] = oid
    oid_shelve.close()

if __name__ == "__main__":
    try:
        main()
    except:
        import IPython; IPython.embed()
