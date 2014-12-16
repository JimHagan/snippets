#!/usr/bin/env python

"""
* PyBingMaps 0.1
* Drew Volpe <drew@dewdrops.net>
*
"""

import json
from optparse import OptionParser
import sys

import urllib2

# Drew's Bing Keys
BING_KEY = 'AhmsvXAX7bYHzAwQ0kQxUL0YzUm4mTN52JhfOn6MdiHjBpUvFwjh1-ZkObPGK9C2' # for virtual earth
BING_APP_ID = 'CC8A1C24BB17FEADE4E1CD5C794074481468A2F8' # for live.net


def __url_quote__(input_str):
    return urllib2.quote(input_str.replace('.',''))



class BingAPI:

    __ve_url_base = 'http://dev.virtualearth.net/REST/v1/Locations'
    __live_url_base = 'http://api.search.live.net/json.aspx?'

    def __init__(self, bing_key):
        self._bing_key = bing_key

    def __get_response_from_url__(self, url):
        request = urllib2.Request(url)
        request.add_header('User-Agent','PyBing - Mozilla/1.0 compatible')
        opener = urllib2.build_opener()
        resp = json.loads(opener.open(request).read())
        resourceSets = resp["resourceSets"]
        resources = resourceSets[0]["resources"][0]
        point = resources['point']['coordinates']
        return point, resources

    def get_location_by_address(self, address, city, state):
        """ Given an address, returns a (lat, lon) pair and a dict of resources """
        state = __url_quote__(state)
        city = __url_quote__(city)
        address = __url_quote__(address)
        url = self.__ve_url_base + '/US/%s/%s/%s?key=%s' % (state, city, address, self._bing_key)
        return self.__get_response_from_url__(url)

    def get_location_by_point(self, lat, lon):
        """ Given a point, returns a (lat, lon) pair and a dict of resources """
        url = self.__ve_url_base + '/%s,%s?key=%s' % (lat, lon, BING_KEY)
        return self.__get_response_from_url__(url)

    def local_business_search(self, search_term, lat, lon):
        url = self.__live_url_base + 'Appid=%s&query=%s&sources=Phonebook' %\
                                     (BING_APP_ID, search_term)

    

def main(args):

    usage = 'usage: %prog <address> <city> <state> \n' +\
            'Example: %prog "55 Northern Ave" Boston MA'

    parser = OptionParser(usage)
    (options, args) = parser.parse_args()

    if len(args) is not 3:
        parser.print_help()
        sys.exit(1)

    address, city, state = args

    bing_api = BingAPI(BING_KEY)

    print 'Getting location by address for: %s' % ', '.join(args)
    point, resources = bing_api.get_location_by_address(address, city, state)
    print 'Point: (%s,%s) ' % (point[0], point[1])
    print 'Resources: ' + str(resources)

    print '====='
    print 'Getting location by point for: (%s, %s) ' % (point[0], point[1])
    point, resources = bing_api.get_location_by_point(point[0], point[1])    
    print 'Point: (%s,%s) ' % (point[0], point[1])
    print 'Resources: ' + str(resources)
    
    print '====='
    print 'done'

if __name__ == '__main__':
    main(sys.argv)


