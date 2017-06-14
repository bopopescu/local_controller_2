import chain_flow
import datetime
import time

class Execute_Cf_Environment():
  def __init__(self,cf ):
       self.cf = cf
     

  def execute(self):
     time_stamp = datetime.datetime.today()
     old_day  = time_stamp.day
     old_hour = time_stamp.hour
     old_minute = time_stamp.minute
     old_second = time_stamp.second
     self.cf.execute_initialize()
     while True:
       time.sleep(.1)
       #self.cf.queue_event("SUB_SECOND_TICK",10)
       time_stamp = datetime.datetime.today()
       hour = time_stamp.hour
       minute = time_stamp.minute
       second = time_stamp.second
       day    = time_stamp.day
       if old_second != second :
         self.cf.queue_event( "TIME_TICK", second )
       if old_minute != minute :
         self.cf.queue_event( "MINUTE_TICK", minute )
       if old_hour != hour :
         self.cf.queue_event( "HOUR_TICK", minute )
       if old_day != day :
         self.cf.queue_event( "DAY_TICK", day )

       old_hour    = hour
       old_minute  = minute
       old_second  = second
       old_day     = day
       try:
          self.cf.execute(  ) 
       except:
          print( "chain flow exception" )
          print( "current chain is ",self.cf.current_chain["name"] )
          print( "current link  is ",self.cf.current_link          )
          raise


class CF_Interpreter(chain_flow.CF_Base_Interpreter ):
  def __init__(self):
       chain_flow.CF_Base_Interpreter.__init__(self)

  def  terminate( self,  link_name ):
     self.opcodes[ "Terminate"] =    self.terminate_code

  
  
  def  halt( self, link): 
    self.insert_link( link ,"Halt", [] )
   
   
  def  one_step( self, link, function, parameters):
     self.insert_link( link ,"Reset", [function, parameters] )
    
  
  def  reset( self, link):
    self.insert_link( link ,"Reset", [] )
 
         
  
  def  send_event( self, event_name,data ):
      self.insert_link( link ,"SendEvent",[event_name, data] )
   

  #note python dow is Monday 0  Sunday 6
  def  wait_tod( self, link,dow,hour,minute,second):
    self.insert_link( link ,"WaitTod",[dow,hour,minute,second] )
   
   
  def  wait_event( self, link,event_name):
    self.insert_link( link ,"WaitEvent",[event_name] )
 
   
  def  wait_time( self, link, time_tick):   
     self.insert_link( link ,"WaitTime",[time_tick] )
     
   
  def  wait_condition( self, link, function, parameters ): 
     self.insert_link( link ,"Wait",[function, parameters] )
    
   
   
  def  wait_event_reset( self, link, event_name, time_count):
    self.insert_link( link ,"WaitEvent_Reset",[event_name,time_count,0] )

  def wait_event_count( self, link, event_name, count ):
    self.insert_link( link ,"WaitEvent_Reset",[event_name, count,0] )
      
  def  wait_condition( self, link,function,parameters ):
     self.insert_link( link ,"Wait_Reset",[function, parameters] )
   
  def  verify_condition( self, link,function,parameters):
     self.insert_link( link ,"Verify",[function, parameters] )
    
   
  def  nop( self, link):
      self.insert_link( link ,"Nop" )
      
  def  log( self, link, message ):
     self.insert_link( link ,"Log",[message] )
   
  def  enable_chain( self, link, chain_names ):  
     self.insert_link(link,"Enable_Chain",[chain_names])
   
   
  def  disable_chain( self, link, chain_names):
       self.insert_link(link,"Disable_Chain",[chain_names] )
     
   
  def  init_state( self, link):
     self.opcodes["Init_State_Machine"] = self.init_state
     pass
   
  def  change_state( self, link, chain, state ):
    self.insert_link(link,"Change_State",[chain,state] )
   
  def  system_reset( self, link):
    self.insert_link(link,"RESET_SYSTEM")
     
      
        
        
        
        
      
        
         
     





# test code
if __name__ == "__main__":
    cf = CF_Interpreter()
    cf.define_chain( "Chain_1", True )
    cf.log( "test1","Chain_1 +++ is printed" )
    cf.reset("test2")
    cf.define_chain( "Chain_2", True )
    cf.log( "test1","Chain_2 +++ is printed" )
    cf.reset("test2")

    cf.execute_initialize()
    for i in range(0,10):
       print( i )
       cf.queue_event("TEST", [] )
       cf.execute(  )
    print("done")
