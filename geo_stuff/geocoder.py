import sys
from optparse import OptionParser
import json
import urllib2

def __url_quote__(input_str):
    return urllib2.quote(input_str.replace('.',''))
    
    
class Geocoder(object):
    
    __osm_url_base__ = "http://open.mapquestapi.com/nominatim/v1/search.php?q="
    __osm_url_params__ = "&format=json"

    def get_location_by_address(self, address):
        """Returns ((lat, lon), details) for <address>."""
        url = urllib2.os.path.join(self.__osm_url_base__, __url_quote__(address), self.__osm_url_params__)
        request = urllib2.Request(url) 
        opener = urllib2.build_opener()
        try:
            resp = json.loads(opener.open(request).read())[0]
            return ((float(resp['lat']), float(resp['lon'])), resp)
        except IndexError, e:
            return (None, None)
        
        
        
def main(args):
    usage = 'usage: %prog <address> \n' +\
            'Example: %prog "55 Northern Ave Boston MA"'

    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Fetch addresses instead of (lat, lon)")
    (options, args) = parser.parse_args()

    if len(args) is not 1:
        parser.print_help()
        sys.exit(1)

    address = args[0]

    geocoder = Geocoder()

    print 'Getting location by address for: %s' % address
    lat_lon, details = geocoder.get_location_by_address(address)
    
    print lat_lon
    if options.verbose:
        print details


if __name__ == '__main__':
    main(sys.argv)