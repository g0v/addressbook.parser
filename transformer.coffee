#!/usr/bin/env coffee
# -*- coding: utf-8 -*-

fs = require 'fs'
file = process.argv[2]
uuid = require 'node-uuid'

# Check command-line arguments
#
if !file
    console.log """must specify path for json file to be transformed.
        transform.coffee [json file]
    """
    process.exit 1


# Parse JSON file
#
fs.readFile file, 'utf8', (err, raw) ->
    if (err)
        console.log "error: #{error}"
        return

    raw = JSON.parse raw
    data = []
    map = {}
    # index = 0

    for x in raw
        name = x.機關名稱
        parent = x.上層機關
        org =
            id: do uuid.v1
            # id: "#{index++}"
            # ref: x
            name: name
            other_names: []
            identifiers: []
            classification: "Organization"
            parent_id: ""
            founding_date: ""
            dissolution_date: ""
            image: ""
            contact_details: []

        if parent != ""
            last = ""
            ancestors = parent.split "＼"
            org.parent_id = ancestors[ancestors.length - 2]
            # console.log "parent: #{parent}, #{ancestors[ancestors.length - 2]}"
        else
            org.parent_id = ""

        map[name] = org

        data.push org
        org.identifiers.push "schema": "Distinguished Name", "identitfier": x.機關 DN
        org.identifiers.push "schema": "OID"               , "identitfier": x.機關 OID
        org.contact_details.push label: "機關電話", type: "voice"      , value: x.機關電話, source: ""
        org.contact_details.push label: "機關傳真", type: "tax"        , value: x.機關傳真, source: ""
        org.contact_details.push label: "機關網址", type: "url"        , value: x.機關網址, source: ""
        org.contact_details.push label: "機關地址", type: "address"    , value: x.機關地址, source: ""
        org.contact_details.push label: "郵遞區號", type: "postcode"   , value: x.郵遞區號, source: ""
        org.contact_details.push label: "機關代號", type: "uid"        , value: x.機關代號, source: ""
        org.contact_details.push label: "機關 email", type: "email"    , value: x.機關 email, source: ""

    for x in data
        if x.parent_id != ""
            x.parent_id = map[x.parent_id].id

    console.log "#{JSON.stringify data, null, 4}"
