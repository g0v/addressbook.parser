import os
import unittest

import org_info_parser


HTML_PAGE_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../raw_data/oid.raw-2.16.886.101.90010.data'
)


class TestOrgInfoParser(unittest.TestCase):
    def test_parse_org_info(self):
        expect = {
            '\xa4W\xbch\xbe\xf7\xc3\xf6': '',
            '\xb6l\xbb\xbc\xb0\xcf\xb8\xb9': '',
            '\xbe\xf7\xc3\xf6DN': 'l=\xb9\xfc\xa4\xc6\xbf\xa4,c=TW',
            '\xbe\xf7\xc3\xf6OID': '2.16.886.101.90010',
            '\xbe\xf7\xc3\xf6email': '',
            '\xbe\xf7\xc3\xf6\xa5N\xb8\xb9': '',
            '\xbe\xf7\xc3\xf6\xa6W\xba\xd9': '\xb9\xfc\xa4\xc6\xbf\xa4',
            '\xbe\xf7\xc3\xf6\xa6a\xa7}': '',
            '\xbe\xf7\xc3\xf6\xb6\xc7\xafu': '',
            '\xbe\xf7\xc3\xf6\xb9q\xb8\xdc': '',
        }
        with open(HTML_PAGE_PATH) as fp:
            html_page = fp.read()
            result = org_info_parser.parse_org_info(html_page)
            self.assertDictEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
