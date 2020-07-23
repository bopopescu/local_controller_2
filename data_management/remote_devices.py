
remote_devices = {}
remote_devices["satellite_1"] = { "address":100 , "type":"CLICK" ,"turn_off_bit":"C1","clear_duration_counters":"C2", "wd_bit":"C200", "unknown":"SC10","mode_switch":"SC11" }             
remote_devices["satellite_2"] = { "address":125 , "type":"CLICK", "turn_off_bit":"C1","clear_duration_counters":"C2", "wd_bit":"C200", "unknown":"SC10","mode_switch":"SC11" }  
remote_devices["satellite_3"] = { "address":170 , "type":"CLICK" ,"turn_off_bit":"C1","clear_duration_counters":"C2", "wd_bit":"C200", "unknown":"SC10","mode_switch":"SC11" }

irrigation_io = {}
irrigation_io["satellite_1"] =  {  "type":"CLICK" ,"pins_number":44, "unknown":"C201", "clear_duration_counters":"C2","duration_counter":"DS2" }
irrigation_io["satellite_2"] =  {  "type":"CLICK" ,"pins_number":22, "unknown":"C201", "clear_duration_counters":"C2","duration_counter":"DS2" }
irrigation_io["satellite_3"] =  {  "type":"CLICK" ,"pins_number":22, "unknown":"C201", "clear_duration_counters":"C2","duration_counter":"DS2" }


main_valve_list = []
main_valve_list.append( { "type":"CLICK", "remote":"satellite_1","main_valve":43, "cleaning_valve":44 } )

#
#  debouncing is handled by subordinate device
#  latching is enabled or disabled
#  latching consists of High or Low Latching
#
gpio_input_devices = {}
gpio_input_devices["main_valve_set_switch"]   =  {"type":"CLICK", "remote":"satellite_1","input":"X002", "latch_enable":True ,"latch_high":True }
gpio_input_devices["main_valve_reset_switch"] =  {"type":"CLICK", "remote":"satellite_1","input":"X003", "latch_enable":True,"latch_high":True } 

analog_devices = {}
analog_devices["plc_current"]    = { "type":"CLICK", "remote":"satellite_1", "read_register":"DF1", "conversion_factor":1.0 }
analog_devices["coil_current"]   = { "type":"CLICK", "remote":"satellite_1", "read_register":"DF2", "conversion_factor":1.0 }
              

#
# redis keys for for flow sensors have the input sensor appended by input number, ie.  _1, _2
#
#
counter_devices = {}
counter_devices["main_sensor"] =   { "type":"CLICK", "remote":"satellite_1", "latch_bit":"C201","read_register":"DS301",  "conversion_factor":0.0224145939 }  
counter_devices["avocado_5"]   =   { "type":"CLICK", "remote":"satellite_3", "latch_bit":"C201","read_register":"DS302", "conversion_factor":0.0008005212  } 



'''

[ ["satellite_1","C201","DS301",1], 
  ["satellite_3","C201","DS301",8 ]

]

{
   "set_switches":   [ ["satellite_1","X002"] ],
   "reset_switches": [ ["satellite_1","X003"] ]
}
[ 
  ["satellite_1",[43],"satellite_1",[44] ]
]

[ 
   ["main_sensor", "satellite_1",1, 0.0224145939],
   ["avocado_5", "satellite_3",1,    0.0008005212 ],
   ["avocado_10", "satellite_3",2,    0.0008005212 ]
   
]


[
   { "name":"satellite_1", "pins":44, "bits":["C201","C2","DS2"] },
   { "name":"satellite_2", "pins":22, "bits":["C201","C2","DS2"] },
   { "name":"satellite_3", "pins":22, "bits":["C201","C2","DS2"] }
]
'''
