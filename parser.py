import urllib2 as url
import re
from csv import reader

def main():
    infoURL = 'http://oid.nat.gov.tw/infobox1/personmain.jsp'

    # query data from infoURL
    response = url.urlopen(infoURL)

    info = response.info()
    if _is_big5_charset(info.plist):
        web_data = response.read().decode('big5')
    else:
        web_data = response.read()

    # parser data inside NextLevel tag
    # NextLevel(\'l=\u9ad8\u96c4\u5e02,c=TW\',2,\'\u9ad8\u96c4\u5e02\')
    requestList = []
    for line in re.findall(r'NextLevel\((.*?)\)', web_data, re.M):
        utf_line = line.encode('utf-8')
        if __debug__:
            print "input %s: %s" % (type(utf_line), utf_line)
        requestList.append(utf_line)

    # remove first one, that is not data
    del requestList[0]

    # get strcut
    # sDn, sLevel, sTitle
    questList = []
    for line in reader(requestList, delimiter=',', quotechar='\''):

        dict = {}

        # decode o=abcd,c=TW or l=abcd,c=TW
        for params in line[0].split(','):
            for foo in re.findall(r'(\w)=(.*)', params, re.M):
                dict[foo[0]] = foo[1]

        dict['sLevel'] = line[1]
        dict['sTitle'] = line[2]

        questList.append(dict)

        if __debug__:
            print dict

    return questList


def _is_big5_charset(plist):
    assert isinstance(plist, list)

    big5_set_list = ['big5', 'ms950', 'cp950']
    re_pat = re.compile('charset=(?P<CODE>\S*)')

    for item in plist:
        m = re_pat.match(item)
        if not m:
            continue

        if m.group('CODE').lower() not in big5_set_list:
            continue

        return True
    return False

if __name__ == '__main__':
    questList = main()

    if __debug__:
        print (len(questList), questList)


# request to http://oid.nat.gov.tw/infobox1/personmain.jsp
# parameter sTitle sDn sLevel sDn

# save data use OID

# misc
# [l.split(',') for l in re.findall(r'showdata\((.*?)\)', data, re.M)]
