#!/usr/bin/env lsc

Firebase = require 'firebase'
optimist = require 'optimist'

fs = require 'fs'
path = require 'path'


argv = require('optimist')
  .usage('Usage: $0')

  .demand('firebase_url')
  .describe('firebase_url', 'Firebase URL (e.g. https://test.firebaseio.com/).')
  .alias('f', 'firebase_url')

  .demand('json')
  .describe('json', 'The JSON file to import.')
  .alias('j', 'json')

  .argv


file = path.resolve argv.json
fs.readFile file, 'utf8', (error, raw) ->
   if error
      console.log "Error: #{error}"
      return

   data = []
   [data."#{o.id}" = o for o in JSON.parse raw]

   ## upload to Firebase
   orgRef = new Firebase argv.firebase_url
   orgRef.set data, (error) ->
      if error
         console.log "Error: #{error}"

      console.log "Upload complete"
      process.exit if error then 1 else 0
