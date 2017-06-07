import redis
from redis_graph_common import Redis_Graph_Common
import copy
import json

class Build_Configuration(object):

   def __init__( self, redis_handle, redis_graph_common ):
      self.common = redis_graph_common
      self.common.delete_all()
      self.namespace     = []
      self.redis        = redis_handle
 
   def build_namespace( self,name ):
       return_value = copy.deepcopy(self.namespace) 
       return_value.append(name)
       return return_value


   def pop_namespace( self ):
       del self.namespace[-1]    

   def add_header_node( self, label,name=None, properties = {}, json_flag= True ):
     if name == None:
        name = label
     properties["name"] = name
     self.construct_node( True, label, label, name, properties, json_flag )

   def end_header_node( self, assert_namespace ):
       #print self.namespace
       #print( "end_header_node",len(self.namespace),self.namespace)
       assert (assert_namespace == self.namespace[-1][0]) ,"miss match namespace  got  "+assert_namespace+" expected "+self.namespace[-1][0]
       del self.namespace[-1]    


   def check_namespace( self ):
       assert len(self.namespace) == 0, "unbalanced name space, current namespace: "+ json.dumps(self.namespace)
       print "name space is in balance"
      
   def add_info_node( self, label,name, properties = {}, json_flag= True ):
     properties["name"] = name
     
     self.construct_node( False, label, label, name, properties, json_flag )

   # concept of namespace name is a string which ensures unique name
   # the name is essentially the directory structure of the tree
   def construct_node(self, push_namespace,relationship, label, name, properties, json_flag = True ):
 
       
       redis_key, new_name_space = self.common.construct_node( self.namespace, relationship,label,name ) 
       for i in properties.keys():
           if json_flag == True:
              temp = json.dumps(properties[i] )
           else:
              temp = properties[i]
           self.redis.hset(redis_key, i, temp )
       
       
       if push_namespace == True:
          self.namespace = new_name_space
       
if __name__ == "__main__":
   # test driver
   redis  = redis.StrictRedis( host = "127.0.0.1", port=6379, db = 11 )   
   common = Redis_Graph_Common( redis)
   bc = Build_Configuration( common)   
   bc.construct_node( True, "HEAD","HEAD","HEAD",{})
   bc.construct_node( True, "Level_1","Level_1","level11",{})
   bc.construct_node( True, "Level_2","level_2","level21",{} )
   bc.pop_namespace()
   bc.construct_node( True, "Level_1","Level_1","level12",{})
   bc.construct_node( True, "Level_2","level_2","level22",{} )
   print redis.keys("*")
   common.delete_all()
   print redis.keys("*")


