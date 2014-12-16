#!/usr/bin/env python
from kml_strings import *
from siphon.databench.models import POI, Point
import zipfile
import os
import csv
import sys

latnames = ('LAT', 'LATITUDE')
lonnames = ('LON', 'LONG', 'LONGITUDE')


def kml_begin_file(color_radius="Red", color_line="Red", color_marker="Green"):
    """ Begin KML file.  Specify radius color, marker color, and line color """

    # Initializations
    color_inputs = {'red': 'red', 'r': 'red', 'green': 'green', 'g': 'green', 'blue': 'blue', 'b': 'blue', 'black': 'black', 'k': 'black'}
    colors = {'red': '2222FF', 'green': '22FF22', 'blue': 'FF2222', 'black': '000000'}  # BB GG RR
    radius_opacity = '7F'
    line_opacity = 'FF'  # 7F = 50% opaque, 3F = 25% opaque, FF = 100% opaque
    radius_outline = False  # outline radius?

    # Find color mappings
    radius_color = colors[color_inputs[color_radius.lower()]]
    line_color = colors[color_inputs[color_line.lower()]]
    marker_color = colors[color_inputs[color_marker.lower()]]

    # Output string
    return kml_top + kml_style % (radius_opacity, radius_color, radius_outline, line_opacity, line_color, marker_color)


def kml_append_poi(poi):
    print poi.street
    print poi.city
    print poi.state
    print poi.zip
    address = poi.street + ', ' + poi.city + ', ' + poi.state + ' ' + poi.zip
    if poi.radius:
        latlon = Point(poi.lat, poi.lon, poi.radius)
        return kml_placemark_with_radius % (poi.name, address, poi.lat, poi.lon, poi.radius, poi.name, poi.lon, poi.lat, \
                " ".join([ str(c[1]) + "," + str(c[0])+"\n" for c in latlon.get_radius_circle_points()]))
    else:
        return kml_placemark % (poi.name, address, poi.lat, poi.lon, poi.name, poi.lon, poi.lat)


def kml_end_file():
    return kml_bottom


def main(argv):
    """ Import point of interest (POI) CSV file, and convert to KML.  The POI
    CSV file contains the following fields: NAME, STREET, CITY, STATE, ZIP,
    LAT/LATITUDE, LON/LONG/LONGITUDE, RADIUS (optional) """

    if len(argv) < 2:
        raise Exception('You must specify a POI CSV file.')
    input_file = argv[1]

    if len(argv) < 3:
        output_file = input_file[0:-3] + 'kmz'
    else:
        output_file = argv[2]

    reader = csv.DictReader(open(input_file, 'r'))
    latset = set(reader.fieldnames) & set(['LAT', 'LATITUDE'])
    latfield = latset.pop()
    lonset = set(reader.fieldnames) & set(['LON', 'LONG', 'LONGITUDE'])
    lonfield = lonset.pop()

    kml_file = output_file[0:-3] + 'kml'
    with open(kml_file, 'wb') as kml:
        kml.write(kml_begin_file(color_radius='Green', color_marker='Green'))
        for row in reader:
            print row
            row['RADIUS'] = float(row['RADIUS']) if 'RADIUS' in row else 0.0
            #if 'TYPE1' not in row: row['TYPE1'] = ''
            #if 'TYPE2' not in row: row['TYPE2'] = ''
            #if 'TYPE3' not in row: row['TYPE3'] = ''
            print row['NAME']
            print row['STREET']
            print row['CITY']
            print row['STATE']
            print row['ZIP']
            print row['LAT']
            print row['LON']
            poi = POI(name=row['NAME'], street=row['STREET'], city=row['CITY'], state=row['STATE'], zip=row['ZIP'], \
                    lat=float(row[latfield]), lon=float(row[lonfield]), radius=row['RADIUS'])
            kml.write(kml_append_poi(poi))
        kml.write(kml_end_file())
        kml.close()

    kmz = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
    kmz.write(kml_file)
    kmz.close()

    os.remove(kml_file)

    print "File %s written.\n" % output_file

if __name__ == '__main__':
    main(sys.argv)
