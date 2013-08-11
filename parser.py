# -*- coding: utf-8 -*-
from json import dumps
from sys import exit
from urllib import urlencode
import re
import urllib2 as url
import codecs

from org_info_parser import OrgInformation

def main():
    info_URL = 'http://oid.nat.gov.tw/infobox1/personmain.jsp'
    data_URL = 'http://oid.nat.gov.tw/infobox1/showdata.jsp'

    try:
        # query data from infoURL
        response = url.urlopen(info_URL)
    except url.URLError, e:
        print 'Open url (%s) failed : %s' % (info_URL, e)
        return 1
    except ValueError, e:
        print '%s' % e
        return 1

    web_data = _get_response_data(response)

    param_list = _collect_showdata_param(web_data)

    raw_data_list = _collect_showdata_response(data_URL = data_URL,
                                               param_list = param_list)

    org_info = OrgInformation()
    for raw_data in raw_data_list:
        org_info.parse_data(raw_data)

    # Get org_info data iter
    data = []
    for info in org_info.get_info_iter():
        data.append(info)

    _save_to_json(file_name = "raw_data/oid.nat.gov.tw.json", data = data)


def _save_to_json(file_name, data):
    """
    Save data to json format, this will use file_name to save
    """

    with codecs.open(file_name, 'w', 'utf-8') as f:
        f.write(dumps(data, ensure_ascii = False, indent=4))


def _collect_showdata_param(data):
    """
    find request param in data
    this will find special param, like "javascript:showdata(<PARAM>)"
    """

    param_list = []
    param_pat = re.compile(r'javascript:showdata\(\'(?P<PARAM>\S*)\'\)')

    for match in re.finditer(param_pat, data):
        param = match.group('PARAM')
        param_list.append(param)

    return param_list


def _collect_showdata_response(data_URL, param_list):
    """
    request secound data by data_URL
    this will use param_list to fetch data, requeset URL must encode by big5
    """
    assert isinstance(param_list, list)

    data_list = []
    for param in param_list:
        encode_data = urlencode({'sSdn':param.encode('big5')})
        request = url.Request(data_URL, encode_data)
        response = url.urlopen(request)

        raw_data = _get_response_data(response)
        data_list.append(raw_data)

    return data_list


def _fetch_struct(data):
    """
    fetch struct from data
    data format will be "o=abcd,c=TW" or "l=abcd,c=TW"
    Then send item_dict out
    item_dict :{ sDn    : data_1,
                 sLevel : data_2,
                 sTitle : data_3
               }
    """
    item_dict = {}

    for params in data[0].split(','):
        for foo in re.findall(r'(\w)=(.*)', params, re.M):
            item_dict[foo[0]] = foo[1]

    item_dict['sLevel'] = data[1]
    item_dict['sTitle'] = data[2]

    return item_dict


def _get_response_data(response):
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


def _fetch_data(base_url, request):
    """
    request data from base_url
    use GET to do it
    parameter sTitle sDn sLevel sDn
    """
    big5_request = {}
    big5_request['sSdn'] = request['sTitle'].decode('utf-8').encode('big5')

    params = urlencode(big5_request)
    data_url = "%s?%s" % (base_url, params)
    try:
        response = url.urlopen(data_url)
    except url.URLError, e:
        print 'Open url (%s) failed : %s' % (data_url, e)
        return
    except ValueError, e:
        print '%s' % e
        return

    raw_data = _get_response_data(response)

    return raw_data

if __name__ == '__main__':
    main()
