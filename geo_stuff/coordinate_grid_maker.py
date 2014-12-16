from geocoder import Geocoder


class CoordinateGridMaker(object):
    
    def __init__(self):
        pass
    
    def __convert_m_to_degrees(self, m):
        """Rough approximation to convert meters to degrees of lat/lon. This is an overestimate of 
        degrees for everywhere but at the equator."""
        return (m/1000.0) / 111.3

    def get_nationwide_grid(self, grid_spacing_m):
        """Return a grid of points for the entire contiguous US with spacing = <grid_spacing_m>."""
        northernmost = 49.384358 #Lake of the Woods, MN 
        southernmost = 24.520833 #Ballast Key, FL
        easternmost = -66.949778 #West Quoddy Head, ME
        westernmost = -124.733056 #Cape Alava, WA
        return self.get_lat_lon_grid(northernmost, southernmost, easternmost, westernmost, grid_spacing_m)
    
    def get_grid_with_center(self, center_lat, center_lon, width_m, height_m, grid_spacing_m):
        """Return a grid of points centered on (center_lat, center_lon), with specified width and
        height with specified spacing from point to point."""
        width_deg = self.__convert_m_to_degrees(width_m)
        height_deg = self.__convert_m_to_degrees(height_m)
        north = center_lat + height_deg/2.0
        south = center_lat - height_deg/2.0
        east = center_lon + width_deg/2.0
        west = center_lon - width_deg/2.0
        return self.get_lat_lon_grid(north, south, east, west, grid_spacing_m)
    
    def get_grid_with_address(self, address, width_m, height_m, grid_spacing_m):
        """Return a grid of points centered on <address>."""
        geocoder = Geocoder()
        lat_lon, details = geocoder.get_location_by_address(address)
        lat = lat_lon[0]; lon = lat_lon[1];
        return self.get_grid_with_center(lat, lon, width_m, height_m, grid_spacing_m)
    
    def get_lat_lon_grid(self, north_bound, south_bound, east_bound, west_bound, grid_spacing_m):
        """Return a grid of points withing the specified boundaries with the distance from point to
        point = <grid_spacing_m>."""
        # in degress, this is the distance between the centers of the squares that make up the grid
        grid_spacing_deg = self.__convert_m_to_degrees(grid_spacing_m)
        
        # Run across the grid, add points along the way
        lat_lons = []
        cur_lat = south_bound + (grid_spacing_deg / 2.0)
        cur_lon = west_bound + (grid_spacing_deg / 2.0)

        while cur_lat < north_bound:
            while cur_lon < east_bound:
                lat_lons.append((cur_lat, cur_lon))
                cur_lon += grid_spacing_deg
            cur_lat += grid_spacing_deg
            cur_lon = west_bound + (grid_spacing_deg / 2.0)
    
        return lat_lons

