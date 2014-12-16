import kml.kml_toolkit as kml
import base.dbaccess as db


def kml_folder_with_device_homes(device_records):
    """Expects a set of data as returned by study_pickler.load_results_by_device_pickles(). 
    Returns a KMLFolder, populated with the home locations of the devices in the records."""
    folder = kml.KMLFolder("home")
    for device, data in device_records.items():
        if data:
            home = data['best_home_location']
            if home:
                blu_style = kml.KMLBalloonStyle('BlueStyle', 'blu')
                descript = "Home of %s" % device
                home.radius_m = 0
                pmark = kml.KMLPlacemarkPoint("", home.centroid, styles=[blu_style],
                                                description_html=descript)
                folder.add_placemark(pmark)
    return folder
    
def kml_folder_with_device_works(device_records):
    """Expects a set of data as returned by study_pickler.load_results_by_device_pickles(). 
    Returns a KMLFolder, populated with the work locations of the devices in the records."""
    folder = kml.KMLFolder("work")
    for device, data in device_records.items():
        if data:
            work = data['best_work_location']
            if work:
                grn_style = kml.KMLBalloonStyle('GreenStyle', 'grn')
                descript = "Work of %s" % device
                work.radius_m = 0
                pmark = kml.KMLPlacemarkPoint("", work.centroid, styles=[grn_style],
                                                description_html=descript)
                folder.add_placemark(pmark)
    return folder
    
def kml_folder_with_pois_containing(search_term):
    """Returns a KMLFolder, populated with KMLPlacemarkPoints corresponding to the POI's that contain
    <string>."""
    conn = db.new_siphon_connection()
    pois = db.all_pois(conn)
    pois = [poi for poi in pois if poi.name.count(search_term)]
    folder = kml.KMLFolder("pois")
    for poi in pois:
        pmark = kml.KMLPlacemarkPoint("", poi)
        folder.add_placemark(pmark)
    
    return folder