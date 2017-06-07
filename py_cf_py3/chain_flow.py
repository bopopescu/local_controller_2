class Opcodes():

    def __init__(self):

        self.opcodes = {}
        self.opcodes["Terminate"] = self.terminate_code
        self.opcodes["Break"] = self.break_code
        self.opcodes["Halt"] = self.halt_code
        self.opcodes["One_Step"] = self.one_step_code
        self.opcodes["Reset"] = self.reset_code
        self.opcodes["SendEvent"] = self.send_event_code
        self.opcodes["WaitTod"] = self.wait_tod_code
        self.opcodes["WaitTodGE"] = self.wait_tod_ge_code
        self.opcodes["WaitTodGE"] = self.wait_tod_le_code
        self.opcodes["WaitEvent"] = self.wait_event_code
        self.opcodes["WaitEventCount"] = self.wait_event_count_code
        self.opcodes["WaitTime"] = self.wait_time_code
        self.opcodes["Wait"] = self.wait_condition_code

        self.opcodes["WaitEvent_Reset"] = self.wait_event_code_reset

        self.opcodes["Wait_Reset"] = self.wait_condition_code_reset
        self.opcodes["Verify"] = self.verify_condition_code
        self.opcodes["Nop"] = self.nop
        self.opcodes["Log"] = self.log
        self.opcodes["Enable_Chain"] = self.enable_chain
        self.opcodes["Disable_Chain"] = self.disable_chain
        self.opcodes["Change_State"] = self.change_state
        self.opcodes["RESET_SYSTEM"] = self.system_reset
        self.opcodes["Code"] = self.code_code
        self.opcodes["Suspend_Chain"] = self.suspend_chain_code
        self.opcodes["Resume_Chain"] = self.resume_chain_code
        self.opcodes["Code_Step"] = self.code_step_code

    def get_opcode(self, opcode_name):
        return self.opcodes[opcode_name]

    def add_opcode(self, name, code):
        self.opcodes[name] = code

    def terminate_code(self, cf_handle, chainObj, parameters, event):
        return "TERMINATE"

    def break_code(self, cf_handle, chainObj, parameters, event):
        return "BREAK"

    def code_code(self, cf_handle, chainObj, parameters, event):
        return_value = parameters[0](cf_handle, chainObj, parameters, event)
        # print "return_value%%%%%%%%%%%%%%%%%%%%%%", return_value
        return return_value

    def reset_code(self, cf_handle, chainObj, parameters, event):
        return "RESET"

    def halt_code(self, cf_handle, chainObj, parameters, event):
        return "HALT"

    def system_reset(self, cf_handle, chainObj, parameters, event):

        return "SYSTEM_RESET"

    def nop(self, cf_handle, chainObj, parameters, event):
        return "CONTINUE"

    def wait_event_code(self, cf_handle, chainObj, parameters, event):
        returnValue = "HALT"
        # print "event_name",event["name"]
        if event["name"] == parameters[0]:
            returnValue = "DISABLE"

        return returnValue

    def wait_event_count_code(self, cf_handle, chainObj, parameters, event):

        returnValue = "HALT"
        if event["name"] == "INIT":
            parameters[2] = 0
        else:
            if event["name"] == parameters[0]:
                parameters[2] = parameters[2] + 1
                if parameters[2] >= int(parameters[1]):
                    returnValue = "DISABLE"

        return returnValue

    def wait_event_code_reset(self, cf_handle, chainObj, parameters, event):
        returnValue = "RESET"
        if event["name"] == parameters[0]:
            returnValue = "DISABLE"

        return returnValue

    def wait_time_code(self, cf_handle, chainObj, parameters, event):

        returnValue = "HALT"

        if event["name"] == "INIT":
            parameters[1] = 0
        else:
            if event["name"] == "TIME_TICK":
                parameters[1] = parameters[1] + 1
                # print "Time Tick",parameters[0],parameters[1]
        if parameters[0] <= parameters[1]:
            returnValue = "DISABLE"

        return returnValue

    def one_step_code(self, cf_handle, chainObj, parameters, event):
        if event["name"] == "INIT":

            func = parameters[0]
            func(cf_handle, chainObj, parameters, event)
        return "DISABLE"

    def code_step_code(self, cf_handle, chainObj, parameters, event):
        if event["name"] == "INIT":
            func = parameters[0]
            func(cf_handle, chainObj, parameters, event)
        return "CONTINUE"

    def send_event_code(self, cf_handle, chainObj, parameters, event):
        # print "send event ",parameters[0]
        event_name = parameters[0]
        if len(parameters) > 1:
            event_data = parameters[1]
        else:
            event_data = None

        event = {}
        event["name"] = event_name
        event["data"] = event_data
        cf_handle.event_queue.append(event)

        return "DISABLE"

    def wait_tod_code(self, cf_handle, chainObj, parameters, event):

        returnValue = "HALT"
        dow = parameters[0]
        hour = parameters[1]
        minute = parameters[2]
        second = parameters[3]

        time_stamp = datetime.datetime.today()

        if ((dow == time_stamp.weekday()) or
                (dow == "*")) == False:
            return returnValue

        if ((hour == time_stamp.hour) or
                (hour == "*")) == False:
            return returnValue

        if ((minute == time_stamp.minute) or
                (minute == "*")) == False:
            return returnValue

        if ((second == time_stamp.second) or
                (second == "*")) == False:
            return returnValue

        return "DISABLE"

    def wait_tod_ge_code(self, cf_handle, chainObj, parameters, event):

        returnValue = "HALT"
        dow = parameters[0]
        hour = parameters[1]
        minute = parameters[2]
        second = parameters[3]

        time_stamp = datetime.datetime.today()

        if ((dow == "*") or
                (dow >= time_stamp.weekday())) == False:
            return returnValue

        if ((hour == "*") or
                (hour >= time_stamp.hour)) == False:
            return returnValue

        if ((minute == "*") or
                (minute >= time_stamp.minute)) == False:
            return returnValue

        if ((second == "*") or
                (second >= time_stamp.second)) == False:
            return returnValue

        return "DISABLE"

    def wait_tod_le_code(self, cf_handle, chainObj, parameters, event):

        returnValue = "HALT"
        dow = parameters[0]
        hour = parameters[1]
        minute = parameters[2]
        second = parameters[3]

        time_stamp = datetime.datetime.today()

        if ((dow == "*") or
                (dow <= time_stamp.weekday())) == False:
            return returnValue

        if ((hour == "*") or
                (hour <= time_stamp.hour)) == False:
            return returnValue

        if ((minute == "*") or
                (minute <= time_stamp.minute)) == False:
            return returnValue

        if ((second == "*") or
                (second <= time_stamp.second)) == False:
            return returnValue

        return "DISABLE"

    def wait_condition_code(self, cf_handle, chainObj, parameters, event):
        waitFn = parameters[0]
        if waitFn(cf_handle, chainObj, parameters, event):
            returnValue = "DISABLE"
        else:
            returnValue = "HALT"

        return returnValue

    def wait_condition_code_reset(
            self,
            cf_handle,
            chainObj,
            parameters,
            event):

        waitFn = parameters[0]
        if waitFn(cf_handle, chainObj, parameters, event):
            returnValue = "DISABLE"
        else:
            returnValue = "RESET"

        return returnValue

    def verify_condition_code(self, cf_handle, chainObj, parameters, event):

        waitFn = parameters[0]
        if waitFn(cf_handle, chainObj, parameters, event):
            returnValue = "CONTINUE"
        else:
            returnValue = "RESET"

        return returnValue

    def log(self, cf_handle, chainObj, parameters, event):
        if event["name"] == "INIT":
            print( "Log ---", parameters[0] )
        return "DISABLE"

    def enable_chain(self, cf_handle, chainObj, parameters, event):
        chains = parameters[0]

        for j in chains:
            # print "enable", j
            cf_handle.enable_chain_base(j)
        return "DISABLE"

    def disable_chain(self, cf_handle, chainObj, parameters, event):
        chains = parameters[0]
        for j in chains:
            # print "disable ",j
            cf_handle.disable_chain_base(j)

        return "DISABLE"

    def resume_chain_code(self, cf_handle, chainObj, parameters, event):
        chains = parameters[0]

        for j in chains:

            cf_handle.resume_chain_code(j)
        return "DISABLE"

    def suspend_chain_code(self, cf_handle, chainObj, parameters, event):
        chains = parameters[0]
        for j in chains:
            cf_handle.suspend_chain_code(j)

        return "DISABLE"

    def change_state(self, cf_handle, chainObj, parameters, event):
        if event["name"] == "INIT":
            chain = parameters[0]
            change_state = parameters[1]

            cf_handle.changeState(chain_state, chain)

        return "DISABLE"




class CF_Base_Interpreter():

    def __init__(self):
        self.chains = []
        self.event_queue = []
        self.current_chain = None
        self.opcodes = Opcodes()
        self.valid_return_codes = {}
        self.valid_return_codes["CONTINUE"] = 1
        self.valid_return_codes["HALT"] = 1
        self.valid_return_codes["RESET"] = 1
        self.valid_return_codes["DISABLE"] = 1
        self.valid_return_codes["TERMINATE"] = 1
        self.valid_return_codes["SYSTEM_RESET"] = 1
        self.valid_return_codes["BREAK"] = 1

    #
    # Chain and link construction
    #

    def define_chain(self, chain_name, auto_start):
        chain = {}
        chain["name"] = chain_name
        chain["index"] = 0
        chain["links"] = []
        chain["auto_start"] = auto_start
        chain["active"] = False
        self.current_chain = chain
        self.chains.append(chain)

    def insert_link(self, link_name, opcode_name, parameters):
        instruction = self.opcodes.get_opcode(opcode_name)
        link = {}
        link["name"] = link_name
        link["op_code_name"] = opcode_name
        link["instruction"] = instruction  # [0] code [1] local parameters
        link["init_flag"] = True
        link["active_flag"] = True
        link["parameters"] = parameters
        assert self.current_chain is not None, "assertion test"
        self.current_chain["links"].append(link)

    def find_chain_object(self, chain_name):
        for i in self.chains:
            if chain_name == i["name"]:
                return i
        return None

    def chain_to_list(self, chain):
        return_value = chain
        if not isinstance(chain, list):
            assert isinstance(chain, str), "chain name is not a string "
            return_value = [chain]
        return return_value

    def reset_chain(self, chain):

        chain = self.chain_to_list(chain)
        for i in chain:
            assert isinstance(i, str), "chain name is not a string"
            k = self.find_chain_object(i)
            k["link_index"] = 0
            links = k["links"]
            for m in links:
                m["active_flag"] = True
                m["init_flag"] = True

    def resume_chain_code(self, chain):
        chain = self.chain_to_list(chain)
        for i in chain:
            assert isinstance(i, str), "chain name is not a string"
            k = self.find_chain_object(i)
            k["active"] = True

    def suspend_chain_code(self, chain):
        chain = self.chain_to_list(chain)
        for i in chain:
            assert isinstance(i, str), "chain name is not a string"
            k = self.find_chain_object(i)
            k["active"] = False

    def disable_chain_base(self, chain):
        chain = self.chain_to_list(chain)
        for i in chain:
            assert isinstance(i, str), "chain name is not a string"
            k = self.find_chain_object(i)
            k["link_index"] = 0
            k["active"] = False
            links = k["links"]
            for m in links:
                m["active_flag"] = False
                m["init_flag"] = True

    def enable_chain_base(self, chain):
        chain = self.chain_to_list(chain)
        for i in chain:
            assert isinstance(i, str), "chain name is not a string"
            # print "i",i
            k = self.find_chain_object(i)
            k["link_index"] = 0
            k["active"] = True
            links = k["links"]
            for m in links:
                m["active_flag"] = True
                m["init_flag"] = True

    def get_chain_state(self, chain):
        assert isinstance(chain, str), "chain name is not a string"
        obj = self.find_chain_object(chain)
        return obj["active_flag"]

    def link_to_list(self, link):
        return_value = link
        if not isinstance(link, list):
            assert isinstance(link, str), "chain name is not a string "
            return_value = [link]
        return return_value

    #
    # Link management
    #

    def find_link_object(self, chain, link):
        links = chain["links"]
        for i in links:
            if link == i["name"]:
                return i
        return None

    def link_to_list(self, link):
        return_value = link
        if not isinstance(link, list):
            assert isinstance(link, str), "chain name is not a string "
            return_value = [link]
        return return_value

    def enable_link(self, link, *ref_chain):

        link = self.link_to_list(link)

        if len(ref_chain) == 0:
            chain = self.current_chain
        else:
            chain = self.find_chain_object(ref_chain[0])

        for j in link:
            k = self.find_link_object(chain, j)
            k["init_flag"] = True
            k["active_flag"] = True

    def disable_link(self, link, *ref_chain):

        link = self.link_to_list(link)

        if len(ref_chain) == 0:
            chain = self.current_chain
        else:
            chain = self.find_chain_object(ref_chain[0])

        for j in link:
            k = self.find_link_object(chain, j)
            k["init_flag"] = True
            k["active_flag"] = False

    # change state to new link
    def change_state(self, active_link, *refChain):
        if len(ref_chain) == 0:
            chain = self.current_chain
        else:
            chain = self.find_chain_object(ref_chain[0])

        link = self.find_link_obect(chain, active_link)
        for i in range(0, len(chain["links"])):
            chain["links"][i]["activeFlag"] = False

        link["initFlag"] = True
        link["activeFlag"] = True

    def send_event(self, event_name, event_data):
        event = {}
        event["name"] = event_name
        event["data"] = event_data
        self.event_queue.append(event)

    def execute_initialize(self):
        self.event_queue = []
        for j in self.chains:

            if j["auto_start"]:
                j["link_index"] = 1
                j["active"] = True
                self.reset_chain(j["name"])

            else:
                j["active"] = False

    def execute(self):
        while True:
            if len(self.event_queue) > 0:
                event = self.event_queue.pop()
                self.execute_event(event)
            else:
                return

    def execute_event(self, event):
        for chain in self.chains:
            if chain["active"]:
                self.current_chain = chain
                self.execute_chain(chain, event)

    def execute_chain(self, chain, event):
        loopFlag = True
        chain["link_index"] = 0
        while loopFlag:
            loopFlag = self.execute_link(chain, event)

    def execute_link(self, chain, event):
        # print "execute_link", chain["name"]

        link_index = chain["link_index"]
        self.current_link = link_index
        # print "execute link",chain["name"],chain["link_index"],event
        if link_index >= len(chain["links"]):
            return False

        link = chain["links"][link_index]
        opcode_name = link["op_code_name"]
        instruction = link["instruction"]
        init_flag = link["init_flag"]
        active_flag = link["active_flag"]
        parameters = link["parameters"]
        return_value = True

        if active_flag:
            if init_flag:
                init_event = {}
                init_event["name"] = "INIT"
                return_value = instruction(self, chain, parameters, init_event)

                link["init_flag"] = False
                # print "initialize",return_value
            else:
                return_value = "CONTINUE"
                # print "no_init"
            if (return_value != "DISABLE") and (return_value != "RESET"):
                temp = instruction(self, chain, parameters, event)
                # print "temp",temp
                return_value = self.check_return_code(chain, link, temp)
                # print "chain",chain["link_index"]
                # print "if" , return_value
            else:

                return_value = self.check_return_code(
                    chain, link, return_value)
                # print "return value",return_value

        else:

            link_index = link_index + 1
            return_value = True
            chain["link_index"] = link_index
            # print "else+++",return_value

        # print "return_value",return_value

        return return_value

    def queue_event(self, event_name, event_data):
        temp = {}
        temp["name"] = event_name
        temp["data"] = event_data
        self.event_queue.append(temp)

    def check_return_code(self, chain, link, returnCode):

        # print "returnCode ",returnCode
        return_value = False

        assert returnCode in self.valid_return_codes, "bad returnCode " + \
            chain["name"]
        if returnCode == "TERMINATE":
            # "TERMINATE ______________ chain name",chain["name"]
            self.disable_chain_base(chain["name"])
            return_value = False

        if returnCode == "BREAK":
            self.disable_link(link["name"])
            return_value = False

        if returnCode == "CONTINUE":
            # print "made it here cont"
            chain["link_index"] = chain["link_index"] + 1
            return_value = True

        if returnCode == "HALT":
            return_value = False

        if returnCode == "DISABLE":
            # print "made it here"
            self.disable_link(link["name"])
            chain["link_index"] = chain["link_index"] + 1
            return_value = True
            # print "chain",chain["link_index"]

        if returnCode == "RESET":

            self.reset_chain(chain["name"])
            chain["link_index"] = 0
            return_value = False

        if returnCode == "SYSTEM_RESET":
            self.execute_initialize()
            return_value = False

        return return_value

  def execute(self):
     time_stamp = datetime.datetime.today()
     old_day = time_stamp.day
     old_hour = time_stamp.hour
     old_minute = time_stamp.minute
     old_second = time_stamp.second
     self.cf.execute_initialize()
     while True:
       time.sleep(.1)
       # self.cf.queue_event("SUB_SECOND_TICK",10)
       time_stamp = datetime.datetime.today()
       hour = time_stamp.hour
       minute = time_stamp.minute
       second = time_stamp.second
       day = time_stamp.day
       if old_second != second:
         self.cf.queue_event("TIME_TICK", second)
       if old_minute != minute:
         self.cf.queue_event("MINUTE_TICK", minute)
       if old_hour != hour:
         self.cf.queue_event("HOUR_TICK", minute)
       if old_day != day:
         self.cf.queue_event("DAY_TICK", day)

       old_hour = hour
       old_minute = minute
       old_second = second
       old_day = day
       try:
          self.cf.execute()
       except:
          print( "chain flow exception")
          print( "current chain is ", self.cf.current_chain["name"] )
          print( "current link  is ", self.cf.current_link)
          raise

# test code
if __name__ == "__main__":

    import datetime
    import time

'''
    cf = CF_Base_Interpreter()
    cf.define_chain("Chain_1", True)
    cf.insert_link("test1", "Log", ["Chain_1 is printed"])
    cf.insert_link("test2", "Reset", [])
    cf.define_chain("Chain_2", True)
    cf.insert_link("test1", "Log", ["Chain_2 is printed"])
    cf.insert_link("test2", "Reset", [])

    cf.execute_initialize()
    for i in range(0, 10):
        print( i )
        cf.queue_event("TEST", [])
        cf.execute()
    print("done")
'''