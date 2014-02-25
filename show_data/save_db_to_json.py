#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import shelve
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def walk(d, level, output):
    for i in d.keys():
        if __debug__:
            print '\t'*level + "%s - %s" % (eval(i)[0], eval(i)[1])

        nl = eval(i)[0]
        sd = eval(i)[1]

        one_data = {}
        one_data.setdefault('NextLevelValue', nl)
        one_data.setdefault('ShowDataValue', sd)
        one_data.setdefault('children', [])

        walk(d[i], level+1, one_data['children'])

        # don't show empty children
        if len(one_data['children']) == 0:
            one_data.pop("children", None)

        output.append(one_data)



def main(f, o):
    oid = shelve.open(f)['oid']

    data = {}
    data.setdefault('oid', [])

    walk(oid, 0, data['oid'])

    with codecs.open(o, 'w', 'utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: ./%s <oid_shelve file> <json_output file>" % sys.argv[0]
        sys.exit(-1)

    main(sys.argv[1], sys.argv[2])
