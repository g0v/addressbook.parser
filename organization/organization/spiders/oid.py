# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.spider import BaseSpider
import re

class OIDSpiders(BaseSpider):
    """
    Parser for OID
    """
    name = 'oid'
    allowed_domains = ["oid.nat.gov.tw"]
    info_URL = 'http://oid.nat.gov.tw/infobox1/personmain.jsp'
    data_URL = 'http://oid.nat.gov.tw/infobox1/showdata.jsp'

    start_urls = [ info_URL ]
    info_list = []

    def parse(self, response):
        self.log('A response from %s' % response.url)
        web_data = self._get_response_data(response)
        param_list = self._collect_showdata_param(web_data)
        raw_data_list = self._collect_showdata_response(data_URL = self.data_URL,
                                                   param_list = param_list)

        for raw_data in raw_data_list:
            self.parse_data(raw_data)

        # Get org_info data iter
        data = []
        for info in self.info_list:
            data.append(info)

        # TODO: let data into OIDItem

    def _get_response_data(self, response):
        """
        Check response is big5 or not.
        Than call decode method.
        """
        info = response.info()
        if self._is_big5_charset(info.plist):
            raw_data = response.read().decode('big5')
        else:
            raw_data = response.read()

        return raw_data


    def _is_big5_charset(self, plist):
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


    def _collect_showdata_param(self, data):
        """
        find request  param in showdata
        this will find special param, like "javascript:showdata(<PARAM>)"
        """

        param_list = []
        param_pat = re.compile(r'javascript:showdata\(\'(?P<PARAM>\S*)\'\)')

        for match in re.finditer(param_pat, data):
            param = match.group('PARAM')
            param_list.append(param)

        return param_list


    def _collect_showdata_response(self, data_URL, param_list):
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


    def parse_data(self, row_data):
        parse_pat = re.compile(r'\<td bgcolor=\"#[A-Za-z]{6}\"\s+align=\"center\"\>(?P<NAME>\S+)\<\/td\>\s+\<td( colspan=[\d] width=\"[\d]{1,2}%\")?\>(?P<VALUE>\S*)\<\/td\>', re.M)
        info_dict = {}
        for match in re.finditer(parse_pat, row_data):
            name = match.group('NAME')
            value = match.group('VALUE')
            info_dict[name] = value

        self.info_list.append(info_dict)
