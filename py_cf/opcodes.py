
import datetime

class Opcodes():
  
  def __init__(self):
        
        self.opcodes = {}
        self.opcodes[ "Terminate"]        =    self.terminate_code
        self.opcodes[ "Break"]            =    self.break_code
        self.opcodes[ "Halt"]             =    self.halt_code
        self.opcodes["One_Step" ]         =    self.one_step_code   
        self.opcodes["Reset" ]            =    self.reset_code     
        self.opcodes["SendEvent"]         =    self.send_event_code 
        self.opcodes["WaitTod" ]          =    self.wait_tod_code  
        self.opcodes["WaitTodGE"]         =    self.wait_tod_ge_code
        self.opcodes["WaitTodGE"]         =    self.wait_tod_le_code
        self.opcodes["WaitEvent"]         =    self.wait_event_code
        self.opcodes["WaitEventCount"]    =    self.wait_event_count_code
        self.opcodes["WaitTime" ]         =    self.wait_time_code       
        self.opcodes["Wait"]              =    self.wait_condition_code  

        self.opcodes["WaitEvent_Reset"]   =    self.wait_event_code_reset
       
        self.opcodes["Wait_Reset"]        =    self.wait_condition_code_reset  
        self.opcodes["Verify"]            =    self.verify_condition_code 
        self.opcodes["Nop"]               =    self.nop  
        self.opcodes["Log"]               =    self.log 
        self.opcodes["Enable_Chain"]      =    self.enable_chain  
        self.opcodes["Disable_Chain"]     =    self.disable_chain 
        self.opcodes["Change_State"]      =    self.change_state 
        self.opcodes["RESET_SYSTEM"]      =    self.system_reset
        self.opcodes["Code"]              =    self.code_code
        self.opcodes["Suspend_Chain"]     =    self.suspend_chain_code
        self.opcodes["Resume_Chain"]      =    self.resume_chain_code
        self.opcodes["Code_Step"]         =    self.code_step_code


  def get_opcode( self, opcode_name):
     return self.opcodes[ opcode_name ]
  
  def add_opcode( self, name,code ):
       self.opcodes[name] = code
   
  def terminate_code( self, cf_handle, chainObj, parameters, event ):
      return "TERMINATE"
 

  def break_code( self, cf_handle, chainObj, parameters, event ):
       return "BREAK"


  def code_code( self, cf_handle, chainObj, parameters, event ):
      return_value =  parameters[0]( cf_handle, chainObj, parameters,event)
      #print "return_value%%%%%%%%%%%%%%%%%%%%%%", return_value
      return return_value
    
    
  def reset_code( self, cf_handle, chainObj, parameters, event ):
      return  "RESET"

  def halt_code( self, cf_handle, chainObj, parameters, event ):
      return  "HALT"
     
  def system_reset(  self, cf_handle, chainObj,parameters, event ):

     return "SYSTEM_RESET"


  def  nop( self, cf_handle,chainObj,parameters,event ):
      return "CONTINUE"

  def  wait_event_code( self, cf_handle, chainObj, parameters, event ):
    returnValue = "HALT"
    #print "event_name",event["name"]
    if event["name"] == parameters[0] :
       returnValue = "DISABLE"
 
    
    return returnValue


  def wait_event_count_code( self, cf_handle, chainObj, parameters, event ):

    returnValue = "HALT"
    if event["name"] == "INIT" :
          parameters[2] = 0
    else:
       if event["name"] == parameters[0] :
          parameters[2] = parameters[2]+1
          if parameters[2] >= int(parameters[1]) :
               returnValue = "DISABLE"
    
    return returnValue

  def  wait_event_code_reset( self, cf_handle,chainObj,parameters,event ):
    returnValue = "RESET"
    if event["name"] == parameters[0] :
       returnValue = "DISABLE"
    

    return returnValue


  def  wait_time_code( self, cf_handle,chainObj,parameters,event ):

   
       returnValue = "HALT"
     
       if event["name"] == "INIT" :
          parameters[1] = 0
       else:
	 if event["name"] == "TIME_TICK":
           parameters[1] = parameters[1] + 1
           #print "Time Tick",parameters[0],parameters[1]
       if parameters[0] <= parameters[1] :
	 returnValue = "DISABLE"

       return returnValue





  def  one_step_code(  self, cf_handle, chainObj,parameters, event ):
     if event["name"] == "INIT": 

        func = parameters[0]
        func(  cf_handle,chainObj,parameters, event )
     return "DISABLE"

  def  code_step_code(  self, cf_handle, chainObj,parameters, event ):
     if event["name"] == "INIT": 
        func = parameters[0]
        func(  cf_handle,chainObj,parameters, event )
     return "CONTINUE"


  

  def send_event_code(  self, cf_handle, chainObj,parameters, event ):
      #print "send event ",parameters[0]
      event_name = parameters[0]
      if len(parameters)  > 1 :
         event_data = parameters[1]
      else:
         event_data = None
     
      event = {}
      event["name"] = event_name
      event["data"] = event_data
      cf_handle.event_queue.append(event)

      return "DISABLE"

  
  def wait_tod_code(  self, cf_handle, chainObj,parameters, event ):
   
 
    returnValue = "HALT"
    dow = parameters[0]
    hour = parameters[1]
    minute = parameters[2]
    second = parameters[3]

    time_stamp = datetime.datetime.today()
   
    if ( ( dow == time_stamp.weekday()) or
	 ( dow == "*" ) ) == False:
	return returnValue
    

    if ( ( hour == time_stamp.hour ) or
	 ( hour == "*" ) ) == False:
	return returnValue
    

    if ( ( minute == time_stamp.minute ) or
	 ( minute == "*" ) ) == False:
	return returnValue
    
    if ( ( second == time_stamp.second ) or
	 ( second == "*" ) ) == False:
	return returnValue
   

    return "DISABLE"

  def wait_tod_ge_code(  self, cf_handle, chainObj,parameters, event ):
   
 
    returnValue = "HALT"
    dow = parameters[0]
    hour = parameters[1]
    minute = parameters[2]
    second = parameters[3]

    time_stamp = datetime.datetime.today()
   
    if (  ( dow == "*" ) or
	 ( dow >= time_stamp.weekday()) ) == False:
	return returnValue
   

    if ( ( hour == "*" ) or
	 ( hour >= time_stamp.hour ) ) == False:
	return returnValue
    

    if ( ( minute == "*"  ) or
	 ( minute >= time_stamp.minute ) ) == False:
	return returnValue
    
    if ( ( second == "*" ) or
	 ( second >= time_stamp.second  ) ) == False:
	return returnValue
   

    return "DISABLE"

  def wait_tod_le_code(  self, cf_handle, chainObj,parameters, event ):
   
 
    returnValue = "HALT"
    dow = parameters[0]
    hour = parameters[1]
    minute = parameters[2]
    second = parameters[3]

    time_stamp = datetime.datetime.today()
   
    if (  ( dow == "*" ) or
	 ( dow <= time_stamp.weekday()) ) == False:
	return returnValue
   

    if ( ( hour == "*" ) or
	 ( hour <= time_stamp.hour ) ) == False:
	return returnValue
    

    if ( ( minute == "*" ) or
	 ( minute <= time_stamp.minute ) ) == False:
	return returnValue
    
    if ( ( second == "*" ) or
	 ( second <= time_stamp.second  ) ) == False:
	return returnValue
   

    return "DISABLE"





  def wait_condition_code(  self, cf_handle, chainObj,parameters, event ):
     waitFn = parameters[0]
     if waitFn( cf_handle, chainObj,parameters, event ) == True:
	returnValue = "DISABLE"
     else:
	returnValue = "HALT"
 
     return returnValue

  def wait_condition_code_reset (  self, cf_handle, chainObj,parameters, event ): 

     waitFn = parameters[0]
     if waitFn( cf_handle, chainObj,parameters, event  ) == True:
	returnValue = "DISABLE"
     else:
	returnValue = "RESET"
   
     return returnValue


  def verify_condition_code(  self, cf_handle, chainObj,parameters, event ):

      waitFn      = parameters[0]
      if waitFn( cf_handle, chainObj,parameters, event  ) == True:
	  returnValue = "CONTINUE"
      else:
	returnValue = "RESET"
      
      return returnValue





  def log(  self, cf_handle, chainObj,parameters, event ):
     if event["name"] == "INIT" :
        print "Log ---",parameters[0] 
     return "DISABLE"
     




  def enable_chain(  self, cf_handle, chainObj,parameters, event ):
     chains = parameters[0]
     
     for j in chains:
        #print "enable", j
        cf_handle.enable_chain_base( j)
     return "DISABLE"



  def disable_chain(  self, cf_handle, chainObj,parameters, event ):
     chains = parameters[0]
     for j in chains:
        #print "disable ",j
	cf_handle.disable_chain_base( j)
  
     return "DISABLE"


  def resume_chain_code(  self, cf_handle, chainObj,parameters, event ):
     chains = parameters[0]
     
     for j in chains:
       
        cf_handle.resume_chain_code( j)
     return "DISABLE"



  def suspend_chain_code(  self, cf_handle, chainObj,parameters, event ):
     chains = parameters[0]
     for j in chains:
	cf_handle.suspend_chain_code( j)
  
     return "DISABLE"







  def change_state(  self, cf_handle, chainObj,parameters, event ):
     if event["name"] == "INIT" :
      chain = parameters[0]
      change_state = parameters[1]
      
      cf_handle.changeState( chain_state, chain  )
    
     return "DISABLE"




