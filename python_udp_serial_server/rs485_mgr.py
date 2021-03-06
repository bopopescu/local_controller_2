#
# File: rs485_mgr.py
# This file handles low level rs485 communication
#
#
#
#
#
import os
import time
import myModbus
import struct
from  myModbus import *

class RS485_Mgr():
   def __init__( self ):
       pass

   def open( self, interface_parameters ):
       try:
           print "interface_parameters",interface_parameters
           self.instrument = Instrument(interface_parameters["interface"],40 )  # 10 is instrument address
           print "timeout", interface_parameters["timeout"]
           self.instrument.serial.timeout = interface_parameters["timeout"]
           self.instrument.serial.parity = serial.PARITY_NONE
           self.instrument.serial.baudrate = interface_parameters["baud_rate"]
           self.instrument.debug = None
           self.interface_parameters = interface_parameters
           return True
       except:
           print "open return false"
           return False
       

   def close( self ):
     try:
       self.instrument.serial.close()
       del(self.instrument)
       self.params = None
     except:
       pass 

   def process_message( self, parameters, message, counters = None ):
       #print "made it to rs485"
       for i in range(0,5):
           #print i
           try:

               response = ""
               #print "message ",len(message)
               response =  self.instrument._communicate( message, 1024)
               time.sleep(.05)
               #print "response ",len(response)
               #print "message",[message],len(response),[response]
               if len(response  ) > 4:
                   receivedChecksum          = response[-2:]
                   responseWithoutChecksum   = response[0 : len(response) - 2]
                   calculatedChecksum = self._calculateCrcString(responseWithoutChecksum)
                   #print "crc",[receivedChecksum, calculatedChecksum], ord(message[0]),parameters["address"]
                   if (receivedChecksum == calculatedChecksum) and (ord(message[0]) == parameters["address"] ): # check checksum
                       #print "made it here",#
                       if counters != None:
                           counters["counts"] = counters["counts"] +1
                       #print i,len(response)
                       return response
              
               if counters != None:
                   counters["failures"] = counters["failures"] +1
               
           except:
              raise # serial errror              
              response = ""
       if counters != None:  
           counters["total_failures"] = counters["total_failures"] +1
           counters["counts"] = counters["counts"] +1
       
       return response
     


   def find_address( self, parameters):
      return parameters["address"]


   def probe_register( self, parameters, counters = None ):
       address     = parameters["address"]
       register    = parameters["search_register"]
       number      = parameters["register_number"]
       payload     = struct.pack("<BBBBBB",address,3,(register>>8)&255,register&255,0,number)  # read register 0 1 length
       calculatedChecksum = self._calculateCrcString(payload)
       payload = payload+calculatedChecksum
       response = self.process_message(parameters,payload,counters )

       receivedChecksum          = response[-2:]
       responseWithoutChecksum   = response[0 : len(response) - 2]
       calculatedChecksum = self._calculateCrcString(responseWithoutChecksum)
       return_value = receivedChecksum == calculatedChecksum # check checksum
       
       if return_value == True :
             return_value = address == ord(response[0])  # check address
       #else:
       #   print "probe failure"
       return return_value
 
       

   def _rightshift( self, inputInteger):
       shifted = inputInteger >> 1
       carrybit = inputInteger & 1
       return shifted, carrybit




   def _calculateCrcString(self,inputstring):
       # Constant for MODBUS CRC-16
       POLY = 0xA001
       # Preload a 16-bit register with ones
       register = 0xFFFF
       for character in inputstring:
           # XOR with each character
           register = register ^ ord(character)
           # Rightshift 8 times, and XOR with polynom if carry overflows
           for i in range(8):
               register, carrybit = self._rightshift(register)
               if carrybit == 1:
                register = register ^ POLY

       return    struct.pack("<H",register)
     

if __name__ == "__main__":
   rs485_mgr = RS485_Mgr()
   interface_parameters = {}
   interface_parameters["interface"]   = "/dev/ttyUSB0"
   interface_parameters["baud_rate"]   = 38400
   interface_parameters["timeout"]     = .02
   parameters = {}
   parameters["address"] = 100
   parameters["search_register"] = 0
   parameters["register_number"] =  1
   counters = {}
   counters["failures"]        = 0
   counters["counts"]          = 0
   counters["total_failures"]  = 0
   if rs485_mgr.open(interface_parameters ):
     for i in range(0,100):
        #print i
        print i, rs485_mgr.probe_register( parameters,counters )
        #time.sleep(.05)
     rs485_mgr.close()
   print counters  


