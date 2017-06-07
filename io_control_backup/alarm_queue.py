
import redis
import json
import base64
import time

class AlarmQueue():
   def __init__(self,redis_server, alarm_queue = "QUEUES:CLOUD_ALARM_QUEUE", action_queue = "QUEUES:SPRINKLER:PAST_ACTIONS"):
       self.redis = redis_server
       self.alarm_queue = alarm_queue
       self.action_queue = action_queue

   def store_past_action_queue( self, event, status ,data = None):
       log_data = {}
       log_data["event"]   = event
       log_data["data"]     = data
       log_data["time" ]    = time.time()
       log_data["status"]   = status
       json_data            = json.dumps(log_data)
       json_data            =  base64.b64encode( json_data )
       self.redis.lpush( self.action_queue , json_data)
       self.redis.ltrim( self.action_queue ,0, 120 )
       self.store_alarm_queue( event,status, data )


   def store_alarm_queue( self, event,status, data ):
       log_data = {}
       log_data["event"] = event
       log_data["data"]     = data
       log_data["time" ]    = time.time()
       log_data["status"]   = status
       json_data            = json.dumps(log_data)
       json_data            =  base64.b64encode( json_data )
       self.redis.lpush( self.alarm_queue , json_data)
       self.redis.ltrim( self.alarm_queue ,0, 1000 )

   def store_event_queue( self, event, data ):
       log_data = {}
       log_data["event"] = event
       log_data["status"] = "INFO"
       log_data["data"]  = data
       log_data["time"]  = time.time()
       json_data = json.dumps(log_data)
       json_data = base64.b64encode(json_data)
       self.redis.lpush( self.alarm_queue, json_data)
       self.redis.ltrim( self.alarm_queue, 0,800)
  
   def update_time_stamp( self,*args ):
         self.redis.hset( "CONTROL_VARIABLES", "sprinkler_time_stamp", time.time() )

if __name__ == "__main__":
   import redis
   redis                        = redis.StrictRedis( host = "192.168.1.84", port=6379, db = 0 )
   alarm_queue = AlarmQueue(redis)
