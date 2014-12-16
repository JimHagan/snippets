import json
from optparse import OptionParser
import sys
import time

import urllib2

from caliper.base.point import POI
from caliper.renderers.poi_renderer import pois_to_kml


class FoursquareAPI:
    """ Object for working with the Foursquare API """

    # Drew's key
    DREW_CLIENT_ID = 'QIWHSAOQ2LEFCLCIIAQIKTCHG0XXX403T4KSD2TP5JDQGCA4'
    DREW_CLIENT_SECRET = 'EUIL5TGGA1G1UYFHSFH53NKUDHLNZDRV2X4CNO4WHOMXUHM1'
    # Jeff's keys
    JEFF_CLIENT_ID = 'LQ4UZAGHSGS5KPGOV1K5BEMPMHWXOMSOQFATX5KXNELBI5V1'
    JEFF_CLIENT_SECRET = 'FMJVUOXUHUKY3EXCSO4LNVG5QBMH01KJTJ4YTJNJ3BRP5ALJ'
    
    VERSION = '20130104' # is valid as of 04/11/2014
    
    url_base = 'https://api.foursquare.com/v2'

    def __init__(self, client_id=JEFF_CLIENT_ID, client_secret=JEFF_CLIENT_SECRET, version=VERSION):
        self.client_id = client_id
        self.client_secret = client_secret
        self.version = version
        
    def __get_response_from_url(self, url, max_retries=0):
        retry_count = 0
        while retry_count < max_retries:
            try:
                url = url + '&client_id=%s&client_secret=%s&v=%s' % (self.client_id, self.client_secret, self.version)
                request = urllib2.Request(url)
                request.add_header('User-Agent', 'PyFoursquare - Mozilla/1.0 compatible')
                opener = urllib2.build_opener()

                response = json.loads(opener.open(request).read())
# print 'got response. meta: %s ' % response.get('meta')
# print 'response: %s ' % response
                return response.get('response')

            except urllib2.URLError, e:
                print '=' * 10
                print 'URLError: %s' % e
                print 'url: %s' % url
                retry_count += 1
                if retry_count > max_retries: 
                   raise e
                print 'sleeping until retry..'
                time.sleep(2 ** retry_count)  # back off increasingly more

    def __response_to_venue_dicts(self, response):
        items = response['venues']
        venues = []
        for item in items:
            v = self.__item_to_venue_dict(item)
            venues.append(v)
        return venues

    def __item_to_venue_dict(self, item_dict):
        """ flattens and cleans up an item dict """
        v = {}
        v['name'] = item_dict['name']
        v['verified'] = item_dict['verified']
        v['id'] = item_dict['id']
        if item_dict['categories']:
            v['category'] = item_dict['categories'][0]['name']
        loc = item_dict['location']
        if loc:
            keys = ['lat', 'lng', 'distance', 'address', 'city', 'state', 'postalCode']
            for k in keys:
                v[k] = loc.get(k)
        stats = item_dict['stats']
        if stats:
            v['checkinsCount'] = stats['checkinsCount']
            v['usersCount'] = stats['usersCount']
        return v

    #
    # Public methods
    #
    def get_venues(self, lat, lon, query_term='', category_id='', distance=0, max_retries=0):
        """ returns list of venues (dicts) near the given point """
        params = 'll=%s,%s' % (lat, lon)
        if query_term:
            params = params + '&query=%s' % urllib2.quote(query_term)
        if category_id:
            params = params + '&categoryId=%s' % category_id
        url = self.url_base + '/venues/search?' + params
        resp = self.__get_response_from_url(url, max_retries=max_retries)
        venues = self.__response_to_venue_dicts(resp)
        if distance > 0:
            venues = [v for v in venues if float(v['distance']) < distance]
        return venues

    def get_closest_venue(self, lat, lon, query_term='', category_id='', distance=0, max_retries=0):
        """ Returns dict of the venue closests to the given point """
        results = self.get_venues(lat, lon, query_term=query_term, category_id=category_id,
                                  distance=distance, max_retries=max_retries)
        best_result = None
        cur_best_dist = sys.maxint
        for result in results:
            dist = int(result['distance'])
            if dist < cur_best_dist:
                best_result = result
                cur_best_dist = dist
        return best_result


def venue_to_poi(venue_dict):
    info_str = 'verified:' + ('True' if venue_dict['verified'] else 'False') +\
        ' checkins:%s' % venue_dict['checkinsCount']
    return POI(info_str, venue_dict['name'], venue_dict.get('address'), venue_dict['city'],
           venue_dict['state'], venue_dict['postalCode'],
           float(venue_dict['lat']), float(venue_dict['lng']), 0.0, venue_dict.get('category'),
           '', '')


def do_foursquare(args):

    usage = 'usage: %prog lat,lon \nExample: 42.169002,-71.183167 --query=walmart'

    parser = OptionParser(usage)
    parser.add_option('--query', dest='query', help='Search term.')
    parser.add_option('--category-id', dest='category_id', help='Foursquare cat id (NOT name)')
    parser.add_option('--output-kml', dest='is_kml', action="store_true", help='Print results as kml')
    parser.add_option('--distance', dest='distance', help='Max dist (m) venue can be from point.')
    (options, args) = parser.parse_args()
    distance = 0
    if options.distance:
        distance = float(options.distance)

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)
    lat_str, lon_str = args[0].split(',')

    foursquare_api = FoursquareAPI()
    venues = foursquare_api.get_venues(float(lat_str), float(lon_str), query_term=options.query,
                                       category_id=options.category_id, distance=distance)
    if not options.is_kml:
        for v in venues:
            print 'v: %s ' % v
        print 'done.'
        sys.exit(0)

    # create POIs and print KML
    pois = []
    for v in venues:
        pois.append(venue_to_poi(v))
    print(pois_to_kml(pois))


if __name__ == '__main__':
    do_foursquare(sys.argv)
