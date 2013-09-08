import shelve
import sys

def walk(d, level):
    for i in d.keys():
        print '\t'*level + "%s - %s" % (eval(i)[0], eval(i)[1])
        walk(d[i], level+1)

def main(f):
    oid = shelve.open(f)['oid']
    walk(oid, 0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: ./%s <oid_shelve file>" % (sys.argv[0])
        sys.exit(-1)

    main(sys.argv[1])

