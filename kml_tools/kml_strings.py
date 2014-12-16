kml_top = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
"""
    
kml_style = """  
<Style id="placemark">
  <PolyStyle>
    <color>%s%s</color>
    <colorMode>normal</colorMode>
    <fill>1</fill>
    <outline>%s</outline>
  </PolyStyle>
  <LineStyle>
    <color>%s%s</color>
    <colorMode>normal</colorMode>
    <width>3</width>
  </LineStyle>
  <IconStyle>
    <color>FF%s</color>
    <colorMode>normal</colorMode>
    <scale>0.5</scale>
    <Icon>
      <href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href>
    </Icon>
  </IconStyle>
  <BalloonStyle>
    <bgColor>ffffffff</bgColor>
    <textColor>ff000000</textColor>
    <text><b>$[name]</b>$[address]</text>
    <displayMode>default</displayMode>
  </BalloonStyle>
</Style>
"""

kml_placemark = """
<Placemark>
  <name><![CDATA[%s]]></name>
  <address>
    <p><![CDATA[%s]]></p>
    <table>
      <tr><td>Lat:</td><td>%s</td></tr>
      <tr><td>Lon:</td><td>%s</td></tr>
      <tr><td>Types:</td><td><![CDATA[%s]]></td></tr>
    </table>
  </address>
  <styleUrl>#placemark</styleUrl>
  <Point>
    <coordinates>%s, %s</coordinates>
  </Point>
</Placemark>
"""

kml_placemark_with_radius = """
<Placemark>
  <name><![CDATA[%s]]></name>
  <address>
    <p><![CDATA[%s]]></p>
    <table>
      <tr><td>Lat/Lon:</td><td>%s, %s</td></tr>
      <tr><td>Radius:</td><td>%s m</td></tr>
      <tr><td>Types:</td><td><![CDATA[%s]]></td></tr>
    </table>
  </address>
  <styleUrl>#placemark</styleUrl>
  <MultiGeometry>
    <Point>
      <coordinates>%s, %s</coordinates>
    </Point>
    <Polygon>
      <extrude>0</extrude>
      <altitudeMode>clampToGround</altitudeMode>
      <outerBoundaryIs>
      <LinearRing>
        <coordinates>
        %s
        </coordinates>
      </LinearRing>
      </outerBoundaryIs>
    </Polygon>
  </MultiGeometry>
</Placemark>
"""

kml_connect = """        
<Placemark>
  <styleUrl>#placemark</styleUrl>
  <LineString>
    <extrude>0</extrude>
    <tessellate>1</tessellate>
    <altitudeMode>clampToGround</altitudeMode>
    <coordinates>%s</coordinates>
  </LineString>
</Placemark>
"""

kml_bottom = """
</Document>
</kml>
"""

kml_grid = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<Style id="hot">
  <IconStyle>
    <color>66333366</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
<Style id="hotter">
  <IconStyle>
    <color>663333cc</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
<Style id="hottest">
  <IconStyle>
    <color>663333ff</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
<Style id="medium">
  <IconStyle>
    <color>66663366</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
<Style id="cold">
  <IconStyle>
    <color>66663333</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
<Style id="colder">
  <IconStyle>
    <color>66cc3333</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
<Style id="coldest">
  <IconStyle>
    <color>66ff3333</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
<Style id="nodata">
  <IconStyle>
    <color>33999999</color><colorMode>normal</colorMode>
    <scale>1.6</scale><Icon><href>file:///home/drew/workspace/simplegeo/icon_rect.png</href></Icon>
  </IconStyle>
</Style>
"""
