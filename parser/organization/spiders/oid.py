# -*- coding: utf-8 -*-
from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from urllib import urlencode
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
        hxs = HtmlXPathSelector(response)
        show_data_param_list = hxs.select("//td/a/@href").re(r'javascript:showdata\(\'(?P<PARAM>\S*)\'\)')
        raw_data_list = self._collect_showdata_response(data_URL = self.data_URL,
                                                        param_list = show_data_param_list)

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
        if self._is_big5_charset(response.encoding):
            raw_data = response.body.decode('big5')
        else:
            raw_data = response.body

        return raw_data


    def _is_big5_charset(self, encoding):
        """
        Check charset is big5 or not
        """
        big5_set_list = ['big5', 'ms950', 'cp950']

        for item in encoding:
            if encoding not in big5_set_list:
                continue

            return True
        return False


    def _collect_showdata_response(self, data_URL, param_list):
        """
        request secound data by data_URL
        this will use param_list to fetch data, requeset URL must encode by big5
        """
        assert isinstance(param_list, list)

        data_list = []
        for param in param_list:
            encode_data = urlencode({'sSdn':param.encode('big5')})
            request = Request(data_URL, encode_data)

            raw_data = self._get_response_data(request)
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
