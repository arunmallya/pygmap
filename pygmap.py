import sys

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


def print_init(fout, input_file):
    # find the center of points in the input file
    fin = open(input_file, "r")

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

    print c_latitude, c_longitude
    
    # write out the initialize() part to map part
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
""" %(c_latitude, c_longitude))

# write out markers for each of the points and the info containing its location
    fin = open(input_file, "r")
    
    counter = 0
    for line in fin:
        info = line.split(" ")

        latitude  = float(info[0])
        longitude = float(info[1])

        fout.write("""
    var contentString%d = '<div id="content">'+ 
    '<div id="siteNotice">'+ 
    '</div>'+ 
    '<div id="bodyContent">'+ 
    '<p> Latitude : %s </p> ' + 
    '<p> Longitude : %s </p> ' + 
    '</div>'+ 
    '</div>';
 
    var infoWindow%d = new google.maps.InfoWindow({
           content: contentString%d
    });

    var myLatLang%d = new google.maps.LatLng(%s, %s);

    var marker%d = new google.maps.Marker({
           position: myLatLang%d,
           map: map,
           title: 'Point_%d' 
    });

    google.maps.event.addListener(marker%d, 'click', function(){
           infoWindow%d.open(map, marker%d);
    });
""" %(counter, latitude, longitude, counter, counter, counter, latitude, longitude, counter, counter, counter, counter, counter, counter))
        counter += 1


    fout.write("""
  }
</script>
</head>

""")

# print_init() ends


def create_map(input_file, output_file):
    fout = open(output_file, "w")
    
    print_header(fout)
    print_init(fout, input_file)
    print_body(fout)

# create_map() ends
