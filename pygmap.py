import sys
import math

def print_header(fout): # prints the required <head>
    fout.write("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0; padding: 0 }
  #map_canvas { height: 100% }
</style>
<script type="text/javascript"
    src="http://maps.googleapis.com/maps/api/js?sensor=false">
</script>

""")

# print_header() ends


def print_body(fout): # prints the required <body>
    fout.write("""
<body onload="initialize()">
  <div id="map_canvas" style="width:100%; height:100%"></div>
</body>

</html>
""")

# print_body() ends

def print_init_header(fout, c_latitude, c_longitude):

    fout.write("""
<script type="text/javascript">
  function initialize()
  {
    var latlng = new google.maps.LatLng(%f, %f);
    var myOptions = {
      zoom: 15,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
    var image0 = './images/gmap_00FFFF_icon.png';
    var image1 = './images/gmap_99FF00_icon.png';
    var image2 = './images/gmap_blue_icon.png';
    var image3 = './images/gmap_CC9900_icon.png';
    var image4 = './images/gmap_FF00FF_icon.png';
    var image5 = './images/gmap_FF0000_icon.png';
    var image6 = './images/gmap_FF9900_icon.png';
    var image7 = './images/gmap_FFFF00_icon.png';

""" %(c_latitude, c_longitude))

# print_init_header() ends

def print_marker_and_info(fout, counter, latitude, longitude, string, color):
    fout.write("""
    var contentString%d = '<div id="content">'+ 
    '<div id="siteNotice">'+ 
    '</div>'+ 
    '<div id="bodyContent">'+ 
    '<p> Latitude : %s </p> ' + 
    '<p> Longitude : %s </p> ' + 
    '<p> %s </p>'
    '</div>'+ 
    '</div>';
 
    var infoWindow%d = new google.maps.InfoWindow({
           content: contentString%d
    });

    var myLatLang%d = new google.maps.LatLng(%s, %s);

    var marker%d = new google.maps.Marker({
           position: myLatLang%d,
           map: map,
           title: 'Point_%d', 
           icon: image%d
    });

    google.maps.event.addListener(marker%d, 'click', function(){
           infoWindow%d.open(map, marker%d);
    });
""" %(counter, latitude, longitude, string, counter, counter, counter, latitude, longitude, counter, counter, counter, color, counter, counter, counter))

# def print_marker_and_info() ends

def check_input_params(options, info):
    # here are the default values for many of the possible input parameters
    string = "" # no additional information is default
    color = 5 # red is default
    polyline = False # no lines by default

    # check which of the input parameters are used
    if options[0] == True: # use specified color
        color = int(info[2])
    if options[1] == True: # has additional information
        # if color was used, then extra info will be from info[3], else info[2]
        if options[0] == True:
            string = str(info[3:])
        else:
            string = str(info[2:])
        
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace(',', ' ')
        string = string.replace('\'', '')
    
    if options[2] == True: # use polyline
        polyline = True

    return (string, color, polyline)

# check_input_params() ends

def find_centroid(fin):
    c_latitude  = 0.0
    c_longitude = 0.0

    counter = 0
    for line in fin:
        info = line.split(" ")

        latitude  = float(info[0])
        longitude = float(info[1])

        c_latitude  += latitude
        c_longitude += longitude

        counter += 1

    fin.close()

    c_latitude  /= counter
    c_longitude /= counter
    
    return (c_latitude, c_longitude)

# def find_centroid() ends


def create_polyline(fout, counter):
    
    fout.write("""
    var polylineCoordinates = [""")

    for i in range(0, counter):
        if i != counter-1:
            fout.write("""
      myLatLang%d,""" %i)
        else:
            fout.write("""
      myLatLang%d
    ];

    var myPolyLine = new google.maps.Polyline({
      path: polylineCoordinates,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    myPolyLine.setMap(map);

""" %i)

def print_init(fout, input_file, options):
    # find the center of points in the input file
    fin = open(input_file, "r")
    c_latitude, c_longitude = find_centroid(fin)
    print c_latitude, c_longitude

    
    # write out the initialize() part to map part
    print_init_header(fout, c_latitude, c_longitude)


    # write out markers for each of the points and the info containing its location
    fin = open(input_file, "r")
    
    counter = 0
    for line in fin:
        info = line.split(" ")

        # check the input parameters
        string, color, polyline = check_input_params(options, info)

        latitude  = float(info[0])
        longitude = float(info[1])

        print_marker_and_info(fout, counter, latitude, longitude, string, color)
        
        counter += 1


    # insert polyline
    if polyline == True:
        create_polyline(fout, counter)

    fout.write("""
  }
</script>
</head>

""")

# print_init() ends


def create_map(input_file, output_file, options=[]):

    fout = open(output_file, "w")
    
    print_header(fout)
    print_init(fout, input_file, options)
    print_body(fout)

# def create_map_file() ends
