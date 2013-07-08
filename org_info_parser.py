# -*- coding: utf-8 -*-

from pprint import pprint
import re

class OrgInformation(object):
    def __init__(self):
        self._parse_pat = re.compile(r'\<td bgcolor=\"#[A-Za-z]{6}\"\s+align=\"center\"\>(?P<NAME>\S+)\<\/td\>\s+\<td( colspan=[\d] width=\"[\d]{1,2}%\")?\>(?P<VALUE>\S*)\<\/td\>', re.M)

        self._info_list = []

    def parse_data(self, row_data):
        info_dict = {}
        for match in re.finditer(self._parse_pat, row_data):
            name = match.group('NAME')
            value = match.group('VALUE')
            info_dict[name.decode('big5')] = value.decode('big5')

        if not info_dict:
            return
        self._info_list.append(info_dict)

        if __debug__:
            pprint(info_dict)


    def get_info_iter(self):
        for info in self._info_list:
            yield info
        raise StopIteration

