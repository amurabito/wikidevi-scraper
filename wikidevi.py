# wikidevi.py
# can't think of a better name for now

import urllib
import urllib2
import simplejson
import sqlite3
import wikipedia

#wikipedia.API_URL = url
url = 'http://wikidevi.com/w/api.php'
#url = 'http://en.wikipedia.org/w/api.php'

print "Enter an AP model: "
model = raw_input()

model = "Linksys_E2000"
model = "Barack"

# need to try to search this query, and see what responses we have


values = {'action' : 'query',
          'prop' : 'revisions',
          'titles' : model,
          'rvprop' : 'content',
          'format' : 'json'}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
json = response.read()

print json
