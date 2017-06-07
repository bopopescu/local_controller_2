
import redis

'''
This script was used to migrate from one redis server to another redis server

'''

redis_ip  = [ "192.168.1.82","192.168.1.84"]
redis_db  = [ 0, 1]

for j in redis_db:
    redis_handle_original = redis.StrictRedis( redis_ip[0], port=6379, db = j )
    redis_handle_copy     = redis.StrictRedis( redis_ip[1], port=6379, db = j )
    keys = redis_handle_original.keys("*")
    for k in keys:
       type = redis_handle_original.type(k)
       if type == "hash":
           hkeys = redis_handle_original.hkeys(k)
           for l in hkeys:
               x = redis_handle_original.hget(k,l)
               redis_handle_copy.hset(k,l,x)
       elif type == "list":
           length = redis_handle_original.llen(k)
           for i in range(0,length):
               data = redis_handle_original.lindex(k,i)
               redis_handle_copy.rpush(k,data)
      
       else:
           data = redis_handle_original.get(k)
           redis_handle_copy.set(k,data)


