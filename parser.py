import urllib2 as url
import re
import csv

infoURL = 'http://oid.nat.gov.tw/infobox1/personmain.jsp'

# query data from infoURL
data = url.urlopen(infoURL).read().decode('big5')

# parser data inside NextLevel tag
# NextLevel(\'l=\u9ad8\u96c4\u5e02,c=TW\',2,\'\u9ad8\u96c4\u5e02\')
requestList = []
for line in re.findall(r'NextLevel\((.*?)\)', data, re.M):
    utf_line = line.encode('utf-8')
    if __debug__:
        print "input %s: %s" % (type(utf_line), utf_line)
    requestList.append(utf_line)

# get strcut
# sDn, sLevel, sTitle
parameter = {}
for tuple in csv.reader(requestList, delimiter=',', quotechar='\''):
    # if __debug__:
    #     print tuple
    parameter.setdefault('sDn', tuple[0])
    parameter.setdefault('sLevel', tuple[1])
    parameter.setdefault('sTitle', tuple[2])

if __debug__:
    print parameter

# request to http://oid.nat.gov.tw/infobox1/personmain.jsp
# parameter sTitle sDn sLevel sDn

# save data use OID

# misc
# [l.split(',') for l in re.findall(r'showdata\((.*?)\)', data, re.M)]
