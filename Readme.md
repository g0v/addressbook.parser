## Taiwan government addressbook

provided organization contact of government

![addressbook on travis-ci](https://travis-ci.org/g0v/addressbook.png)

## Status

this project is in alpha

## Useage

* clone project

        $ git clone https://github.com/g0v/addressbook.git

* list all government tree

        $ python show_oid_shelve.py raw_data/oid_shelve.db

* demo tree

    use browser to open it

        $ open front-end.html

## Documents

* [政府公開通訊錄](http://hack.g0v.tw/kuansim/g6v6MpyacFb)
* [我打了電話](http://hack.g0v.tw/kuansim/HM8MBTIU8Pp)
* [Wiki of g0v/addressbook](https://github.com/g0v/addressbook/wiki)

## Raw data

    raw_data/
    |-- oid.all.tree.json <!-- full tree struct from oid.nat.gov.tw -->
    |-- oid.nat.gov.tw.json <!-- full data from oid.nat.gov.tw -->
    |-- oid.nat.gov.tw.popolo.org.json <!-- full data of popolo from oid.nat.gov.tw -->
    |-- oid.raw-2.16.886.101.90010.data <!-- unit test case data of oid.nat.gov.tw -->
    |-- oid.tree.lite.json              <!-- tree of taiwan government (lite version) -->
    |-- oid_shelve.db                   <!-- source data of oid.nat.gov.tw -->
    `-- orgcode.txt                     <!-- another oid code list -->

## Deploy data

```
$ npm install firebase-import
$  ./node_modules/firebase-import/bin/firebase-import.js -j raw_data/oid.nat.gov.tw.popolo.org.json -f g0v-who.firebaseio.com
```

## License

### data

CC-0

### code

MIT <http://g0v.mit-license.org/>
