
class WatchDogException(Exception):
    """Exception raised for errors in the Watch Dog.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg




class WatchDogControl():
   def __init__(self, io_server , alarm_queue, remote_devices,plc_click ):
        self.alarm_queue     = alarm_queue
        self.remote_devices  = remote_devices
        self.io_server       = io_server
        self.plc_click       = plc_click


   def modbus_check_mode_switches( self,*arg ):
       return_value = True
       for j in self.remote_devices.keys():
           i = self.remote_devices[j]
           if i["type"] == "CLICK" :
               plc = self.plc_click[i["type"]]
               if plc.check_mode_switch( self.io_server, i ) == False:
                  return False
       return True

          
            
  
   def modbus_read_wd_flag( self,*arg ):  #variable arguments put in so that function can be called by chain flow
       for j in self.remote_devices.keys():
           i = self.remote_devices[j]
           if i["type"] == "CLICK":
               plc = self.plc_click[i["type"]]
               plc.read_wd_flag( self.io_server, i )

       return "CONTINUE"
       

   def modbus_write_wd_flag( self,*arg  ): #variable arguments put in so that function can be called by chain flow
     
       for j in self.remote_devices.keys():
          i = self.remote_devices[j]
          if i["type"] == "CLICK":
               plc    = self.plc_click[i["type"]]
               plc.write_wd_flag( self.io_server, i )
              
       return "CONTINUE"  
        
class IO_mgr():
   def __init__(self,redis_server, io_server, plc_interface, remote_devices, gpio_input_devices, analog_devices, counter_devices ):
      self.redis                    = redis_server
      self.io_server                = io_server
      self.gpio_input_devices       = gpio_input_devices
      self.analog_devices           = analog_devices
      self.counter_devices          = counter_devices
      self.plc_interface            = plc_interface
      self.remote_devices           = remote_devices
      self.counter_time_ref         = time.time()


   def clear_gpio_in( self,*arg):
       for redis_key, device in self.gpio_input_devices.items():
           self.redis.hset("GPIO_IN",redis_key,0)
       return "CONTINUE"        
 
   def measure_gpio_in( self ,*arg):
       for redis_key, device in self.gpio_input_devices.items():
           if device["type"] == "CLICK":
               remote       = device["remote"]
               address      = self.remote_devices[remote]["address"]
               plc          = self.plc_interface["CLICK"]
               plc.measure_gpio_in( self.redis, self.io_server, address, device, redis_key )
       return "CONTINUE"        
                

   def measure_gpio_in_pin( self, redis_key ):
       device     = self.gpio_input_devices[redis_key]
       if device["type"] == "CLICK":
          remote     = device["remote"]
          address    = self.remote_devices[remote]["address"]
          plc        = self.plc_interface[ device["type"] ]
          return     plc.measure_gpio_in( self.redis, self.io_server, address, device, redis_key )
       else:
          return None
   
   def measure_analog( self,*arg ):
       for redis_key, device in self.analog_devices.items():
           
           if device["type"] == "CLICK":
               remote       = device["remote"]
               address      = self.remote_devices[remote]["address"]
               plc          = self.plc_interface["CLICK"]
               plc.measure_analog( self.redis, self.io_server, address,  device,redis_key )
       return "CONTINUE"              
              
   def measure_analog_pin( self, redis_key ):
       device     = self.analog_devices[redis_key]
       if device["type"] == "CLICK":
          remote     = device["remote"]
          address    = self.remote_devices[remote]["address"]
          plc        = self.plc_interface[ device["type"] ]
          return     plc.measure_analog( self.redis, self.io_server, address, device, redis_key )
          
             



   def measure_counters( self,*arg ):
         deltat = time.time() - self.counter_time_ref
         self.counter_time_ref = time.time()
         for redis_key,device in self.counter_devices.items():
            if device["type"] == "CLICK":
               plc_interface   = self.plc_interface["CLICK"]
               remote          = device["remote"]
               address         = self.remote_devices[ remote]["address"]
               plc_interface.measure_counters( self.redis,self.io_server, address, device, redis_key, deltat )




class IrrigationIo():
   def __init__(self, io_server, alarm_queue, remote_devices, main_valve_list,remote_io, plc_map ):
       self.io_server           = io_server
       self.alarm_queue         = alarm_queue
       self.remote_devices      = remote_devices
       self.main_valve_list   = main_valve_list
       self.plc_map             = plc_map
       self.remote_io           = remote_io

   def disable_all_sprinklers( self,*arg ):
       return_value = True
       for j in self.remote_devices.keys():
           i = self.remote_devices[j]
           if i["type"] == "CLICK" :
                self.pcl_map[i["type"]].disable_all_sprinklers( i, self.io_server )
              
  

   def turn_on_main_valves( self,*arg ):
       for main_valve in self.main_valve_list:
           if main_valve["type"] == "CLICK":
               address = remote_devices[ main_valve["remote"] ]["address"]
               self.plc_map[main_valve["type"]].turn_on_main_valve( self.io_server,  address, main_valve )
            
    
   def turn_off_main_valves( self,*arg ):
       for main_valve in self.main_valve_list:
           if main_valve["type"] == "CLICK":
               address = remote_devices[ main_valve["remote"] ]["address"]
               self.plc_map[main_valve["type"]].turn_off_main_valve( self.io_server,  address, main_valve )

   def turn_on_cleaning_valves( self,*arg ):
       for main_valve in self.main_valve_list:
           if main_valve["type"] == "CLICK":
               address = remote_devices[ main_valve["remote"] ]["address"]
               self.plc_map[main_valve["type"]].turn_on_cleaning_valve( self.io_server,  address, main_valve )

   def turn_off_cleaning_valves( self,*arg ):
       for main_valve in self.main_valve_list:
           if main_valve["type"] == "CLICK":
               address = remote_devices[ main_valve["remote"] ]["address"]
               self.plc_map[main_valve["type"]].turn_off_cleaning_valve( self.io_server,  address, main_valve )


 
   #
   #  Clearing Duration counter is done through a falling edge
   #  going from 1 to 0 generates the edge
   def clear_duration_counters( self,*arg ):
       for j in self.remote_io.keys():
           i = self.remote_io[j]
           if i["type"] == "CLICK":
               address      = self.remote_devices[j]["address"]
               self.plc_map[remote_dev["type"]].clear_duration_counters( i,address,self.io_server )



   def load_duration_counters( self, time_duration ,*arg):
       duration = (time_duration*60)+15  # convert minutes to seconds
       for j in self.remote_io.keys():
           i = self.remote_io[j]
           if i["type"] == "CLICK":
               address      = self.remote_devices[j]["address"]
               self.plc_map[remote_dev["type"]].load_duration_counters(i ,address,self.io_server ,duration)



   def turn_off_io( self , io_setup ):
      # io_setup is a list of dict { "remote":xx , "bits":[1,2,3,4]
      self.turn_off_main_valves_server()
      for i in io_setup:      
         remote        = i["remote"]
         remote_dev    = self.remote_devices[remote]
         address       = remote_dev["address"]
         bits       = i["bits"]  # list of outputs on remote to turn off
         if remote_dev["type"] == "CLICK":
             self.plc_map[remote_dev["type"]].turn_on_off( address, bits )

   def turn_on_valve( self ,io_setup ):
  
      for i in io_setup:      
         remote        = io_setup["remote"]
         remote_dev    = self.remote_devices[remote]
         address       = remote_dev["address"]
         bits       = i["bits"]  # list of outputs on remote to turn off
         if remote_dev["type"] == "CLICK":
             self.plc_map[remote_dev["type"]].turn_on_io( address, bits )



   def turn_on_io( self ,io_setup ):
      self.turn_on_main_valves_server()
      for i in io_setup:      
         remote        = i["remote"]
         remote_dev    = self.remote_devices[remote]
         address       = remote_dev["address"]
         bits       = i["bits"]  # list of outputs on remote to turn off
         if remote_dev["type"] == "CLICK":
             self.plc_map[remote_dev["type"]].turn_on_io( address, bits )


if __name__ == "__main__": 
   import time    
   import redis
   import modbus_UDP
   import json
   import base64
   import os
   import click
   from   remote_devices import *

   plc_click                = click.PLC_Click()
   redis                    = redis.StrictRedis( host = "192.168.1.82", port=6379, db = 0 )
   modbus_udp               = modbus_UDP.ModbusUDPClient("192.168.1.84")
   alarm_queue              = AlarmQueue( redis )
   watch_dog_control        = WatchDogControl( modbus_udp, alarm_queue, remote_devices,  {"CLICK":plc_click} )
   irrigation_control       = IrrigationIo( modbus_udp, alarm_queue, remote_devices,main_valve_list,irrigation_io, {"CLICK":plc_click} )
   io_mgr = IO_mgr( redis, modbus_udp, {"CLICK":plc_click}, remote_devices, gpio_input_devices, analog_devices, counter_devices )
   
   if watch_dog_control.modbus_check_mode_switches() == True:
      print "plc with mode set properly"
   else:
      print "plc with mode not properly set"
   print "watch dog read", watch_dog_control.modbus_read_wd_flag()
   print "watch dog write",watch_dog_control.modbus_write_wd_flag()
   print "watch dog read", watch_dog_control.modbus_read_wd_flag()
   #print modbus_udp.read_bit(100,23)
   #modbus_udp.write_bit(100,23,1)
   #print modbus_udp.read_bit(100,23)
   #modbus_udp.write_bit(100,23,0)
   #print modbus_udp.read_bit(100,23)
   #print "disable_all_sprinkers",  irrigation_control.disable_all_sprinklers()
   #print modbus_udp.read_bit( 100, plc_click.click_bit_address["C1"])
   #print "turn on main valve"
   irrigation_control.turn_on_main_valves()
   irrigation_control.turn_on_cleaning_valves()
   time.sleep(2)
   io_mgr.measure_analog()
   #irrigation_control.turn_off_main_valves()
   time.sleep(2)
   
   
   
#   irrigation_control.disable_all_sprinklers()
#   irrigation_control.clear_duration_counters()
#   irrigation_control.load_duration_counters( 15 )
   
   io_mgr.clear_gpio_in()
   print  io_mgr.measure_gpio_in_pin( "main_valve_set_switch" )
   io_mgr.measure_gpio_in()
   irrigation_control.turn_off_main_valves()
   irrigation_control.turn_off_cleaning_valves()
   time.sleep(2)
   print io_mgr.measure_analog_pin("coil_current" )
   #irrigation_control.turn_on_main_valves()
   #time.sleep(2)
   #io_mgr.measure_analog()
   #irrigation_control.turn_off_main_valves()
   #time.sleep(2)
   

#   time.sleep(2)#   io_mgr.measure_analog()
   io_mgr.measure_counters()

