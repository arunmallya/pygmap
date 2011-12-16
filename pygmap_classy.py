import sys

class pyGmap:

    def print_header(self, fout): # prints the required <head> in output file
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


    def __init__(self, output_file):
        self.fout = open(output_file, "w")
        print_header(fout)
# init() ends
