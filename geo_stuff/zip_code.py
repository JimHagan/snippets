#!/usr/bin/env python
import urllib, urllib2
import re
import types
from optparse import OptionParser
import sys


def melissa_zip_plus_4(lat, lon, output_file=None):
    """ Performs a HTTP GET query to Melissa Data. Limit: 100 lookups per machine.
    Run on Amazon EC2. """    
    url = 'http://www.melissadata.com/lookups/latlngzip4.asp?'
    header = {'User-Agent': 'PyZip - Mozilla/1.0 compatible'}
    
    if type(lat) != types.StringType:
        lat = '%0.6f' % lat
        lon = '%0.6f' % lon
        
    params = {
        'lat': lat,
        'lng': lon,
        'submit1': 'Submit',
    }
    encoded_params = '&'.join(['%s=%s' %(key,value) for (key,value) in params.items()])

    query_url = url + encoded_params
    request = urllib2.Request(query_url, headers=header)
    response = urllib2.urlopen(request)
    
    output = response.read()
    
    if output_file:
        with open(output_file,'wb') as f:
            f.write(output)
            print 'File %s written.' % output_file
        
    search_zip = re.findall(r'(\d{5}-\d{4})',output)
    if search_zip:
        return search_zip[0]


def usps_zip_plus_4(address, city, state, address2='', output_file=None):
    """ USPS Zip Plus 4 lookup from an address. Pings the USPS zip4.usps.com server
    using an HTTP POST. """
    
    url = 'http://zip4.usps.com/zip4/zcl_0_results.jsp'
    header = {'User-Agent': 'PyZip - Mozilla/1.0 compatible'}
    params = {
        'visited': '1',
        'pagenumber': '0',
        'firmname': '',   
        'address2': address,
        'address1': address2,
        'city': city,
        'state': state,
        'urbanization': '',
        'zip5': '',
    }
    data = urllib.urlencode(params)
    request = urllib2.Request(url, data, headers=header)
    response = urllib2.urlopen(request)

    output = response.read()

    if output_file:
        with open(output_file,'wb') as f:
            f.write(output)
            print 'File %s written.' % output_file
            
    address = re.search(r'<td headers="full".*>\s*.*<br .>\s*(.*)\r',output)
    if address:
        city_state_zip = address.groups()[0].split('&nbsp;')
        zip = city_state_zip[-1]
    else:
        zip = re.search(r'<td headers="zip".*>\s*(.*)\r',output)
        if zip:
            zip = zip.groups()[0]
    
    return zip


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] <street>, <city>, <state>, <street2>\n" +\
                        "   where <street2> is optional.")
    parser.add_option('--file', dest='output_file', help= 'Output HTML file returned by the USPS script')
    
    options, args = parser.parse_args()

    if len(args) < 3:
        parser.print_help()
        sys.exit(1)

    street = args[0]
    city = args[1]
    state = args[2]
    if len(args) > 3:
        street2 = args[3]
    else:
        street2 = ''
    
    zip = zip_plus_4(street, city, state, street2, options.output_file)
    print zip
