import urllib2 as url
import re

infoURL = 'http://oid.nat.gov.tw/infobox1/personmain.jsp'
data = url.urlopen(infoURL).read().decode('big5')
requestList = []
for l in re.findall(r'NextLevel\(\'(.*?)\'\)', data, re.M):
    requestList.append(l.split(','))
    if __debug__:
        print l.split(',')

# get strcut
# sDn, sLevel, sTitle

# request to http://oid.nat.gov.tw/infobox1/personmain.jsp
# parameter sTitle sDn sLevel sDn

# save data use OID

# [l.split(',') for l in re.findall(r'showdata\((.*?)\)', data, re.M)]
