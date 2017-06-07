
if __name__ == "__main__":
   import   json
   import   python_udp_serial_server.modbus_redis_mgr
   import   python_udp_serial_server.rs485_mgr   
   import   python_udp_serial_server.modbus_serial_ctrl
   import   python_udp_serial_server.msg_manager
   import   python_udp_serial_server.python_udp_server
   import   construct_graph

   

  

   gm = construct_graph.Graph_Management("PI_1","main_remote","LaCima_DataStore")
   # Cheating here only assuming one udp io server and one serial link
   udp_io_server = gm.match_relationship("UDP_IO_SERVER")[0]
   temp_link   = gm.match_relationship("SERIAL_LINK")[0]
   rs485_interface =  python_udp_serial_server.rs485_mgr.RS485_Mgr() 
   temp_link["handler"] = rs485_interface
   serial_link = {}
   serial_link[temp_link["name"]] = temp_link  
 

   temp_remote_units  = gm.match_relationship("REMOTE_UNIT")
   remote_units = {}
   for i in temp_remote_units:
     i["interface"] = temp_link["name"]
     remote_units[i["name"]] = i

   serial_link = {}
   serial_link[temp_link["name"]] = temp_link  
   
   msg_mgr         =  python_udp_serial_server.msg_manager.MessageManager()
   print "temp_link",temp_link
   redis_host      =  udp_io_server["redis_host"]
   redis_db        =  int(udp_io_server["redis_db"])
   redis_handler   =  python_udp_serial_server.modbus_redis_mgr.ModbusRedisServer( message_handler= msg_mgr, host = "localhost" , redis_db = redis_db )


   modbus_serial_ctrl  = python_udp_serial_server.modbus_serial_ctrl.ModbusSerialCtrl( serial_link, remote_units, msg_mgr)

 
   for i,j in remote_units.items():
       msg_mgr.add_device( j["modbus_address"], modbus_serial_ctrl )



   msg_mgr.add_device( 255,    redis_handler) # This is for local server function
   print msg_mgr.ping_devices( [100] )
   #print msg_mgr.ping_all_devices()
   udp_server = python_udp_serial_server.python_udp_server.UDP_Server()
   udp_server.process_msg(msg_mgr)



