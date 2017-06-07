#
#
# Stand Alone Modbus Program
#
#
#
#
import   time
#import   myModbus_udp 
import   new_instrument


class ModbusUDPDeviceClient():
   def __init__( self, remotes,address ):
       #self.instrument =   myModbus_udp.Instrument_UDP()  # 10 is instrument address
       self.new_instrument =  new_instrument.Modbus_Instrument()
       self.remotes          = remotes
       
       self.new_instrument.set_ip(address)
    
   def read_bit(self, remote , registeraddress ):
       device = self.remotes[remote]
       self.new_instrument.set_ip(device["UDP"])
       address = device["address"] 
       return self.new_instrument.read_bits(  address, registeraddress,1)[0]
      
   def write_bit(self, remote, registeraddress, value ):
       device = self.remotes[remote]
       self.new_instrument.set_ip(device["UDP"])
       address = device["address"]
       self.new_instrument.write_bits( address, registeraddress, [value] )
        
   def write_registers(self,remote,starting_register,data_list ):
       device = self.remotes[remote]
       self.new_instrument.set_ip(device["UDP"])
       address = device["address"]
       return self.new_instrument.write_registers( address, starting_register,data_list )

   def read_registers( self, remote, starting_register, number ):
       device = self.remotes[remote]
       self.new_instrument.set_ip(device["UDP"])
       address = device["address"]
       return self.new_instrument.read_registers( address, starting_register,number )
  

   def read_float(self, remote , registeraddress ):
       device = self.remotes[remote] 
       self.new_instrument.set_ip(device["UDP"])
       address = device["address"]
       return self.new_instrument.read_floats( address, registeraddress , 1 )[0] 

   def write_float( self, remote, registeraddess,value ):
       device = self.remotes[remote]    
       self.instrument.set_ip(device["UDP"])
       address = device["address"]
       return self.new_instrument.write_floats( address, registeraddress,[value] ) 

   def read_long(self, remote, registeraddress ):
       device = self.remotes[remote] 
       self.new_instrument.set_ip(device["UDP"])
       address = device["address"]
       return self.new_instrument.read_longs( address, registeraddress,1 )[0] 

   def write_long( self, remote, registeraddess,value ): 
       device = self.remotes[remote]   
       self.new_instrument.set_ip(device["UDP"])
       self.new_instrument.address = device["address"]
       return self.instrument.write_longs( address, registeraddress, [address] ) 

   

   def redis_write( self,  server_ip, json_data ):
       self.new_instrument.set_ip( server_ip )

       return self.new_instrument.redis_communicate( 255, json_data )

   def redis_read( self,  server_ip, json_data):
       self.new_instrument.set_ip( server_ip )

       return self.new_instrument.redis_communicate( 254, json_data)

   def ping_device( self, server_ip, address_list ):
       self.new_instrument.set_ip( server_ip )
       json_data = {"action":"ping"   ,"parameters":{ "sub_action":"ping_device"   , "sub_parameter":address_list   } }
       return self.new_instrument.redis_communicate( 253, json_data)

   def ping_all_devices( self, server_ip ):
       self.new_instrument.set_ip( server_ip )
       json_data = {"action":"ping"  ,"parameters":{ "sub_action":"ping_all_devices"    , "sub_parameter": None  } }
       return self.new_instrument.redis_communicate( 253, json_data)

   def clear_all_counters( self , server_ip):
       self.new_instrument.set_ip( server_ip )
       json_data = {"action":"counter"   ,"parameters":{ "sub_action":"clear_all_counters"   , "sub_parameter":None   } }
       return self.new_instrument.redis_communicate( 252, json_data)

   def get_all_counters( self, server_ip ):
       self.new_instrument.set_ip( server_ip )
       json_data = {"action":"counter"   ,"parameters":{ "sub_action": "get_all_counters" , "sub_parameter":None   } }
       return self.new_instrument.redis_communicate( 252, json_data)

   def clear_counter_list( self, server_ip, address_list ):
       self.new_instrument.set_ip( server_ip )
       json_data = {"action":"counter"   ,"parameters":{ "sub_action":"clear_counter_list"   , "sub_parameter":address_list   } }
       return self.new_instrument.redis_communicate( 252, json_data)







if __name__ == "__main__":     
   pass
