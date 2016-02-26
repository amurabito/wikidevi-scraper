#!/usr/bin/python
# wikidevi.py
# v.51 - Poland Springs

import simplemediawiki
from sys import argv

def main():

    wiki = init()
    targetAP = searchForAP(wiki)
    chosenAP = querySpecificPage(wiki, targetAP)
    if chosenAP:
        formatAndPrint(chosenAP)

def init():
    wiki = simplemediawiki.MediaWiki('https://wikidevi.com/w/api.php')
    simplemediawiki.build_user_agent("wikidevi-scraper", ".51", "gitlab.com/admo")
    return wiki


def searchForAP(wiki):

    if len(argv) > 1:
        model = str(argv[1])
    else:
        print "\n\nEnter an Access Point: (or type quit)"
        model = raw_input()

    if 'quit' in model:
        print "thank you for playing!"
        exit(0)

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
    elif totalhits > 20:
        print "over 20 results found, be more specific"
        model = None
    elif totalhits > 1:
        print "more than one found, here are your options: \n"
        i = 1
        searchResults = {}
        for item in results.get('search'):
            if not "REDIRECT" in item['snippet']:
                print str(i) + ":\t" + item['title']
                i += 1
                searchResults.update(item)
                # the bug here is that when we hit a redirect, it causes an off by one error.
                # it's still part of the results.get search result.
        print '\n please select the hardware rev'
        response = raw_input()
        model = results.get('search')[int(response) - 1]['title']
        model = searchResults.get('search')[int(response) - 1]['title']
    else:
        print "nothing found"
        model = None
    return model


def querySpecificPage(wiki, model):
    if model:
        # pull up the model if we have
        values = {'action': 'query',
                  'titles': model,
                  'prop': 'revisions',
                  'rvprop': 'content',
                  'format': 'json'}
        response = wiki.call(values)
        #print response
        return response
    return False

def formatAndPrint(model):
    accessPoint = model['query']['pages']
    temp = str(accessPoint).partition("{{")[2].rpartition("}}")[0].split("\\n")

    # full details, TODO - key off of DEBUG enabled
    #for property in temp:
    #    print property

    # print a summary of key metrics

    keyMetrics = ["|brand", "|model", "revision", "country", "|type", "fcc_id", "cpu1_brand", "cpu1_model", "ram1_brand", "ram1_model", "wi1", "wi2", "lan", "802dot11", "default", "oui"]

    print "Access Point Summary:"
    for item in temp:
        if any(metrics in item for metrics in keyMetrics):
            if not (item.endswith("=") or item.endswith("}}")):
                print item
            continue

if __name__ == "__main__":
    main()
