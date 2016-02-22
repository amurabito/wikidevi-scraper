# wikidevi.py
# can't think of a better name for now

import simplemediawiki

wiki = simplemediawiki.MediaWiki('https://wikidevi.com/w/api.php')

simplemediawiki.build_user_agent("AP_GRABBER", ".5", "gitlab.com/admo")

print "Enter an AP model: "
model = raw_input()

# search for a page containing the AP, then try to pull up the AP details
search = {'action': 'query',
          'list': 'search',
          'srsearch': model,
          'format': 'json'}

wikiresults = wiki.call(search)
results = wikiresults.get('query')
totalhits = results.get('searchinfo').get('totalhits')


# for the simple case, we have only 1 match to the search query
if totalhits == 1:
    model = results.get('search')[0]['title']
elif totalhits > 10:
    print "over 10 results found, be more specific"
    model = None
elif totalhits > 1:
    print "more than one found, here are your options: \n"
    i = 1
    for item in results.get('search'):
        if not "REDIRECT" in item['snippet']:
            print str(i) + ":\t" + item['title']
            i += 1
    print 'please type the number of the model'
    response = raw_input()
    model = results.get('search')[i-1]['title']
else:
    print "nothing found"
    model = None

if model:
    # pull up the model if we have it
    values = {'action': 'query',
              'titles': model,
              'prop': 'revisions',
              'rvprop': 'content',
              'format': 'json'}
    response = wiki.call(values)

    print response

