# This simple "white label" geocoder uses the open cage geocoder as its implementation.
# To install this from github invoke the following command: 
# pip install -e git+git://github.com/lokku/python-opencage-geocoder.git#egg=python-opencage-geocoder
# NOTE: use -e to have access to the source code.  It is necessary to patch a bug that I found using open-cage-geocoder-py-patch.txt
#
# Sample forward geocode: http://127.0.0.1:5000/forward/147%20Farm%20STreet%20Blackstone%20MA%2001504
#
# Sample reverse geocode: http://127.0.0.1:5000/reverse/42.036488/-71.519678/
import json
from opencage.geocoder import OpenCageGeocode
from flask import Flask

app = Flask(__name__)
_key = OPEN_CAGE_KEY = "db6a41dce5777db388d7dc348358690e"
_geocoder = OpenCageGeocode(OPEN_CAGE_KEY)

@app.route("/forward/<address>")
def forward(address):
  return json.dumps(_geocoder.geocode(address))

@app.route("/reverse/<lat>/<lng>/")
def reverse(lat, lng):
  return json.dumps(_geocoder.reverse_geocode(float(lat), float(lng)))
  
if __name__ == "__main__":
    app.run(debug=True)