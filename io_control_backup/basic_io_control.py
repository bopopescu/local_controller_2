#
#
# This module allows the user to manipulate
# remote IO at redis key level    
#      
# This module will find the appropriate remote module to     
# execute the IO action
#      
#
#
#
#
#
#
#
import time

class BasicIo():
   def __init__(self, redis_dict = None, redis_server=None,  plc_interface=None, 
                gpio_bit_input_devices=None, gpio_bit_output_devices= None, 
                gpio_reg_input_devices=None, gpio_reg_output_devices= None,
                analog_devices=None, counter_devices=None ):


        self.redis_dict                 = redis_dict
        self.redis                      = redis_server  
        self.plc_interface              = plc_interface
        self.gpio_bit_input_devices     = gpio_bit_input_devices
        self.gpio_bit_output_devices    = gpio_bit_output_devices 
        self.gpio_reg_input_devices     = gpio_reg_input_devices
        self.gpio_reg_output_devices    = gpio_reg_output_devices
        self.analog_devices             = analog_devices
        self.counter_devices            = counter_devices
        


   def clear_gpio_input( self,*arg):
       if self.gpio_bit_input_devices != None:
           for redis_key, device in self.gpio_bit_input_devices.items():
               self.redis.hset( self.redis_dict["GPIO_BITS"], redis_key,0 )
       if self.gpio_reg_input_devices != None:
           for redis_key, device in self.gpio_reg_input_devices.items():
               self.redis.hset( self.redis_dict["GPIO_REGS"], redis_key,0 )
       return "CONTINUE"        
 
   def get_gpio_bit( self , redis_key ):
       device = self.gpio_bit_input_devices[ redis_key ]
       if  self.plc_interface.has_key( device["type"] ):
           plc  = self.plc_interface[ device["type"]]
           return plc.get_gpio_bit(  redis_key, device )
       else:
           raise #bad device

   def get_gpio_reg( self , redis_key ):
       device = self.gpio_reg_input_devices[ redis_key ]
       if  self.plc_interface.has_key( device["type"] ):
           plc  = self.plc_interface[ device["type"]]
           return plc.get_gpio_reg(  redis_key, device )
       else:
           raise #bad device

   def set_gpio_bit( self , redis_key, value ):
       if value != 0:
          value = 1
       device = self.gpio_bit_input_devices[ redis_key ]
       if  self.plc_interface.has_key( device["type"] ):
           plc  = self.plc_interface[ device["type"]]
           plc.set_gpio_bit(  redis_key, device, value )
       else:
           raise #bad device

   def set_gpio_reg( self , redis_key , value ):
       device = self.gpio_reg_input_devices[ redis_key ]
       if  self.plc_interface.has_key( device["type"] ):
           plc  = self.plc_interface[ device["type"]]
           plc.set_gpio_reg(  redis_key, entry, value )
       else:
           raise #bad device      

    
   def get_analog( self, redis_key ):
       device = self.analog_devices[ redis_key ]
       if  self.plc_interface.has_key( device["type"] ):
           plc  = self.plc_interface[ device["type"]]
           return plc.measure_analog(  redis_key, device  )
       else:
           raise #bad device  
    
   def measure_counter( self, deltat,redis_key ):
      

       device = self.counter_devices[ redis_key ]

       if  self.plc_interface.has_key( device["type"] ):
           plc  = self.plc_interface[ device["type"]]
           return plc.measure_counter(  redis_key, device, deltat )
       else:
           raise #bad device  

if __name__ == "__main__":
  pass
 
