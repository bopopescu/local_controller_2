#
#
# Stand Alone Modbus Program
#
#
#
#
import time
from   myModbus_udp import *



class ModbusUDPClient():
   def __init__( self, address ):
       self.instrument = Instrument_UDP()  # 10 is instrument address
       self.instrument.debug = None
       self.instrument.set_ip(address)
    
   def read_bit(self, modbus_address, registeraddress ):
       self.instrument.address = modbus_address
       return self.instrument.read_bit( registeraddress )
      
   def write_bit(self, address, registeraddress, value ):
       self.instrument.address = address
       self.instrument.write_bit( registeraddress, value)
        
   def write_registers(self,modbus_address,starting_register,data_list ):
       self.instrument.address = modbus_address
       return self.instrument.write_registers( starting_register,data_list )

   def read_registers( self, modbus_address, starting_register, number ):
       self.instrument.address = modbus_address
       return self.instrument.read_registers( starting_register,number )
  

   def read_float(self, modbus_address , registeraddress ): 
        self.instrument.address = modbus_address
        return self.instrument.read_float( registeraddress ) 

   def write_float( self, modbus_address, registeraddess,value ):    
        self.instrument.address = modbus_address
        return self.instrument.write_float( registeraddress,address ) 

   def read_long(self, modbus_address, registeraddress ): 
        self.instrument.address = modbus_address
        return self.instrument.read_long( registeraddress ) 

   def write_long( self, modbus_address, registeraddess,value ):    
        self.instrument.address = modbus_address
        return self.instrument.write_long( registeraddress,address ) 

   # string length is 32 
   def read_string(self, modbus_address, registeraddress ):
       self.instrument.address = modbus_address
       return self.instrument.read_string( registeraddress )
 
   # string length is 32
   def write_string(self,  modbus_address,registeraddress, textstring):
      self.instrument.address = modbus_address
      return self.instrument.write_string(registeraddress, textstring )
   

   def redis_write( self,  modbus_address, json_data ):
       self.instrument.address = modbus_address
       return self.instrument.redis_communicate( modbus_address,255, json_data )

   def redis_read( self,  modbus_address, json_data):
       self.instrument.address = modbus_address
       return self.instrument.redis_communicate( modbus_address,254, json_data)

   def ping_device( self, modbus_address, address_list ):
        self.instrument.address = modbus_address
        json_data = {"action":"ping"   ,"parameters":{ "sub_action":"ping_device"   , "sub_parameter":address_list   } }
        return self.instrument.redis_communicate( 253, json_data)

   def ping_all_devices( self, modbus_address = None ):
        self.instrument.address = modbus_address
        json_data = {"action":"ping"  ,"parameters":{ "sub_action":"ping_all_devices"    , "sub_parameter": None  } }
        return self.instrument.redis_communicate( 253, json_data)

   def clear_all_counters( self , modbus_address= None):
        self.instrument.address = modbus_address
        json_data = {"action":"counter"   ,"parameters":{ "sub_action":"clear_all_counters"   , "sub_parameter":None   } }
        return self.instrument.redis_communicate( 253, json_data)

   def get_all_counters( self, modbus_address=None ):
        self.instrument.address = modbus_address
        json_data = {"action":"counter"   ,"parameters":{ "sub_action": "get_all_counters" , "sub_parameter":None   } }
        return self.instrument.redis_communicate( 253, json_data)

   def clear_counter_list( self, modbus_address, address_list ):
        self.instrument.address = modbus_address
        json_data = {"action":"counter"   ,"parameters":{ "sub_action":"clear_counter_list"   , "sub_parameter":address_list   } }
        return self.instrument.redis_communicate( 253, json_data)




class Modbus_RTU( ModbusUDPClient ):

   def __init__(self, address):
          ModbusUDPClient.__init__(self,address)

   def special_command(self, modbus_address, registeraddress, values):
       self.instrument.address = modbus_address
       return self.instrument.special_command(registeraddress, values)

   def read_eeprom_registers_byte( self, modbus_address, starting_register,number):
       self.instrument.address = modbus_address
       return self.instrument.read_eeprom_registers( starting_register, number )

   def write_eeprom_registers_byte( self, modbus_address, starting_address, data_list ):
       self.instrument.address = modbus_address
       return self.instrument.write_eeprom_registes( starting_address, data_list )

   def  read_fifo( self, modbus_address, queue, max_number ):
       self.instrument.address = modbus_address
       return self.instrument.read_fifo( queue, max_number )

   def  read_eeprom_registers( self,modbus_address, queue, max_number ):
        temp = self.read_eeprom_registers_byte( modbus_address,queue,max_number)
        return_value = []
        for i in temp:
           return_value.append( (i[0]<<24)|(i[1]<<16)|(i[2]<<8)|i[3] )
        return return_value

   def  write_eeprom_registers( self, modbus_address, starting_address, data_list ):
        temp1 = []
        for i in data_list:
          temp2 = []
          temp2.append( (i>>24)&0xff )
          temp2.append( (i>>16)&0xff )
          temp2.append( (i>>8)&0xff)
          temp2.append( (i)&0xff)
          temp1.append( temp2)
        return write_eeprom_registers_byte( self, modbus_address, starting_address, temp1 )
   



if __name__ == "__main__":     
   import time
   from  myModbus_udp import *

   modbus_client = ModbusUDPClient( "192.168.1.81" )
   modbus_rtu    = Modbus_RTU( "192.168.1.81" )
   print  modbus_rtu.read_fifo( 31, 0, 16 ) 
   print  modbus_rtu.read_registers( 31,0,20)
   print  modbus_rtu.read_registers(100,0,10)
   print  modbus_rtu.read_registers(125,0,10)
   print  modbus_rtu.read_registers(170,0,10)
   print  modbus_rtu.write_registers(31,0,[1,2,3])
   print  modbus_rtu.read_registers( 31,0,20)
   print  modbus_rtu.read_eeprom_registers( 31,0,10)
   print  modbus_rtu.read_eeprom_registers_byte( 31,0,10)
   print  modbus_rtu.redis_write( 255,{"test1":123,"test2":124 } )
   print  modbus_rtu.redis_read(255,["test1","test2"] )
   print  modbus_rtu.ping_all_devices(255)
   print  modbus_rtu.get_all_counters(255 )
   print  modbus_rtu.clear_counter_list( 255, [31] )
   print  modbus_rtu.get_all_counters(255 )
   print  modbus_rtu.clear_all_counters( 255 )
   print  modbus_rtu.get_all_counters(255 )

   for i in range(0,255):
     print i
     print  modbus_rtu.ping_device( 255, [125] )
   print  modbus_rtu.read_registers( 31,0,20)
   print  modbus_rtu.read_registers(100,0,10)
   print  modbus_rtu.read_registers(125,0,10)
   print  modbus_rtu.read_registers(170,0,10)

   print  modbus_rtu.get_all_counters(255 )

