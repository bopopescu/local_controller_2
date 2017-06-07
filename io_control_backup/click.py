import time

class PLC_Click():
   """ This package manages the the io dependencies for the click plc """

   
   def __init__(self,alarm_queue = None,io_server = None, redis=None,redis_dict=None ):
       self.alarm_queue       = alarm_queue
       self.io_server         = io_server
       self.redis             = redis
       self.redis_dict        = redis_dict
       self.click_reg_address = {}
       self.click_bit_address = {}
       self.click_io          = {}
       self.click_io["satellite_1"] = [
                  "Y001","Y002","Y003","Y004", # 1-4
                  "Y101","Y102","Y103","Y104","Y105","Y106","Y107","Y108", # 5 -12
                  "Y201","Y202","Y203","Y204","Y205","Y206","Y207","Y208", # 13 -20
                  "Y301","Y302","Y303","Y304","Y305","Y306","Y307","Y308", # 21 -28
                  "Y401","Y402","Y403","Y404","Y405","Y406","Y407","Y408", # 29 -36
                  "Y501","Y502","Y503","Y504", # 37 -40
                  "Y601","Y602","Y603","Y604" # 41 -44
             ]

       self.click_io["satellite_2"] = [
                      "Y001","Y002","Y003","Y004", "Y005","Y006", # 1-6
                      "Y101","Y102","Y103","Y104","Y105","Y106","Y107","Y108", # 7 -14
                      "Y201","Y202","Y203","Y204","Y205","Y206","Y207","Y208" # 15 -22
                ]


       self.click_io["satellite_3"] = [
                     "Y001","Y002","Y003","Y004", "Y005","Y006", # 1-6
                     "Y101","Y102","Y103","Y104","Y105","Y106","Y107","Y108", # 7 -14
                     "Y201","Y202","Y203","Y204","Y205","Y206","Y207","Y208" # 15 -22
                 ]

       for i in range(0,500): 
           temp ="DF"+str(i+1)
           self.click_reg_address[temp] = 0x7000+(i)*2

       for i in range(0,1000):
           temp = "DS"+str(i+1)
           self.click_reg_address[ temp ] = i

       for i in range(0,256):
           temp = "C"+str(i+1)
           self.click_bit_address[ temp ] = 0x4000 + i


       temp = [ "01","02","03","04","05","06","07","08","09","10","12","13","14","15","16" ]
       count = 0
       for i in temp:
          temp = "X0"+i
          self.click_bit_address[temp] = count
          temp = "X1"+i
          self.click_bit_address[temp] = 0x20 + count
          temp = "X2"+i
          self.click_bit_address[temp] = 0x40 + count
          temp = "X3"+i
          self.click_bit_address[temp] = 0x60 + count
          temp = "X4"+i
          self.click_bit_address[temp] = 0x80 + count
          temp = "X5"+i
          self.click_bit_address[temp] = 0xA0 + count
          temp = "X6"+i
          self.click_bit_address[temp] = 0xc0 + count
          temp = "X7"+i
          self.click_bit_address[temp] = 0xe0 + count
          temp = "X8"+i
          self.click_bit_address[temp] = 0x100 + count
          temp = "Y0"+i
          self.click_bit_address[temp] = 0x2000 +count
          temp = "Y1"+i 
          self.click_bit_address[temp] = 0x2020 + count
          temp = "Y2"+i
          self.click_bit_address[temp] = 0x2040 + count
          temp = "Y3"+i
          self.click_bit_address[temp] = 0x2060 + count
          temp = "Y4"+i
          self.click_bit_address[temp] = 0x2080 + count
          temp = "Y5"+i
          self.click_bit_address[temp] = 0x20A0 + count
          temp = "Y6"+i
          self.click_bit_address[temp] = 0x20c0 + count
          temp = "Y7"+i
          self.click_bit_address[temp] = 0x20e0 + count
          temp = "Y8"+i
          self.click_bit_address[temp] = 0x2100 + count
          count = count+1

       for i in range(1,999):
           temp = "SC"+str(i)
           self.click_bit_address[temp] = 0xf000 + i-1

   #
   # Specialized Functions related to sprinkler I/O and Click Programming
   #
   #
   #
   #
   #disable_all_sprinklers["xxxx"] = {"type":"CLICK","remote":"satellite_1","turn_off_bit":"dcc" }
   def disable_all_sprinklers( self, irrigation_record ):
      
       remote        = irrigation_record["remote"]
       output_bit    = irrigation_record["turn_off_bit"]
       if isinstance( output_bit, str):
           output_bit     = self.click_bit_address[ output_bit ]
       self.io_server.write_bit( remote, output_bit,1 )
      
   # 
   def turn_on_valves( self, remote, valve_list ):
  
       for valve in valve_list:  
          valve     = valve -1
          valve     = self.click_io[remote][ valve ]
          valve     = self.click_bit_address[valve]
          self.io_server.write_bit( remote,valve,1)
       
     
    
   def turn_off_valves( self, remote, valve_list  ):
       for valve in valve_list:
          valve     = valve -1  
          valve     = self.click_io[remote][ valve ]
          valve     = self.click_bit_address[valve]
          self.io_server.write_bit( remote,valve,0)
       
        
   #
   #  Clearing Duration counter is done through a falling edge
   #  going from 1 to 0 generates the edge
   def clear_duration_counters( self, duration_record ):
        remote       = duration_record["remote"]
        write_bit    = duration_record["clear_duration_counters"]
        if isinstance( write_bit, str):
             write_bit             = self.click_bit_address[write_bit]
        self.io_server.write_bit( remote, write_bit, 1 )
        self.io_server.write_bit( remote, write_bit, 0 )

         
                 


   def load_duration_counters( self,   duration,device ):
        #print "device",device
        #print "duration",duration
        remote            = device["remote"]
        write_bit         = device["clear_duration_counters"]
        write_register    = device["duration_counter"]
        #print "write register",write_register
        if isinstance( write_bit, str):
             write_bit             = self.click_bit_address[write_bit]
        if isinstance( write_register, str):
             write_register        = self.click_reg_address[write_register]
        #print "write_register",write_register
      
        self.io_server.write_registers( remote,write_register, [duration] )
        self.io_server.write_bit( remote, write_bit, 0 )  # counter is reset
        self.io_server.write_bit( remote, write_bit, 1 )  # counter is released from reset
        #print "duration counter",self.io_server.read_registers( remote,write_register,2)



   #
   #
   # Watch Dog Speciality functions
   #
   #
   #   
   # mode switch["xxxx"]     =   {"type":"CLICK", "remote":"satellite_1","read_bit":xxxx,"alarm_key":alarm_key,"alert_msg":alert_msg }
   # watchdog switch["xxxx"] =   {"type":"CLICK", "remote":"satellite_1","wd_bit":xxxx,"alarm_key":alarm_key,"alert_msg":alert_msg }


   def read_mode_switch( self, device ):
       remote =  device["remote"]
       rd_bit =  device["mode_switch"]
       if isinstance( rd_bit, str):
           rd_bit             = self.click_bit_address[  rd_bit]
       return self.io_server.read_bit( remote, rd_bit)

   def read_mode( self, device ):
       remote =  device["remote"]
       rd_bit =  device["mode"]
       if isinstance( rd_bit, str):
           rd_bit             = self.click_bit_address[ rd_bit]
       return self.io_server.read_bit( remote, rd_bit)

  
   def read_wd_flag( self, device ):
       remote =  device["remote"]
       rd_bit =  device["wd_bit"]
       if isinstance( rd_bit, str):
           rd_bit             = self.click_bit_address[ rd_bit]
       return self.io_server.read_bit( remote, rd_bit)
      

   def write_wd_flag( self, device, value  ):
       remote =  device["remote"]
       wd_bit =  device["wd_bit"]
       if isinstance( wd_bit, str):
           wd_bit             = self.click_bit_address[ wd_bit]
       if value != 0:
          value = 1
       self.io_server.write_bit( remote, wd_bit, value)
       





   #
   #
   # Basic IO Functions
   #
   #
   #
   #


 
                  

   def set_gpio_bit( self , redis_key, gpio_output, value ):
       remote        = gpio_output["remote"]
       output_bit    = gpio_output["output_bit"]
       if isinstance( output_bit, str):
           output_bit     = self.click_bit_address[ output_bit ]
       self.io_server.write_bit( remote, output_bit )
       self.redis.hset(self.redis_dict["GPIO_BITS"],redis_key,value )
            



        
   def get_gpio_bit( self , redis_key, gpio_input ):

       remote       = gpio_input["remote"]
       input_bit    = gpio_input["input_bit"]
       latch_enable = gpio_input["latch_enable"]
       latch_high   = gpio_input["latch_high"]
 
     
       if isinstance( input_bit, str):
           input_bit     = self.click_bit_address[input_bit ]
       value = self.io_server.read_bit( remote, input_bit )
       
       if latch_enable == False:
           self.redis.hset( self.redis_dict["GPIO_BITS"], redis_key,value)
       else:
           temp = self.redis.hget(self.redis_dict["GPIO_BITS"],redis_key )
           if temp != None:
              temp = int(temp)
           else:
              temp = input_bit
           if latch_high == True:
                if temp != 0:
                   
                   self.redis.hset( self.redis_dict["GPIO_BITS"],redis_key,1 )
                else:
                   
                   self.redis.hset( self.redis_dict["GPIO_BITS"],redis_key,value )
           else:        
               if temp == 0:
                    self.redis.hset(self.redis_dict,redis_key,0 )
               else:
                   self.redis.hset(self.redis_dict,redis_key,value )
      
       return self.redis.hget(self.redis_dict["GPIO_BITS"],redis_key)       
          

   def set_gpio_reg( self , redis_key, gpio_reg_output, valve ):
       remote        = gpio_ref_output["remote"]
       output_reg    = gpio_ref_output["output_reg"]
       if isinstance( output_bit, str):
           output_reg     = self.click_bit_address[ output_reg ]
       self.io_server.write_registers( remote, output_ref )
       self.redis.hset(self.redis_dict["GPIO_BITS"],redis_key,value )
            



        
   def get_gpio_reg( self , redis_key, gpio_reg_input ):

       remote       = gpio_input["remote"]
       input_reg    = gpio_input["input_reg"]
     
       if isinstance( input_bit, str):
           input_reg     = self.click_bit_address[ input_reg ]
       value = self.io_server.read_registers( remote, [input_reg] )
       self.redis.hset( self.redis_dict["GPIO_REGS"], redis_key,value)


   def measure_analog( self, redis_key, analog_input ):
       read_register      = analog_input["read_register"]
       remote             = analog_input["remote"]
       conversion_factor  = analog_input["conversion_factor"] 
       if isinstance( read_register, str):
           register           = self.click_reg_address[read_register]
       
       value              = self.io_server.read_float( remote, register )
       conv_value         = value * conversion_factor
       
       self.redis.hset( self.redis_dict["GPIO_ADC"], redis_key, conv_value)
       return conv_value
              
   
    
    
 



   def measure_counter( self,redis_key, counter_device, deltat=60 ):

       remote                = counter_device["remote"]
       latch_bit             = counter_device["latch_bit"]
       read_register         = counter_device["read_register"]
       conversion_factor     = counter_device["conversion_factor"]
       
       if isinstance( latch_bit, str):
           latch_bit             = self.click_bit_address[latch_bit]
       if isinstance( read_register, str):
             read_register         = self.click_reg_address[read_register]
       
       
       self.io_server.write_bit( remote, latch_bit, 1 )
       time.sleep(.001)
       self.io_server.write_bit( remote,latch_bit,0)
       time.sleep(.010)
       
       
       temp_value            = self.io_server.read_registers( remote, read_register, 1 )
       #print "temp_value",temp_value
       value = ((temp_value[0]/deltat)*60)   # normalize count to 60 sec
       self.redis.hset( self.redis_dict["COUNTER"], redis_key, value )
       #print redis_key,temp_value,deltat,conversion_factor,value
       return value



