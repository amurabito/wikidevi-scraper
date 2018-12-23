#!/usr/bin/python
# wikidevi.py
# v.53 - Arrowhead

import simplemediawiki
import coloredlogs
import logger as log
from sys import argv

class APFinder(): 


    def __init__(self):
        self.wiki = simplemediawiki.MediaWiki('https://wikidevi.com/w/api.php')
        simplemediawiki.build_user_agent(
            "wikidevi-scraper", ".51", "gitlab.com/admo")
        coloredlogs.install()

    def main(self):

        targetAP = self.searchForAP()
        chosenAP = self.querySpecificPage(targetAP)
        if chosenAP:
            self.formatAndPrint(chosenAP)

    def searchForAP(self):

        if len(argv) > 1:
            model = str(argv[1])
        else:
            print "Enter an Access Point:"
            model = raw_input()

        if 'quit' in model:
            log.info("exiting.")
            exit(0)

        # search for a page containing the AP, then try to pull up the AP details
        search = {'action': 'query',
                  'list': 'search',
                  'srsearch': model,
                  'format': 'json'}

        wikiresults = self.wiki.call(search)
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
            searchResults = list()
            for item in results.get('search'):
                if "REDIRECT" not in item['snippet']:
                    print str(i) + ":\t" + item['title']
                    i += 1
                    searchResults.append(item)
            print '\n please select the hardware rev'
            response = raw_input()
            model = searchResults.__getitem__(int(response) - 1)['title']
        else:
            print "nothing found"
            model = None
        return model


    def querySpecificPage(self, model):
        if model:
            # pull up the model if we have
            values = {'action': 'query',
                      'titles': model,
                      'prop': 'revisions',
                      'rvprop': 'content',
                      'format': 'json'}
            response = self.wiki.call(values)
            # print response
            return response
        return False


    def formatAndPrint(self, model):
        accessPoint = model['query']['pages']
        temp = str(accessPoint).partition("{{")[2].rpartition("}}")[0].split("\\n")

        # full details, TODO - key off of DEBUG enabled
        # for property in temp:
        #    print property

        # print a summary of key metrics

        keyMetrics = ["|brand", "|model", "revision", "country", "|type",
                      "fcc_id", "cpu1_brand", "cpu1_model", "ram1_brand",
                      "ram1_model", "wi1", "wi2", "lan", "802dot11",
                      "default", "oui"]

        print "Access Point Summary:"
        for item in temp:
            if any(metrics in item for metrics in keyMetrics):
                if not (item.endswith("=") or item.endswith("}}")):
                    print item
                continue

if __name__ == "__main__":
    wikidevi = APFinder()
    wikidevi.main()