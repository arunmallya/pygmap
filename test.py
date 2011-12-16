from pygmap_classy import *

myMap = pyGmap("map.html")
myMap.add_polyLine("./sample_input_files/locations_I.txt", [False, False], ["#FF0000", 1.0, 2])
myMap.add_polyLine("./sample_input_files/locations_II_color_extrainfo.txt", [True, True], ["#99FF00", 1.0, 2])
myMap.end_map()
