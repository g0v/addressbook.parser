# -*- coding: utf-8 -*-
from pprint import pprint
import re

ORG_PATTERN = re.compile(
    r'\<td bgcolor=\"#[A-Za-z]{6}\"\s+align=\"center\"\>(?P<NAME>\S+)\<\/td\>\s+\<td( colspan=[\d] width=\"[\d]{1,2}%\")?\>(?P<VALUE>\S*)\<\/td\>',
    re.MULTILINE
)


def parse_org_info(html_page):
    info_dict = {}
    for m in ORG_PATTERN.finditer(html_page):
        name = m.group('NAME')
        value = m.group('VALUE')
        info_dict[name] = value
    return info_dict


class OrgInformation(object):
    def __init__(self):
        self._info_list = []

    def parse_data(self, row_data):
        info_dict = {}
        for match in ORG_PATTERN.finditer(row_data):
            name = match.group('NAME')
            value = match.group('VALUE')
            info_dict[name] = value

        if not info_dict:
            return
        self._info_list.append(info_dict)

        if __debug__:
            pprint(info_dict)


    def get_info_iter(self):
        for info in self._info_list:
            yield info
        raise StopIteration

