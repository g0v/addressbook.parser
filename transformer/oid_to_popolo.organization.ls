#!/usr/bin/env lsc
# -*- coding: utf-8 -*-

fs = require 'fs'
uuid = require 'node-uuid'
optimist = require 'optimist'
path = require 'path'

# Check command-line arguments
#
argv = require('optimist')
  .usage('must specify path for json file to be transformed.
  $0')

  .demand('input_file')
  .describe('input_file', 'The JSON file to transformed.')
  .alias('i', 'input_file')

  .describe('source_file', 'The old JSON file to find old data.')
  .alias('s', 'source_file')

  .demand('output_file')
  .describe('output_file', 'Output JSON path.')
  .alias('o', 'output_file')

  .argv

source_data = ""
o = path.resolve argv.source_file
if fs.existsSync o
    source_data := JSON.parse fs.readFileSync o, 'utf8'

checkByOID = ->
    for x in source_data
        ids = x.identifiers
        for id in ids
           if id.schema is "OID" and id.identitfier is it
                # console.log "Found old #{id.schema} is #{id.identitfier}"
                return x.id
    return uuid.v1

file = argv.input_file
# Parse JSON file
#
fs.readFile file, 'utf8', (err, raw) ->
    if err
        console.log "error: #{error}"
        return

    raw = JSON.parse raw
    data = []
    map = {}
    # index = 0

    for x in raw
        name = x.機關名稱
        parent = x.上層機關
        oid = x.機關OID
        org =
            id: checkByOID oid
            name: name
            other_names: []
            identifiers: []
            classification: "Organization"
            parent_id: ""
            founding_date: ""
            dissolution_date: ""
            image: ""
            contact_details: []
            links: []
            "@context": label_zh: "@id": "rdfs:label", "@language": "zh"

        if parent != ""
            last = ""
            ancestors = parent.split "＼"
            org.parent_id = ancestors[ancestors.length - 2]
            # console.log "parent: #{parent}, #{ancestors[ancestors.length - 2]}"
        else
            org.parent_id = ""

        map[name] = org

        data.push org
        org.identifiers =
            * "schema": "Distinguished Name", "identitfier": x.機關DN
            * "schema": "OID"               , "identitfier": oid
        org.contact_details =
            * label_zh: "機關電話"  , type: "voice"      , value: x.機關電話, source: ""
            * label_zh: "機關傳真"  , type: "tax"        , value: x.機關傳真, source: ""
            * label_zh: "機關網址"  , type: "url"        , value: x.機關網址, source: ""
            * label_zh: "機關地址"  , type: "address"    , value: x.機關地址, source: ""
            * label_zh: "郵遞區號"  , type: "postcode"   , value: x.郵遞區號, source: ""
            * label_zh: "機關代號"  , type: "uid"        , value: x.機關代號, source: ""
            * label_zh: "機關email" , type: "email"      , value: x.機關email, source: ""

    for x in data
        if x.parent_id != ""
            x.parent_id = map[x.parent_id].id

    fs.writeFileSync argv.output_file,
                     JSON.stringify data, null, 4
