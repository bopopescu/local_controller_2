class IrrigationControl():
   def __init__(self,  irrigation_devices=None, main_valve_list=None, plc_map=None , redis=None ):
       self.redis              = redis
       self.irrigation_devices = irrigation_devices
       self.main_valve_list  = main_valve_list
       self.plc_map            = plc_map

   def disable_all_sprinklers( self,*arg ):
      
       for redis_key, device in self.irrigation_devices.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               #print "device",device
               plc.disable_all_sprinklers( device )
      
              
  

   def turn_on_main_valves( self,*arg ):
       self.redis.hset("CONTROL_VARIABLES","MASTER_VALVE_SETUP","ON")
       print "main on"
       for redis_key, device in self.main_valve_list.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               remote = device["remote"]
               valve_list = [device["main_valve"]]
               if len( valve_list ) > 0:
                   plc.turn_on_valves( remote, valve_list)
            
   def turn_off_main_valves( self,*arg ):
       self.redis.hset("CONTROL_VARIABLES","MASTER_VALVE_SETUP","OFF")
       print "main off"
       for redis_key, device in self.main_valve_list.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               remote = device["remote"]
               valve_list = [device["main_valve"]]
               if len( valve_list ) > 0:
                   plc.turn_off_valves( remote, valve_list)
    

   def turn_on_cleaning_valves( self,*arg ):
       for redis_key, device in self.main_valve_list.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               remote = device["remote"]
               valve_list = [device["cleaning_valve"]]
               if len( valve_list ) > 0:
                   plc.turn_on_valves(  remote, valve_list)
            
   def turn_off_cleaning_valves( self,*arg ):
       for redis_key, device in self.main_valve_list.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               remote = device["remote"]
               valve_list =[ device["cleaning_valve"]]
               if len( valve_list ) > 0:
                   plc.turn_off_valves( remote, valve_list)

 
   #
   #  Clearing Duration counter is done through a falling edge
   #  going from 1 to 0 generates the edge
   def clear_duration_counters( self,*arg ):
       for redis_key, device in self.irrigation_devices.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               plc.clear_duration_counters( device )

   def load_duration_counters( self, time_duration ,*arg):
       duration = (time_duration*60)+15  # convert minutes to seconds
       for redis_key, device in self.irrigation_devices.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               plc.load_duration_counters( duration,device )
               


   def turn_off_io( self , io_setup ):
       # io_setup is a list of dict { "remote":xx , "bits":[1,2,3,4]
       self.turn_off_main_valves()
       for i in io_setup:      
           remote        = i["remote"]
           bits          = i["bits"]  # list of outputs on remote to turn off
           dev_type      = self.irrigation_devices[remote]["type"]
           if self.plc_map.has_key( dev_type ):
               plc = self.plc_map[ dev_type ]
               plc.turn_off_valves( remote, bits )
       self.disable_all_sprinklers()

   def turn_on_io( self ,io_setup ):
       # io_setup is a list of dict { "remote":xx , "bits":[1,2,3,4]

       for i in io_setup:      
           remote        = i["remote"]
           bits          = i["bits"]  # list of outputs on remote to turn off
           dev_type      = self.irrigation_devices[remote]["type"]
           if self.plc_map.has_key( dev_type ):
               plc = self.plc_map[ dev_type ]
               plc.turn_on_valves( remote, bits )
       self.turn_on_main_valves()


   def turn_on_valve( self ,io_setup ):
       # io_setup is a list of dict { "remote":xx , "bits":[1,2,3,4]

       for i in io_setup:      
           remote        = i["remote"]
           bits          = i["bits"]  # list of outputs on remote to turn off
           dev_type      = self.irrigation_devices[remote]["type"]
           if self.plc_map.has_key( dev_type ):
               plc = self.plc_map[ dev_type ]
               plc.turn_on_valves( remote, bits )
       


class WatchDogControl():
   def __init__(self,  irrigation_devices=None, plc_map=None ):
       self.irrigation_devices = irrigation_devices
       self.plc_map       = plc_map

   def read_wd_flag( self,*arg ):
       return_value = []
       for key, device in self.irrigation_devices.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               return_value.append( plc.read_wd_flag( device ) )
       return return_value

   def write_wd_flag( self,value,*arg ):
       for key, device in self.irrigation_devices.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               plc.write_wd_flag( device,value)
      
   def read_mode_switch( self,*arg ):
       return_value = []
       for key, device in self.irrigation_devices.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               return_value.append( plc.read_mode_switch( device ) )
       return return_value

   def read_mode( self,*arg ):
       return_value = []
       for key, device in self.irrigation_devices.items():
           if self.plc_map.has_key( device["type"] ):
               plc = self.plc_map[ device["type"] ]
               return_value.append( plc.read_mode( device ) )
       return return_value

      

if __name__ == "__main__":
  pass
 
