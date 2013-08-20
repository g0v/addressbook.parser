# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class OrganizationItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class DGPAItem(Item):
    '''
    Example:
    {"expanded":false,
    "classes":"folder",
    "hasChildren":true,
    "id":"100000000A",
    "text":"國民大會(100000000A)",
    "children":null}
    '''
    orgID = Field()
    name = Field()
    hasChildren = Field()
    classes = Field()


class DGPADetailItem(Item):
    name = Field()
    orgID = Field()
    tel = Field()
    fax = Field()
    address = Field()
    url = Field()
    email = Field()
    google_map = Field()


class ShowdataItem(Item):

    dn = Field()
    level = Field()
    title = Field()


class OIDItem(Item):

    oid = Field()
    oid_name = Field()
    dn = Field()
    fax = Field()
    tel = Field()
    email = Field()
    address = Field()
    postal_address = Field()
    up_gov = Field()
    url = Field()
