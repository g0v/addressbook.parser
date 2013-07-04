# -*- coding: utf-8 -*-

import re

class OrgInformation(object):
    def __init__(self, row_data):
        self._row_data = row_data
        self._info = {}
        self._parse_pat = re.compile('\<td bgcolor=\"#[A-Za-z]{6}\"\s+align=\"center\"\>(?P<NAME>\S+)\<\/td\>\s+\<td( colspan=[\d] width=\"[\d]{1,2}%\")?\>(?P<VALUE>\S*)\<\/td\>', re.M)
        
        self._info_parser()
        
    def _info_parser(self):
        for match in re.finditer(self._parse_pat, self._row_data):
            name = match.group('NAME')
            value = match.group('VALUE')
            self._info[name] = value
            print name
            print value
            print '-'*64