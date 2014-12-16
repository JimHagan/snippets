
import base64
import hashlib
import hmac
import sys
import time
import urllib
import urllib2
import urlparse

import simplejson

#
# Uses GOOG local search to look businesses near a lat,lon.
#
# Originally written for hotel auto-poi detection.
#
# WON"T WORK UNTIL GOOGLE GIVES US ACCESS TO THE PLACES API
# WORK-IN-PROGRESS

from csv_unicode import *

# key, client id for dewdrops@gmail.com's adsense account
__GMAPS_KEY = 'ABQIAAAA86kSMaoCcw6cwabQ8q83URQAFhXEiFfbbaHvFuadpIDKV-RicBTmEHZOGyFeFYGuCqhlZHBN_n05LQ'
__AFS_CLIENT_ID = 'partner-pub-5545152270546437'


__base_places_url = 'https://maps.googleapis.com/maps/api/place/search/json?'


def sign_url(input_str):

    print("URL To Sign: " + input_str)
    url = urlparse.urlparse(input_str)

    print("Private Key: " + __GMAPS_KEY)

    # We only need to sign the path+query part of the string
    urlToSign = url.path + "?" + url.query
    print("Original Path + Query: " + urlToSign)

    # Decode the private key into its binary format
    # We need toe decode the URL-encoded private key
    decodedKey = __GMAPS_KEY #base64.urlsafe_b64decode(__CADIO_MOBILE_GMAPS_KEY)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decodedKey, urlToSign, hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    print '======'
    endecoded_signature = base64.urlsafe_b64encode(signature.digest())
    print("")
    print("B64 Signature: " + endecoded_signature)
    return endecoded_signature


def compute_confidence(search_string, result_title):
    words = search_string.lower().split(' ')
    result_title = result_title.lower()

    words_found = 0
    for w in words:
        if result_title.find(w) > -1:
            words_found += 1

    return (float(words_found) / len(words))


def get_places(search_str, lat, lon):

    parameters_dict = {'location': '%s,%s' % (lat,lon), 'radius':'2000',
                       'sensor': 'true', 'client': __AFS_CLIENT_ID }
    parameters = ''
    for k,v in parameters_dict.iteritems():
        parameters = parameters + '%s=%s&' % (k,v)

    url = __base_places_url + parameters

    signature = sign_url(url)
    url = url + '&signature=%s' % signature
    response = None
    num_errors=0
    while not response and num_errors < 3:
        time.sleep(1)
        try:
            print 'fetching: %s' % url
            request = urllib2.Request(url)
            request.add_header('User-Agent','DataView - Mozilla/1.0 compatible')
            opener = urllib2.build_opener()
            resp = simplejson.loads(opener.open(request).read())
            print 'resp: %s' % resp
            response = resp
        except urllib2.URLError as e:
            num_errors += 1
            print 'URLError: ' + str(e)
            print 'Retrying...'
            time.sleep(num_errors*2)
    return []

def local_search(search_term, lat, lon):

    get_places(search_term, lat, lon)

    return []

#    results = response['responseData']['results']
#    print 'Got response with %s results for search: "%s"' % (len(results), query_str)
#
#    for r in results[0:10]:
#        confidence = compute_confidence(search_term, r['titleNoFormatting'])
#        record = [search_term, lat, lon, \
#                  str(confidence), r['accuracy'], r['lat'], r['lng'],
#                  r['titleNoFormatting'], r['streetAddress'],
#                  r['city'], r['region'] ]
#        print 'Record: ' + ','.join(record)
#    return results[0:10]
