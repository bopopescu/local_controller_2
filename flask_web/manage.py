import load_files
from functools import wraps
from werkzeug.contrib import authdigest
import flask

from flask import Flask
from flask import render_template,jsonify,request

#from app.flow_rate_functions    import *
#from app.system_state           import *
#from app.statistics_modules     import *
#from app.template_support       import *
import os
import redis
import json
redis_config = redis.StrictRedis('localhost', port=6379, db=2)
redis_server_ip    = redis_config.get("REDIS_SERVER_IP")
redis_server_db    = redis_config.get("REDIS_SERVER_DB")
redis_server_port  = redis_config.get("REDIS_SERVER_PORT")
redis_password_ip = redis_config.get("PASSWORD_SERVER_IP")
redis_password_db = redis_config.get("PASSWORD_SERVER_DB")
redis_password_port = redis_config.get("PASSWORD_SERVER_PORT")

redis_startup         = redis.StrictRedis( redis_password_ip, redis_password_port, redis_password_db )
startup_dict          = redis_startup.hgetall("web")


app = Flask(__name__)

#from io_control.io_controller_class import Build_Controller_Classes
#from io_control.new_instrument import Modbus_Instrument
#client_driver = Modbus_Instrument()
#controller_classes = Build_Controller_Classes(client_driver)
  
#udp_ping_client = controller_classes.get_controller_class( "192.168.1.84" )

redis_handle    = redis.StrictRedis(redis_server_ip, redis_server_port  , redis_server_db)
sys_files = load_files.SYS_FILES(redis_handle)
app_files = load_files.APP_FILES(redis_handle)

#flow_rate_functions = FlowRateFunctions(redis_handle  )
#system_status          = System_Status( redis_handle )
#statistics_module      = Statistics_Module(redis_handle)
#template_support       = template_support(redis_handle,statistics_module)

#  get handle to graphical data base
#  
#
#
#
#  
     
import construct_graph
gm = construct_graph.Graph_Management("PI_1","main_remote","LaCima_DataStore")


#
#  Set up redis data source
#
#
data_stores = gm.find_data_stores()
data_server_ip   = data_stores[0]["ip"]
data_server_port = data_stores[0]["port"]
#print "data_stores",data_stores, data_server_ip,data_server_port
redis_data_handle = redis.StrictRedis( host = data_server_ip, port=data_server_port, db = 12 )


#
#
# Setting up moisture controllers
#
#

#
#  Find moisture trigger ket
#
#



temp = gm.match_relationship("MOISTURE_MANUAL_UPDATE_FLAG")[0]
moisture_update_flag = temp["name"]

print moisture_update_flag

#moisture controllers
moisture_controllers = gm.assemble_name_list("name",gm.match_relationship("MOISTURE_CTR"))

moisture_data_sources = gm.form_dict_from_keys("name","queue_name", gm.match_relationship("MOISTURE_DATA"))



print moisture_controllers, moisture_data_sources

#
#
# Now see if moisture controllers have data sources
#
#

moisture_data_keys = gm.assemble_name_list("name",gm.match_relationship("MOISTURE_DATA"))

assert set(moisture_controllers).intersection(moisture_data_keys) != [], "problem in graphical data base"

print "db ok"
  

temp = gm.match_relationship("ETO_SITES")
eto_measurement    = temp[0]["measurement"]
temp = gm.match_relationship("RAIN_SOURCES")
rain_measurement    =  temp[0]["measurement"]

interfaces = []
remotes = {}
remote_interfaces = gm.match_relationship("UDP_IO_SERVER")
for i in remote_interfaces:

  interfaces.append(i["ip"])

remote_units = gm.match_relationship("REMOTE_UNIT")
remotes[ interfaces[0]] =[]

for i in remote_units:
   remotes[interfaces[0]].append(i["modbus_address"])

print interfaces
print remotes




  
class FlaskRealmDigestDB(authdigest.RealmDigestDB):
    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            request = flask.request
            if not self.isAuthenticated(request):
                return self.challenge()

            return f(*args, **kwargs)

        return decorated


app.config['SECRET_KEY']      = startup_dict["SECRET_KEY"]
app.config["DEBUG"]           = startup_dict["DEBUG"]
app.template_folder           = 'templates'
app.static_folder             = 'static'

authDB = FlaskRealmDigestDB(startup_dict["RealmDigestDB"])
temp =  json.loads(startup_dict["users"])
for i in temp:
    authDB.add_user(i["user"], i["password"] )


from flask import request, session

######################### Set up Static RoutesFiles ########################################

@app.route('/favicon.ico')
@authDB.requires_auth
def get_fav():
  return app.send_static_file("favicon.ico")
   
  

@app.route('/static/js/<path:filename>')
@authDB.requires_auth
def get_js(filename):
  return app.send_static_file(os.path.join('js', filename))

@app.route('/static/js_library/<path:filename>')
@authDB.requires_auth
def get_js_library(filename):
 return app.send_static_file(os.path.join('js_library', filename))

@app.route('/static/css/<path:filename>')
@authDB.requires_auth
def get_css(filename):
 return app.send_static_file(os.path.join('css', filename))

@app.route('/static/images/<path:filename>')
@authDB.requires_auth
def get_images(filename):
 return app.send_static_file(os.path.join('images', filename))

@app.route('/static/dynatree/<path:filename>')
@authDB.requires_auth
def get_dynatree(filename):
 return app.send_static_file(os.path.join('dynatree', filename))

@app.route('/static/themes/<path:filename>')
@authDB.requires_auth
def get_themes(filename):
 return app.send_static_file(os.path.join('themes', filename))

@app.route('/static/html/<path:filename>')
@authDB.requires_auth
def get_html(filename):
 return app.send_static_file(os.path.join('html', filename))

@app.route('/static/app_images/<path:filename>')
@authDB.requires_auth
def get_app_images(filename):
 return app.send_static_file(os.path.join('app_images', filename))



#@app.route('/static/html/<path:filename>')
#@authDB.requires_auth
#def get_html(filename):
# return render_template(filename)

@app.route('/static/data/<path:filename>')
@authDB.requires_auth
def get_data(filename):
  return app.send_static_file(os.path.join('data', filename))


@app.route("/ajax/get_system_file/<path:file_name>")
@authDB.requires_auth
def get_system_file(file_name):
   
   data = sys_files.load_file(file_name)
   
   return json.dumps(data)

@app.route("/ajax/get_app_file/<path:file_name>")
@authDB.requires_auth
def get_app_file(file_name):
   return json.dumps(app_files.load_file(file_name))

@app.route("/ajax/save_app_file/<path:file_name>",methods=["POST"] )
@authDB.requires_auth
def save_app_file(file_name):
    json_object = request.json
    app_files.save_file(file_name, json_object );
    return json.dumps('SUCCESS')


@app.route('/ajax/get_status',methods=["GET"])
@authDB.requires_auth
def get_status():
   temp = system_status.get_status()
   return temp


@app.route('/ajax/schedule_data',methods=["GET"])
@authDB.requires_auth
def schedule_data():
   temp = system_status.schedule_data()
   return temp


@app.route('/ajax/native_mode_change',methods=["POST"])
@authDB.requires_auth
def change_native_mode():
   json_object = request.json
   temp = system_status.native_mode_change(json_object)
   return temp

@app.route('/ajax/mode_change',methods=["POST"])
@authDB.requires_auth
def change_mode():
   json_object = request.json
   temp = system_status.mode_change(json_object)
   return temp


@app.route('/ajax/get_redis_keys',methods=["POST"])
@authDB.requires_auth
def get_redis():
   return_value = {}
   param = request.get_json()

   for i in param:
     
      temp = redis_handle.get( i )
      return_value[i] = temp
      
   return json.dumps( return_value )
   
@app.route('/ajax/set_redis_keys',methods=["POST"])
@authDB.requires_auth
def set_redis():
   return_value = []
   param = request.get_json()
   for i in param.keys():
       redis_handle.set( i,param[i] )
   return json.dumps('SUCCESS')

@app.route('/ajax/get_redis_hkeys',methods=["POST"])
@authDB.requires_auth
def hget_redis():
   return_value = {}
   param = request.get_json()
   
   for i in param["key_list"]:
     
      temp = redis_handle.hget( param["hash_name"], i )
      return_value[i] = temp
      
   return json.dumps( return_value )
   
@app.route('/ajax/set_redis_hkeys',methods=["POST"])
@authDB.requires_auth
def hset_redis():
   return_value = []
   param = request.get_json()
   print "param ---",param
   for i in param["key_list"].keys():
       redis_handle.hset( param["hash_name"], i,param["key_list"][i] )
   return json.dumps('SUCCESS')

@app.route('/ajax/get_redis_all_hkeys',methods=["POST"])
@authDB.requires_auth
def all_hget_redis():
   return_value = {}
   param = request.get_json()
   hash_name = param["hash_name"]
   keys = redis_handle.hkeys(hash_name)
   for i in keys:
     
      temp = redis_handle.hget( hash_name, i )
      return_value[i] = temp
      
   return json.dumps( return_value )


@app.route('/ajax/get_all_redis_list',methods=["POST"])
@authDB.requires_auth
def get_all_redis_list():
   return_value     = {}
   param            = request.get_json()
   list_name        = param["list_name"]
   
   number           = redis_handle.llen(list_name)
   
   return_value = redis_handle.lrange(list_name,0,number)
   
   return json.dumps( return_value )


 
@app.route('/ajax/delete_redis_list',methods=["POST"])
@authDB.requires_auth
def delete_redis_list():
   return_value     = {}
   param            = request.get_json()
   list_name        = param["list_name"]
   index            = param["index"]
   token            = param["delete_token"]
   for i in range(0,len(index) ):
      if index[i] != 0:
          redis_handle.lset(list_name,i,token)
   redis_handle.lrem(list_name,len(index),token)
   return json.dumps("SUCCESS")

@app.route('/ajax/delete_element',methods=["POST"])
@authDB.requires_auth
def delete_element():
   return_value     = {}
   param            = request.get_json()
   object_name      = param["object_name"]
 
   redis_handle.delete(object_name)
   return json.dumps("SUCCESS")

@app.route('/ajax/ping_modbus_device',methods=["POST"])
@authDB.requires_auth
def ping_modbus_devie():
   return_value     = {}
   param            = request.get_json()
   interface        = param["interface"] 
   remote           = param["remote"]
   print "ping",remote
   temp = udp_ping_client.ping_device(  [ remote ] )
   temp1  = json.loads( temp[1] )
   
   print "temp1",temp1
   if temp1[0]["result"] == True :
         return_value = "ping received for remote: "+remote
   else:
         return_value = "ping NOT received for remote: "+remote

   return json.dumps(return_value)



@app.route('/ajax/update_schedule',methods=["POST"])
@authDB.requires_auth
def update_schedule():
   return_value     = {}
   param              = request.get_json()
   action             = param["action"] 
   schedule           = param["schedule"] 
   schedule_data      = param["data"] 
   statistics_module.save_schedule_data( action,schedule, schedule_data )
   return json.dumps("SUCCESS")


@app.route('/ajax/update_flow_limit',methods=["POST"])
@authDB.requires_auth
def update_flow_limit():
   return_value     = {}
   param              = request.get_json() 
   schedule           = param["schedule"]
   sensor             = param["sensor"] 
   data               = param["limit_data"]
   statistics_module.process_flow_limit_values( sensor, schedule, data)
   return json.dumps("SUCCESS")

@app.route('/ajax/update_current_limit',methods=["POST"])
@authDB.requires_auth
def update_current_limit():
   return_value     = {}
   param              = request.get_json() 
   schedule           = param["schedule"]
   data               = param["limit_data"]
   statistics_module.process_current_limit_values( schedule, data)
   return json.dumps("SUCCESS")

@app.route('/ajax/update_resistance_limit',methods=["POST"])
@authDB.requires_auth
def update_resistance_limit():
   return_value     = {}
   param              = request.get_json() 
   controller         = param["controller"]
   data               = param["limit_data"]
   template_support.process_resistance_limit_values( controller, data)
   return json.dumps("SUCCESS")

@app.route('/index.html')
@authDB.requires_auth
def index_a():
  filename = "control"
  return render_template("diagnostics",filename="schedule_control")



@app.route('/')
@authDB.requires_auth
def index():
  filename = "control"
  print "made it here"
  return render_template("diagnostics",filename="schedule_control")

 
@app.route('/control/<filename>')
@authDB.requires_auth
def control(filename):
  return render_template("control",filename=filename)



str_prop = {}
str_prop["coil"] = {}
str_prop["coil"]["header"]        = "Recent Coil Current"
str_prop["coil"]["queue"]         = "/ajax/strip_chart/QUEUES:SPRINKLER:CURRENT:coil_current"
str_prop["coil"]["limit_low"]     = 0
str_prop["coil"]["limit_high"]    = 20
str_prop["coil"]["scale"]         = 1.
str_prop["coil"]["x_axis"]        = "Time"
str_prop["coil"]["y_axis"]        = "mAmp"
str_prop["plc"] = {}
str_prop["plc"]["header"]         = "Recent Plc Current"
str_prop["plc"]["queue"]          = "/ajax/strip_chart/QUEUES:SPRINKLER:CURRENT:plc_current"
str_prop["plc"]["limit_low"]      = -1.
str_prop["plc"]["limit_high"]     = 20
str_prop["plc"]["scale"]          = 1.
str_prop["plc"]["x_axis"]        = "Time"
str_prop["plc"]["y_axis"]        = "mAmp"


@app.route("/ajax/strip_chart/<queue>",methods=["POST"])
@authDB.requires_auth
def get_strip_chart(queue):
   # find element
   scale = 1
   for i in str_prop.keys():
     if str_prop[i]["queue"] == queue:
        scale = str_prop[i]["scale"]
  
   temp = flow_rate_functions.strip_chart(queue,scale)
   return temp


@app.route('/strip_chart/<filename>')
@authDB.requires_auth
def strip_chart(filename):
   if str_prop.has_key(filename ):
       header       = str_prop[filename]["header"]
       queue        = str_prop[filename]["queue"]
       limit_low    = str_prop[filename]["limit_low"]
       limit_high   = str_prop[filename]["limit_high"]
       x_axis       = str_prop[filename]["x_axis"]
       y_axis       = str_prop[filename]["y_axis"]
       return render_template("strip_chart", queue= queue, header_name = header,limit_low = limit_low,limit_high=limit_high,x_axis=x_axis,y_axis=y_axis )

@app.route('/diagnostics/<filename>')
@authDB.requires_auth
def diagnostics(filename):
    
       return render_template("diagnostics", filename = filename )


sel_prop = {}
sel_prop["flow"] = {}
sel_prop["flow"]["header"]        = "Flow Rate History GPM"
sel_prop["flow"]["queue"]          = "/ajax/sel_strip_chart/QUEUES:SPRINKLER:FLOW:"
sel_prop["flow"]["limit_low"]     = 0
sel_prop["flow"]["limit_high"]    = 40
sel_prop["flow"]["sel_function"]  = '/ajax/flow_sensor_names'
sel_prop["flow"]["sel_label"]     = "Flow Sensors"
sel_prop["flow"]["x_axis"]        = "Time"
sel_prop["flow"]["y_axis"]        = "GPM"
@app.route('/ajax/flow_sensor_names',methods=["GET"])
@authDB.requires_auth
def get_flow_sensor_names():
   temp = flow_rate_functions.get_flow_rate_sensor_names()
   return temp


@app.route('/ajax/start_moisture_conversion',methods=["POST"] )
@authDB.requires_auth
def start_moisture_conversion():
     param              = request.get_json() 
     index              = int(param["index"])
     
     print "event received",param,index
     print moisture_update_flag


     redis_data_handle.lpush( moisture_update_flag ,moisture_controllers[index] )

     return json.dumps(json.dumps(param))
     return "SUCCESS"

@app.route('/ajax/soil_moisture_update',methods=["POST"] )
@authDB.requires_auth
def soil_moisture_update():
     param              = request.get_json() 
     print param["index"], type( param["index"] )
     key_name = moisture_controllers[param["index"]]
     print moisture_data_sources
     key = moisture_data_sources[key_name]

     temp_json = redis_data_handle.lindex(key,0)
     temp_data = json.loads(temp_json)
     print "temp_data",temp_data
     print "temp_data",temp_data.keys()
     print "temp_data_meas",temp_data["measurements"].keys()
     temp_data_meas = temp_data["measurements"]
     output_data ="<h3> Output Data for Controller: "+temp_data["name"]
     output_data = output_data + " "+temp_data["description"]+" </h3>"
     output_data = output_data +"<h4><ul>"
     output_data = output_data +"<li> Read Status      : "+str(temp_data_meas["read_status"]) +" </li> "
     output_data = output_data +"<li> Time Stamp       : "+str(temp_data_meas["time_stamp"]) +" </li> "
     output_data = output_data +"<li> Air Temperature  : "+str(temp_data_meas["air_temperature"]) +" Deg F </li> "
     output_data = output_data +"<li> Air Humidity     : "+str(temp_data_meas["air_humidity"]) +"  %</li>"
     output_data = output_data +"<li> Soil Temperature : "+str(temp_data_meas["soil_temperature"]) +"  Deg F</li>"
     output_data = output_data +"</ul></h4>"
     description_map = temp_data["description_map"] 
     depth_map = temp_data["depth_map"]
     for i in range( len(description_map)):
        if description_map[i] != "empty":
           units = "ohms"
           if int( temp_data_meas["sensor_configuration"][i]) == 2:
              units = "cb"
           output_data = output_data + "<h3> sensor: "+str(i)+" description: "+description_map[i]+" </h3>"
           output_data = output_data+"<h4><ul>"
           output_data = output_data +"<li> sensor configuration: "+str(temp_data_meas["sensor_configuration"][i]) +" </li> " 
           output_data = output_data +"<li> sensor depth        : "+str(depth_map[i]) +"  inches </li> " 
           output_data = output_data +"<li> sensor data         : "+str(temp_data_meas["sensor_data"][i]) +"  "+units+" </li> " 
           output_data = output_data +"<li> raw resistance data : "+str(temp_data_meas["resistive_data"][i]) +" ohm </li> "
           output_data = output_data + "</ul></h4>"
     return json.dumps(output_data)



@app.route('/ajax/sel_strip_chart/<queue>',methods=["POST"])
@authDB.requires_auth
def sel_strip_chart(queue):


   temp = flow_rate_functions.sel_chart( queue )
   return temp

@app.route('/sel_chart/<filename>',methods=["GET"])
@authDB.requires_auth
def sel_chart(filename):
   if sel_prop.has_key(filename ):
       header_name   = sel_prop[filename]["header"]
       queue         = sel_prop[filename]["queue"]
       limit_low     = sel_prop[filename]["limit_low"]
       limit_high    = sel_prop[filename]["limit_high"]
       sel_function  = sel_prop[filename]["sel_function"]
       sel_label     = sel_prop[filename]["sel_label"]
       x_axis        = sel_prop[filename]["x_axis"]
       y_axis        = sel_prop[filename]["y_axis"]

    
       return render_template("sel_chart", queue= queue, header_name = header_name,limit_low = limit_low,limit_high=limit_high, 
                               sel_function = sel_function,sel_label = sel_label, x_axis=x_axis,y_axis=y_axis )


@app.route("/system_actions",methods=["GET"])
@authDB.requires_auth
def system_actions():  
       system_actions  = app_files.load_file("system_actions.json")
       
       return render_template( "system_actions",  
                               title="Configure System Events",
                               system_actions       =  app_files.load_file( "system_actions.json" ) ,
                               system_actions_json  =  json.dumps( system_actions ) )

@app.route("/add_schedule",methods=["GET"])
@authDB.requires_auth
def add_schedule():  
       return render_template( "schedule_list", 
                               template_type = "add", 
                               title="Add Schedule",
                               schedule_list      =  statistics_module.schedule_data.keys(),
                               pin_list           =  json.dumps(sys_files.load_file("controller_cable_assignment.json")),
                               schedule_data_json =  json.dumps(statistics_module.schedule_data)  ) 
@app.route("/copy_schedule",methods=["GET"])
@authDB.requires_auth
def copy_schedule():  
       return render_template( "schedule_list", 
                               template_type = "copy", 
                               title="Copy Schedule",
                               schedule_list      =  statistics_module.schedule_data.keys(),
                               pin_list           =  json.dumps(sys_files.load_file("controller_cable_assignment.json")),
                               schedule_data_json =  json.dumps(statistics_module.schedule_data)  ) 

@app.route("/delete_schedules",methods=["GET"])
@authDB.requires_auth
def delete_schedules_a():  
       print "length",len(statistics_module.schedule_data.keys())
       return render_template( "schedule_list", 
                               template_type = "delete", 
                               title="Delete Schedules",
                               schedule_list      =  statistics_module.schedule_data.keys(),
                               pin_list           =  json.dumps(sys_files.load_file("controller_cable_assignment.json")),
                               schedule_data_json =  json.dumps(statistics_module.schedule_data)  ) 



@app.route("/edit_schedules",methods=["GET"])
@authDB.requires_auth
def edit_schedules():  
       return render_template( "schedule_list", 
                               template_type = "edit",
                               title="Edit Schedule",
                               schedule_list      =  statistics_module.schedule_data.keys(),
                               pin_list           =  json.dumps(sys_files.load_file("controller_cable_assignment.json")),
                               schedule_data_json =  json.dumps(statistics_module.schedule_data)  ) 

 
  
 
  
@app.route('/configure_flow_limits/<int:flow_id>/<int:schedule_id>',methods=["GET"])
@authDB.requires_auth
def overall_flow_limits(flow_id,schedule_id):
       schedule_list = statistics_module.schedule_data.keys()
       sensor_name  = statistics_module.sensor_names[flow_id]
       max_flow_rate = 33
       canvas_list = template_support.generate_canvas_list( schedule_list[schedule_id], flow_id   ) 
       return render_template("overall_flow_limits", 
                               schedule_id=schedule_id,
                               flow_id=flow_id,  
                               header_name="Flow Overview  Max Flow Rate "+str(max_flow_rate), 
                               flow_sensors = statistics_module.sensor_names,
                               schedule_list = schedule_list, 
                               max_flow_rate = max_flow_rate, 
                               canvas_list= canvas_list )

@app.route('/configure_current_limits/<int:schedule_id>',methods=["GET"])
@authDB.requires_auth
def overal_current_limits(schedule_id):
       max_current = 30
       schedule_list = statistics_module.schedule_data.keys()
       canvas_list = template_support.generate_current_canvas_list( schedule_list[schedule_id]  ) 
       return render_template("overall_current_limits", 
                               schedule_id=schedule_id,
                               header_name="Valve Current Overview  Max Current "+str(max_current),
                               schedule_list = schedule_list, 
                               max_flow_rate = max_current, 
                               canvas_list= canvas_list )

  
@app.route('/overal_resistance_limits/<int:controller_id>',methods=["GET"])
@authDB.requires_auth
def overal_resistance_limits(controller_id):
       max_current      = 30
       controller_list,valve_list  = template_support.get_controller_list(controller_id)
       
       canvas_list      = template_support.resistance_canvas_list(  controller_id ) 
       return render_template("overal_resistance_limits", 
                               controller_id     = controller_id,
                               header_name       ="Valve Resistance Max Value:  "+str(max_current), 
                               controller_list   = controller_list,
                               max_current       = max_current, 
                               canvas_list       = canvas_list,
                               valve_list_json   = json.dumps(valve_list) )

@app.route('/overall_resistance/<int:controller_id>',methods=["GET"])
@authDB.requires_auth
def overall_resistance(controller_id):
       max_current      = 30
       controller_list,valve_list  = template_support.get_controller_list(controller_id)
       canvas_list      = template_support.resistance_canvas_list(  controller_id )
      
       return render_template("overall_resistance", 
                               controller_id     = controller_id,
                               header_name       ="Valve Resistance Max Value:  "+str(max_current), 
                               controller_list   = controller_list,
                               max_current       = max_current, 
                               canvas_list       = canvas_list )
       


@app.route('/eto_setup',methods=["GET"])
@authDB.requires_auth
def eto_setup():
       eto_data                = app_files.load_file( "eto_site_setup.json" )
       pin_list                = sys_files.load_file("controller_cable_assignment.json")
       return render_template("eto_setup_main",eto_data = eto_data, eto_data_json = json.dumps(eto_data), st = str, pin_list_json = json.dumps(pin_list) ) 
                             

@app.route('/configure_filter_cleaning',methods=["GET"])
@authDB.requires_auth
def configure_filter_cleaning():
       cleaning_interval = redis_handle.hget( "CONTROL_VARIABLES", "CLEANING_INTERVAL" )
       
       cleaning_list   = [ 0, 1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000 ]
      
       if cleaning_interval == None:
           cleaning_interval = cleaning_list[4]
       
       cleaning_interval = int(cleaning_interval)
       try:
          cleaning_index = cleaning_list.index(cleaning_interval)
       except:
          cleaning_index = len( cleaning_list)/2
           
       return render_template("configure_filter_cleaning",
                               cleaning_list = cleaning_list , 
                               cleaning_index = cleaning_index,
                               title_name ="Configure Filter Cleaning Parameters",
                               header_name ="Configure Filter Cleaning Parameters"  ) 
                           

@app.route('/configure_max_flow_rate',methods=["GET"])
@authDB.requires_auth
def configure_max_flow_rate(): 
       flow_cut_off = redis_handle.hget( "CONTROL_VARIABLES", "FLOW_CUT_OFF" )
  
       cut_off_list   = [ 1,2,3,4,5,10,15,20,25,30,35,40,45,50 ]
      
       if flow_cut_off == None:
           flow_cut_off = 30
  
       flow_cut_off = int(flow_cut_off)   
       try:
          flow_index = cut_off_list.index(flow_cut_off)
       except:
          flow_index = len(cut_off_list)/2
       
       return render_template("configure_max_flow_rate",
                               cut_off_list = cut_off_list , 
                               flow_index = flow_index,
                               title_name ="Configure Max Flow Cut Off Parameters",
                               header_name ="Configure Max Flow Cut Off Parameters"  ) 



@app.route('/site_map/<int:map_type>',methods=["GET"])
@authDB.requires_auth
def site_map(map_type):  
       return render_template( "site_map", map_type = map_type ) 
 

@app.route('/display_environmental_conditions',methods=["GET"])
@authDB.requires_auth
def display_environmental_conditions():
       keys  = redis_handle.hkeys("EQUIPMENT_ENVIRON")
       units = []
       for i in keys:
           temp =  json.loads(redis_handle.hget("EQUIPMENT_ENVIRON",i))
           temp["data"] = json.dumps(temp["data"])
           units.append( temp     )
       
       return render_template( "display_environmental_conditions",units = units ) 

                       
@app.route('/modbus_statistics',methods=["GET"])
@authDB.requires_auth
def modbus_statistics():
       interfaces = json.loads(redis_handle.get("MODBUS_INTERFACES"))
       return render_template( "modbus_statistics",interfaces = interfaces ) 

@app.route('/modbus_ping',methods=["GET"])
@authDB.requires_auth
def modbus_ping():
        
       json_interfaces = json.dumps(interfaces)
       json_remotes = json.dumps( remotes )
       print json_interfaces
       print json_remotes
       return render_template( "modbus_ping",interfaces = interfaces , remotes = remotes , json_interfaces = json_interfaces, json_remotes = json_remotes ) 


@app.route('/overall_flow_statistics/<int:flow_id>/<int:schedule_id>',methods=["GET"])
@authDB.requires_auth
def overall_flow_statistics(flow_id,schedule_id):
       schedule_list = statistics_module.schedule_data.keys()
       sensor_name  = statistics_module.sensor_names[flow_id]
       max_flow_rate = 33
       canvas_list = template_support.generate_canvas_list( schedule_list[schedule_id], flow_id   ) 
       return render_template("overall_flow_statistics", 
                               schedule_id=schedule_id,
                               flow_id=flow_id,  
                               header_name="Flow Overview  Max Flow Rate "+str(max_flow_rate), 
                               flow_sensors = statistics_module.sensor_names,
                               schedule_list = schedule_list, 
                               max_flow_rate = max_flow_rate, 
                               canvas_list= canvas_list )

@app.route('/overall_current_statistics/<int:schedule_id>',methods=["GET"])
@authDB.requires_auth
def overal_current_statistics(schedule_id):
       max_current = 20
       schedule_list = statistics_module.schedule_data.keys()
       canvas_list = template_support.generate_current_canvas_list( schedule_list[schedule_id]  ) 
       return render_template("overall_current_statistics", 
                               schedule_id=schedule_id,
                               header_name="Valve Current Overview  Max Current "+str(max_current),
                               schedule_list = schedule_list, 
                               max_flow_rate = max_current, 
                               canvas_list= canvas_list )


@app.route('/eto_raw_data',methods=["GET"])
@authDB.requires_auth
def eto_raw_data():
       eto_data =  redis_data_handle.get(eto_measurement)
       rain_data = redis_data_handle.get(rain_measurement)
       return render_template( "eto_raw_data",eto_data = eto_data, rain_data = rain_data ) 


@app.route('/soil_moisture_data',methods=["GET"])
@authDB.requires_auth
def soil_moisture_raw_data():
        return render_template( "soil_moisture_data", web_moisture_names=moisture_controllers )

@app.route('/soil_moisture_data_a',methods=["GET"])
@authDB.requires_auth
def soil_moisture_raw_data_a():
        moisture_resistive_data = json.loads(redis_handle.hget("MOISTURE_CONTROL",'MOISTURE_RESISTIVE_DATA'))
        air_temp               = redis_handle.hget("MOISTURE_CONTROL",'AIR_TEMP_FLOAT')
        air_humidity           = redis_handle.hget("MOISTURE_CONTROL","AIR_HUMIDITY_FLOAT")
        read_status            = redis_handle.hget("MOISTURE_CONTROL","READ_STATUS")
        moisture_data          = json.loads(redis_handle.hget("MOISTURE_CONTROL","MOISTURE_DATA"))
        one_wire_device        = redis_handle.hget("MOISTURE_CONTROL","ONE_WIRE_DEVICE_FOUND")
        moisture_temp          = redis_handle.hget("MOISTURE_CONTROL","MOISTURE_SOIL_TEMP_FLOAT")
        temp          = json.loads(redis_handle.hget("MOISTURE_CONTROL","MOISTURE_CONFIGURATION"))
        moisture_configuration = []
        for i in range(0,len(moisture_data)):
           if temp[i] == 0 :
          
             moisture_configuration.append("Not Used")
           if temp[i] == 1:
             moisture_data[i] = str(moisture_data[i]) + " ohms"
             moisture_configuration.append("Resistive Element")
           if temp[i] == 2:
             moisture_data[i] = str( moisture_data[i])+ "  cb"
             moisture_configuration.append("Water Mark")

 
        return render_template( "soil_moisture_data_a", moisture_resistive_data=moisture_resistive_data,air_temp=air_temp, 
                               air_humidity=air_humidity, read_status=read_status, moisture_data=moisture_data,one_wire_device=one_wire_device,
                               moisture_temp=moisture_temp, moisture_configuration = moisture_configuration ) 



@app.route('/soil_moisture_plc',methods=["GET"])
@authDB.requires_auth
def soil_moisture_plc_status():
       #eto_data =  redis_handle.hget("CONTROL_VARIABLES","ETO_DATA")
       #rain_data = redis_handle.hget("CONTROL_VARIABLES","RAIN_DATA")
       return render_template( "soil_moisture_plc_status" ) 


@app.route('/view_running_process',methods=["GET"])
@authDB.requires_auth
def view_running_process():
   os.system("/home/pi/new_python/python_process.bsh > tmp_file")
   with open("tmp_file","r") as myfile:
       data = myfile.readlines()
   print "length of data",len(data)
   return render_template( "view_running_processes",file_list = data ) 



@app.route('/list_reboot_files',methods=["GET"])
@authDB.requires_auth
def list_reboot_files():

   os.system("ls -l /tmp/*.errr > tmp_file")
   data = ""
   with open("tmp_file","r") as myfile:
       data = myfile.readlines()
   print "length of data",len(data)
   return render_template( "list_reboot_files" ,file_list = data )
 
@app.route('/reboot_system',methods=["GET"])
@authDB.requires_auth
def reboot_system():
   os.system("sudo reboot")
   return "system rebooted"

display_control = []
temp  = {}
temp["name"]              = "Average Flow"
temp["flow_sensor_flag"]  = True
temp["time_step_flag"]    = False
temp["ajax_path"]      = "-----------TBD----------"
temp['limit_low']      = 0
temp['limit_high']     = 40
temp['x_axis']         = "Time"
temp['y_axis']         = "GPM"
temp["time_generation"] = False
temp["average_generation"] = True
temp["label_array"]        =  ['Time',"GPM"]

display_control.append(temp)
temp  = {}
temp["name"]               = "Time Series Flow"
temp["flow_sensor_flag"]   = True
temp["time_step_flag"]     = True
temp["ajax_path"]          = "-----------TBD----------"
temp['limit_low']          = 0
temp['limit_high']         = 40
temp['x_axis']             = "Time"
temp['y_axis']             = "GPM"
temp["time_generation"]    = True
temp["average_generation"] = False
temp["label_array"]        =  ['Time', 'Flow Rate 1',"Flow Rate 2","Flow Rate 3","Flow Rate 4","Flow Rate 5"]

display_control.append(temp)
temp  = {}
temp["name"]              = "Total Flow"
temp["flow_sensor_flag"]  = True
temp["time_step_flag"]    = False
temp["ajax_path"]      = "-----------TBD----------"
temp['limit_low']      = 1
temp['limit_high']     = 10000
temp['x_axis']         = "Time"
temp['y_axis']         = "Gallons"
temp["time_generation"]    = False
temp["average_generation"] = True
temp["label_array"]        =  ['Time',"Gallons"]

display_control.append(temp)
temp  = {}
temp["name"]              = "Average Current"
temp["flow_sensor_flag"]  = False
temp["time_step_flag"]    = False
temp["ajax_path"]      = "-----------TBD----------"
temp['limit_low']      = 0
temp['limit_high']     = 20
temp['x_axis']         = "Time"
temp['y_axis']         = "mAmp"
temp["time_generation"]    = False
temp["average_generation"] = True

temp["label_array"]        =  ['Time',"mAmp"]

display_control.append(temp)
temp  = {}
temp["name"]              = "Time Series Current"
temp["flow_sensor_flag"]  = False
temp["time_step_flag"]    = True
temp["ajax_path"]      = "-----------TBD----------"
temp['limit_low']      = 0
temp['limit_high']     = 20
temp['x_axis']         = "Time"
temp['y_axis']         = "mAmp"

temp["time_generation"]    = True
temp["average_generation"] = False
temp["label_array"]        =  ['Time', 'Coil Current 1',"Coil Current 2","Coil Current 3","Coil Current 4","Coil Current 5"]

display_control.append(temp)

chart_list = []
for i in display_control:
   chart_list.append(i["name"])

 

@app.route('/detail_statistics_ajax/<int:chart_type>/<int:flow_sensor_id>/<int:schedule_id>/<int:step_id>/<int:time_id>',methods=["GET"])
@authDB.requires_auth
def detail_statistics_ajax(chart_type, flow_sensor_id,schedule_id,step_id,time_id):
   if chart_type == 0:
       schedule_name = statistics_module.schedule_data.keys()[schedule_id]
       sensor_name   = statistics_module.flow_rate_sensor_names[ flow_sensor_id ]
      
       return_value  = statistics_module.get_average_flow_data_queue( step_id, sensor_name, schedule_name )

   if chart_type == 1:
       schedule_name = statistics_module.schedule_data.keys()[schedule_id]
       sensor_name   = statistics_module.flow_rate_sensor_names[ flow_sensor_id ]
       return_value  = statistics_module.get_time_index_flow( time_id, step_id, sensor_name, schedule_name )
   if chart_type == 2:
       schedule_name = statistics_module.schedule_data.keys()[schedule_id]
       sensor_name   = statistics_module.flow_rate_sensor_names[ flow_sensor_id ]
       return_value  = statistics_module.get_total_flow_data( step_id, sensor_name, schedule_name )

   if chart_type == 3:
       schedule_name = statistics_module.schedule_data.keys()[schedule_id]
       return_value  = statistics_module.get_average_current_data_queue( step_id,  schedule_name )


   if chart_type == 4:
       schedule_name = statistics_module.schedule_data.keys()[schedule_id]
       return_value  = statistics_module.get_time_index_current( time_id, step_id,schedule_name )
   
   return_value = json.dumps(return_value)
   return return_value


@app.route('/detail_statistics/<int:chart_type>/<int:flow_sensor_id>/<int:schedule_id>/<int:step_id>/<int:time_id>',methods=["GET"])
@authDB.requires_auth
def detail_1(chart_type, flow_sensor_id,schedule_id,step_id,time_id):

       if chart_type < 0:
           chart_type = 0
       if chart_type > len(display_control)-1:
           chart_type = len(display_control)-1
          
       chart_data        = display_control[ chart_type ]
       schedule_list     = statistics_module.schedule_data.keys()
       
       if schedule_id > len(schedule_list)-1:
           schedule_id = len(schedule_list)-1
       
       logscale = False
       step_number       = statistics_module.schedule_data[ schedule_list[schedule_id] ]["step_number"]
       conversion_factor = statistics_module.conversion_rate[ flow_sensor_id ]
       if step_id > step_number-1:
          step_id = step_number-1
       if time_id > 50:
           time_id = 50
       flow_sensors      = statistics_module.flow_rate_sensor_names
       if chart_type == 0:
            legend_name = "Flow Meter: "+flow_sensors[flow_sensor_id]+"     <br>Schedule:  "+schedule_list[schedule_id]+" <br>Step Number:  "+ str(step_id+1)
       if chart_type == 1:
            legend_name = "Flow Meter: "+flow_sensors[flow_sensor_id]+"     <br>Schedule:  "+schedule_list[schedule_id]+" <br>Step Number:  "+ str(step_id+1) +" <br>Time Index:  "+ str(time_id+1)

       if chart_type == 2:
            legend_name = "Flow Meter: "+flow_sensors[flow_sensor_id]+"     <br>Schedule:  "+schedule_list[schedule_id]+" <br>Step Number:  "+ str(step_id+1)
            logscale = True

       if chart_type == 3:
            legend_name = "Coil Current:<br>Schedule:  "+schedule_list[schedule_id]+" <br>Step Number:  "+ str(step_id+1) 
            conversion_factor = 1.0

       if chart_type == 4:
            legend_name = "Coil Current:<br>Schedule:  "+schedule_list[schedule_id]+" <br>Step Number:  "+ str(step_id+1) +" <br>Time Index:  "+ str(time_id+1)
            conversion_factor = 1.0
       
    
       return render_template(  "detail_statistics",
                                logscale              = logscale,
                                legend_name           = legend_name,
                                conversion_factor     = conversion_factor,
                                chart_list            = chart_list,
                                chart_data            = chart_data,
                                chart_type            = chart_type,
                                flow_sensor_id        = flow_sensor_id,
                                schedule_id           = schedule_id,
                                step_id               = step_id,
                                time_id               = time_id,
                                header_name           = chart_data["name"],
                                schedule_list         = schedule_list,
                                flow_sensors          = flow_sensors,
                                step_number           = step_number ,
                                label_array           = chart_data["label_array"],
                                schedule_data         = json.dumps(statistics_module.schedule_data),
                                schedule_list_json    = json.dumps( schedule_list) )
                                

if __name__ == '__main__':
  print "startup_dict",startup_dict
  app.run(threaded=True , use_reloader=True, host='0.0.0.0',port=int(startup_dict["PORT"]) ,ssl_context=(startup_dict["crt_file"], startup_dict["key_file"]))
