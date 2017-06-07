class WatchDogException(Exception):
    """Exception raised for errors in the Watch Dog.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg



#
# This class is mainly called from chain flow modules
#
#
#
#
class WatchDogControl():
   def __init__(self, watch_dog_devices , plc_control ):
        self.watch_dog_devices    = watch_dog_devices
        self.plc_control          = plc_control


   def modbus_check_mode_switches( self,*arg ):  # not all devices have mode switches
       for redis_key, device in self.watch_dog_devices.items():
           if self.plc_control.has_key( device["type"]):
               plc = plc_control[ device["type"] ]
               if hasattr( plc,"check_mode_switch"):
                   if plc.check_mode_switch( self, redis_key,device ):
                       raise    
           else:
               raise   # unsupported plc type

       return "DISABLE"   
            
  
   def modbus_read_wd_flag( self,*arg ):  #variable arguments put in so that function can be called by chain flow
       for redis_key, device in self.watch_dog_devices.items():
           if self.plc_control.has_key( device["type"]):
               plc = plc_control[ device["type"] ]
               value = plc.read_wd_flag( redis_key, device )
               if value != 0:
                   raise  WatchDogException("plc watch dog failure redis_key:  "+redis_key)
           else:
               raise #unsupported plc type           
       
       return "DISABLE"
       

   def modbus_write_wd_flag( self,*arg  ): #variable arguments put in so that function can be called by chain flow
       for redis_key, device in self.watch_dog_devices.items():
           if self.plc_control.has_key( device["type"]):
               plc = plc_control[ device["type"] ]
               plc.write_wd_flag( redis_key, device )
           else:
               raise #unsupported plc type           
       
       return "DISABLE"

if __name__ == "__main__":
  pass
   
