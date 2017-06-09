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


class Remote_Interface_server():

   def __init__(self, redis_handle ):
     self.redis      = redis_handle
     self.cmds = {}
     self.cmds["PING"]                         = True
     self.cmds["REDIS_GET"]                    = self.redis_get
     self.cmds["REDIS_SET"]                    = self.redis_set
     self.cmds["REDIS_LLEN"]                   = self.redis_llen
     self.cmds["REDIS_LINDEX"]                 = self.redis_lindex
     self.cmds["REDIS_LSET"]                   = self.redis_lset
     self.cmds["REDIS_TRIM"]                   = self.redis_trim
     self.cmds["REDIS_PUSH"]                   = self.redis_lpush
     self.cmds["REDIS_POP"]                    = self.redis_rpop
     self.cmds["REDIS_DEL"]                    = self.redis_del
     self.cmds["REDIS_HGET"]                   = self.redis_hget
     self.cmds["REDIS_HSET"]                   = self.redis_hset
     self.cmds["REDIS_HGET_ALL"]               = self.redis_hget_all    
     self.cmds["REDIS_HDEL"]                   = self.redis_hdel
     self.cmds["REDIS_HKEYS"]                  = self.redis_hkeys
     self.cmds["REDIS_KEYS"]                   = self.redis_keys



   def redis_hkeys( self, command_data ):
     
       object_data = {}
       object_data["results"] = []
       for i in command_data:
          object_data["results"].append( self.redis.hkeys(i["hash"]).decode("utf-8")  )
       return object_data
 

   def redis_keys( self, command_data):
       object_data = {}
       object_data["results"] = []
       for i in command_data:
           object_data["results"].append( self.redis.keys(i["key"]).decode("utf-8") )
       return object_data

   def redis_get( self, command_data ):

        object_data = {}
        object_data["results"] = []
        for i in command_data:
           object_data["results"].append({"key":i, "data": self.redis.get(i).decode("utf-8")  } )
        return object_data

   def redis_set( self, command_data ):
        object_data = {}
        object_data["results"] = []
        for i in command_data:
           key  = i["key"]
           data = i["data"]
           self.redis.set(key,data )
        return object_data

   def redis_llen( self, command_data ):
       object_data = {}
       object_data["results"] = []
       for i in command_data:
          key = i
          object_data["results"].append({"key":i, "data":self.redis.llen(i)})
       return object_data

   def redis_lindex( self, command_data ):
       object_data = {}
       object_data["results"] = []
       for i in command_data:
          key    = i["key"]
          index  = int(i["index"])
          object_data["results"].append({"key":key, "index":index, "data":self.redis.lindex( key, index ).decode("utf-8")  })
       return object_data

   def redis_lset( self, command_data ):
       object_data = {}
       object_data["results"] = []
       for i in command_data:
          key    = i["key"]
          index  = int(i["index"])
          value  = i["data"]
          self.redis.lset(key,index,value)
       return object_data

   def redis_trim( self, command_data ):
       object_data = {}
       object_data["results"] = []
       for i in command_data:
          #print( "i",i)
          key      = i["key"]
          start    = i["start"]
          end      = i["end"]
          self.redis.ltrim(key,start, end)
    
       return object_data 

   def redis_lpush( self, command_data ):
       object_data = {}
       object_data["results"] = []
      
       for i in command_data:
            key    = i["key"]
            for j in i["data"]:
               self.redis.lpush( key, j )
      
       return object_data 

   def redis_rpop( self, command_data ):
       object_data = {}
       object_data["results"] = []

       for i in command_data:
          key    = i["key"]
          number = i["number"]
          temp1 = {"key": key,"number":number }
          temp = []
          for j in range(0,number):
              temp_1 = self.redis.rpop(key).decode("utf-8") 
              if temp_1 != None:
                 temp.append(temp_1)
          temp1["data"] = temp
          object_data["results"].append(temp1)
       return object_data 

   def redis_del( self, command_data):
       object_data = {}
       object_data["results"] = []
       
       for i in command_data:
          self.redis.delete(i)
       
       return object_data






   def redis_hdel( self, command_data): 
         object_data            = {}
         object_data["results"] = []
         for i in command_data:
            self.redis.hdel(i["hash"], i["key"] )
         return object_data
         
 


   #
   #  Array of dictionary where each element has the following values
   #       hash   = i["hash"]
   #       key    = i["key"]
   #       
   #
   # returns array of dictionaries where each dictionary has the following elements
   # "hash"
   # "key"
   # "value" 
      #       hash   = i["hash"]
   #       key    = i["key"]


   def redis_hget( self, command_data):
        object_data = {}
        object_data["results"] = []
        for i in command_data:
           object_data["results"].append({"hash":i["hash"], "key":i["key"], "data": self.redis.hget(i["hash"],i["key"]  ).decode("utf-8")  })
        return object_data

 
         

   #
   #  Array of dictionary where each element has the following values
   #       hash   = i["hash"]
   #       key    = i["key"]
   #       value  = i["data"]
   #
   # returns true

   def redis_hset( self, command_data): 
        object_data = {}
        object_data["results"] = []
        for i in command_data:
           #print( i)
           hash = i["hash"]
           key  = i["key"]
           data = i["data"]
           self.redis.hset(hash, key,data )
        return object_data

   #
   #  Array of dictionary where each element is dictionary key
   #       key    = i["key"]
   #       number = i["number"]
   #
   # returns array of dictionarys
    
   def redis_hget_all( self, command_data):
        object_data = {}
        object_data["results"] = []
        for i in command_data:
           object_data["results"].append({"hash":i["hash"],  "data": self.redis.hgetall(i["hash"]) } )
        return object_data



              

   def process_commands( self, command_data ):
       #print( "command ",command_data["command"])
       try:
            
            if self.cmds.has_key( command_data["command"] ) == True:
               if command_data["command"] == "PING":
                  object_data = command_data
                  object_data["reply"] = command_data["command"]
               else:
                  
                  object_data = self.cmds[ command_data["command"] ]( command_data["data"] )
                  object_data["reply"] = command_data["command"]
                  object_data["command"] = command_data["command"] 
            else:  
              object_data = {}
              object_data["reply"] = "BAD_COMMAND"
        
      
       except:
         print ("exception")
         object_data = {}
         object_data["reply"] = "BAD_COMMAND"
         object_data["results"] = None
       return object_data

   def on_request(self, ch, method, props, body):
       try:
           input_data   = json.loads( base64.b64decode(body))
           #print( "input_data",input_data)
           output_data  = self.process_commands( input_data )
           #print( "output_data",output_data)
       except:
          print( "exception")
          output_data = {}
          output_data["reply"] = "BAD_COMMAND"
          output_data["results"] = None
          output_data = json.dumps(output_data)

       #print( "data output = ",output_data)
       response     = base64.b64encode(  json.dumps(output_data ) )
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
   

   user_name = redis_handle.hget("redis_gateway", "user_name" ).decode("utf-8") 

   password  = redis_handle.hget("redis_gateway", "password"  ).decode("utf-8") 

   vhost     = redis_handle.hget("redis_gateway", "vhost"     ).decode("utf-8") 

   queue     = redis_handle.hget("redis_gateway", "queue"     ).decode("utf-8") 

   port      = int(redis_handle.hget("redis_gateway", "port"  ))
   server    = redis_handle.hget("redis_gateway", "server"    ).decode("utf-8") 

   
   print( "server",server)
   logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.CRITICAL)
   
   
   command_handler = Remote_Interface_server(redis_handle)
 
  
   credentials = pika.PlainCredentials( user_name, password )
   parameters = pika.ConnectionParameters( server,
                                                port,  #ssl port
                                                vhost,
                                                credentials,
                                                ssl = True ,
                                                 )
   connection = pika.BlockingConnection(parameters)
   channel = connection.channel()
   
   #channel.queue_delete(queue=queue)
   channel.queue_declare(queue=queue)
   channel.basic_qos(prefetch_count=1)
   channel.basic_consume( command_handler.on_request, queue=queue)
   print (" [x] Awaiting RPC requests")
   channel.start_consuming()

