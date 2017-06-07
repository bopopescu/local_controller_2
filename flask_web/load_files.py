
#
# File: load_files.py
# load sys files and application files
# The data is stored in the following
#    System Files are stored in the following in json format 
#    	As a dictionary with the key of FILES:SYS
#    	The key of the dictionary are the file names
#    APP Files are stored in the following in json format 
#    	As a dictionary with the key of 
#    	The key of the dictionary are the file names

#  import redis
#  make redis dictionary "SYS:FILES"
# store json_object to redis data "global_sensors"
import os
from os import listdir
from os.path import isfile, join
import base64
import redis
import json

redis                     = redis.StrictRedis( host = "127.1.1.1", port=6379, db = 0 )
app_files = "/home/pi/new_python/app_data_files/"
sys_files = "/home/pi/new_python/system_data_files/"


app_list = redis.hkeys("APP_FILES")
sys_list = redis.hkeys("SYS_FILES")


class APP_FILES():
   def __init__( self,redis):
       self.path = app_files
       self.key  = "FILES:APP"
       self.redis = redis

   def file_directory( self ):
       return self.redis.hkeys( self.key )
  
   def delete_file( self, name):
       self.redis.hdel( self.key, name )


   def save_file( self, name, data ):
       f = open(self.path+name, 'w')
       json_data = json.dumps(data)
       f.write(json_data)
       compact_data = base64.b64encode(json_data)
       self.redis.hset( self.key,name, compact_data)

   def load_file( self, name ):
       compact_data = self.redis.hget( self.key,name)
       json_data = base64.b64decode(compact_data)
       data      = json.loads(json_data)
       return data

   def delete_file( self, name):
       os.remove( self.path+name)

class SYS_FILES():
   def __init__( self,redis ):

       self.path = sys_files
       self.key  = "FILES:SYS"
       self.redis = redis

   def file_directory( self ):
       return self.redis.hkeys( self.key )

   def delete_file( self, name):
       self.redis.hdel( self.key, name )


   def save_file( self, name, data ):
       f = open(self.path+name, 'w')
       json_data = json.dumps(data)
       f.write(json_data)
       compact_data = base64.b4encode(json_data)
       self.redis.hset( self.key,name, compact_data)

   def load_file( self, name ):
       compact_data = self.redis.hget( self.key,name)
       data = json.loads(base64.b64decode(compact_data))
       return data

   def delete_file( self, name):
       os.remove( self.path+name)


if __name__ == "__main__":
   # delete APP FILES DATA
   if len(app_list) > 0:
       redis.hdel("FILES:APP",app_list)
   

   # delete SYS FILES DATA
   if len(sys_list) > 0:
       redis.hdel("FILES:SYS",sys_list)
   

   files = [ f for f in listdir(app_files)  ]

   # load app files
   for i in files:

       fileName, fileExtension = os.path.splitext(i)

       if fileExtension == ".json":
           f = open(app_files+i, 'r')
           data = f.read()
           data = base64.b64encode(data)
           redis.hset("FILES:APP", i , data)
   

   # load sys files

   files = [ f for f in listdir(sys_files)  ]
   for i in files:
       print "i",i
       fileName, fileExtension = os.path.splitext(i)
       if fileExtension == ".json":
           f = open(sys_files+i, 'r')
           data = f.read()
           data = base64.b64encode(data)
           redis.hset("FILES:SYS", i , data)
           print "data","done"

   ####
   #### INSURING THAT ETO_MANAGEMENT FLAG IS DEFINED
   ####
   temp = redis.get("ETO_MANAGE_FLAG")
   if temp == None: 
       # not defined
       redis.set( "ETO_MANAGE_FLAG",1)

   temp = redis.hget("CONTROL_VARIABLES","ETO_MANAGE_FLAG")
   if temp == None: 
       # not defined
       redis.hset( "CONTROL_VARIABLES","ETO_MANAGE_FLAG",1)


   ####
   ####  Construct ETO Data QUEUES
   ####

   file_data = redis.hget("FILES:APP","eto_site_setup.json")
   temp          = base64.b64decode(file_data)
   eto_site_data = json.loads(temp) 

   redis.delete("ETO_RESOURCE_A")
   for j in eto_site_data:
       redis.hset( "ETO_RESOURCE_A",j["controller"]+"|"+str(j["pin"]),0)

   keys = redis.hkeys("ETO_RESOURCE")
   print "keys",keys
   for i in keys:
       print "i",i
       value = redis.hget("ETO_RESOURCE",i)
       if redis.hexists("ETO_RESOURCE_A",i):
           redis.hset("ETO_RESOURCE_A",i,value)
   redis.delete("ETO_RESOURCE")
   redis.rename("ETO_RESOURCE_A","ETO_RESOURCE")

   if redis.hget("CONTROL_VARIABLES","ETO_RESOURCE_UPDATED") != "TRUE":
       redis.hset("CONTROL_VARIABLES","ETO_RESOURCE_UPDATED","FALSE")
   #  
   # delete process keys
   #
   keys = redis.hkeys("WD_DIRECTORY")
   for i in keys:
     print "i",i
     redis.hdel( "WD_DIRECTORY",i)

   redis.hset("SYS_DICT", "CONTROL_VARIABLES",   "system control and status variables")
   redis.hset("SYS_DICT", "FILES:APP",           "dictionary of application files")
   redis.hset("SYS_DICT", "FILES:SYS",           "dictionary of system files")
   redis.hset("SYS_DICT", "ETO_RESOURCE",        "dictionary of eto resource")
   redis.hset("SYS_DICT", "SCHEDULE_COMPLETED",  "markers to prevent multiple keying of sprinklers")
   redis.hset("SYS_DICT", "OHM_MESS",            "ohm measurement for active measurements")
   redis.hset("QUEUES_DICT","QUEUES:SPRINKLER:PAST_ACTIONS","QUEUE OF RECENT IRRIGATION EVENTS AND THEIR STATUS")
   redis.hset("QUEUES_DICT","QUEUES:CLOUD_ALARM_QUEUE","QUEUE OF EVENTS AND ACTIONS TO THE CLOUD")
   redis.hset("QUEUES_DICT","QUEUES:SPRINKLER:FLOW:<schedule_name>","QUEUE OF PAST FLOW DATA")
   redis.hset("QUEUES_DICT","QUEUES:SPRINKLER:CURRENT:<schedule_name>","QUEUE OF PAST CURRENT DATA") 
   redis.hset("QUEUES_DICT","QUEUES:SYSTEM:PAST_ACTIONS","QUEUE OF RECENT SYSTEM EVENTS AND THEIR STATUS")
  
   

