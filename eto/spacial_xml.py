#
# This file reads the csv for the spacial csv
#
#
#
import os
import glob
import xmltodict
from xml.etree import cElementTree as ET

class Spatial_Cimis_XML():
   def __init__(self):  #no parameters
     pass

   def get_cimis_data( self ):
     os.chdir("email_data")
     print "made it here"
     files = glob.glob("C*.xml")  # get a list of files that match spatial cimis files
     print "files",files
     if len(files) == 0:
        os.chdir("../")
        return 0
     try:
       with open (files[0], "r") as myfile:
          data=myfile.read().replace('\n', '')
       print "data",data
       dic= xmltodict.parse(data)
       print("dic",dic)
       eto = dic["cimis_data"]["daily_data"]["cimis-goes"][1]["eto"]["#text"]
       eto = float(eto)
     except:
        eto = .5  # this will force to local eto calculation
     os.chdir("../" ) #return back to parnent dir
     
     return eto





   def elementtree_to_dict(self,element):
       node = dict()
       text = getattr(element, 'text', None)
       if text is not None:
           node['text'] = text
       #node.update(element.items()) # element's attributes
       child_nodes = {}
       for child in element: # element's children
          child_nodes.setdefault(child, []).append( elementtree_to_dict(child) )
       # convert all single-element lists into non-lists
       for key, value in child_nodes.items():
          if len(value) == 1:
             child_nodes[key] = value[0]

       node.update(child_nodes.items())

       return node


if __name__ == "__main__":
    x = Spatial_Cimis_XML()
    print("spacial eto", x.get_cimis_data() )




