class pyGmap:

    def print_header(self): # prints the required <head> in output file
        self.fout.write("""
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


    def print_body(self): # prints the required <body>
        self.fout.write("""
<body onload="initialize()">
  <div id="map_canvas" style="width:100%; height:100%"></div>
</body>

</html>
""")
# print_body() ends

    def print_init_header(self):

        self.fout.write("""
<script type="text/javascript">
  function initialize()
  {
    var latlng = new google.maps.LatLng(22.330239, 87.323653);
    var myOptions = {
      zoom: 2,
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

""")
# print_init_header() ends


    def print_init_footer(self):
        self.fout.write("""
  }
</script>
</head>

""")
# print_init_footer() ends


    def end_map(self):
        self.print_init_footer()
        self.print_body()
        self.fout.close()
# end_map() ends


    def check_input_params(self, options, info):
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

        return (string, color)
# check_input_params() ends


    def print_marker_and_info(self, latitude, longitude, string, color):
        counter = self.pointCounter

        self.fout.write("""
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
        self.pointCounter += 1
# def print_marker_and_info() ends


    def add_points(self, inputFile, options):
        # write out markers for each of the points and the info containing its location
        fin = open(inputFile, "r")

        counter = 0
        for line in fin:
            info = line.split(" ")

            # check the input parameters
            string, color = self.check_input_params(options, info)

            latitude  = float(info[0])
            longitude = float(info[1])

            self.print_marker_and_info(latitude, longitude, string, color)
        
            counter += 1

        return counter
# add_points() ends


    def create_polyline(self, start_counter, end_counter, polyLineOptions):

        self.fout.write("""
        var polylineCoordinates%d = [""" % self.polyLineCounter)

        for i in range(start_counter, end_counter):
            if i != end_counter-1:
                self.fout.write("""
          myLatLang%d,""" %i)
            else:
                self.fout.write("""
          myLatLang%d
        ];

        var myPolyLine%d = new google.maps.Polyline({
          path: polylineCoordinates%d,
          strokeColor: "%s",
          strokeOpacity: %f,
          strokeWeight: %d
        });

        myPolyLine%d.setMap(map);

    """ %(i, self.polyLineCounter, self.polyLineCounter, polyLineOptions[0], polyLineOptions[1], polyLineOptions[2], self.polyLineCounter))
#create_polyline() ends


    def add_polyLine(self, inputFile, pointOptions, polyLineOptions):
        # first plot the points, then connect them with a polyline
        start_counter = self.pointCounter # starting point of this polyline
        end_counter = start_counter + self.add_points(inputFile, pointOptions)

        # now the polyline
        self.create_polyline(start_counter, end_counter, polyLineOptions)

        # increment count of polyLines
        self.polyLineCounter += 1
# add_polyLine() ends


    def __init__(self, output_file):
        self.fout = open(output_file, "w")
        self.print_header()
        self.print_init_header()
        self.pointCounter = 0
        self.polyLineCounter = 0
# init() ends
