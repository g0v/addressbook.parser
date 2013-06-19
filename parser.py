import urllib2 as url
import re
from csv import reader

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

# remove first one, that is not data
del requestList[0]

# get strcut
# sDn, sLevel, sTitle
questList = []
for tuple in reader(requestList, delimiter=',', quotechar='\''):

    dict = {}
    for foo in re.findall( '(\w)=(.*)',tuple[0].split(',')[0], re.M):
        dict[foo[0]] = foo[1]

    dict['sLevel'] = tuple[1]
    dict['sTitle'] = tuple[2]

    questList.append(dict)

    if __debug__:
        print dict


if __debug__:
    print (len(questList), questList)

# request to http://oid.nat.gov.tw/infobox1/personmain.jsp
# parameter sTitle sDn sLevel sDn

# save data use OID

# misc
# [l.split(',') for l in re.findall(r'showdata\((.*?)\)', data, re.M)]
