
from opcodes import *

class CF_Base_Interpreter():

  def __init__(self):
    self.chains = []
    self.event_queue = []
    self.current_chain = None
    self.opcodes = Opcodes()
    self.valid_return_codes = {}
    self.valid_return_codes[ "CONTINUE"] = 1
    self.valid_return_codes[ "HALT"    ] = 1
    self.valid_return_codes[ "RESET"   ] = 1
    self.valid_return_codes[ "DISABLE" ] = 1
    self.valid_return_codes[ "TERMINATE"] = 1
    self.valid_return_codes[ "SYSTEM_RESET"] = 1
    self.valid_return_codes[ "BREAK" ] = 1

   
  
  #
  # Chain and link construction
  #

  def define_chain( self, chain_name, auto_start ):
    chain                 = {}
    chain["name"]         = chain_name
    chain["index"]        = 0
    chain["links"]        = []
    chain["auto_start"]    = auto_start
    chain["active"]       = False
    self.current_chain  = chain
    self.chains.append(chain)
     
  def insert_link( self, link_name, opcode_name, parameters):
     instruction = self.opcodes.get_opcode( opcode_name)
     link = {}
     link["name"]          = link_name
     link["op_code_name"]    = opcode_name
     link["instruction"]   = instruction  # [0] code [1] local parameters
     link["init_flag"]      = True
     link["active_flag"]    = True
     link["parameters"]    = parameters
     assert self.current_chain != None, "assertion test"
     self.current_chain["links"].append(link)

  def find_chain_object( self, chain_name ):
     for i in self.chains:
       if chain_name == i["name"]:
	 return i
     return None
  
  def chain_to_list( self, chain):
   return_value = chain
   if type(chain ) is not list:
      assert type(chain) is str, "chain name is not a string "
      return_value = [ chain ]
   return return_value
  
  def reset_chain( self, chain ):
 
     chain = self.chain_to_list( chain)
     for i in chain:
          assert type(i) is str, "chain name is not a string"
          k = self.find_chain_object( i)
          k["link_index"] = 0
          links = k["links"]
          for m in links:
	     m["active_flag"] = True
	     m["init_flag"] = True


  def resume_chain_code( self, chain ):
     chain = self.chain_to_list( chain)
     for i in chain: 
          assert type(i) is str, "chain name is not a string"
          k = self.find_chain_object( i)
          k["active"] = True
 
  def suspend_chain_code( self, chain ):
     chain = self.chain_to_list( chain)
     for i in chain: 
          assert type(i) is str, "chain name is not a string"
          k = self.find_chain_object( i)
          k["active"] = False



      
  def disable_chain_base( self, chain ):
     chain = self.chain_to_list( chain)
     for i in chain: 
          assert type(i) is str, "chain name is not a string"
          k = self.find_chain_object( i)
          k["link_index"] = 0
          k["active"] = False
          links = k["links"]
          for m in links:
	     m["active_flag"] = False
	     m["init_flag"] = True

  def enable_chain_base( self, chain ):
     chain = self.chain_to_list( chain)
     for i in chain: 
          assert type(i) is str, "chain name is not a string"
          #print "i",i
          k = self.find_chain_object( i)
          k["link_index"] = 0
          k["active"] = True
          links = k["links"]
          for m in links:
	     m["active_flag"] = True
	     m["init_flag"] = True

  def get_chain_state( self, chain ):
     assert type(chain) is str, "chain name is not a string"
     obj = self.find_chain_object( chain )
     return obj["active_flag"]

  def link_to_list( self, link):
   return_value = link
   if type(link ) is not list:
      assert type(link) is str, "chain name is not a string "
      return_value = [ link ]
   return return_value


  #
  # Link management
  #
  
  def find_link_object( self, chain, link ):
     links = chain["links"]
     for i in links:
       if link == i["name"]:
	 return i
     return None
   
  def link_to_list( self, link):
     return_value = link
     if type(link ) is not list:
      assert type(link) is str, "chain name is not a string "
      return_value = [ link ]
     return return_value  
 
 
 
  def enable_link( self, link, *ref_chain):
    
    link = self.link_to_list( link )
    
    if len(ref_chain) == 0:
      chain = self.current_chain
    else:
      chain = self.find_chain_object( ref_chain[0] )
    
    
    for j in link:
       k = self.find_link_object( chain, j )
       k["init_flag"] = True
       k["active_flag"] = True
       
  def disable_link( self, link, *ref_chain):
    
    link = self.link_to_list( link )
    
    if len(ref_chain) == 0:
      chain = self.current_chain
    else:
      chain = self.find_chain_object( ref_chain[0] )
    
    
    for j in link:
       k = self.find_link_object( chain, j )
       k["init_flag"] = True
       k["active_flag"] = False


  # change state to new link
  def change_state( self, active_link, *refChain  ):
    if len(ref_chain) == 0:
      chain = self.current_chain
    else:
      chain = self.find_chain_object( ref_chain[0] )
    
    link = self.find_link_obect( chain, active_link )
    for i in range( 0, len(chain["links"])): 
	chain["links"][i]["activeFlag"] = False
   
    link["initFlag"] = True
    link["activeFlag"] = True

  def send_event( self, event_name, event_data):
    event = {}
    event["name"] = event_name
    event["data"] = event_data
    self.event_queue.append(event)


  def execute_initialize( self ):
     self.event_queue = []
     for j in self.chains:
     
        if j["auto_start"]== True:
	   j["link_index"] = 1
	   j["active"] = True
	   self.reset_chain(  j["name"] )
	   
	else:
           j["active"] = False
	
	
	
  def execute( self ):
    while True:
       if len( self.event_queue ) > 0 :
         event = self.event_queue.pop()
         self.execute_event( event )
       else:
          return

  def execute_event( self,event ):
    for chain in self.chains:
       if chain["active"] == True:
         self.current_chain = chain
         self.execute_chain( chain, event )
      
   
  def execute_chain( self, chain, event ):
      loopFlag = True
      chain["link_index"] = 0
      while loopFlag == True:
	loopFlag = self.execute_link( chain,event )      
      
 
  def execute_link( self, chain, event  ):
     #print "execute_link", chain["name"]
     
     link_index          = chain["link_index"]
     self.current_link   = link_index
     #print "execute link",chain["name"],chain["link_index"],event
     if link_index >= len(chain["links"]):
       return False
     
     link             = chain["links"][link_index]
     opcode_name      = link["op_code_name"]
     instruction      = link["instruction"]
     init_flag        = link["init_flag"]
     active_flag      = link["active_flag"]
     parameters       = link["parameters"]
     return_value     = True
   
     if active_flag == True:
        if init_flag == True:
           init_event = {}
           init_event["name"] = "INIT"
           return_value = instruction(  self,  chain,parameters,  init_event )

	   link["init_flag"] = False
	   #print "initialize",return_value
	else:
	   return_value = "CONTINUE"
	   #print "no_init"
	if (return_value != "DISABLE") and (return_value != "RESET"): 
          temp = instruction( self, chain,parameters,event)
          #print "temp",temp
	  return_value = self.check_return_code( chain, link, temp)
	  #print "chain",chain["link_index"]
          #print "if" , return_value
	else:

         return_value = self.check_return_code( chain,link,return_value )
         #print "return value",return_value	
       
     else:
       
        link_index = link_index + 1
	return_value = True
        chain["link_index"] = link_index
        #print "else+++",return_value
  
     #print "return_value",return_value

     return return_value	     


  def queue_event( self, event_name, event_data ):
     temp = {}
     temp["name"] = event_name
     temp["data"] = event_data
     self.event_queue.append(temp)


  def check_return_code( self, chain, link , returnCode ):

     #print "returnCode ",returnCode
     return_value = False
     
     assert  self.valid_return_codes.has_key( returnCode ),"bad returnCode "+ chain["name"]
     if returnCode == "TERMINATE" :
       # "TERMINATE ______________ chain name",chain["name"]
       self.disable_chain_base( chain["name"] )
       return_value = False
     
    
     if returnCode == "BREAK" :
        self.disable_link( link["name"] )
        return_value = False
     

     if returnCode == "CONTINUE" :
       #print "made it here cont"
       chain["link_index"] = chain["link_index"]+1
       return_value = True
     

     if returnCode == "HALT" :
       return_value = False
     

     if returnCode == "DISABLE" :
        #print "made it here"
        self.disable_link(  link["name"] )
	chain["link_index"] = chain["link_index"] +1
	return_value = True
        #print "chain",chain["link_index"]
     

     if returnCode == "RESET" :
       
	self.reset_chain( chain["name"] )
	chain["link_index"] = 0
	return_value = False
    
     if returnCode == "SYSTEM_RESET" :
        self.execute_initialize()
        return_value = False
     
     return return_value

# test code
if __name__ == "__main__":
   
    cf = CF_Base_Interpreter()
    cf.define_chain( "Chain_1", True )
    cf.insert_link( "test1","Log",["Chain_1 is printed"] )
    cf.insert_link( "test2","Reset", [] )
    cf.define_chain( "Chain_2", True )
    cf.insert_link( "test1","Log",["Chain_2 is printed"] )
    cf.insert_link( "test2","Reset", [] )

    cf.execute_initialize()
    for i in range(0,10):
       print i
       cf.queue_event("TEST", [] )
       cf.execute(  )
    print("done")
