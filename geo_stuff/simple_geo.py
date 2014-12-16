#!/usr/bin/env python

from optparse import OptionParser
import time
import sys

import simplegeo.places as places
import oauth2 as oath

# Drew's simpleGeo API
__OAUTH_TOKEN__ = "2e5T9qZVwPacupLXk2Yqv8bYJ3BcqZKT"
__OAUTH_SECRET__ = "VBbG5ufsDZzxTREg3aEH68pny7wtf9va"


def row_from_properties(props):
    name = props.get('name', '')
    distance = str(props.get('distance', ''))
    subcategory = ''
    if props.get('classifiers'):
        subcategory = props['classifiers'][0].get('subcategory', '')
    address = props.get('address', '')
    city = props.get('city', '')
    province = props.get('province', '')
    return [name, distance, address, city, province, subcategory]

def local_category_search(category, lat, lon, radius_m):
    time.sleep(0.2) # play nice with server

    """ Returns a list of places which match the given category. Sorted by
        order from the given lat, lon """
    radius_km = radius_m / 1000
    if radius_km < 1:
        radius_km = 1
    client = places.Client(__OAUTH_TOKEN__, __OAUTH_SECRET__)
    results = client.search(float(lat), float(lon), category=category, radius=radius_km)

    print '====='
    print 'Results: %s' % results
    if results:
        for r in results:
            print str(r.coordinates)
            print 'as row %s' % row_from_properties(r.properties)
    return results
    
def main(args):

    parser = OptionParser(usage="Usage: %prog")
#    options, args = parser.parse_args()
#    if len(args) != 3:
#        parser.print_help()
#        sys.exit(1)

    term, lat, lon = 'Movie', '35.91268', '-78.936403'
    print 'local search: %s, %s, %s' % (term, lat, lon)
    local_category_search(term, lat, lon, 2000)

    
if __name__ == '__main__':
    main(sys.argv)
