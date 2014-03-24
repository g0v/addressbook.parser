## Taiwan government addressbook

provided organization contact of government

![addressbook status on travis-ci](https://travis-ci.org/g0v/addressbook.parser.png?branch=master)


## Status

this project is in alpha

## Useage

* clone project

        $ git clone https://github.com/g0v/addressbook.parser.git

* list all government tree

        $ python show_data/show_oid_shelve.py raw_data/oid_shelve.db

* demo tree

    * use browser to open it

        $ open demo/front-end.html

    * [demo link at github io](http://g0v.github.io/addressbook.parser/)

## Documents

* [政府公開通訊錄](http://hack.g0v.tw/kuansim/g6v6MpyacFb)
* [我打了電話](http://hack.g0v.tw/kuansim/HM8MBTIU8Pp)
* [Wiki of g0v/addressbook](https://github.com/g0v/addressbook.parser/wiki)

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
$ npm install firebase optimist
$ ./org-to-firebase.ls -j raw_data/oid.nat.gov.tw.popolo.org.json -f https://g0v-org.firebaseio.com/org/
```

## License

### data

CC-0

### code

MIT <http://g0v.mit-license.org/>
