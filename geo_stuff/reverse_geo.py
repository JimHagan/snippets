#!/usr/bin/env python

# 
# 
# 

import time
import sys

import simplegeo
import oauth2 as oath

from csv_unicode import *

oauth_token = "2e5T9qZVwPacupLXk2Yqv8bYJ3BcqZKT"
oauth_secret= "VBbG5ufsDZzxTREg3aEH68pny7wtf9va"

client = simplegeo.Client(oauth_token, oauth_secret)

keys = ['street_number', 'street', 'county_name',\
        'county_code', 'state_name', 'state_code', 'place_name']

def get_reverse_geo(lat, lon):
    print 'looking up (%s, %s) ' % (lat, lon)
    result = client.get_nearby_address(lat, lon)
    props = result['properties']
    if not props:
        print 'No props returned for lat/lon: %s, %s' %\
              (str(lat), str(lon))
        return ['Not found']

    print 'Props: ' + str(props)
    output_list = [str(lat), str(lon)]
    
    for k in keys:
        if props[k]:
            output_list.append(props[k])
        else:
            output_list.append("")

    return output_list

#
# main
#
def main(args):
    if len(args) == 1 or len(args) > 3:
        print 'wrong number of args. Usage:  <lat> <lon>  OR:  <filename>'
        sys.exit(111)

    print 'starting...'

    col_names = ['lat','lon']
    col_names.extend(keys)
    print 'Output format: %s' % str(col_names)
    
    if len(args) == 3:
        result = get_reverse_geo(args[1], args[2])
        print str(result)
        #print str(reduce(lambda x,y: x+y, [x + ',' for x in output_list])    
    else:

        out = UnicodeWriter(open('reverse_geo_output.csv','w'), delimiter=',')
        out.writerow(col_names)

        file_reader = UnicodeReader(open(args[1]), delimiter=',')
        file_reader.next() # skip header

        for row in file_reader:
            lat, lon = row[0], row[1]
            if lat and lon:
                result = get_reverse_geo(lat, lon)
                out.writerow(result)
                print 'for  (%s, %s), result: ' % (lat, lon) + str(result)
            time.sleep(0.5)
    print 'done.'


if __name__ == '__main__':
    main(sys.argv)

