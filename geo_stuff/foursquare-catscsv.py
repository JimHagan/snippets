#!/usr/bin/env python

import csv
import json
from optparse import OptionParser
import sys
import urllib
import urllib2

FOURSQUARE_MATT_CLIENT_ID = 'LHJVGDY0Q34VBBVBZGOBJIR0STGXQFM1INU2Y24XIDWSKKVV'
FOURSQUARE_MATT_CLIENT_SECRET = '54XOYGESDKE0SH0JK25PFSXMTAKBXZ2DOS0FGQBTP3FW21O3'

def call_foursquare_api(url, parms):
    parms['client_id'] = FOURSQUARE_MATT_CLIENT_ID
    parms['client_secret'] = FOURSQUARE_MATT_CLIENT_SECRET
    parms_encoded = urllib.urlencode(parms)
    req = urllib2.Request(url + '?' + parms_encoded)
    print 'Making request to:', req.get_full_url()
    f = urllib2.urlopen(req)
    responseJson = json.loads(f.read())
    assert responseJson['meta']['code'] == 200
    return responseJson['response']

def print_foursquare_categories():
    def print_category(cat, level):
        print '   ' * level + '%s (%s)' % (cat.get('name'), cat.get('id'))
        for c in cat.get('categories', []):
            print_category(c, level+1)

    url = 'https://api.foursquare.com/v2/venues/categories'
    parms = { 'v': '20110405' }  # Without explicitly passing version, API doesn't return IDs for top-level categories
    resp = call_foursquare_api(url, parms)
    cats = resp['categories']
    for cat in cats:
        print_category(cat, 0)

def venue_search(lat, lon, radius, search_term=None, category_id=None):
    if search_term and category_id:
        raise Exception("Don't pass BOTH search_term and category_id; the API ignores search_term if we pass a category_id")

    url = 'https://api.foursquare.com/v2/venues/search'
    parms = { 'll': '%f,%f' % (lat, lon),
              # Foursquare says this radius 'does not currently affect search results'
              'llAcc': '%i' % radius,
              # Cuts me off at 50 results regardless of what I set this to
              'limit': '200',
#             'intent': 'match',  # NO venues get returned when I use 'match'
            }
    if search_term:
        parms['query'] = search_term
    if category_id:
        # If we pass a category ID, the API **ignores** what we send for the 'query'
        parms['categoryId'] = category_id  # Foursquare says this is 'experimental' and will not work with 'intent'

    resp = call_foursquare_api(url, parms)
    
    # It returns multiple groups of venues: e.g., a 'trending' group and a 'nearby' group.
    group_types_to_num_venues = {}
    for group in resp['groups']:
        group_types_to_num_venues[group['type']] = group['items']
    print 'Group type (num venues)'
    for type in group_types_to_num_venues.keys():
        print '   %s (%i)' % (type, len(group_types_to_num_venues[type]))
    
    # If we've searched using the 'query' parm, then the 'places' group type is returned and is what we care about
    # If we've searched WITHOUT using the 'query' parm, then the 'nearby' group type is returned and is what we care about
    assert (search_term and 'places' in group_types_to_num_venues) or \
           (not search_term and 'nearby' in group_types_to_num_venues)

    # We shouldn't have both 'places' and 'nearby' group types
    assert (not ('places' in group_types_to_num_venues and 'nearby' in group_types_to_num_venues))

    # The returned_venues are those venues that are in the group type that we care about ('places' or 'nearby')
    returned_venues = []
    for group in resp['groups']:
        if group['type'] in ('places', 'nearby'):
            returned_venues = group['items']
            break

    pois = []
    if returned_venues:
        for venue in returned_venues:
            poi = (venue.get('name', ''),
                   venue.get('id', ''),
                   str(venue.get('location').get('lat', '0.0')),
                   str(venue.get('location').get('lng', '0.0')),
                   str(venue.get('location').get('distance', '0')),
                   venue.get('location').get('address', ''),
                   venue.get('location').get('city', ''),
                   venue.get('location').get('state', ''),
                   venue.get('location').get('postalCode', ''),
                   str(venue.get('verified', '')),
                   ' '.join(cat.get('name') for cat in venue.get('categories')),
                   str(venue.get('stats').get('checkinsCount', 0)),
                   str(venue.get('stats').get('usersCount', 0)))
            poi_utf8 = tuple(p.encode('UTF-8') for p in poi)
            pois.append(poi_utf8)
    
    return pois

def write_pois_to_csv(pois, filename):
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Name', 'ID', 'Lat', 'Lon', 'Distance', 'Address', 'City', 'State',
                             'Zip', 'Verified', 'Categories', '# Checkins', '# Users'])
        for poi in pois:
            csv_writer.writerow(poi)

if __name__ == '__main__':
    parser = OptionParser(usage="Usage: %prog [options] <lat,lon> <radius> <output_filename>")
    parser.add_option('--search_term', dest='search_term', help='search term')
    parser.add_option('--category_id', dest='category_id', help='category ID')
    options, args = parser.parse_args()
    if len(args) != 3:
        parser.print_help()
        sys.exit(1)
    lat, lon = args[0].split(',')
    radius = args[1]
    output_filename = args[2]
    pois = venue_search(float(lat), float(lon), float(radius), options.search_term, options.category_id)
    write_pois_to_csv(pois, output_filename)

# ./foursquare.py 39.991851,-83.007889 35000 --search_term=walmart results/frankoh-walmart.csv
# ./foursquare.py 33.031693,-116.872559 80000 --search_term=walmart results/sandieg-walmart.csv
# ./foursquare.py 37.455238,-122.194061 45000 --search_term=walmart results/santacl-walmart.csv
# ./foursquare.py 42.364379,-71.054935 45000 --search_term=walmart results/boston-walmart.csv
# ./foursquare.py 36.165597,-86.785126 50000 --search_term=walmart results/nash-walmart.csv
# ./foursquare.py 33.448430,-112.074337 40000 --search_term=walmart results/phoe-walmart.csv

# ./foursquare.py 42.364379,-71.054935 45000 --search_term=starbucks results/boston-starbucks.csv

# ./foursquare.py 39.991851,-83.007889 35000 --category_id=4bf58dd8d48988d17f941735 results/frankoh-movies.csv
# ./foursquare.py 33.031693,-116.872559 80000 --category_id=4bf58dd8d48988d17f941735 results/sandieg-movies.csv
# ./foursquare.py 37.455238,-122.194061 45000 --category_id=4bf58dd8d48988d17f941735 results/santacl-movies.csv
# ./foursquare.py 42.364379,-71.054935 45000 --category_id=4bf58dd8d48988d17f941735 results/boston-movies.csv
# ./foursquare.py 36.165597,-86.785126 50000 --category_id=4bf58dd8d48988d17f941735 results/nash-movies.csv
# ./foursquare.py 33.448430,-112.074337 40000 --category_id=4bf58dd8d48988d17f941735 results/phoe-movies.csv

# These both only return two Wal-Marts -- so apparently there's an (undocumented) max-radius cutoff
# ./foursquare.py 39.5,-95.6 2500000 --search_term=walmart results/us-walmart.csv
# ./foursquare.py 39.5,-95.6 25000 --search_term=walmart results/us-walmart2.csv
