

import os
import struct
import sys
import time
import select
import socket
import json

#####################
## Named constants ##
#####################

##############################
## Modbus instrument object ##
##############################
_NUMBER_OF_BYTES_PER_REGISTER = 2
_SECONDS_TO_MILLISECONDS = 1000
_ASCII_HEADER = ':'
_ASCII_FOOTER = '\r\n'
MODE_RTU   = 'rtu'
MODE_ASCII = 'ascii'

class Instrument_UDP():

    def __init__(self ):
        self.port = 5005
        self.address = 10  # this is a default value
        self.mode=MODE_RTU
        self.precalculate_read_size = True
        self.sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP
        """If this is :const:`True`, the serial port will be closed after each call. Defaults to :data:`CLOSE_PORT_AFTER_EACH_CALL`. To change it, set the value ``minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True`` ."""

    def set_ip( self,ip ):

        self.ip = ip


    def read_bit(self, registeraddress, functioncode=2):

        return self._genericCommand(functioncode, registeraddress)


    def write_bit(self, registeraddress, value, functioncode=5):
       self._genericCommand(functioncode, registeraddress, value)


    def read_register(self, registeraddress, numberOfDecimals=0, functioncode=3, signed=False):

        return self._genericCommand(functioncode, registeraddress, numberOfDecimals=numberOfDecimals, signed=signed)



    def write_register(self, registeraddress, value, numberOfDecimals=0, functioncode=16, signed=False):


        self._genericCommand(functioncode, registeraddress, value, numberOfDecimals, signed=signed)


    def read_long(self, registeraddress, functioncode=3, signed=False):

        return self._genericCommand(functioncode, registeraddress, numberOfRegisters=2, signed=signed, payloadformat='long')


    def write_long(self, registeraddress, value, signed=False):

        MAX_VALUE_LONG =  4294967295  # Unsigned INT32
        MIN_VALUE_LONG = -2147483648  # INT32

        self._genericCommand(16, registeraddress, value, numberOfRegisters=2, signed=signed, payloadformat='long')


    def read_float(self, registeraddress, functioncode=3, numberOfRegisters=2):

        return self._genericCommand(functioncode, registeraddress, numberOfRegisters=numberOfRegisters, payloadformat='float')


    def write_float(self, registeraddress, value, numberOfRegisters=2):
        self._genericCommand(16, registeraddress, value, \
            numberOfRegisters=numberOfRegisters, payloadformat='float')


    def read_string(self, registeraddress, numberOfRegisters=16, functioncode=3):
        return self._genericCommand(functioncode, registeraddress, \
            numberOfRegisters=numberOfRegisters, payloadformat='string')


    def write_string(self, registeraddress, textstring, numberOfRegisters=16):

        self._genericCommand(16, registeraddress, textstring, \
            numberOfRegisters=numberOfRegisters, payloadformat='string')


    def read_registers(self, registeraddress, numberOfRegisters, functioncode=3):

        return self._genericCommand(functioncode, registeraddress, \
            numberOfRegisters=numberOfRegisters, payloadformat='registers')

    def read_registers(self, registeraddress, numberOfRegisters, functioncode=3):

        return self._genericCommand(functioncode, registeraddress, \
            numberOfRegisters=numberOfRegisters, payloadformat='registers')


    def read_eeprom_registers(self, registeraddress, numberOfRegisters, functioncode=30):

        temp = self._genericCommand(functioncode, registeraddress, \
            numberOfRegisters=numberOfRegisters*2, payloadformat='string')
        length = len(temp)/4
        return_value = []
        for i in range(0,length):
            temp_value = []
            temp_value.append(ord(temp[:1]))
            temp_value.append(ord(temp[1:2]))
            temp_value.append(ord(temp[2:3]))
            temp_value.append(ord(temp[3:4]))
            return_value.append(temp_value)
            temp = temp[4:]
        return return_value
    
    def read_fifo(self, registeraddress, numberOfRegisters, functioncode=33):

        temp = self._genericCommand(functioncode, registeraddress, \
            numberOfRegisters=numberOfRegisters, payloadformat='registers')
        length = ord(temp[:1])
        temp = temp[1:]
        return_value = []
        temp_value = []
       
        for i in range(0,length/2):
             value_a = ord(temp[0:1])*256 + ord(temp[1:2])
             value_b = ord(temp[2:3])*256 + ord(temp[3:4])
             temp = temp[4:]
             return_value.append([value_a,value_b])
        return return_value
    
    def write_registers(self, registeraddress, values):
        if not isinstance(values, list):
            raise TypeError('The "values parameter" must be a list. Given: {0!r}'.format(values))
        # Note: The content of the list is checked at content conversion.

        self._genericCommand(16, registeraddress, values, numberOfRegisters=len(values), payloadformat='registers')

        
    def special_command(self, registeraddress, values):

        # Note: The content of the list is checked at content conversion.

        self._genericCommand(40, registeraddress, values, numberOfRegisters=len(values), payloadformat='registers')



    def write_eeprom_registers(self, registeraddress, values):

        # Note: The content of the list is checked at content conversion.
        value = ""
        for i in range(0,len(values)):
            
            for j in range(0,4):
              value = value + chr(values[i][j])
    
        temp = self._genericCommand(31, registeraddress, value, numberOfRegisters=len(value)/2, payloadformat='string')
  
    def redis_communicate( self, address, function_code, json_data ):
       pay_load_data =  json.dumps(json_data)
       message = self._embedPayload(address, MODE_RTU, function_code, pay_load_data)
       response=  self._communicate(message, 1024)
       receivedChecksum = response[-2:]
       responseWithoutChecksum = response[0 : len(response) - 2]
       calculatedChecksum = self._calculateCrcString(responseWithoutChecksum)
       return_value = receivedChecksum == calculatedChecksum
       return return_value, responseWithoutChecksum[2:]
       

    


    #####################
    ## Generic command ##
    #####################


    def _genericCommand(self, functioncode, registeraddress, value=None, \
            numberOfDecimals=0, numberOfRegisters=1, signed=False, payloadformat=None):

        NUMBER_OF_BITS = 1
        NUMBER_OF_BYTES_FOR_ONE_BIT = 1
        NUMBER_OF_BYTES_BEFORE_REGISTERDATA = 1
        ALL_ALLOWED_FUNCTIONCODES = list(range(1, 7)) + [15, 16]+[30,31,33]  # To comply with both Python2 and Python3
        MAX_NUMBER_OF_REGISTERS = 255

        # Payload format constants, so datatypes can be told apart.
        # Note that bit datatype not is included, because it uses other functioncodes.
        PAYLOADFORMAT_LONG      = 'long'
        PAYLOADFORMAT_FLOAT     = 'float'
        PAYLOADFORMAT_STRING    = 'string'
        PAYLOADFORMAT_REGISTER  = 'register'
        PAYLOADFORMAT_REGISTERS = 'registers'

        ALL_PAYLOADFORMATS = [PAYLOADFORMAT_LONG, PAYLOADFORMAT_FLOAT, \
            PAYLOADFORMAT_STRING, PAYLOADFORMAT_REGISTER, PAYLOADFORMAT_REGISTERS]

        ## Check combinations of input parameters ##
        numberOfRegisterBytes = numberOfRegisters * _NUMBER_OF_BYTES_PER_REGISTER

                    # Payload format
        if functioncode in [3, 4, 6, 16,30,31,40] and payloadformat is None:
            payloadformat = PAYLOADFORMAT_REGISTER

        if functioncode in [3, 4, 6, 16,30,31,33,40]:
            if payloadformat not in ALL_PAYLOADFORMATS:
                raise ValueError('The payload format is unknown. Given format: {0!r}, functioncode: {1!r}.'.\
                    format(payloadformat, functioncode))
        else:
            if payloadformat is not None:
                raise ValueError('The payload format given is not allowed for this function code. ' + \
                    'Given format: {0!r}, functioncode: {1!r}.'.format(payloadformat, functioncode))

                    # Signed and numberOfDecimals
        if signed:
            if payloadformat not in [PAYLOADFORMAT_REGISTER, PAYLOADFORMAT_LONG]:
                raise ValueError('The "signed" parameter can not be used for this data format. ' + \
                    'Given format: {0!r}.'.format(payloadformat))

        if numberOfDecimals > 0 and payloadformat != PAYLOADFORMAT_REGISTER:
            raise ValueError('The "numberOfDecimals" parameter can not be used for this data format. ' + \
                'Given format: {0!r}.'.format(payloadformat))

                    # Number of registers
        if functioncode not in [3, 4, 6,16,30,31,33,40] and numberOfRegisters != 1:
            raise ValueError('The numberOfRegisters is not valid for this function code. ' + \
                'NumberOfRegisters: {0!r}, functioncode {1}.'.format(numberOfRegisters, functioncode))

        if functioncode not in [ 16,30,31,40] and payloadformat == PAYLOADFORMAT_REGISTER and numberOfRegisters != 1:
            raise ValueError('Wrong numberOfRegisters when writing to a ' + \
                'single register. Given {0!r}.'.format(numberOfRegisters))
            # Note: For function code 16 there is checking also in the content conversion functions.

                    # Value
       
        if functioncode in [ 16,31,40] and value is None:
            raise ValueError('The input value is not valid for this function code. ' + \
                'Given {0!r} and {1}.'.format(value, functioncode))


        ## Build payload to subordinate ##
        if functioncode in [1, 2]:
            payloadToSubordinate = self._numToTwoByteString(registeraddress) + \
                            self._numToTwoByteString(NUMBER_OF_BITS)

        elif functioncode in [3, 4,30,33]:
            payloadToSubordinate = self._numToTwoByteString(registeraddress) + \
                            self._numToTwoByteString(numberOfRegisters)

        elif functioncode == 5:
            payloadToSubordinate = self._numToTwoByteString(registeraddress) + \
                            self._createBitpattern(functioncode, value)

        elif functioncode == 6:
            payloadToSubordinate = self._numToTwoByteString(registeraddress) + \
                            self._numToTwoByteString(value, numberOfDecimals, signed=signed)

        elif functioncode == 15:
            payloadToSubordinate = self._numToTwoByteString(registeraddress) + \
                            self._numToTwoByteString(NUMBER_OF_BITS) + \
                            self._numToOneByteString(NUMBER_OF_BYTES_FOR_ONE_BIT) + \
                            self._createBitpattern(functioncode, value)

        elif functioncode in[ 16, 31,40 ]:
            if payloadformat == PAYLOADFORMAT_REGISTER:
                registerdata = self._numToTwoByteString(value, numberOfDecimals, signed=signed)

            elif payloadformat == PAYLOADFORMAT_STRING:
                registerdata = self._textstringToBytestring(value, numberOfRegisters)

            elif payloadformat == PAYLOADFORMAT_LONG:
                registerdata = self._longToBytestring(value, signed, numberOfRegisters)

            elif payloadformat == PAYLOADFORMAT_FLOAT:
                registerdata = self._floatToBytestring(value, numberOfRegisters)

            elif payloadformat == PAYLOADFORMAT_REGISTERS:
                registerdata = self._valuelistToBytestring(value, numberOfRegisters)

            assert len(registerdata) == numberOfRegisterBytes
            payloadToSubordinate = self._numToTwoByteString(registeraddress) + \
                            self._numToTwoByteString(numberOfRegisters) + \
                            self._numToOneByteString(numberOfRegisterBytes) + \
                            registerdata

        payloadFromSubordinate = self._performCommand(functioncode, payloadToSubordinate)
        if functioncode in [33]:
            return payloadFromSubordinate


        ## Calculate return value ##
        if functioncode in [1, 2]:
            registerdata = payloadFromSubordinate[NUMBER_OF_BYTES_BEFORE_REGISTERDATA:]
 
            return self._bitResponseToValue(registerdata)

        if functioncode in [3, 4,30]:
            registerdata = payloadFromSubordinate[NUMBER_OF_BYTES_BEFORE_REGISTERDATA:]

            if payloadformat == PAYLOADFORMAT_STRING:
                return self._bytestringToTextstring(registerdata, numberOfRegisters)

            elif payloadformat == PAYLOADFORMAT_LONG:
                return self._bytestringToLong(registerdata, signed, numberOfRegisters)

            elif payloadformat == PAYLOADFORMAT_FLOAT:
                
                return self._bytestringToFloat(registerdata, numberOfRegisters)

            elif payloadformat == PAYLOADFORMAT_REGISTERS:
                return self._bytestringToValuelist(registerdata, numberOfRegisters)

            elif payloadformat == PAYLOADFORMAT_REGISTER:
                return self._twoByteStringToNum(registerdata, numberOfDecimals, signed=signed)


    ##########################################
    ## Communication implementation details ##
    ##########################################


    def _performCommand(self, functioncode, payloadToSubordinate):
        DEFAULT_NUMBER_OF_BYTES_TO_READ = 1000

  
        # Build message
        message = self._embedPayload(self.address, self.mode, functioncode, payloadToSubordinate)

        # Calculate number of bytes to read
        number_of_bytes_to_read = DEFAULT_NUMBER_OF_BYTES_TO_READ
        if self.precalculate_read_size:
            try:
                number_of_bytes_to_read = self._predictResponseSize(self.mode, functioncode, payloadToSubordinate)
            except:
                if self.debug:
                    template = 'MinimalModbus debug mode. Could not precalculate response size for Modbus {} mode. ' + \
                        'Will read {} bytes. Message: {!r}'
                    self._print_out(template.format(self.mode, number_of_bytes_to_read, message))

        # Communicate
        
        response = self._communicate(message, number_of_bytes_to_read)

        # Extract payload
        payloadFromSubordinate = self._extractPayload(response, self.address, self.mode, functioncode)
        return payloadFromSubordinate


    def _communicate(self, message, number_of_bytes_to_read):

       
        self.sock.sendto(message, (self.ip, self.port))        


        
        self.sock.setblocking(0)
        ready = select.select([self.sock], [], [], 5.0)
        answer = ""
        if ready[0]:
            data = self.sock.recvfrom(1024)
            answer = data[0]
            
        if len(answer) == 0:
            print "no communication with the instrument"
            raise IOError('No communication with the instrument (no answer)')

        return answer



    def _embedPayload(self,subordinateaddress, mode, functioncode, payloaddata):

      firstPart = self._numToOneByteString(subordinateaddress) + self._numToOneByteString(functioncode) + payloaddata

      if mode == MODE_ASCII:
        message = _ASCII_HEADER + \
                _hexencode(firstPart) + \
                _hexencode(self._calculateLrcString(firstPart)) + \
                _ASCII_FOOTER
      else:
        message = firstPart + self._calculateCrcString(firstPart)

      return message


    def _extractPayload(self, response, subordinateaddress, mode, functioncode):
     BYTEPOSITION_FOR_ASCII_HEADER          = 0  # Relative to plain response

     BYTEPOSITION_FOR_SLAVEADDRESS          = 0  # Relative to (stripped) response
     BYTEPOSITION_FOR_FUNCTIONCODE          = 1

     NUMBER_OF_RESPONSE_STARTBYTES          = 2  # Number of bytes before the response payload (in stripped response)
     NUMBER_OF_CRC_BYTES                    = 2
     NUMBER_OF_LRC_BYTES                    = 1
     BITNUMBER_FUNCTIONCODE_ERRORINDICATION = 7

     MINIMAL_RESPONSE_LENGTH_RTU            = NUMBER_OF_RESPONSE_STARTBYTES + NUMBER_OF_CRC_BYTES
     MINIMAL_RESPONSE_LENGTH_ASCII          = 9

     # Argument validity testing

     plainresponse = response

     # Validate response length
     if mode == MODE_ASCII:
        if len(response) < MINIMAL_RESPONSE_LENGTH_ASCII:
            raise ValueError('Too short Modbus ASCII response (minimum length {} bytes). Response: {!r}'.format( \
                MINIMAL_RESPONSE_LENGTH_ASCII,
                response))
     elif len(response) < MINIMAL_RESPONSE_LENGTH_RTU:
            raise ValueError('Too short Modbus RTU response (minimum length {} bytes). Response: {!r}'.format( \
                MINIMAL_RESPONSE_LENGTH_RTU,
                response))

     # Validate the ASCII header and footer.
     if mode == MODE_ASCII:
        if response[BYTEPOSITION_FOR_ASCII_HEADER] != _ASCII_HEADER:
            raise ValueError('Did not find header ({!r}) as start of ASCII response. The plain response is: {!r}'.format( \
                _ASCII_HEADER,
                response))
        elif response[-len(_ASCII_FOOTER):] != _ASCII_FOOTER:
            raise ValueError('Did not find footer ({!r}) as end of ASCII response. The plain response is: {!r}'.format( \
                _ASCII_FOOTER,
                response))

        # Strip ASCII header and footer
        response = response[1:-2]

        if len(response) % 2 != 0:
            template = 'Stripped ASCII frames should have an even number of bytes, but is {} bytes. ' + \
                    'The stripped response is: {!r} (plain response: {!r})'
            raise ValueError(template.format(len(response), response, plainresponse))

        # Convert the ASCII (stripped) response string to RTU-like response string
        response = _hexdecode(response)

     # Validate response checksum
     if mode == MODE_ASCII:
        calculateChecksum = self._calculateLrcString
        numberOfChecksumBytes = NUMBER_OF_LRC_BYTES
     else:
        calculateChecksum = self._calculateCrcString
        numberOfChecksumBytes = NUMBER_OF_CRC_BYTES

     receivedChecksum = response[-numberOfChecksumBytes:]
     responseWithoutChecksum = response[0 : len(response) - numberOfChecksumBytes]
     calculatedChecksum = self._calculateCrcString(responseWithoutChecksum)

     if receivedChecksum != calculatedChecksum:
        template = 'Checksum error in {} mode: {!r} instead of {!r} . The response is: {!r} (plain response: {!r})'
        text = template.format(
                mode,
                receivedChecksum,
                calculatedChecksum,
                response, plainresponse)
        raise ValueError(text)

     # Check subordinate address
     responseaddress = ord(response[BYTEPOSITION_FOR_SLAVEADDRESS])

     if responseaddress != subordinateaddress:
        raise ValueError('Wrong return subordinate address: {} instead of {}. The response is: {!r}'.format( \
            responseaddress, subordinateaddress, response))

     # Check function code
     receivedFunctioncode = ord(response[BYTEPOSITION_FOR_FUNCTIONCODE])

     if receivedFunctioncode == self._setBitOn(functioncode, BITNUMBER_FUNCTIONCODE_ERRORINDICATION):
        raise ValueError('The subordinate is indicating an error. The response is: {!r}'.format(response))

     elif receivedFunctioncode != functioncode:
        print "receivedFunctioncode",receivedFunctioncode, functioncode
        raise ValueError('Wrong functioncode: {} instead of {}. The response is: {!r}'.format( \
            receivedFunctioncode, functioncode, response))

     # Read data payload
     firstDatabyteNumber = NUMBER_OF_RESPONSE_STARTBYTES

     if mode == MODE_ASCII:
        lastDatabyteNumber = len(response) - NUMBER_OF_LRC_BYTES
     else:
        lastDatabyteNumber = len(response) - NUMBER_OF_CRC_BYTES

     payload = response[firstDatabyteNumber:lastDatabyteNumber]
     return payload

############################################
## Serial communication utility functions ##
############################################


    def _predictResponseSize(mode, functioncode, payloadToSubordinate):
     MIN_PAYLOAD_LENGTH = 4  # For implemented functioncodes here
     BYTERANGE_FOR_GIVEN_SIZE = slice(2, 4)  # Within the payload

     NUMBER_OF_PAYLOAD_BYTES_IN_WRITE_CONFIRMATION = 4
     NUMBER_OF_PAYLOAD_BYTES_FOR_BYTECOUNTFIELD = 1

     RTU_TO_ASCII_PAYLOAD_FACTOR = 2

     NUMBER_OF_RTU_RESPONSE_STARTBYTES   = 2
     NUMBER_OF_RTU_RESPONSE_ENDBYTES     = 2
     NUMBER_OF_ASCII_RESPONSE_STARTBYTES = 5
     NUMBER_OF_ASCII_RESPONSE_ENDBYTES   = 4

     # Calculate payload size
     if functioncode in [5, 6, 15, 16]:
        response_payload_size = NUMBER_OF_PAYLOAD_BYTES_IN_WRITE_CONFIRMATION

     elif functioncode in [1, 2, 3, 4]:
        given_size = self._twoByteStringToNum(payloadToSubordinate[BYTERANGE_FOR_GIVEN_SIZE])
        if functioncode == 1 or functioncode == 2:
            # Algorithm from MODBUS APPLICATION PROTOCOL SPECIFICATION V1.1b
            number_of_inputs = given_size
            response_payload_size = NUMBER_OF_PAYLOAD_BYTES_FOR_BYTECOUNTFIELD + \
                                    number_of_inputs // 8 + (1 if number_of_inputs % 8 else 0)

        elif functioncode == 3 or functioncode == 4:
            number_of_registers = given_size
            response_payload_size = NUMBER_OF_PAYLOAD_BYTES_FOR_BYTECOUNTFIELD + \
                                    number_of_registers * _NUMBER_OF_BYTES_PER_REGISTER

     else:
        raise ValueError('Wrong functioncode: {}. The payload is: {!r}'.format( \
            functioncode, payloadToSubordinate))

     # Calculate number of bytes to read
     if mode == MODE_ASCII:
        return NUMBER_OF_ASCII_RESPONSE_STARTBYTES + \
            response_payload_size * RTU_TO_ASCII_PAYLOAD_FACTOR + \
            NUMBER_OF_ASCII_RESPONSE_ENDBYTES
     else:
        return NUMBER_OF_RTU_RESPONSE_STARTBYTES + \
            response_payload_size + \
            NUMBER_OF_RTU_RESPONSE_ENDBYTES


    def _calculate_minimum_silent_period(baudrate):

     BITTIMES_PER_CHARACTERTIME = 11
     MINIMUM_SILENT_CHARACTERTIMES = 3.5

     bittime = 1 / float(baudrate)
     return bittime * BITTIMES_PER_CHARACTERTIME * MINIMUM_SILENT_CHARACTERTIMES

##############################
# String and num conversions #
##############################


    def _numToOneByteString( self,inputvalue):
         return chr(inputvalue)


    def _numToTwoByteString(self,value, numberOfDecimals=0, LsbFirst=False, signed=False):

     multiplier = 10 ** numberOfDecimals
     integer = int(float(value) * multiplier)

     if LsbFirst:
        formatcode = '<'  # Little-endian
     else:
        formatcode = '>'  # Big-endian
     if signed:
        formatcode += 'h'  # (Signed) short (2 bytes)
     else:
        formatcode += 'H'  # Unsigned short (2 bytes)

     outstring = self._pack(formatcode, integer)
     assert len(outstring) == 2
     return outstring


    def _twoByteStringToNum(self,bytestring, numberOfDecimals=0, signed=False):

     formatcode = '>'  # BIG-end
     if signed:
        formatcode += 'h'  # (Signed) short (2 bytes)
     else:
        formatcode += 'H'  # Unsigned short (2 bytes)

     fullregister = self._unpack(formatcode, bytestring)
     
     if numberOfDecimals == 0:
        return fullregister
     divisor = 10 ** numberOfDecimals
     return fullregister / float(divisor)


     def _longToBytestring(self,value, signed=False, numberOfRegisters=2):
        formatcode = '>'  # BIG-end
        if signed:
           formatcode += 'l'  # (Signed) long (4 bytes)
        else:
           formatcode += 'L'  # Unsigned long (4 bytes)
        outstring = self._pack(formatcode, value)
        assert len(outstring) == 4
        return outstring


    def _bytestringToLong(self,bytestring, signed=False, numberOfRegisters=2):

      formatcode = '>'  # BIG end
      if signed:
        formatcode += 'l'  # (Signed) long (4 bytes)
      else:
        formatcode += 'L'  # Unsigned long (4 bytes)

      return self._unpack(formatcode, bytestring)


    def _floatToBytestring(self,value, numberOfRegisters=2):

      formatcode = '<'  # BIG end
      if numberOfRegisters == 2:
        formatcode += 'f'  # Float (4 bytes)
        lengthtarget = 4
      elif numberOfRegisters == 4:
        formatcode += 'd'  # Double (8 bytes)
        lengthtarget = 8
      else:
        raise ValueError('Wrong number of registers! Given value is {0!r}'.format(numberOfRegisters))

      outstring = self._unpack(formatcode, value)
      assert len(outstring) == lengthtarget
      return outstring


    def _bytestringToFloat(self,bytestring, numberOfRegisters=2):
 
      numberOfBytes = _NUMBER_OF_BYTES_PER_REGISTER * numberOfRegisters

      formatcode = '<'  # BIG end
      if numberOfRegisters == 2:
         formatcode += 'f'  # Float (4 bytes)
      elif numberOfRegisters == 4:
         formatcode += 'd'  # Double (8 bytes)
      else:
         raise ValueError('Wrong number of registers! Given value is {0!r}'.format(numberOfRegisters))
  
      if len(bytestring) != numberOfBytes:
         raise ValueError('Wrong length of the byte string! Given value is {0!r}, and numberOfRegisters is {1!r}.'.\
            format(bytestring, numberOfRegisters))
      h1 = self._twoByteStringToNum( bytestring[0:2] )
      h2 = self._twoByteStringToNum( bytestring[2:] )
      temp = struct.pack("<HH",h1,h2)
 
      return self._unpack(formatcode, temp)


    def _textstringToBytestring(self,inputstring, numberOfRegisters=16):
      maxCharacters = _NUMBER_OF_BYTES_PER_REGISTER * numberOfRegisters

      bytestring = inputstring.ljust(maxCharacters)  # Pad with space
      assert len(bytestring) == maxCharacters
      return bytestring


    def _bytestringToTextstring(self,bytestring, numberOfRegisters=16):
      maxCharacters = _NUMBER_OF_BYTES_PER_REGISTER * numberOfRegisters

      textstring = bytestring
      return textstring


    def _valuelistToBytestring(self,valuelist, numberOfRegisters):
      MINVALUE = 0
      MAXVALUE = 65535


      if not isinstance(valuelist, list):
         raise TypeError('The valuelist parameter must be a list. Given {0!r}.'.format(valuelist))


      numberOfBytes = _NUMBER_OF_BYTES_PER_REGISTER * numberOfRegisters

      bytestring = ''
      for value in valuelist:
         bytestring += self._numToTwoByteString(value, signed=False)

      assert len(bytestring) == numberOfBytes
      return bytestring


    def _bytestringToValuelist(self,bytestring, numberOfRegisters):

 
       numberOfBytes = _NUMBER_OF_BYTES_PER_REGISTER * numberOfRegisters
 

       values = []
       for i in range(numberOfRegisters):
           offset = _NUMBER_OF_BYTES_PER_REGISTER * i
           substring = bytestring[offset : offset + _NUMBER_OF_BYTES_PER_REGISTER]
           values.append(self._twoByteStringToNum(substring))

       return values


    def _pack(self,formatstring, value):
       try:
          result = struct.pack(formatstring, value)
       except:
          errortext = 'The value to send is probably out of range, as the num-to-bytestring conversion failed.'
          errortext += ' Value: {0!r} Struct format code is: {1}'
          raise ValueError(errortext.format(value, formatstring))

       if sys.version_info[0] > 2:
          return str(result, encoding='latin1')  # Convert types to make it Python3 compatible
       return result


    def _unpack(self,formatstring, packed):


      if sys.version_info[0] > 2:
        packed = bytes(packed, encoding='latin1')  # Convert types to make it Python3 compatible

      try:
        value = struct.unpack(formatstring, packed)[0]
      except:
        errortext = 'The received bytestring is probably wrong, as the bytestring-to-num conversion failed.'
        errortext += ' Bytestring: {0!r} Struct format code is: {1}'
        raise ValueError(errortext.format(packed, formatstring))

      return value


    def _hexencode(self,bytestring):
       outstring = ''
       for c in bytestring:
          outstring += '{0:02X}'.format(ord(c))
       return outstring


    def _hexdecode(self,hexstring):
      if len(hexstring) % 2 != 0:
        raise ValueError('The input hexstring must be of even length. Given: {!r}'.format(hexstring))

      if sys.version_info[0] > 2:
        by = bytes(hexstring, 'latin1')
        try:
            return str(binascii.unhexlify(by), encoding='latin1')
        except binascii.Error as err:
            new_error_message = 'Hexdecode reported an error: {!s}. Input hexstring: {}'.format(err.args[0], hexstring)
            raise TypeError(new_error_message)

      else:
        try:
            return hexstring.decode('hex')
        except TypeError as err:
            raise TypeError('Hexdecode reported an error: {}. Input hexstring: {}'.format(err.message, hexstring))


    def _bitResponseToValue(self,bytestring):

        RESPONSE_ON  = '\x01'
        RESPONSE_OFF = '\x00'

        if bytestring == RESPONSE_ON:
           return 1
        elif bytestring == RESPONSE_OFF:
          return 0
        else:
           raise ValueError('Could not convert bit response to a value. Input: {0!r}'.format(bytestring))


    def _createBitpattern(self,functioncode, value):

      if functioncode == 5:
         if value == 0:
            return '\x00\x00'
         else:
            return '\xff\x00'

      elif functioncode == 15:
         if value == 0:
            return '\x00'
         else:
            return '\x01'  # Is this correct??

    def _twosComplement(self,x, bits=16):

      upperlimit = 2 ** (bits - 1) - 1
      lowerlimit = -2 ** (bits - 1)
      if x > upperlimit or x < lowerlimit:
         raise ValueError('The input value is out of range. Given value is {0}, but allowed range is {1} to {2} when using {3} bits.' \
            .format(x, lowerlimit, upperlimit, bits))

      # Calculate two'2 complement
      if x >= 0:
        return x
      return x + 2 ** bits


    def _fromTwosComplement(self,x, bits=16):

      upperlimit = 2 ** (bits) - 1
      lowerlimit = 0
      if x > upperlimit or x < lowerlimit:
        raise ValueError('The input value is out of range. Given value is {0}, but allowed range is {1} to {2} when using {3} bits.' \
            .format(x, lowerlimit, upperlimit, bits))

      # Calculate inverse(?) of two'2 complement
      limit = 2 ** (bits - 1) - 1
      if x <= limit:
        return x
      return x - 2 ** bits

####################
# Bit manipulation #
####################


    def _XOR(self,integer1, integer2):
       return integer1 ^ integer2


    def _setBitOn( self,x, bitNum):
       return x | (1 << bitNum)


    def _rightshift(self,inputInteger):
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
        register = self._XOR(register, ord(character))

        # Rightshift 8 times, and XOR with polynom if carry overflows
        for i in range(8):
            register, carrybit = self._rightshift(register)
            if carrybit == 1:
                register = self._XOR(register, POLY)

      return self._numToTwoByteString(register, LsbFirst=True)


    def _calculateLrcString(self,inputstring):
      register = 0
      for character in inputstring:
        register += ord(character)

      lrc = ((register ^ 0xFF) + 1) & 0xFF
      lrcString = self._numToOneByteString(lrc)
      return lrcString






