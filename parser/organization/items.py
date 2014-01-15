# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
'''
Example data in oid.nat.gov.tw:
    {
        "機關DN": "ou=abc,ou=123,o=def,c=TW",
        "機關傳真": "xx-xxxxx",
        "機關OID": "x.xx",
        "上層機關": "PARENT_NAME",
        "機關電話": "xx-xxxxx",
        "郵遞區號": "xxx",
        "機關網址": "http://example.url",
        "機關代號": "XXXXXXX",
        "機關email": "xx@mail",
        "機關地址": "address",
        "機關名稱": "FULL_NAME"
    }
'''


class OrganizationItem(Item):
    ''' an organization item
    '''
    # save item source url here
    source_url = Field()

    dn = Field()

    oid = Field()
    name = Field()

    parent_name = Field()

    tel = Field()
    fax = Field()

    address = Field()
    postal_address = Field()

    email = Field()
    url = Field()
