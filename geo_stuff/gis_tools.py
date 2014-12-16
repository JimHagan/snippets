from collections import namedtuple
import math
import numpy as np
from django.contrib.gis.geos import Point

# According to the WGS84 standard, the average earth radius is equal
# to 6 371 008.7714 m, and the radius of a sphere of equal volume
# (e.g. the geometric mean radius) is 6 371 000.7900 m.
# http://earth-info.nga.mil/GandG/publications/tr8350.2/wgs84fin.pdf, p.40
#
# Also this seems to be used by most developers, including each of
# the implementations listed on the Wikipedia page for Haversine,
# as well as Matlab:
# http://www.mathworks.com/help/toolbox/map/ref/earthradius.html
EARTH_RADIUS = 6371000.0
METERS_PER_MILE = 1609.344
METERS_PER_DEGREE_LAT = 2 * np.pi * EARTH_RADIUS / 360.
DEGREES_LAT_PER_METER = 1. / METERS_PER_DEGREE_LAT


def compute_distance(lat1, lon1, lat2, lon2):
    """ Computes distance in meters between two lat/lon pairs using Haversine formula """
    #
    # R = Earth Radius
    # lat_d = lat2 - lat1
    # lon_d = lon2 - lon1
    # a = sin^2(lat_d / 2) + cos(lat1) * cos(lat2) * sin^2(lon_d / 2)
    #
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * \
        math.sin(delta_lon / 2) * math.sin(delta_lon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return c * EARTH_RADIUS


def bounding_box(lat, lon, radius_m):
    """ Computes square bounding box in lat/lon coordinates around a single point
    with radius specified in meters (where the circle is wholly contained by the
    bounding box"""
    min_lon = lon - radius_m / \
              math.fabs(math.cos(math.radians(lat)) * METERS_PER_DEGREE_LAT)
    max_lon = lon + radius_m / \
              math.fabs(math.cos(math.radians(lat)) * METERS_PER_DEGREE_LAT)
    min_lat = lat - (radius_m / METERS_PER_DEGREE_LAT)
    max_lat = lat + (radius_m / METERS_PER_DEGREE_LAT)

    BBTuple = namedtuple("BBTuple", "min_lat, max_lat, min_lon, max_lon")
    return BBTuple(min_lat=min_lat,
                   max_lat=max_lat,
                   min_lon=min_lon,
                   max_lon=max_lon)


def round_point(pt, digits=0):
    """Round the precision of a geos.Point to a specified number of digits."""
    return Point(round(pt.x, digits), round(pt.y, digits))


def slice_by_lat(lat, poly):
    """ Slice the (lat,lon) polygon horizontally (by latitude): specify the latitude and return the
    interpolated longitude coordinate(s) of the polygon boundaries """
    min_lon = np.Inf
    max_lon = -np.Inf
    n = len(poly)
    if poly[0][0] == poly[n - 1][0] and poly[0][1] == poly[n - 1][1]:
        # if polygon is closed, neglect last point and treat polygon as open
        n -= 1
    p1_lat, p1_lon = poly[0]
    for i in range(1, n + 1):
        p2_lat, p2_lon = poly[i % n]  # when i == n, use point [0] to close the polygon
        if p1_lat != p2_lat:
            if lat >= min(p1_lat, p2_lat) and lat <= max(p1_lat, p2_lat):
                lon_on_segment = (lat - p1_lat) * (p2_lon - p1_lon) / (p2_lat - p1_lat) + p1_lon  # x extrapolated onto polygon side
                min_lon = min(min_lon, lon_on_segment)
                max_lon = max(max_lon, lon_on_segment)
        elif lat == p1_lat:  # if side is horizontal, check whether y is on the side.
            min_lon = min(min_lon, p1_lon, p2_lon)
            max_lon = max(max_lon, p1_lon, p2_lon)
        p1_lat, p1_lon = p2_lat, p2_lon
    if np.isinf(min_lon):
        min_lon = np.NaN if np.isinf(max_lon) else max_lon
    if np.isinf(max_lon):
        max_lon = np.NaN if np.isinf(min_lon) else min_lon
    return (min_lon, max_lon)


def get_radius_circle_points(lat, lon, radius_m, numpoints=50):
    """ Returns lat/lon coordinates for the circle defined by this point's center and
    radius.  Returns a list of 'numpoints+1' tuples (closing the circle), where each
    tuple is a (lat, lon). """

    # Find latitude +/- radius
    latradius = 180 / math.pi * (radius_m / EARTH_RADIUS)

    # Find longitude +/- radius
    lonradius = 180 / math.pi * (radius_m / EARTH_RADIUS / math.cos(lat * math.pi / 180))

    # Build elliptical polygon
    points_in_circle = []
    for i in range(numpoints):
        theta = i * 2 * math.pi / numpoints
        points_in_circle.append(((lat + math.sin(theta) * latradius),
                                 (lon + math.cos(theta) * lonradius)))

    points_in_circle.append(points_in_circle[0])
    return points_in_circle


def inside_polygon(x, y, poly):
    """ Adapted from http://local.wasp.uwa.edu.au/~pbourke/geometry/insidepoly/
    Method: ray tracing in x plane: number of boundary crossings is odd if inside polygon
    Determine if a point is inside a polygon, where a polygon is a list of contiguous (x,y) pairs.
    If a point is on the border of a polygon, it is considered to be inside the polygon."""
    n = len(poly)
    if poly[0][0] == poly[n - 1][0] and poly[0][1] == poly[n - 1][1]:
        # if polygon is closed, neglect last point and treat polygon as open
        n -= 1

    inpoly = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]  # when i == n, use point [0] to close the polygon
        if p1y != p2y:
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):   # > min but <= max: don't count vertices twice
                    if x <= max(p1x, p2x):  # we might have a crossing
                        x_on_segment = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x  # x extrapolated onto polygon side
                        if round(x, 6) == round(x_on_segment, 6):   # must round due to floating point math
                            return True
                        if x < x_on_segment:
                            inpoly = not inpoly  # True if odd, False if even
        elif y == p1y:  # if side is horizontal, check whether (x,y) is on the side.
            if x >= min(p1x, p2x):
                if x <= max(p1x, p2x):
                    return True
        p1x, p1y = p2x, p2y
    return inpoly

""" State abbreviation mapping dict """
state_abbreviation_mappings = {'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 'ARKANSAS': 'AR', 'CALIFORNIA': 'CA',
            'COLORADO': 'CO', 'CONNECTICUT': 'CT', 'DELAWARE': 'DE', 'FLORIDA': 'FL', 'GEORGIA': 'GA',
            'HAWAII': 'HI', 'IDAHO': 'ID', 'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA',
            'KANAWA': 'KS', 'KENTUCKY': 'KY', 'LOUISIANA': 'LA', 'MAINE': 'ME', 'MARYLAND': 'MD',
            'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI', 'MINNESOTA': 'MN', 'MISSISSIPPI': 'MS', 'MISSOURI': 'MO',
            'MONTANA': 'MT', 'NEBRASKA': 'NE', 'NEVADA': 'NV', 'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ',
            'NEW MEXICO': 'NM', 'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', 'OHIO': 'OH',
            'OKLAHOMA': 'OK', 'OREGON': 'OR', 'PENNSYLVANIA': 'PA', 'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
            'SOUTH DAKOTA': 'SD', 'TENNESSEE': 'TN', 'TEXAS': 'TX', 'UTAH': 'UT', 'VERMONT': 'VT',
            'VIRGINIA': 'VA', 'WASHINGTON': 'WA', 'WEST VIRGINIA': 'WV', 'WISCONSIN': 'WI', 'WYOMING': 'WY',
            'DISTRICT OF COLUMBIA': 'DC'}

canada_province_abbreviation_mappings = {'ALBERTA': 'AB', 'ALB': 'AB', 'BRITISH COLUMBIA': 'BC', 'MANITOBA': 'MB',
        'MAN': 'MB', 'NEW BRUNSWICK': 'NB', 'NEWFOUNDLAND': 'NL', 'NOVA SCOTIA': 'NS', 'NORTHWEST TERRITORIES': 'NT',
        'NUNAVUT': 'NU', 'ONTARIO': 'ON', 'ONT': 'ON', 'PRINCE EDWARD ISLAND': 'PE', 'PQ': 'QC', 'PROVINCE OF QUEBEC': 'QC',
        'QUEBEC': 'QC', 'SASKATCHEWAN': 'SK', 'SAS': 'SK', 'YUKON TERRITORY': 'YT', 'QUBEC': 'QC'}
