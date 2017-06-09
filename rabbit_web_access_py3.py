#!/usr/bin/env python
import pika
import json
import base64
import time
import os
import redis
import logging
import farm_template_py3

global connection
from web_access_py3 import *

class Remote_Interface_server():

   def __init__(self ):
        self.redis                 = redis
        self.cmds                  = {}
        self.cmds["GET_WEB_PAGE"]  = self.get_web_page
        self.cmds["POST_WEB_PAGE"] = self.post_web_page
        self.cmds["PING"]          = self.ping

   def get_web_page( self, command_data ):
           
       results = web_client.get_path( command_data["path"] )
       return results

   def post_web_page( self, command_data ):
       results = web_client.post_path( path = command_data["path"], payload = command_data["data"] )
       
       return results

   def ping( self, command_data ):
      pass

          


   def process_commands( self, command_data ):
 
       try:
           object_data = {}
           command = command_data["command"]
           print( "command",command )
           if self.cmds.has_key( command ):
               result = self.cmds[command]( command_data)
               return  json.dumps( result )
           else:
           
              object_data = {}
              object_data["reply"] = "BAD_COMMAND_1"
              return json.dumps(object_data)
      
       except:
 
           object_data = {}
           object_data["reply"] = "BAD_COMMAND_2"
           object_data["results"] = None
           raise
           return json.dumps(object_data)                  


def on_request(ch, method, props, body):
    global rt
   
    try:
 
       input_data   = json.loads( base64.b64decode(body))
 
       output_data  = rt.process_commands( input_data )
       
    except:

       output_data = {}
       output_data["reply"] = "BAD_COMMAND_3"
       output_data["results"] = None
       output_data = json.dumps(output_data)


    response     = base64.b64encode(  output_data )
    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body= str(response) )
    ch.basic_ack(delivery_tag = method.delivery_tag)

  
if __name__ == "__main__":

   gm = farm_template_py3.Graph_Management("PI_1","main_remote","LaCima_DataStore")
   #
   # Now Find Data Stores
   #
   #
   #
   data_store_nodes = gm.find_data_stores()
   # find ip and port for redis data store
   data_server_ip   = data_store_nodes[0]["ip"]
   data_server_port = data_store_nodes[0]["port"]
   # find ip and port for ip server
   print( "data_server_ip",data_server_ip,data_server_port)
   redis_handle = redis.StrictRedis( host = data_server_ip, port=data_server_port, db = 2 )

   user_name = redis_handle.hget("web_gateway", "user_name" ).decode("utf-8") 

   password  = redis_handle.hget("web_gateway", "password"  ).decode("utf-8") 

   vhost     = redis_handle.hget("web_gateway", "vhost"     ).decode("utf-8") 

   queue     = redis_handle.hget("web_gateway", "queue"     ).decode("utf-8") 

   port      = int(redis_handle.hget("web_gateway", "port"  ))
   server    = redis_handle.hget("web_gateway", "server"    ).decode("utf-8") 


   web_client = Web_Client_Interface( )
   logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
   
   
   rt = Remote_Interface_server()
   credentials = pika.PlainCredentials( user_name, password )
   parameters = pika.ConnectionParameters(server,
                                           port,  #ssl port
                                           vhost,
                                           credentials,
                                           ssl = True ,
                                          heartbeat_interval=2000 )
   connection = pika.BlockingConnection(parameters)
   channel = connection.channel()
   #connection.socket.settimeout(10000)
   #channel.queue_delete(queue=queue)
   #time.sleep(20)
   channel.queue_declare(queue=queue)
   channel.basic_qos(prefetch_count=1)
   channel.basic_consume(on_request, queue=queue)
   print (" [x] Awaiting RPC requests")
   
   channel.start_consuming()
   #   print "start consuming is ended"
