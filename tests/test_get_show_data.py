import unittest

import get_show_data_all

class TestGetShowData(unittest.TestCase):
    def test_collect_showdata_param_1(self):
        show_data = (
            "showdata('"
            "l=\xe5\xbd\xb0\xe5\x8c\x96\xe7\xb8\xa3,"
            "c=TW"
            "')"
        )
        expect = (
            "l=\xe5\xbd\xb0\xe5\x8c\x96\xe7\xb8\xa3,"
            "c=TW"
        )
        result = get_show_data_all.collect_showdata_param(show_data)
        self.assertEqual(result, expect)

    def test_collect_showdata_param_2(self):
        show_data = (
            "showUnitdata('"
            "ou=\xe5\x9f\x8e\xe5\xb8\x82\xe6\x9a\xa8\xe8\xa7\x80\xe5\x85\x89\xe7\x99\xbc\xe5\xb1\x95\xe8\x99\x95,"
            "o=\xe7\xb8\xa3\xe6\x94\xbf\xe5\xba\x9c,"
            "l=\xe5\xbd\xb0\xe5\x8c\x96\xe7\xb8\xa3,"
            "c=TW"
            "')"
        )
        expect = (
            "ou=\xe5\x9f\x8e\xe5\xb8\x82\xe6\x9a\xa8\xe8\xa7\x80\xe5\x85\x89\xe7\x99\xbc\xe5\xb1\x95\xe8\x99\x95,"
            "o=\xe7\xb8\xa3\xe6\x94\xbf\xe5\xba\x9c,"
            "l=\xe5\xbd\xb0\xe5\x8c\x96\xe7\xb8\xa3,"
            "c=TW"
        )
        result = get_show_data_all.collect_showdata_param(show_data)
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
