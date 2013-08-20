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

    start_urls = [
        info_URL
    ]

    def parse(self, response):
        self.log('A response from %s' % response.url)
        web_data = self._get_response_data(response)
        param_list = self._collect_showdata_param(web_data)


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

