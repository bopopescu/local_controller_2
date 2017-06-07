# external control 
import datetime
import time
import string
import urllib2
import math
import redis

import json

import py_cf
import os
import subprocess
import signal
import json
import base64

import cloud_event_queue
# devices is list of redis keys that
# contain redis keys
# the redis keys are a list of three elements
# 0 is the current time
# 1 is the pid
# 2 is the max elasped time

# to detect crash ---> check pid change


device_directory = "WD_DIRECTORY"


class Watch_Dog_Client():
   def __init__(self, redis, key, description ):
       self.device_directory       = device_directory
       self.redis                  = redis
       self.key                    = key
       self.description            = description
       self.redis.hset( self.device_directory, key, None)
       self.pat_wd()
   

   def pat_wd( self, *arg  ):                                                    
       temp                      = {}
       temp["time"]              = time.time()
       temp["max_dt"]            = 5*60
       temp["pid"]               = os.getpid()
       temp["description"]       = self.description
       data = base64.b64encode(json.dumps(temp) )
       self.redis.hset( self.device_directory, self.key, data )





### add event wd_pid_change event -----

class Watch_Dog_Ctrl():
   def __init__(self, redis ):
       self.redis      = redis
       self.device_directory  = device_directory
  
   def store_alarm_queue( self, event, data ):
      cloud_queue.store_event_queue(  event, data,status ="RED" )
     
   
   def poll_devices( self, chainFlowHandle, chainObj, parameters, event ):
       
       keys = self.redis.hkeys(self.device_directory)
       print "keys",keys
       for i in keys:
          print "i",i
          try:
             temp         = self.redis.hget(self.device_directory, i)
             temp         = json.loads(base64.b64decode(temp))
             
             if temp !=  None:
                curr_time    = temp["time"] 
                max_dt       = temp["max_dt"]  
                pid          = temp["pid"]    
                description  = temp["description"]
                time_base  = time.time()
                max_time  = curr_time + float(max_dt)
                if time_base > max_time :
                     self.store_alarm_queue( "wd_kill_process", {"index":i, "description": description} )
                     os.kill( pid, signal.SIGKILL)
                     self.redis.hdel( self.device_directory,i)
                     
          except:
            self.store_alarm_queue( "wd_exception",{"index":i} )
            self.redis.hdel(self.device_directory, i)
            print "exception  for index ",i
           


     
if __name__ == "__main__":
  
  redis = redis.StrictRedis( host = 'localhost', port=6379, db = 0 )
  cloud_queue = cloud_event_queue.Cloud_Event_Queue( redis )
 
  wd = Watch_Dog_Ctrl( redis  )
  wd.store_alarm_queue( "wd_startup",None )
  #
  # Adding chains
  #
  cf = py_cf.CF_Interpreter()
  
#  
# ETO processing elements  
# 
 
  
  cf.define_chain("watch_dog_thread",True)
  cf.insert_link( "link_2","One_Step",[ wd.poll_devices ])
  cf.insert_link( "link_3","WaitTod",["*","*","*",30 ])
  cf.insert_link( "link_4","Reset",[])  




 



  #
  # Executing chains
  #
  cf_environ = py_cf.Execute_Cf_Environment( cf )
  cf_environ.execute()



