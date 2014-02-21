#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import json
import pprint
import re
import shelve
import signal
import socket
import sys
import time
import urllib2
from urllib import urlencode
from retry_decorator import retry
import org_info_parser

try:
    import uniout
except ImportError, e:
    pass

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

CANCEL = False

data_URL = 'http://oid.nat.gov.tw/infobox1/showdata.jsp'
time_str = time.strftime("%Y%m%dT%H%M%S", time.localtime())


def save_to_json(file_name, data):
    """ Save data to json format, this will use file_name to save
    """
    with codecs.open(file_name, 'w', 'utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))


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
        pprint.pprint('error: cannot parse showdata -- [%s]' % data)
    return ''


def collect_goverment(data):
    g = re.compile(r'[ol]=(?P<GOVERNMENT>\S*),c=TW')

    for match in re.finditer(g, data):
        return match.group('GOVERNMENT')


@retry(socket.timeout)
def request_data(url, param):
    """ request data on url with param
    """
    request = urllib2.Request(url, param)
    response = urllib2.urlopen(request)

    global CANCEL
    if CANCEL:
        return None
    else:
        return get_response_data(response)


def walk_oid(d, output, oid_loaded_set, level):
    for i in d:
        show_data = eval(i)[SHOW_DATA]

        param = collect_showdata_param(show_data)
        if not param:
            continue

        if __debug__:
            pprint.pprint('    ' * level + 'sSdn : %s' % param)

        try:
            utf8_param = param.decode('utf-8')
            if utf8_param in oid_loaded_set:
                continue

            encode_param = urlencode({'sSdn': utf8_param.encode('big5')})
            output.setdefault('success_decode', []).append(encode_param)

        except UnicodeDecodeError:
            if __debug__:
                pprint.pprint('error: cannot decode utf-8 param -- [%s]' % param)
            output.setdefault('failed_decode', []).append(param)

        walk_oid(d[i], output, oid_loaded_set, level+1)


def signal_handler(signal, frame):
    pprint.pprint('You pressed Ctrl+C cancel work! saving data...')
    global CANCEL
    CANCEL = True


def main(db_file, append_source):
    oid = shelve.open(db_file)['oid']
    raw_data_list = {}
    append_oid = json.load(open(append_source))
    oid_loaded_set = set([info[u'機關DN'] for info in append_oid])

    walk_oid(oid, raw_data_list, oid_loaded_set, 0)

    print "You can pressed Ctrl+C to cancel"
    signal.signal(signal.SIGINT, signal_handler)

    info_list = []
    for encode_param in raw_data_list['success_decode']:
        global CANCEL

        raw_data = request_data(data_URL, encode_param)
        if not raw_data and CANCEL:
            break

        info = org_info_parser.parse_org_info(raw_data)
        if __debug__:
            pprint.pprint(info)

        if info:
            info_list.append(info)

        if CANCEL:
            break

    append_oid += info_list
    save_to_json(file_name="../raw_data/oid.nat.gov.tw_%s.json" % (time_str),
                 data=append_oid)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        pprint.pprint("Usage: ./%s <oid_shelve_db> <append_source>" % sys.argv[0])
        sys.exit(-1)

    main(sys.argv[1], sys.argv[2])
