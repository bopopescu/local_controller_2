#
#
#  File: io_controller_class.py
#
#
#
#
#

import struct    
import bitstruct 
import os
import sys
import time
import select
import socket
import json
import redis


import datetime
from  psoc_4m_base_class import PSOC_BASE_4M

class Moisture_Controller():
    
    def __init__(self,new_instrument, slave_id, ip, port = 5005  ):
        self.name            = name
        self.new_instrument = new_instrument
        self.slave_id       = slave_id
        self.ip             = ip
        self.port           = port
                          


class PSOC_4M_MOISTURE_UNIT(PSOC_BASE_4M):

   def __init__(self, ip,port,slave_address, instrument ):
       self.ip = ip
       self.port = port
       self.slave_address = slave_address
       self.instrument = instrument
       self.system_id = 0x201
       PSOC_BASE_4M.__init__( self,ip,port,slave_address, instrument, self.system_id)
       
       # additional write address definitions definitions
       self.check_one_wire_presence_addr                     = 27
       self.make_soil_temperature_addr                       = 28
       self.make_air_temp_humidity_addr                      = 29
       self.force_moisture_reading_addr                      = 30  
       self.update_moisture_sensor_configuration_addr        = 31
  
       self.update_flash_addr                                = 33
       self.clear_moisture_flag_addr                         = 34
       
       self.sensor_length                                    = 16
       
       self.new_measurement_flag_start = 20
       self.new_measurement_flag_list = [ "NEW_MOISTURE_DATA_FLAG"]
       
       # status
       self.status_start   =    13
       self.status_list    =  [
                                          
                                          "ONE_WIRE_DEVICE_FOUND",
                                          "NEW_MOISTURE_DATA_FLAG"
                               ]
       self.moisture_control_start = 15   
       self.moisture_control_list  = [
                             
                           
                           
                           "AIR_HUMIDITY_FLOAT" ,       
                           "AIR_TEMP_FLOAT",
                           "MOISTURE_SOIL_TEMP_FLOAT",
                           "RESISTOR_FLOAT",
                           


                        ]
       self.capacitance_mask_start = 23
       self.capacitance_mask_list  = [ "CAPACITANCE_MASK"]
       
       # Moisture Data
       self.moisture_data_start  =    30   
       self.moisture_data_number =    16      
       
       self.moisture_data_resistive_start              = 70                
       self.moisture_resistive_configuration_number    = 16                      
    
     
       # Moisture Configuration Data
       self.moisture_configuration_start  =    110
       self.moisture_configuration_number =     16
 
                                             
       
       
 


   # 
   #
   #  Read Variables
   #
   #
 
 
   def check_status( self ):
       return_value = {}
       self.instrument.set_ip( self.ip,self.port )

       data =  self.instrument.read_registers( self.slave_address,  self.status_start, len(self.status_list) )

       for i in range(0,len(self.status_list)):
          
           return_value[  self.status_list[i]  ] = data[i]
           
       return return_value
       

   
        
   def read_moisture_control(self  ):
       return_value = {}
       self.instrument.set_ip( self.ip,self.port )
       data =  self.instrument.read_floats( self.slave_address,  self.moisture_control_start, len(self.moisture_control_list) )

       for i in range(0,len(self.moisture_control_list)):
          
           return_value[  self.moisture_control_list[i]  ] = data[i]
           
       return return_value
       


       
   def read_moisture_data( self  ):
        return_value = {}
        self.instrument.set_ip( self.ip,self.port )
        data =  self.instrument.read_floats( self.slave_address,  self.moisture_data_start ,self.moisture_configuration_number  )
        return data
        
         
   def read_moisture_resistive_data( self  ):
        return_value = {}
        self.instrument.set_ip( self.ip,self.port )
        data =  self.instrument.read_floats( self.slave_address,  self.moisture_data_resistive_start ,self.moisture_resistive_configuration_number  )
        return data
        
        
      
      
      
      
        
   def read_moisture_configuration( self ):
       return_value = {}
       self.instrument.set_ip( self.ip,self.port )
       data = self.instrument.read_registers( self.slave_address, self.moisture_configuration_start, self.moisture_configuration_number )
       return data
       
  
   def check_one_wire_presence ( self): #sampling rate is in minutes
         self.instrument.set_ip( self.ip,self.port )
         self.instrument.write_registers(self.slave_address, self.check_one_wire_presence_addr, [0] )
         
   def make_soil_temperature ( self ): #sampling rate is in minutes
         self.instrument.set_ip( self.ip,self.port )
         self.instrument.write_registers(self.slave_address, self.make_soil_temperature_addr, [0] )
         
   def make_air_temp_humidity( self): #sampling rate is in minutes
         self.instrument.set_ip( self.ip,self.port )
         self.instrument.write_registers(self.slave_address, self.make_air_temp_humidity_addr, [0] )

  
   def clear_new_moisture_data_flag( self ):
       self.instrument.set_ip( self.ip,self.port )
       self.instrument.write_registers( self.slave_address, self.clear_moisture_flag_addr, [0] )
       
 
   
   def force_moisture_reading ( self): #sampling rate is in minutes
         self.instrument.set_ip( self.ip,self.port )
         self.instrument.write_registers( self.slave_address, self.force_moisture_reading_addr, [0] )
         
        
   def  update_moisture_sensor_configuration ( self, sensor_data ): # sensor data consisting of 0,1,2
        if len( sensor_data) != self.sensor_length :
            raise
        valid_data = set([0,1,2])
        for i in sensor_data:
          if i not in valid_data:
             raise ValueError("Bad Value for Sensor should be 0,1 or 2 Got "+i)
        self.instrument.set_ip( self.ip,self.port )  
        self.instrument.write_registers( self.slave_address, self.update_moisture_sensor_configuration_addr ,sensor_data )
  


        
 




           
if __name__ == "__main__":     
   import new_instrument
   client_driver       = new_instrument.Modbus_Instrument()
   moisture_controller = PSOC_4M_MOISTURE_UNIT( "192.168.1.82",5005,40,client_driver )
 
   print "time",moisture_controller.read_time()
   print time.time()
   print moisture_controller.clear_new_moisture_data_flag()
   print moisture_controller.check_status()

   print moisture_controller.check_one_wire_presence()
   time.sleep(.3)
   print moisture_controller.make_soil_temperature()
   time.sleep(.3)
   print moisture_controller.make_air_temp_humidity()
   time.sleep(.3)
   print moisture_controller.make_air_temp_humidity()
   time.sleep(.3)
   # test read functions first
 
   print moisture_controller.check_status()
   print moisture_controller.read_moisture_control()
   print moisture_controller.read_moisture_configuration( )
   print moisture_controller.force_moisture_reading()
   time.sleep(1.)
   print moisture_controller.read_moisture_data()
   print moisture_controller.read_moisture_resistive_data()
       
       
  


    