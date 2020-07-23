import datetime
import time
import string
import urllib2
import math
import redis

import json

import os
import base64


  


class Sprinkler_Control():
  def __init__(self,ir_ctl ):
      self.system_files            = ir_ctl.system_files
      self.app_files               = ir_ctl.app_files
      self.redis                   = ir_ctl.redis
      self.io                      = ir_ctl.remote_io
      self.redis_15                = ir_ctl.redis_15
      self.commands                = self.register_commands()
      self.current_log_object      = None
      self.flow_log_object         = None
      self.excessive_flow_queue    = []
      json_data=open(self.system_files+"/global_sensors.json")
      json_object = json.load(json_data)
      self.flow_scale              =  json_object[0][3] #0.0224145939
      self.clean_filter_flag       = 0
      #print "flow scale",self.flow_scale
  

  #This function checks to see if command has been given
  def check_for_updates( self, chainFlowHandle, chainObj, parameters,event ):  
    length = self.redis.llen(  "sprinkler_ctrl_queue" )
    if length > 0:
        returnValue = True
    else:
        returnValue = False
    return returnValue
      
  def send_reboot_msg( self, chainFlowHandle, chainObj, parameters,event ):
    self.store_event_queue( "reboot", { "action":"reboot" } )
    self.store_alarm_queue( "reboot", { "action":"reboot" } )

  # This function processes a command
  def dispatch_sprinkler_mode(self, chainFlowHandle, chainObj, parameters,event ):
      length = self.redis.llen( "sprinkler_ctrl_queue")
      #print("sprinkler ctrl length is ",length)
      if length > 0:
         data = self.redis.rpop("sprinkler_ctrl_queue")
         #print "b64 data",data
         data = base64.b64decode(data)
         #print "json data",data
         object_data = json.loads(data )
         #print self.commands
         #print "------------------------------------->object data"
         #print object_data
         if self.commands.has_key( object_data["command"] ) :
           print "input commands",object_data["command"]
           self.commands[object_data["command"]]( object_data,chainFlowHandle, chainObj, parameters,event )
           print self.redis.llen("IRRIGATION_QUEUE")
      return "DISABLE"


  # These are the supported commands
  def register_commands( self ):
     temp = {}
     temp["RESTART_PROGRAM"]           = self.restart_program
     temp["OFFLINE"]                   = self.offline_command
     temp["QUEUE_SCHEDULE"]            = self.queue_schedule
     temp["QUEUE_SCHEDULE_STEP"]       = self.queue_schedule_step
     temp["QUEUE_SCHEDULE_STEP_TIME"]  = self.queue_schedule_step_time
     temp["RESTART_PROGRAM"]           = self.restart_program
     temp["NATIVE_SPRINKLER"]          = self.direct_valve_control       
     temp["CLEAN_FILTER"]              = self.clean_filter
     temp["OPEN_MASTER_VALVE"]         = self.open_main_valve
     temp["CLOSE_MASTER_VALVE"]        = self.close_main_valve
     temp["RESET_SYSTEM"]              = self.reset_system
     temp["CHECK_OFF"]                 = self.check_off
     temp["SHUT_DOWN"]                 = self.shut_down
     temp["TURN_ON"  ]                 = self.turn_on
     temp["SKIP_STATION"]              = self.skip_station
     return temp

 
  def shut_down( self, data_object,chainFlowHandle, chainObj, parameters,event ):
      self.redis.set("SHUT_DOWN",1)

  def turn_on( self, data_object,chainFlowHandle, chainObj, parameters,event ):
    self.redis.set("SHUT_DOWN",0)

  def skip_station( self, data_object,chainFlowHandle, chainObj, parameters,event ):
     self.redis.set("SKIP_STATION", 1 )


  # this is a hack  only called by check off
  def measure_flow_rate ( self, chainFlowHandle, chainObj, parameters,event ):
     results = self.io.get_flow_sensors()
     i = 1
     for j in  results :
       flow_value     = j["flow_value"]
       title          = j["title"]

       if i == 1 :
         self.redis.set("global_flow_sensor",flow_value )
         
       i = i+1

  def check_off( self,data_object, chainFlowHandle, chainObj, parameters,event ):
        temp = self.redis.get("schedule_name") 
        schedule_name = "Check_Off"
        self.redis.set( "schedule_name",schedule_name)
        self.store_event_queue( "check_off", { "action":"start" } )
        self.redis.set( "sprinkler_ctrl_mode","CHECK_OFF")
        self.io.disable_all_sprinklers()
        self.io.turn_on_main_valves()
        
        time.sleep(90)
        self.measure_flow_rate ( chainFlowHandle, chainObj, parameters,event )
        self.measure_flow_rate (  chainFlowHandle, chainObj, parameters,event )
        self.close_main_valve( data_object, chainFlowHandle,chainObj, parameters,event )
        print "off flow rate ",int(self.redis.get( "global_flow_sensor" ))*self.flow_scale
        if int(self.redis.get( "global_flow_sensor" ))*self.flow_scale   > 2:
           self.redis.set("SHUT_DOWN",1)
           self.store_event_queue( "check_off", { "action":"bad" } )
           self.store_alarm_queue( "check_off", { "action":"bad" } )
        else:
           self.store_event_queue( "check_off", { "action":"good" } )
        self.store_event_queue( "check_off", { "action":"done" } )
        self.redis.set( "schedule_name",temp)

  def check_off_direct( self, chainFlowHandle, chainObj, parameters,event ):
        temp = self.redis.get("schedule_name") 
        schedule_name = "Check_Off"
        self.redis.set( "schedule_name",schedule_name)
        print "check_off start"
        self.redis.set( "sprinkler_ctrl_mode","CHECK_OFF")
        self.io.disable_all_sprinklers()
        self.io.turn_on_main_valves()
        time.sleep(90)
        self.measure_flow_rate ( chainFlowHandle, chainObj, parameters,event )
        print "made 1"
        time.sleep(60)
        print "made 2 "
        self.measure_flow_rate (  chainFlowHandle, chainObj, parameters,event )
        self.close_main_valve( 2,chainFlowHandle,chainObj, parameters,event )
        print "made 3"
        temp = int(self.redis.get( "global_flow_sensor" ))*self.flow_scale
        if temp   > 2:
           print "bad path"
           self.redis.set("SHUT_DOWN",1)
           self.store_event_queue( "check_off", { "action":"bad","flow_rate":temp } )
           self.store_alarm_queue( "check_off", { "action":"bad","flow_rate":temp } )
        else:
           print "good path"
           self.store_event_queue( "check_off", { "action":"good","flow_rate":temp } )
        self.store_event_queue( "check_off", { "action":"done" } )
        print "check_off end"
        self.redis.set( "schedule_name",temp)
 
  #tested   
  #"OFFLINE" 
  def offline_command( self, data_object, chainFlowHandle,chainObj, parameters,event ):
      self.redis.set( "sprinkler_ctrl_mode","OFFLINE")
      self.close_main_valve( data_object, chainFlowHandle,chainObj, parameters,event )
      chainFlowHandle.disable_chain_base( ["main_valve_timed_off","monitor_irrigation_cell","monitor_irrigation_job_queue"])
      chainFlowHandle.enable_chain_base( ["monitor_irrigation_job_queue"])
      self.io.disable_all_sprinklers()
      self.clear_redis_sprinkler_data()
      self.clear_redis_irrigate_queue()
      self.redis.set( "schedule_name","offline")
      self.current_log_object = None
      self.flow_log_object = None
      self.redis.set("SHUT_DOWN",1)

  #"QUEUE_SCHEDULE" 
  def queue_schedule( self, data_object, chainFlowHandle, chainObj, parameters, event ):
      schedule_name =  data_object["schedule_name"]
      self.load_auto_schedule(schedule_name)
      self.redis.set("SHUT_DOWN",0)    
    
  #"QUEUE_SCHEDULE_STEP" 
  def queue_schedule_step( self, data_object, chainFlowHandle, chainObj, parameters, event ):
      self.schedule_name =  data_object["schedule_name"]
      self.schedule_step =  data_object["step"]
      self.schedule_step =   int(self.schedule_step)
      self.load_step_data( self.schedule_name, self.schedule_step ,None ) 
      self.redis.set("SHUT_DOWN",0)
    

  #"QUEUE_SCHEDULE_STEP_TIME" 
  def queue_schedule_step_time( self, data_object, chainFlowHandle, chainObj, parameters, event ):
      schedule_name        =  data_object["schedule_name"]
      self.schedule_step        =  data_object["step"]
      self.schedule_step_time   =  data_object["run_time"]
      self.schedule_step             = int(self.schedule_step)
      self.schedule_step_time        = int(self.schedule_step_time)  
      self.load_step_data( schedule_name, self.schedule_step, self.schedule_step_time ) 
      self.redis.set("SHUT_DOWN",0)
       
    
     

  #"NATIVE_SPRINKLER"
  def direct_valve_control( self, data_object, chainFlowHandle, chainObj, parameters, event ):      
        remote                = data_object["schedule_remote_queue"] 
        pin                   = data_object["schedule_pin_queue"]         
        schedule_step_time    = data_object["schedule_time_queue"]    
        pin = int(pin)
        schedule_step_time = int(schedule_step_time) 
        self.load_native_data( remote,pin,schedule_step_time)
        self.redis.set("SHUT_DOWN",0)
 
       
  # tested  
  #"CLEAN_FILTER"

  def  clean_filter_direct( self, chainFlowHandle, chainObj, parameters,event ):
       self.io.disable_all_sprinklers()
       temp = self.redis.get("schedule_name")
       self.store_event_queue( "clean_filter", { "action":"start" } )
       schedule_name = "Clean_Filter"
       self.redis.set( "schedule_name",schedule_name)
       self.io.turn_off_cleaning_valves()
       self.io.turn_on_main_valves()
       time.sleep(90)  # let line charge up
       self.io.turn_off_main_valves()
       time.sleep(5)
       self.io.turn_on_cleaning_valves()
       time.sleep(20)
       self.io.turn_on_main_valves()
       time.sleep(10)
       self.io.turn_off_main_valves()
       self.io.turn_off_cleaning_valves()
       self.store_event_queue( "clean_filter", { "action":"stop" } )
       self.redis.set("schedule_name",temp)
       self.clean_filter_flag = 1
       self.redis.set("cleaning_sum",0)

  def  clean_filter( self, data_object, chainFlowHandle, chainObj, parameters, event ):
       temp = self.redis.get("schedule_name")
       schedule_name = "Clean_Filter"
       self.store_event_queue( "clean_filter", { "action":"start" } )
       self.redis.set( "schedule_name",schedule_name)
       self.io.turn_off_cleaning_valves()
       self.io.turn_on_main_valves()
       time.sleep(90)  # let line charge up
       self.io.turn_off_main_valves()
       time.sleep(5)
       self.io.turn_on_cleaning_valves()
       time.sleep(20)
       self.io.turn_on_main_valves()
       time.sleep(10)
       self.io.turn_off_main_valves()
       self.io.turn_off_cleaning_valves()
       self.store_event_queue( "clean_filter", { "action":"stop" } )
       self.redis.set("schedule_name",temp)
       self.clean_filter_flag = 1
       self.redis.set("cleaning_sum",0)
  # tested  
  #"OPEN_MASTER_VALVE"
  def open_main_valve( self, data_object, chainFlowHandle, chainObj, parameters, event ):
      #print "made and open main valuve"
      self.io.turn_on_main_valves()
      chainFlowHandle.disable_chain_base([ "main_valve_timed_off"])
      chainFlowHandle.enable_chain_base( ["main_valve_timed_off" ])
     
  # tested  
  #"CLOSE_MASTER_VALVE"  
  def close_main_valve( self, data_object, chainFlowHandle, chainObj, parameters, event ):
      chainFlowHandle.disable_chain_base( ["main_valve_timed_off"])
      self.io.turn_off_main_valves()
      
    
 

     
  # tested 
  #"RESTART_SYSTEM"
  def  reset_system( self, data_object, chainFlowHandle, chainObj, parameters, event ):
     self.redis.set( "sprinkler_ctrl_mode","RESET_SYSTEM")
     os.system("reboot")  

  # tested
  # RESTART_PROGRAM
  def restart_program( self, data_object, chainFlowHandle, chainObj, parameters, event ):
     self.redis.set( "sprinkler_ctrl_mode","RESTART_PROGRAM")
     quit()
  

  # support function
  def clear_redis_irrigate_queue( self ):
    self.redis.delete( "IRRIGATION_QUEUE" )
    self.redis.delete( "IRRIGATION_CELL_QUEUE")

  #tested
  def clear_redis_sprinkler_data(self):
     self.redis.set( "sprinkler_ctrl_mode","OFFLINE")
     self.redis.set( "schedule_name","offline" )
     self.redis.set( "schedule_step_number",0 )
     self.redis.set( "schedule_step",0 )
     self.redis.set( "schedule_time_count",0 )
     self.redis.set( "schedule_time_max",0 )




  #
  #
  #  Next set of functions load data from IRRIGATION command
  #
  #
  #

  def load_auto_schedule( self, schedule_name):
     schedule_control = self.get_json_data( schedule_name )
 
     step_number      = len( schedule_control["schedule"] )
     
     ###
     ### load schedule start
     ###
     ###
     json_object = {}
     json_object["type"]            = "START_SCHEDULE"
     json_object["schedule_name"]   =  schedule_name
     json_object["step_number"]     =  step_number
     
     json_string = json.dumps( json_object)
     self.redis.lpush( "IRRIGATION_QUEUE", json_string )
     ###
     ### load step data
     ###
     ###
     for i in range(1,step_number+1):
        self.load_step_data( schedule_name, i ,None )
     ###
     ### load schedule end
     ###
     ###
     json_object = {}
     json_object["type"]            = "END_SCHEDULE"
     json_object["schedule_name"]   =  schedule_name
     json_object["step_number"]     =  step_number
     json_string = json.dumps( json_object)
     self.redis.lpush( "IRRIGATION_QUEUE", json_string  )
     
  





  # note schedule_step_time can be None then use what is in the schedule
  def load_step_data( self, schedule_name, schedule_step,  schedule_step_time  ):
     #print "schedule name ----------------->",schedule_name, schedule_step, schedule_step_time 
    
     temp = self.get_schedule_data( schedule_name, schedule_step)
     if temp != None :
        schedule_io = temp[0]
        schedule_time = temp[1]
        if  schedule_step_time == None:
            schedule_step_time = schedule_time
        
        json_object = {}
        json_object["type"]            = "IRRIGATION_STEP"
        json_object["schedule_name"]   =  schedule_name
        json_object["step"]            =  schedule_step
        json_object["io_setup"]        =  schedule_io
        json_object["run_time"]        =  schedule_step_time
        json_object["elasped_time"]    =  0
        json_string = json.dumps( json_object)
        print "step load",json_string
        self.redis.lpush(  "IRRIGATION_QUEUE", json_string )
     else:
       post_error("non_existant_schedule", remote, "plc_current" )




  # this is for loading user specified data
  def load_native_data( self, remote,bit,time ):
      json_object = {}
      json_object["type"]            = "IRRIGATION_STEP"
      json_object["schedule_name"]   = "MANUAL"
      json_object["step"]            = 1
      json_object["io_setup"]        =  [[remote, [bit], time ]]
      json_object["run_time"]        = time
      json_object["elasped_time"]    = 0
      json_string = json.dumps( json_object)
      print "native load",json_string
      self.redis.lpush( "IRRIGATION_QUEUE", json_string )
      print self.redis.llen("IRRIGATION_QUEUE")


  def get_schedule_data( self, schedule_name, schedule_step):
      schedule_control = self.get_json_data( schedule_name )
      if schedule_control != None:
         io_control = schedule_control["schedule"][schedule_step -1]
         m = io_control[0]
         schedule_time   = m[2]
         return [ io_control, schedule_time ]
      return None
 
  def get_json_data( self, schedule_name ):
     print("get json data ",schedule_name)
     sprinkler_ctrl = self.redis.get("sprinkler_ctrl")
     sprinkler_ctrl = json.loads( base64.b64decode( sprinkler_ctrl ))
     for j in sprinkler_ctrl :  
       if j["name"] == schedule_name:
          json_data=open(self.app_files+"/"+j["link"])
          return json.load(json_data)
         
     return None
      


  #
  # This function takes data from the IRRIGATION QUEUE And Transferrs it to the IRRIGATION_CELL_QUEUE
  # IRRIGATION_CELL_QUEUE only has one element in it
  #
  def load_irrigation_cell(self, chainFlowHandle, chainObj, parameters,event ): 
      ## if queue is empty the return

      ## this is for resuming an operation
      length =   self.redis.llen("IRRIGATION_CELL_QUEUE" )
      print "length 2 is ",length
      if length > 0:
        return "DISABLE" 

      
      length = self.redis.llen("IRRIGATION_QUEUE")
      print "length 1 is ",length
      if length == 0:
          return "RESET"

      json_string = self.redis.rpop(  "IRRIGATION_QUEUE" )
      print "json string is ",json_string
      json_object = json.loads(json_string)
      if json_object["type"] == "IRRIGATION_STEP":
         print "made it here ", json_string
         self.redis.lpush( "IRRIGATION_CELL_QUEUE", json_string )
         self.process_cell( chainFlowHandle, chainObj, parameters,event ) 
         return "DISABLE"

      if json_object["type"] == "START_SCHEDULE" :
        self.redis.set( "schedule_step_number", json_object["step_number"] ) 
        self.store_event_queue( "irrigation_schedule_start", json_object )
        return "RESET"

      if json_object["type"] == "END_SCHEDULE" :
        self.store_event_queue( "irrigation_schedule_stop", json_object )
        return "RESET"
   
      return "RESET"
   


  def check_redis_value( self, key):
     value =  self.redis.get( key )
     if value == None:
        value = 0
     else:
        value = float(value)
     return value


  def check_to_clean_filter(self, chainFlowHandle, chainObj, parameters,event ):
     cleaning_interval = self.check_redis_value( "cleaning_interval")
     if cleaning_interval == 0 :
          return  # no cleaning interval active
     
     flow_value   =  self.check_redis_value( "global_flow_sensor" )*self.flow_scale
     cleaning_sum =  self.check_redis_value( "cleaning_sum")
     cleaning_sum = cleaning_sum + flow_value
     #print "clean_filter",cleaning_interval, flow_value,cleaning_sum
     if cleaning_sum > cleaning_interval :
         self.redis.set("cleaning_sum",0)
         self.clean_filter_direct( chainFlowHandle, chainObj, parameters, event )   
     else:
         self.redis.set("cleaning_sum",cleaning_sum)


  def check_for_excessive_flow_rate( self, chainFlowHandle, chainObj, parameters,event ):
     flow_value   =  self.check_redis_value( "global_flow_sensor" )*self.flow_scale  
     max_flow_rate_cutoff = self.check_redis_value("max_flow_rate_cutoff")
     max_flow_rate_time   = self.check_redis_value("max_flow_rate_time" )
     #print "excessive_flow",flow_value, max_flow_rate_cutoff,max_flow_rate_time
     if max_flow_rate_cutoff == 0:
        return False  # feature is not turned on
     if flow_value > max_flow_rate_cutoff :
        temp = True
     else:
        temp = False
     self.excessive_flow_queue.append( temp)
     if len( self.excessive_flow_queue) > max_flow_rate_time:
       self.excessive_flow_queue.pop(0)
       returnValue = True
       for i in self.excessive_flow_queue:
          #print "i",i
          if i != True:

            
            return False
          
     else:
        returnValue = False
     #print "returnValue ",returnValue
     if returnValue == True:
       self.redis.set("SHUT_DOWN",1)
     return returnValue

  ###
  ###  These functions handle the irrigation_cell_queue
  ###


  def process_cell(self, chainFlowHandle, chainObj, parameters,event ):
     
     
     # check to see if something is in the queue
     length =   self.redis.llen( "IRRIGATION_CELL_QUEUE" )
     self.check_to_clean_filter( chainFlowHandle, chainObj, parameters,event )
     
     # check for excessive Flow
     #print "process_cell length",length
     if length > 0 :
         json_string                             = self.redis.lindex( "IRRIGATION_CELL_QUEUE",0 )
         json_object                             = json.loads(json_string)
         if json_object.has_key("clean_filter") == False:
            json_object["clean_filter"] = 0
         if ( self.clean_filter_flag == 1 ) :
              json_object["clean_filter" ] = 1
              self.clean_filter_flag = 0
        
          
         run_time                                = int( json_object["run_time"])
         elasped_time                            = int(json_object["elasped_time"])
         schedule_step                           = int(json_object["step"])
         step_number                             = json_object["step"]
         schedule_name                           = json_object["schedule_name"]
        
         print "made it here ",self.redis.get("SHUT_DOWN")
         if  self.check_redis_value("SHUT_DOWN") == 1:
              self.io.turn_off_io(json_object["io_setup"])
              self.io.disable_all_sprinklers()
              return #  System is not processing commands right now

         print "made it past shutdown"

         #print("json object", json_object)
         if elasped_time == 0  :  # this is one time initialization
           #print("made it init")
           self.redis.set("SKIP_STATION",0)
           self.excessive_flow_queue = []
           run_time  = self.eto_update( run_time , json_object["io_setup"] )
           #print("run time",run_time)
           self.io.load_duration_counters( run_time  )
           
           if  run_time  != 0: 
              #print("xxxxxxxxxxxxxxxxxxx")
              temp = self.io.turn_on_io(  json_object["io_setup"] )["active"]
              #print "turn on io",temp
              if temp == 0:
                 self.store_alarm_queue( "irrigation_io_abort", json_object )
                 
                 # disabling station because of high currents in sprinkler lines
                 station_by_pass = 1
              else:
                 
	         station_by_pass = 0
	   else:
              station_by_pass = 1
              self.store_event_queue( "irrigation_eto_abort", json_object )
	   
           if station_by_pass == 0:
             self.redis.set( "MASTER_VALVE_SETUP","ON")
             #print("made it past station by pass")
             elasped_time = 1
             self.redis.set( "sprinkler_ctrl_mode","AUTO")
             self.redis.set( "schedule_name", schedule_name )
             self.redis.set( "schedule_step_number", step_number )
             self.redis.set( "schedule_step", schedule_step )
             self.redis.set( "schedule_time_count", elasped_time )
             self.redis.set( "schedule_time_max",   run_time )  
             self.log_start_step( schedule_name, json_object["step"])
             json_object["elasped_time"] = elasped_time
             json_object["run_time"] = run_time
             json_string = json.dumps( json_object )
             flow = self.check_redis_value( "global_flow_sensor" )
             current = self.redis.lindex("coil_current_queue",0)
             self.log_step_data( schedule_name, step_number, elasped_time, flow, current )
	     self.redis.lset( "IRRIGATION_CELL_QUEUE", 0, json_string )
             #print "returning reset"
             returnValue =  "RESET"
           else:
             self.clean_up_irrigation_cell(json_object)
             #print "return contine"
             returnValue =  "CONTINUE"

         elif  self.check_redis_value("SKIP_STATION") == 1:
             self.redis.set("SKIP_STATION",0)
             self.redis.set( "MASTER_VALVE_SETUP","OFF")
             self.clean_up_irrigation_cell(json_object)
             self.store_event_queue( "manual_step_abort", json_object )
             print "skip step"
             returnValue = "DISABLE"
             return returnValue

         elif  run_time > elasped_time :
           #print "run time",run_time,elasped_time
           # These are the normal actions  
           if self.check_for_excessive_flow_rate(chainFlowHandle, chainObj, parameters,event ) == True:
                self.redis.set( "MASTER_VALVE_SETUP","OFF")
                self.clean_up_irrigation_cell(json_object)
                self.store_alarm_queue( "irrigation_excessive_flow_abort", json_object )
                print "excessive flow abort"
                returnValue = "DISABLE"
                return returnValue
               
           self.update_eto_queue_a( 1, json_object["io_setup"] )
           if self.io.turn_on_io( json_object["io_setup"] )["active"] == 1:
                self.redis.set( "MASTER_VALVE_SETUP","ON")
                elasped_time  = elasped_time +1
                self.redis.set( "schedule_time_count", elasped_time )
                json_object["elasped_time"] = elasped_time
                json_string = json.dumps( json_object )
                self.redis.lset( "IRRIGATION_CELL_QUEUE", 0, json_string )
                #print "normal reset"
                returnValue = "RESET"
           else:
             self.redis.set( "MASTER_VALVE_SETUP","OFF")
             self.clean_up_irrigation_cell(json_object)
             self.store_alarm_queue( "irrigation_io_abort", json_object )
             print "irrigation_io_abort"
             returnValue = "DISABLE"              
	   
 	
         else:
            print "normal end"
            self.update_eto_queue_a( 1, json_object["io_setup"] )
            self.redis.set( "MASTER_VALVE_SETUP","OFF")
            self.clean_up_irrigation_cell(json_object)
            returnValue = "DISABLE"
     
     
     else:
      #print "length 0 Continue"
      returnValue =  "DISABLE"
  
     print "cell returnValue is ",returnValue
     return returnValue







  def clean_up_irrigation_cell( self ,json_object ):
     self.redis.delete("IRRIGATION_CELL_QUEUE")
     self.redis.set( "schedule_name","offline" )
     self.redis.set( "schedule_step_number",0 )
     self.redis.set( "schedule_step",0 )
     self.redis.set( "schedule_time_count",0 )
     self.redis.set( "schedule_time_max",0 ) 
     self.redis.set( "sprinkler_ctrl_mode","AUTO")
     self.io.turn_off_io(json_object["io_setup"])
     self.io.disable_all_sprinklers()
     self.io.clear_duration_counters()
     self.log_step_stop()



  def log_step_data( self, schedule_name, step, time, flow, current ):
      self.store_event_queue( "step_data", { "schedule":schedule_name, "step":step, "elasped_data":time, "flow":flow, "current":current } )     

  def log_start_step( self, schedule_name, step):
    self.current_log_object = self.initialize_object( "current_log",schedule_name,step)
    self.flow_log_object = self.initialize_object( "flow_log",schedule_name,step )
    self.store_event_queue( "start_step", { "schedule":schedule_name, "step":step } )

  def log_step_stop( self ):

    self.store_object( self.current_log_object,"coil" )
    self.store_object( self.flow_log_object,"flow"    )
    obj = {}
    obj["coil"] = self.current_log_object
    obj["flow"] = self.flow_log_object
    self.store_event_queue( "irrigatation_store_object", obj )
    self.current_log_object = None
    self.flow_log_object = None

    
    
  def initialize_object( self, name,schedule_name,step ):
       obj                 = {}
       obj["name"]         = name
       obj["time"]         = time.time()
       obj["schedule_name"] = schedule_name
       obj["step"]          = step
       obj["fields"]        = {}
       #
       #  Add in limit data
       #
       #
       return obj

 


  def initialize_field( self, obj ,field):
     if obj["fields"].has_key(field) == False:
       obj["fields"][field]            = {}
       obj["fields"][field]["max"]     = -1000000
       obj["fields"][field]["min"]     =  1000000
       obj["fields"][field]["count"]   = 0
       obj["fields"][field]["data"]    = []
   

  def compute_object_statistics( self, obj ):
     print "compute object statistics", obj
     for j in obj["fields"] :
        temp = obj["fields"][j]
        temp["total"] = 0
        count = 0
        for  m in temp["data"]:
          count = count +1
          if count > 5: 
            temp["total"] = temp["total"] +m
         
        print "count ",count
        if count > 5:
          temp["average"] = temp["total"]/(count -5)
        else:
          temp["average"] = 0
        temp["std"] = 0
        count = 0
        for m in temp["data"]:
           count = count +1
           if count > 5 :
             temp["std"] = temp["std"] + (m -temp["average"])*(m-temp["average"])
             temp["std"] = math.sqrt(temp["std"]/(count-5))
           else:
             temp["std"] = 0


  def add_limits( self, obj, queue_type ):
       if queue_type == "flow":
         key = "log_data:flow:"+obj["schedule_name"]+":"+str(obj["step"])
       else:
         key = "log_data:coil:"+obj["schedule_name"]+":"+str(obj["step"])
       print "key",key
       composite_string = self.redis.lindex(key,0)
       if composite_string != None:
	  try:
	    composite_object = json.loads( composite_string )
	  except:
	    composite_object = None
       else:
	    composite_object = None
       obj["limits"] = composite_object
	    


  def store_object( self, obj ,queue_type ):
    if obj == None:
       return
    #self.add_limits(obj, queue_type )
    self.compute_object_statistics( obj )
    queue = "log_data:"+queue_type+":"+obj["schedule_name"]+":"+str(obj["step"])
    json_data = json.dumps(obj)
    
    self.redis.lpush( queue, json_data )
    self.redis.ltrim( queue,0,100)

                                                                                                                                                                                 
  def store_event_queue( self, event, data ):
    log_data = {}
    log_data["event"] = event
    log_data["data"]  = data
    log_data["time"]  = time.time()
    json_data = json.dumps(log_data)
    json_data = base64.b64encode(json_data)
    self.redis.lpush( "cloud_event_queue", json_data)
    self.redis.ltrim( "cloud_event_queue", 0,800)
  

  def store_alarm_queue( self, event, data ):
    log_data = {}
    log_data["event"] = event
    log_data["data"]  = data
    log_data["time" ] = time.time()

    json_data = json.dumps(log_data)
    json_data = base64.b64encode(json_data)
    self.redis.lpush( "cloud_alarm_queue", json_data)
    self.redis.ltrim( "cloud_alarm_queue", 0,800)


## 1 gallon is 0.133681 ft3
## assuming a 5 foot radius
## a 12 gallon/hour head 0.2450996343 inch/hour
## a 14	gallon/hour head 0.2859495733 inch/hour
## a 16	gallon/hour head 0.3267995123 inch/hour
##
##
##
##
## capacity of soil
## for silt 2 feet recharge rate 30 % recharge inches -- .13 * 24 *.3 = .936 inch 
## for sand 1 feet recharge rate 30 % recharge inches -- .06 * 12 *.3 = .216 inch
##
## recharge rate for is as follows for 12 gallon/hour head:
## sand 1 feet .216/.245 which is 52 minutes
## silt 2 feet recharge rate is 3.820 hours or 229 minutes
##
## {"controller":"satellite_1", "pin": 9,  "recharge_eto": 0.216, "recharge_rate":0.245 },
## eto_site_data






  def eto_update( self, schedule_run_time, io_list ):
     file_data = open(self.app_files+"/"+"eto_site_setup.json" )
     self.eto_site_data = json.load(file_data  )
     manage_eto = self.redis.get( "ETO_MANAGE_FLAG" )
     if manage_eto == None:
        manage_eto = 1
        self.redis.set( "ETO_MANAGE_FLAG",manage_eto)
     manage_eto = int( manage_eto )   
       
     if manage_eto == 1:
         sensor_list = self.find_queue_names( io_list )
         if len(sensor_list) != 0:
            run_time = self.find_largest_runtime( schedule_run_time, sensor_list )
            if run_time < schedule_run_time :
               schedule_run_time = run_time 
         #self.update_eto_queue(schedule_run_time, sensor_list )
   
     return schedule_run_time

  def find_queue_names( self, io_list ):
     eto_values = []
     for j in io_list:
        controller = j[0]
        bit        = j[1]
        bit        = bit[0] 
        index = 0
        for m in self.eto_site_data:
          
          if (m["controller"] == controller) and (m["pin"] == bit): 
             queue_name = "ETO_RESOURCE"+"|"+controller+"|"+str(bit)
             data = self.redis.get(  queue_name )
             eto_values.append( [index, data, queue_name ] )
          index = index +1
             
          
         
     #print "queue names is ",eto_values   
     return eto_values


  def find_largest_runtime( self, run_time, sensor_list ):

     runtime = 0
     for j in sensor_list:
        index = j[0]
        deficient = float(j[1])
        eto_temp = self.eto_site_data[index]
        recharge_eto = float( eto_temp["recharge_eto"] )
        recharge_rate = float(eto_temp["recharge_rate"])
        if float(deficient) > recharge_eto :
            runtime_temp = (deficient  /recharge_rate)*60
            if runtime_temp > runtime :
               runtime = runtime_temp
 
     print "run time",runtime
     return runtime


  def update_eto_queue_a( self, run_time, io_list ):
     
     file_data = open(self.app_files+"/"+"eto_site_setup.json" )
     self.eto_site_data = json.load(file_data  )

     manage_eto = self.redis.get( "ETO_MANAGE_FLAG" )
     if manage_eto == None:
        manage_eto = 1
        self.redis.set( "ETO_MANAGE_FLAG",manage_eto)
     manage_eto = int( manage_eto )   
       
     if manage_eto == 1:
         sensor_list = self.find_queue_names( io_list )
         if len(sensor_list) != 0:
             self.update_eto_queue(run_time,sensor_list)

  def update_eto_queue( self, run_time, sensor_list ):
  
     for l in  sensor_list:
        j_index = l[0]
        queue_name = l[2]
        j = self.eto_site_data[ j_index ]
        deficient = self.redis.get(  queue_name )
        if deficient == None:
           deficient = 0
        else:
          deficient = float(deficient)
        recharge_rate = float(j["recharge_rate"])
        deficient = deficient - (recharge_rate/60)*run_time 
        if deficient < 0 :
           deficient = 0 
        self.redis.set( queue_name, deficient )

     




####
####  
####
####
####

class Monitor():

  def __init__(self,redis, redis_15   ):
      self.redis       = ir_ctl.redis
      self.remote_io = ir_ctl.remote_io
      self.redis_15  = ir_ctl.redis_15
      self.log_current   = ir_ctl.sprinkler_control.log_coil_current
      self.log_flow      = ir_ctl.sprinkler_control.log_flow_rate


  
    
  def update_time_stamp( self, chainFlowHandle, chainObj, parameters, event ):
      self.redis.set( "sprinkler_time_stamp", time.time() )



  def measure_flow_rate ( self, chainFlowHandle, chainObj, parameters,event ):
     results = self.remote_io.get_flow_sensors()
     print "results",results
     i = 1
     for j in  results :
       flow_value     = j["flow_value"]
       title          = j["title"]

       if self.log_flow != None :
          self.log_flow( title,flow_value )
       self.redis_15.lpush("redis_flow_queue_"+str(i),flow_value )
       self.redis_15.ltrim("redis_flow_queue_"+str(i),0,800)
       if i == 1 :
         self.redis.set("global_flow_sensor",flow_value )
         self.store_event_queue( "global_flow_sensor", { "flow":flow_value } )
       self.store_event_queue("flow_sensor", {"title":title, "value":flow_value } ) 
       i = i+1

  def measure_current( self, chainFlowHandle, chainObj, parameters,event ): 
     results = self.remote_io.get_current_sensors()
     self.redis_15.lpush("plc_current_queue",results["plc_current"] )
     self.redis_15.ltrim("plc_current_queue",0,800)
     self.redis_15.lpush("coil_current_queue",results["coil_current"] )
     self.redis_15.ltrim("coil_current_queue",0,800)
     self.redis.set( "coil_current", results["coil_current"] )
     self.redis.set( "plc_current",  results["plc_current"] )
     self.store_event_queue( "coil_current", { "coil_current":results["coil_current"]  } ) 
     self.store_event_queue( "plc_current", { "plc_current":results["plc_current"] } ) 
     if self.log_current  != None:
        self.log_current( results["coil_current"] )
    

    

class Valve_Control():
  def __init__(self, redis, io  ):
      self.redis           = redis
      self.io              = io
     
  # tested
  def check_switches_set( self, chainFlowHandle, chainObj, parameters, event ):
      returnValue = False
      if  event['name'] == 'TIME_TICK':
          temp = int(redis.get("main_valve_set_switch"))
          if temp != 0: 
               redis.set("main_valve_set_switch",0)
               returnValue = True
          else:
               returnValue = False
      return returnValue

 
  def detect_switch_off( self, chainFlowHandle, chainObj, parameters, event ):
      returnValue = "CONTINUE"
      if  event['name'] == 'TIME_TICK' :
          temp = int(redis.get("main_valve_reset_switch"))
          if temp != 0: 
             redis.set("main_valve_reset_switch",1)
             chainFlowHandle.disable_chain_base( ["main_valve_timed_off"] )
             returnValue = "HALT"
      return returnValue
  
  
  def turn_on( self, chainFlowHandle, chainObj, parameters, event ):
           self.io.turn_on_main_valves()
  
  def turn_off_if_no_in_queue( self, chainFlowHandle, chainObj, parameters, event ):
        length =   self.redis.llen( "IRRIGATION_CELL_QUEUE" )
        if length == 0 :
          self.io.turn_off_main_valves()
          self.io.turn_off_cleaning_valves()
  
  
  def verify_off_switch_not_set( self, chainFlowHandle, chainObj, parameters, event ):
      returnValue = True
      if  event['name'] == 'TIME_TICK' :
             temp = int(redis.get("main_valve_reset_switch"))
             if temp != 0: 
                returnValue = False
                length =   self.redis.llen( "IRRIGATION_CELL_QUEUE" )
                if length == 0:
                  self.io.turn_off_main_valves()
             else:
               returnValue = True
      return returnValue
 
  def insure_that_valve_on( self, chainFlowHandle, chainObj, parameters, event ):
      
      if( event['name'] == 'MINUTE_TICK') :
          self.turn_on( chainFlowHandle, chainObj, parameters, event )
      
     
##
## Tested
##
##
class Remote_Io():
  def __init__(self, redis ):
       self.redis = redis
  
  def do_commands( self, parameters ):
      temp = json.dumps( parameters )
      temp = base64.b64encode(temp)
      self.redis.lpush( "io_ctrl_queue", temp )
      
  def do_rpc( self, parameters ):
      parameters["return_queue"] = "irr_rpc_queue"
      self.redis.delete("irr_rpc_queue")
      temp = json.dumps( parameters )
      temp = base64.b64encode(temp)
      self.redis.lpush( "io_ctrl_queue", temp )
      if parameters.has_key("time") :
         wait_time = parameters["time"]
      else:
         wait_time = 1000
        
      for i in range(0, wait_time ):
        time.sleep(.01) # wait for up to 10 seconds 
        if self.redis.llen("irr_rpc_queue") > 0:
            temp = self.redis.rpop("irr_rpc_queue")
            temp = base64.b64decode(temp)
            temp = json.loads(temp)
            return temp
            
      raise Exception("I/O_Server_TimeOut")

  
  # tested
  def modbus_read_mode( self ):
      temp = {}
      temp["command"] = "modbus_read_mode"
      self.do_commands( temp )
  #tested    
  def modbus_read_mode_switch( self  ):
      temp = {}
      temp["command"] = "modbus_read_mode_switch"
      self.do_commands( temp )
  #tested
  def modbus_read_wd_flag( self  ):
      temp = {}
      temp["command"] = "modbus_read_wd_flag"
      self.do_commands( temp )
  #tested
  def modbus_write_wd_flag( self  ):
      temp = {}
      temp["command"] = "modbus_write_wd_flag"
      self.do_commands( temp )


  #tested
  def construct_modbus_counters( self ):
      temp = {}
      temp["command"] = "construct_modbus_counters"
      self.do_commands( temp )
  #tested
  def turn_on_cleaning_valves( self ):
      temp = {}
      temp["command"] = "turn_on_cleaning_valves"
      self.do_rpc( temp )
  #tested
  def turn_off_cleaning_valves(self):
      temp = {}
      temp["command"] = "turn_off_cleaning_valves"
      self.do_rpc( temp )
  #tested
  def turn_on_main_valves( self ):
      self.redis.set( "MASTER_VALVE_SETUP","ON")
      temp = {}
      temp["command"] = "turn_on_main_valves"
      self.do_rpc( temp )
  #tested
  def turn_off_main_valves( self ):
      self.redis.set( "MASTER_VALVE_SETUP","OFF")
      temp = {}
      temp["command"] = "turn_off_main_valves"
      self.do_rpc( temp )
  #tested
  def turn_on_io( self , io_setup ):
      temp = {}
      temp["command"] = "turn_on_io"
      temp["io_setup"]  = json.dumps( io_setup )
      return self.do_rpc( temp )
 
  #tested
  def turn_off_io( self, io_setup ):
      temp = {}
      temp["command"] = "turn_off_io"
      temp["io_setup"]  = json.dumps( io_setup )
      self.do_rpc( temp )
  #tested
  def check_switches_set( self ):
      temp = {}
      temp["command"] = "check_switches_set"
      return_obj = self.do_rpc( temp )
      return return_obj["return_code"]
  #tested
  def detect_switch_off(self):
      temp = {}
      temp["command"] = "detect_switches_off"
      return_obj = self.do_rpc( temp )
      return return_obj["return_code"]
  #tested
  def get_current_sensors( self ):
      temp = {}
      temp["command"] = "measure_current"
      return_obj = self.do_rpc( temp )
      return return_obj["return_code"]
  #tested
  def get_flow_sensors( self ):
      temp = {}
      temp["command"] = "measure_flow_rate"
      return_obj = self.do_rpc( temp )
      return return_obj["return_code"]

  #tested
  def clean_filter(self):
      temp = {}
      temp["command"] = "clean_filter"
      temp["time" ]  = 1000 # 100 second wait
      self.do_rpc( temp )
    
  #tested
  def disable_all_sprinklers( self ):
      self.turn_off_main_valves()
      temp = {}
      temp["command"] = "disable_all_sprinklers"
      temp["time" ]  = 2000 # 20 second wait
      self.do_rpc( temp )
  
  #tested
  def load_duration_counters(self, time_duration  ): 
      temp = {}
      temp["command"] = "load_duration_counters"
      temp["time_duration"] = time_duration
      self.do_rpc(temp)    
  #tested
  def clear_duration_counters(self):
     temp = {}
     temp["command"] = "clear_duration_counters"
     self.do_rpc(temp)


class Watch_Dog_Client():
   def __init__(self, redis, directory, key, description ):
       print "init",key,description
       self.redis      = redis
       self.directory  = directory
       self.key        = key
       self.description  = description
       self.redis.hset(directory,key,None)
       self.pat_wd( None, None, None, None)
   

   def pat_wd( self, chainFlowHandle, chainObj, parameters, event ):
       print "made it here ","key",self.key
       self.redis.delete( self.key )
       temp = {}
       temp["time"]    = time.time()
       temp["max_dt"]  = 5*60
       temp["pid"]     = os.getpid()
       temp["description"] = self.description
       self.redis.set( self.key, json.dumps(temp) )


      

if __name__ == "__main__":

   import time    
   import redis
   import modbus_UDP
   import json
   import base64
   import os
   import click
   from   remote_devices import *
   from   io_ctrl import *


   plc_click                = click.PLC_Click()   
   modbus_udp               = modbus_UDP.ModbusUDPClient("192.168.1.84")
   alarm_queue              = AlarmQueue( redis )
   watch_dog_control        = WatchDogControl( modbus_udp, alarm_queue, remote_devices,{"CLICK":plc_click} )
   #irrigation_control       = IrrigationControl( modbus_udp, alarm_queue, remote_devices,main_valve_list,remote_io, {"CLICK":plc_click} )




   class Irrigation_Control( redis_db_handle, redis_db_port, redis_db_number):
       def __init__(self, app_files, system_files ):
           self.redis_handle                        = redis.StrictRedis( redis_db_handle,redis_db_port, redis_db_number )
           #self.redis_15                     = redis.StrictRedis(ho, port=6379, db=15)
           self.modbus_udp                   = modbus_UDP.ModbusUDPClient(redis_io_ip)
           self.alarm_queue                  = AlarmQueue( self.handle )
           self.watch_dog_control            = WatchDogControl( modbus_udp, alarm_queue, remote_devices,{"CLICK":plc_click} )
           #self.irrigation_io                = IrrigationControl( modbus_udp, alarm_queue, remote_devices,main_valve_list,remote_io, {"CLICK":plc_click} )
           self.device_directory             = "WD_DIRECTORY"
           self.app_files                    = app_files
           self.system_files                 = system_files
           #self.remote_io                    = Remote_Io( self.redis)
           #self.valve_control                = Valve_Control( self.redis, self.irrigation_io )
           #self.sprinkler_control            = Sprinkler_Control( self )
           #self.monitor                      = Monitor(  self )
           self.wc                           = Watch_Dog_Client(self., self.device_directory,"irrigation_ctrl","irrigation control")
           self.wc.pat_wd( None, None, None, None )


   ir_ctl = Irrigation_Control("/media/mmc1/app_data_files","/media/mmc1/system_data_files")

#
# Adding chains
#import sys
   sys.path.append('../py_cf')
   import mymodule
   cf = py_cf.CF_Interpreter()

   '''


   cf.define_chain( "plc_monitor_control_queue", True ) 
   cf.insert_link( "link_1","One_Step", [ ir_ctl.sprinkler_control.dispatch_sprinkler_mode ] ) 
   cf.insert_link( "link_2","Wait",     [ ir_ctl.sprinkler_control.check_for_updates       ] ) 
   cf.insert_link( "link_3","Reset",    [] )
  




   cf.define_chain("monitor_irrigation_job_queue", True )
   cf.insert_link( "link_1",  "WaitEvent",[ "TIME_TICK" ] )
   cf.insert_link( "link_2",  "Code",[ ir_ctl.sprinkler_control.load_irrigation_cell ] )
   cf.insert_link( "link_3", "Log",["loading irrigation cell"] )
   cf.insert_link( "link_4",  "Enable_Chain",[["monitor_irrigation_cell" ]])
   cf.insert_link( "link_5",  "WaitEvent",[ "CELL_DONE" ] )
   cf.insert_link( "link_6",  "Reset",[] )


   cf.define_chain("monitor_irrigation_cell", False )
   cf.insert_link( "link_1",  "WaitEvent",[ "MINUTE_TICK" ] )
   cf.insert_link( "link_2",  "Code",[ ir_ctl.sprinkler_control.process_cell ] )
   cf.insert_link( "link_3",  "SendEvent",["CELL_DONE"] ) 
   cf.insert_link( "link_4",  "Disable_Chain",[["monitor_irrigation_cell" ]])

   '''   
   #tested
   cf.define_chain("plc_watch_dog", True ) 
   cf.insert_link( "link_1",  "Log",        ["plc watch dog thread"] )
   cf.insert_link( "link_4",  "One_Step",   [ ir_ctl.watch_dog_control.modbus_read_wd_flag  ]      )
   cf.insert_link( "link_4",  "One_Step",   [ ir_ctl.watch_dog_control.modbus_write_wd_flag  ]      )
   cf.insert_link( "link_6",  "WaitEvent",  [ "MINUTE_TICK" ] )
   cf.insert_link( "link_7",  "Reset",    [] )

   #tested
   cf.define_chain("watch_dog_thread",True)
   cf.insert_link( "link_1","WaitTod",["*","*","*",30 ])
   cf.insert_link( "link_2","One_Step",[ ir_ctl.wc.pat_wd ])
   cf.insert_link( "link_3","WaitTod",["*","*","*",55 ])
   cf.insert_link( "link_4","Reset",[])  

   #tested
   #cf.define_chain("Reboot message", True)  # send reboot message on reboot
   #cf.insert_link( "link_2", "One_Step", [ ir_ctl.sprinkler_control.send_reboot_msg ] )
  

   '''
   cf.define_chain("Clean Filter", True)
   cf.insert_link( "link_1", "WaitTod", ["*",13,"*","*"] )
   cf.insert_link( "link_2", "One_Step", [ ir_ctl.sprinkler_control.irrigation_io.disable_all_sprinklers ] )
   cf.insert_link( "link_3", "One_Step", [ ir_ctl.sprinkler_control.irrigation_io.turn_off_cleaning_valves ] )
   cf.insert_link( "link_4", "One_Step", [ ir_ctl.sprinkler_control.irrigation_io.turn_on_main_valves ] )
   cf.insert_link( "link_5", "WaitTime", [100] )
   cf.insert_link( "link_6", "One_Step", [ ir_ctl.sprinkler_control.irrigation_io.turn_off_main_valves ] ) 
   cf.insert_link( "link_7", "One_Step", [ ir_ctl.sprinkler_control.irrigation_io.turn_on_cleaning_valves ] )   
   cf.insert_link( "link_8", "WaitTime", [40] )    
   cf.insert_link( "link_9", "One_Step", [ ir_ctl.sprinkler_control.irrigation_io.turn_on_main_valves ] )    
   cf.insert_link( "link_10", "WaitTime", [20] )
   cf.insert_link( "link_11", "One_Step",  [ ir_ctl.sprinkler_control.irrigation_io.turn_off_main_valves ] ) 
   cf.insert_link( "link_12", "One_Step",  [ ir_ctl.sprinkler_control.irrigation_io.turn_off_cleaning_valves ] )
   cf.insert_link( "link_13", "One_Step", [ ir_ctl.sprinkler_control.irrigation_io.disable_all_sprinklers ] )
   cf.insert_link( "link_14", "WaitTod", ["*",14,"*","*" ] )
   cf.insert_link( "link_15",  "Reset",[] )

   cf.define_chain("Check Direct Off", True)
   cf.insert_link( "link_1", "WaitTod", ["*",12,"*","*"] )
   cf.insert_link( "link_3", "One_Step", [ ir_ctl.sprinkler_control.check_off_direct ] )
   cf.insert_link( "link_4", "WaitTod", ["*",13,"*","*" ] )
   cf.insert_link( "link_5",  "Reset",[] )
   '''



   #cf.define_chain("monitor_flow_rate", True)
   #cf.insert_link(  "link_1",  "WaitEvent",[ "MINUTE_TICK" ] )
   #cf.insert_link( "link_1",  "Log",      ["Monitor flow rate"] )
   #cf.insert_link(  "link_2",  "One_Step", [ ir_ctl.monitor.measure_flow_rate ] )
   #cf.insert_link(  "link_3",  "One_Step", [ ir_ctl.monitor.measure_current ] )
   #cf.insert_link(  "link_4",  "One_Step", [ ir_ctl.monitor.update_time_stamp ] )
   #cf.insert_link(  "link_5",  "Reset",[] )

   #cf.define_chain
   '''
   cf.define_chain("clear_modbus_statistics", True)
   cf.insert_link( "link_1", "WaitTod", ["*",8,"*","*"] )
   cf.insert_link( "link_2", "One_Step", [ ir_ctl.clear_modbus_statistics.construct_modbus_counters ] )
   cf.insert_link( "link_3", "WaitTod", ["*",9,"*","*" ] )
   cf.insert_link( "link_4",  "Reset",[] )




   cf.define_chain("manual_main_valve_on",True)
   cf.insert_link( "link_0",   "Log",["start"] )
   cf.insert_link( "link_1",    "Code", [ ir_ctl.valve_control.turn_off_if_no_in_queue ])
   cf.insert_link( "link_test", "Log",["valve off"] )
   cf.insert_link( "link_2",    "Wait",     [ ir_ctl.valve_control.check_switches_set ] )
   cf.insert_link( "link_3",    "Verify",   [ ir_ctl.valve_control.verify_off_switch_not_set ] )
   cf.insert_link( "link_4",    "One_Step", [ ir_ctl.valve_control.turn_on] )
   cf.insert_link( "link_test", "Log",["valve on"] )
   cf.insert_link( "link_5",    "Code",     [  ir_ctl.valve_control.insure_that_valve_on ] )
   cf.insert_link( "link_6",    "WaitHour",  [9] )
   cf.insert_link( "link_7",    "One_Step", [  ir_ctl.valve_control.turn_off_if_no_in_queue ])
   cf.insert_link( "link_8",    "Log",[ "reset" ] )
   cf.insert_link( "link_9",    "Reset",    [] )
  
  
   cf.define_chain("main_valve_timed_off",False)
   cf.insert_link( "link_1",  "Code", [  ir_ctl.valve_control.detect_switch_off ] )
   cf.insert_link( "link_4",    "One_Step", [ ir_ctl.valve_control.turn_on] )
   cf.insert_link( "link_2",  "Code", [ ir_ctl.valve_control.insure_that_valve_on ] )
   cf.insert_link( "link_3",  "WaitHour",  [9] )
   cf.insert_link( "link_4",  "One_Step", [ ir_ctl.valve_control.turn_off_if_no_in_queue ])
   cf.insert_link( "link_5",  "Halt",    [] )

   ''' 




#
# Executing chains
#
   cf_environ = py_cf.Execute_Cf_Environment( cf )
   cf_environ.execute()


#
#
#  Test Code
#  for individual commands
#
#

#ir_ctl.plc_watch_dog.modbus_read_mode(None,None,None,None)
#ir_ctl.plc_watch_dog.modbus_read_mode_switch( None,None,None,None) 
#ir_ctl.plc_watch_dog.modbus_read_wd_flag( None,None,None,None)
#ir_ctl.plc_watch_dog.modbus_write_wd_flag( None,None,None,None)
#ir_ctl.remote_io.construct_modbus_counters()
#ir_ctl.remote_io.turn_off_main_valves()
#ir_ctl.remote_io.clean_filter()
#ir_ctl.remote_io.disable_all_sprinklers()
#io_setup = [["satellite_1", [12], 10]]
#ir_ctl.remote_io.turn_on_io( io_setup )
#time.sleep(200)
#ir_ctl.remote_io.turn_off_io( io_setup )
#print( "check switches set", ir_ctl.remote_io.check_switches_set())
#print( "detect_switch_off",  ir_ctl.remote_io.detect_switch_off())
#ir_ctl.remote_io.load_duration_counters(  10  )
#ir_ctl.remote_io.clear_duration_counters()
#print("current sensors",ir_ctl.remote_io.get_current_sensors())
#print("flow sensors",ir_ctl.remote_io.get_flow_sensors())
#
#print( "done")
       
     

      

