#
# This file reads the csv for the spacial csv
#
#
#
import os
import glob

class Station_Cimis():
   def __init__(self):  #no parameters
     pass

   def get_cimis_data( self ):
     print "made it here"
     os.chdir("email_data")
     print "made it here #"
     try:
        files = glob.glob("C*.csv")  # get a list of files that match spatial cimis files
        if len(files) == 0:
           return 0
        print "station cimis # of files",files
        lines = open(files[0]).readlines()
        print "lines",lines
        keys = (lines[0].strip()).split(",")
        #print("keys",keys)
        values = (lines[1].strip()).split(",")
        cimis_data = {}
        cimis_data["evap"]    = float(values[29])
        cimis_data["precp"]   = float(values[5])
        print "cimis_data",cimis_data
        
     except:
       
       cimis_data["evap"]    = 0
       cimis_data["precp"]   = 0

 
     os.chdir("../" ) #return back to parnent dir
     print "Station",os.getcwd()
     return cimis_data
     

if __name__ == "__main__":
    x = Station_Cimis()
    cimis_data = x.get_cimis_data()
    print("station eto", cimis_data["evap"],cimis_data["precp"] )
