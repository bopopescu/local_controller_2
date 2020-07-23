#
#
#  configuration data
#  configuration.py
#
#  Note configuration takes data from files and various sources and creates object
#  data for various external processes
#



server_1_serial_interfaces = {}
#server_1_serial_interfaces[ "rtu_1" ] = { "type":"rs485_modbus", "interface_parameters":{ "interface":None, "timeout":.15, "baud_rate":38400 } ,"search_device":"current_monitor" } 
server_1_serial_interfaces[ "rtu_2" ] = { "type":"rs485_modbus", "interface_parameters":{ "interface":None, "timeout":.15, "baud_rate":38400 } ,"search_device":"main_controller" } 

server_1_remote_devices = {}
server_1_remote_devices["current_monitor"] = { "interface": "rtu_2", "parameters":{ "address":40 , "search_register":1,"register_number":10 }  }
server_1_remote_devices["main_controller"] = { "interface": "rtu_2", "parameters":{ "address":100 , "search_register":0, "register_number":1 } }
server_1_remote_devices["remote_1"]        = { "interface": "rtu_2", "parameters":{ "address":125 , "search_register":0 ,"register_number":1  } }
server_1_remote_devices["remote_2"]        = { "interface": "rtu_2", "parameters":{ "address":170 , "search_register":0, "register_number":1 } }

remote_devices = {}
remote_devices["satellite_1"] = {"remote":  "satellite_1", "UDP":"127.0.0.1", "address":100 , "type":"CLICK" ,
                                  "turn_off_bit":"C1","clear_duration_counters":"C2", 
                                  "wd_bit":"C200", "mode":"SC10","mode_switch":"SC11" } 
            
remote_devices["satellite_2"] = { "remote": "satellite_2", "UDP":"127.0.0.1", "address":125 , "type":"CLICK", 
                                  "turn_off_bit":"C1","clear_duration_counters":"C2", 
                                  "wd_bit":"C200", "mode":"SC10","mode_switch":"SC11" }
  
remote_devices["satellite_3"] = { "remote": "satellite_3" ,"UDP":"127.0.0.1", "address":170 , "type":"CLICK" ,
                                  "turn_off_bit":"C1","clear_duration_counters":"C2", "wd_bit":"C200", "mode":"SC10","mode_switch":"SC11" }

irrigation_io = {}
irrigation_io["satellite_1"] =  { "remote":  "satellite_1", "type":"CLICK" ,"pins_number":44, "unknown":"C201", "clear_duration_counters":"C2","duration_counter":"DS2"   ,"turn_off_bit":"C1"}
irrigation_io["satellite_2"] =  {  "remote": "satellite_2"  , "type":"CLICK" ,"pins_number":22, "unknown":"C201", "clear_duration_counters":"C2","duration_counter":"DS2", "turn_off_bit":"C1"}
irrigation_io["satellite_3"] =  {  "remote": "satellite_3" , "type":"CLICK" ,"pins_number":22, "unknown":"C201", "clear_duration_counters":"C2","duration_counter":"DS2"  ,"turn_off_bit":"C1"}

main_valve_list = {}
main_valve_list["satellite_1"] =  { "type":"CLICK", "remote":"satellite_1","main_valve":43, "cleaning_valve":44 } 
#
#  debouncing is handled by subordinate device
#  latching is enabled or disabled
#  latching consists of High or Low Latching
#
gpio_bit_input_devices = {}
gpio_bit_input_devices["main_valve_set_switch"]   =  {"type":"CLICK", "remote":"satellite_1","input_bit":"X002", "latch_enable":True ,"latch_high":True }
gpio_bit_input_devices["main_valve_reset_switch"] =  {"type":"CLICK", "remote":"satellite_1","input_bit":"X003", "latch_enable":True,"latch_high":True } 

main_switch_keys = [ "main_valve_set_switch" ]
main_reset_keys  = [ "main_valve_reset_switch"]

analog_devices = {}
analog_devices["plc_current"]    = { "type":"CLICK", "remote":"satellite_1", "read_register":"DF1", "conversion_factor":1.0 }
analog_devices["coil_current"]   = { "type":"CLICK", "remote":"satellite_1", "read_register":"DF2", "conversion_factor":1.0 }
              

#
# redis keys for for flow sensors have the input sensor appended by input number, ie.  _1, _2
#
#
counter_devices = {}
counter_devices["main_sensor"] =   { "type":"CLICK", "remote":"satellite_1", "latch_bit":"C201","read_register":"DS301",  "conversion_factor":0.0224145939 }  


#mode switch["xxxx"] =   {"type":"CLICK", "remote":"satellite_1","read_bit":xxxx,"alarm_key":alarm_key,"alert_msg":alert_msg }
#watchdog switch["xxxx"] =   {"type":"CLICK", "remote":"satellite_1","wd_bit":xxxx,"alarm_key":alarm_key,"alert_msg":alert_msg }
#disable_all_sprinklers["xxxx"] = {"type":"CLICK","remote":"satellite_1","turn_off_bit":"dcc" }

   
