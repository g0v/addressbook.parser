#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pprint

# 3-party module
import uniout


DEBUG_OID_ORG_MAP = False


class OidOrgMap(object):
    def __init__(self):
        self._id_name_map = {}
        self._name_id_map = {}

    def add_org(self, oid, name):
        if DEBUG_OID_ORG_MAP:
            print 'ADD      %s  (%s)' % (oid, name)

        self._id_name_map[oid] = name
        self._name_id_map[name] = oid

    def get_id_org(self, oid):
        return self._id_name_map.get(oid, '')

    def get_org_id(self, org_name):
        return self._name_id_map.get(org_name, '')

    def is_known_org(self, org_name):
        return org_name in self._name_id_map

    def show_oid_map(self):
        print '----------------------'
        pprint.pprint(self._id_name_map)
        print '----------------------'
        pprint.pprint(self._name_id_map)


def trace_oid_tree(oid_tree, callback):
    assert callable(callback)
    callback(oid_tree['oid'], oid_tree['name'])

    for child in oid_tree.get('children', []):
        trace_oid_tree(child, callback)


def build_oid_org_map(oid_tree_json):
    oo_map = OidOrgMap()

    with open(oid_tree_json) as fp:
        oid_tree = json.load(fp)
        trace_oid_tree(oid_tree, oo_map.add_org)

    if DEBUG_OID_ORG_MAP:
        oo_map.show_oid_map()

    return oo_map


def self_test():
    oid_tree_json = 'raw_data/oid.tree.lite.json'

    oo_map = build_oid_org_map(oid_tree_json)
    assert isinstance(oo_map, OidOrgMap)

    oo_map.show_oid_map()


if __name__ == '__main__':
    DEBUG_OID_ORG_MAP = True
    self_test()
