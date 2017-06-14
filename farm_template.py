import json

import redis_graph
from redis_graph.redis_graph_populate import Build_Configuration
from redis_graph.redis_graph_common import Redis_Graph_Common
import copy

class Construct_Farm(redis_graph.redis_graph_populate.Build_Configuration):

   def __init__( self, redis_handle, redis_graph_common ):
     
         super(Construct_Farm, self).__init__(redis_handle, redis_graph_common )
    

   def construct_system( self,name,properties={}):
       properties["name"] = name
       self.construct_node( push_namespace = True,  relationship="SYSTEM", label = "SYSTEM", name = name, 
          properties=properties)
       
   def end_system( self):
       self.pop_namespace()

   def construct_site( self,name, address, properties={}):
       properties["name"] = name
       properties["address"] = address
       self.construct_node(  push_namespace=True,relationship="SITE", label="SITE", name=name, 
               properties =properties)

   def end_site( self ):
      self.pop_namespace()

   def add_redis_data_store( self, name, ip, port=6379, properties = {} ):
       
       properties["ip"] = ip
       properties["port"] = port
       self.construct_node( push_namespace=True,relationship="DATA_STORE", label="DATA_STORE", name=name,
                               properties= properties )
   def start_moisture_store( self ):
       self.construct_node( push_namespace=True,relationship="MOISTURE_STORE", label="MOISTURE_STORE", name="MOISTURE_STORE",
                               properties= {} )

   def end_moisture_store( self ):
      self.pop_namespace()

      
   def add_moisture_sensor_store( self, name, description, description_map, depth_map, update_time ):
       properties = {}
       properties["description"] = description
       properties["description_map"] = json.dumps(description_map)
       properties["update_time"] = update_time
       properties["depth_map"] = json.dumps(depth_map)
       self.construct_node( push_namespace=True,relationship="MOISTURE_DATA", label="MOISTURE_DATA", name=name,
                               properties= properties )
   
   def add_status_store( self, name, queue_name):
       properties = {}
       properties["queue_name"] = queue_name
       self.construct_node( push_namespace=True,relationship="STATUS_STORE", label="STATUS_STORE", name=name,
                               properties= properties )

   def start_info_store( self ):
       self.construct_node( push_namespace=True,relationship="INFO_STORE", label="INFO_STORE", name="INFO_STORE",
                               properties= {} )

  
   def add_eto_store(self ):
       self.construct_node( push_namespace=False,relationship="ETO_STORE", label="ETO_STORE", name="ETO_STORE",
                               properties= {} )


   def add_air_temperature_humidity_store(self):
       self.construct_node( push_namespace=False,relationship="TEMP_HUMIDITY", label="TEMP_HUMIDITY", name="TEMP_HUMIDITY",
                               properties= {} )

   def add_air_temperature_humidity_daily_log(self):
       self.construct_node( push_namespace=False,relationship="TEMP_HUMIDITY_DAILY", label="TEMP_HUMIDITY_DAILY", name="TEMP_HUMIDITY_DAILY",
                               properties= {} )
       self.construct_node( push_namespace=False,relationship="TEMP_HUMIDITY_DAILY_ETO", label="TEMP_HUMIDITY_DAILY_ETO", name="TEMP_HUMIDITY_DAILY_ETO",
                               properties= {} )


   def end_info_store(self):   
       self.pop_namespace()



   def end_redis_data_store( self):
       self.pop_namespace()

   def add_udp_io_sever(self, name, ip,remote_type, port, properties={} ):
       properties["name"]=name
       properties["ip"] = ip
       properties["remote_type"] = remote_type
       properties["port"] = port
       return self.construct_node(  push_namespace=True,relationship="UDP_IO_SERVER", 
               label="UDP_IO_SERVER", name=name, properties = properties )


   def end_udp_io_server(self ):
       self.pop_namespace()


   def add_rtu_interface(self, name ,protocol, baud_rate, properties={} ):
       properties["name"] = name
       properties["protocol"]= protocol
       properties["baud_rate"] = baud_rate
       return self.construct_node(  push_namespace=True,relationship="RTU_INTERFACE", 
                 label="RTU_INTERFACE", name=name,properties = properties)

   def end_rtu_interface( self ):
       self.pop_namespace()



   def add_remote( self, name,modbus_address,type, function, properties = {}):

       properties["name"]           = name
       properties["modbus_address"] = modbus_address
       properties["type"]           = type
       properties["function"]       = function
       self.construct_node(  push_namespace=True,relationship="REMOTE", label="REMOTE", name=name, 
               properties = properties )


   def construct_controller( self,name, ip,type,properties={} ):
       properties["name"] = name
       properties["ip"]   = ip
       self.construct_node(  push_namespace=True,relationship="CONTROLLER", label="CONTROLLER", name=name, 
               properties = properties)


   def end_controller( self ):
       self.pop_namespace()

   def start_service( self, properties = {} ):
       self.construct_node(  push_namespace=TRUE,relationship="SERVICES", label="SERVICES", name=name, 
               properties = properties)


   def construct_web_server( self, name,url,properties = {} ):
       properties["name"]  = name
       properties["url"]   = url
       self.construct_node(  push_namespace=False,relationship="WEB_SERVER", label="WEB_SERVER", name=name, 
               properties = properties)

   def add_rabbitmq_command_rpc_queue( self,name, properties = {} ):
       properties["name"]  = "COMMAND_RPC_QUEUE"
       
       self.construct_node(  push_namespace=False,relationship="COMMAND_RPC_QUEUE", label="COMMAND_RPC_QUEUE", 
                                name=name, properties = properties)

   def add_rabbitmq_web_rpc_queue( self,name, properties = {} ):
       properties["name"]  = "WEB_RPC_QUEUE"
       
       self.construct_node(  push_namespace=False,relationship="WEB_RPC_QUEUE", label="WEB_RPC_QUEUE", 
                                name=name, properties = properties)

   def add_rabbitmq_event_queue( self,name, properties = {} ):
       properties["name"]  = "EVENT_QUEUE"
       
       self.construct_node(  push_namespace=False,relationship="RABBITMQ_EVENT_QUEUE", label="RABBITMQ_EVENT_QUEUE", 
                                name=name, properties = properties)



   def add_rabbitmq_status_queue( self,name,vhost,queue,port,server  ):
       properties          = {}
       properties["name"]  = "STATUS_QUEUE"
       properties["vhost"]    = vhost
       properties["queue"]    = queue
       properties["port"]     = port
       properties["server"]   = server
       
       self.construct_node(  push_namespace=False,relationship="RABBITMQ_STATUS_QUEUE", label="RABBITMQ_STATUS_QUEUE", 
                                name=name, properties = properties)


   def add_ntpd_server( self,name, properties = {} ):
       properties["name"]  = "NTPD_SERVER"
       
       self.construct_node(  push_namespace=False,relationship="NTPD_SERVER", label="NTPD_SERVER", 
                                name=name, properties = properties)


   def start_eto_server( self,name, properties = {} ):
       properties["name"]  = "ETO_SERVER"
       self.construct_node(  push_namespace=False,relationship="ETO_SERVER", label="ETO_SERVER", 
                                name=name, properties = properties)

   def add_eto_setup_code( self, access_codes, altitude , properties = {} ):
       properties["name"]          = "ETO_SETUP_DATA"
       properties["messo_eto"]     = json.dumps( access_codes["messo_eto"] )
       properties["messo_precp"]   = json.dumps( access_codes["messo_precp"] )
       properties["cimis_eto"]     = json.dumps( access_codes["cimis_eto"] )
       properties["cimis_spatial"] = json.dumps( access_codes["cimis_spatial"])
       properties["altitude"]      = altitude
       
       self.construct_node(  push_namespace=False,relationship="ETO_SETUP_DATA", label="ETO_SETUP_DATA", 
                                name="ETO_SETUP_DATA", properties = properties)


   def end_eto_server(self):
         self.pop_namespace()
   

   def add_linux_server_monitor( self, name,properties = {} ):
       properties["name"]  = "Linux Server Monitor"
       
       self.construct_node(  push_namespace=False,relationship="LINUX_SERVER_MONITOR", label="LINUX_SERVER_MONITOR", 
                                name=name, properties = properties)

   def add_schedule_monitoring( self, name,properties = {} ):
       properties["name"]  = "NTPD_SERVER"
       
       self.construct_node(  push_namespace=False,relationship="NTPD_SERVER", label="NTPD_SERVER", 
                                name=name, properties = properties)



   def add_moisture_monitoring( self, name, properties = {} ):
       properties["name"]  = "NTPD_SERVER"
       
       self.construct_node(  push_namespace=False,relationship="NTPD_SERVER", label="NTPD_SERVER", 
                                name=name, properties = properties)

   def irrigation_monitoring( self, name,properties = {} ):
       properties["name"]  = "IRRIGATION_MONITOR"
       
       self.construct_node(  push_namespace=False,relationship="IRRIGATION_MONITOR", label="IRRIGATION_MONITOR", 
                                name=name, properties = properties)

   def add_device_monitoring( self, name, properties = {} ):
       properties["name"]  = "DEVICE_MONITOR"
       
       self.construct_node(  push_namespace=False,relationship="DEVICE_MONITOR", label="DEVICE_MONITOR", 
                                name=name, properties = properties)

   def add_process_monitoring( self,name, properties = {}  ):
       properties["name"]  = "PROCESS_MONITOR"
       
       self.construct_node(  push_namespace=False,relationship="PROCESS_MONITOR", label="PROCESS_MONITOR", 
                                name=name, properties = properties)
   def add_watch_dog_monitoring( self,name, properties = {}  ):
       properties["name"]  = "WATCH_DOG_MONITORING"
       
       self.construct_node(  push_namespace=False,relationship="WATCH_DOG_MONITORING", label="WATCH_DOG_MONITORING", 
                                name=name, properties = properties)


   def add_io_collection( self, name, properties = {} ):
       properties["name"]  = "IO_COLLECTION"
       
       self.construct_node(  push_namespace=False,relationship="PROCESS_MONITOR", label="PROCESS_MONITOR", 
                                name=name, properties = properties)

   def add_local_ai( self, name, properties = {} ):
       properties["name"]  = "LOCAL_AI"
       
       self.construct_node(  push_namespace=False,relationship="PROCESS_MONITOR", label="PROCESS_MONITOR", 
                                name=name, properties = properties)

   


