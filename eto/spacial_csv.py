#
# This file reads the csv for the spacial csv
#
#
#
import os
import glob

class Spatial_Cimis():
   def __init__(self):  #no parameters
     pass

   def get_cimis_data( self ):
     os.chdir("email_data")
     try:
        files = glob.glob("C*.csv")  # get a list of files that match spatial cimis files
        if len(files) == 0:
           os.chdir("../")
           return 0
        lines = open(files[0]).readlines()
        keys = (lines[0].strip()).split(",")
        values = (lines[1].strip()).split(",")
        key = "CIMIS ETo (in) (in/day)" 
        position = keys.index(key)
        cimis_data    = float(values[position])
     except:
         cimis_data = 0
     #print "value" , cimis_data
     os.chdir("../" ) #return back to parnent dir
     print "Spacial",os.getcwd()
     return cimis_data

if __name__ == "__main__":
    x = Spatial_Cimis()
    print("spacial eto", x.get_cimis_data() )
