#!/usr/bin/env python

import json
import time
import redis
import logging



class Status_Queue():

   def __init__(self,redis_handle,status_queue ):
        self.redis_handle   = redis_handle
        self.status_queue   = status_queue
        


   def queue_message( self, routing_key, data  ):
       data["routing_key"] = routing_key
       self.redis_handle.rpush( self.status_queue, json.dumps(data))
       self.redis_handle.ltrim( self.status_queue, 0, 100 )
      


   def free_messages( self ):
 
       if self.redis_handle.llen( self.status_queue ) > 0:
           return_value = True
       else:
           return_value = False
       return return_value


   def dequeue_message( self ):
       return self.redis_handle.lpop(self.status_queue ).decode("utf-8") 


   def get_message( self ):
       return self.redis_handle.lindex(self.status_queue, -1).decode("utf-8")           


if __name__ == "__main__":

   import time
   import farm_template_py3
   import pika
   import json
   import time
   import os

   redis_startup       = redis.StrictRedis( host = "localhost", port=6379, db = 2 )

   rabbit_user_name = redis_startup.hget("status_gateway", "user_name" )
   rabbit_password  = redis_startup.hget("status_gateway", "password"  )

   graph_management = farm_template_py3.Graph_Management("PI_1","main_remote","LaCima_DataStore")
   status_servers = graph_management.match_terminal_relationship("RABBITMQ_STATUS_QUEUE")
   #print ("status_servers",type(status_servers),len(status_servers))
   status_server  = status_servers[0]

   vhost     = status_server["vhost"]
   queue     = status_server[ "queue"]
   port      = int(status_server[ "port" ])
   server    = status_server["server"]    
   #print "user_name",rabbit_user_name
   #print "password",rabbit_password
   credentials = pika.PlainCredentials( rabbit_user_name, rabbit_password )
   parameters = pika.ConnectionParameters(     server,
                                                port,  #ssl port
                                                vhost,
                                                credentials,
                                                ssl = True ,
                                                 )

   connection = pika.BlockingConnection(parameters)
   channel = connection.channel()
   channel.exchange_declare(exchange= queue,
                             type='fanout')
 
   data_store_nodes = graph_management.find_data_stores()
   
  
   # find ip and port for redis data store
   data_server_ip   = data_store_nodes[0]["ip"]
   data_server_port = data_store_nodes[0]["port"]
   redis_handle = redis.StrictRedis( host = data_server_ip, port=data_server_port, db = 12 )

   status_stores = graph_management.match_terminal_relationship("CLOUD_STATUS_STORE")
   #print ("status_stores",status_stores)
   status_store  = status_stores[0]
   queue_name    = status_store["queue_name"]

   status_queue = Status_Queue( redis_handle, queue_name )
 
   

   while True:
       time.sleep(1.0)
       if status_queue.free_messages() :
          data_json  = status_queue.get_message()
          data       = json.loads(data_json)
          routing_key = data["routing_key"]
  
          channel.basic_publish(exchange=queue,
                                routing_key=routing_key,
                                body=data_json)
          print(" [x] Sent %r" % "test message")
          status_queue.dequeue_message()

   connection.close()
  
   
