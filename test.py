from pygmap_classy import *

myMap = pyGmap("map.html")
# creates a new instance of the map in output file "map.html"

myMap.add_points("./sample_input_files/locations_I.txt", [False, False])
# add points contained in the given file.
# They do not have color or any other extra information

myMap.add_polyLine("./sample_input_files/locations_II_color_extrainfo.txt", [True, True], ["#99FF00", 1.0, 2])
# add points contained in the given file and join them with lines
# They have color and other extra information
# The polyline must have color <<"#99FF00">> (hex coded), an opacity of <<1.0>> and weight of <<2>>

myMap.end_map()
# done with the map
# <<map.html>> is ready to be opened now
