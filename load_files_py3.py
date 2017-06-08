
#
# File: load_files.py
# load sys files and application files
# The data is stored in the following
#    System Files are stored in the following in json format
#    	As a dictionary with the key of FILES:SYS
#    	The key of the dictionary are the file names
#    APP Files are stored in the following in json format
#    	As a dictionary with the key of
#    	The key of the dictionary are the file names

#  import redis
#  make redis dictionary "SYS:FILES"
# store json_object to redis data "global_sensors"
import os
from os import listdir
from os.path import isfile, join
import redis
import json
import farm_template_py3
import base64


graph_management = farm_template_py3.Graph_Management(
    "PI_1", "main_remote", "LaCima_DataStore")
data_store_nodes = graph_management.find_data_stores()
# find ip and port for redis data store
data_server_ip = data_store_nodes[0]["ip"]
data_server_port = data_store_nodes[0]["port"]
print(data_server_ip,data_server_port)

redis_handle = redis.StrictRedis(data_server_ip, data_server_port, db=0)
app_files = "/home/pi/new_python/app_data_files/"
sys_files = "/home/pi/new_python/system_data_files/"


app_list = redis_handle.hkeys("APP_FILES")
sys_list = redis_handle.hkeys("SYS_FILES")


class APP_FILES():
    def __init__(self, redis_handle):
        self.path = app_files
        self.key = "FILES:APP"
        self.redis_handle = redis_handle

    def file_directory(self):
        return self.redis_handle.hkeys(self.key)

    def delete_file(self, name):
        self.redis_handle.hdel(self.key, name)

    def save_file(self, name, data):
        f = open(self.path + name, 'w')
        json_data = json.dumps(data)
        f.write(json_data)
        compact_data = base64.b64encode(json_data)
        self.redis_handle.hset(self.key, name, compact_data)

    def load_file(self, name):
        compact_data = self.redis_handle.hget(self.key, name)
        json_data = base64.b64decode(compact_data)
        data = json.loads(json_data)
        return data

    def delete_file(self, name):
        os.remove(self.path + name)


class SYS_FILES():
    def __init__(self, redis_handle):

        self.path = sys_files
        self.key = "FILES:SYS"
        self.redis_handle = redis_handle

    def file_directory(self):
        return self.redis_handle.hkeys(self.key)

    def delete_file(self, name):
        self.redis_handle.hdel(self.key, name)

    def save_file(self, name, data):
        f = open(self.path + name, 'w')
        json_data = json.dumps(data)
        f.write(json_data)
        compact_data = base64.b4encode(json_data)
        self.redis_handle.hset(self.key, name, compact_data)

    def load_file(self, name):
        compact_data = self.redis_handle.hget(self.key, name)
        data = json.loads(base64.b64decode(compact_data))
        return data

    def delete_file(self, name):
        os.remove(self.path + name)


if __name__ == "__main__":
    # delete APP FILES DATA
    print("made it here")
    if len(app_list) > 0:
        redis_handle.hdel("FILES:APP", app_list)

    # delete SYS FILES DATA
    if len(sys_list) > 0:
        redis_handle.hdel("FILES:SYS", sys_list)

    files = [f for f in listdir(app_files)]
    # load app files
    for i in files:

        fileName, fileExtension = os.path.splitext(i)

        if fileExtension == ".json":
            print("i",i)
            f = open(app_files + i, 'r')
            data = f.read()
            print(type(data))
            redis_handle.hset("FILES:APP", i, data)
            print("data",data)

    # load sys files

    files = [f for f in listdir(sys_files)]
    for i in files:
        print("i", i)
        fileName, fileExtension = os.path.splitext(i)
        if fileExtension == ".json":
            f = open(sys_files + i, 'r')
            data = f.read()
            redis_handle.hset("FILES:SYS", i, data)
            print("data", data)

    ####
    # INSURING THAT ETO_MANAGEMENT FLAG IS DEFINED
    ####
    temp = redis_handle.get("ETO_MANAGE_FLAG")
    if temp is None:
        # not defined
        redis_handle.set("ETO_MANAGE_FLAG", 1)

    temp = redis_handle.hget("CONTROL_VARIABLES", "ETO_MANAGE_FLAG")
    if temp is None:
        # not defined
        redis_handle.hset("CONTROL_VARIABLES", "ETO_MANAGE_FLAG", 1)

    ####
    # Construct ETO Data QUEUES
    ####

    file_data = redis_handle.hget("FILES:APP", "eto_site_setup.json").decode("utf-8") 

    eto_site_data = json.loads(file_data) 

    redis_handle.delete("ETO_RESOURCE_A")
    for j in eto_site_data:
        redis_handle.hset("ETO_RESOURCE_A",
                          j["controller"] + "|" + str(j["pin"]), 0)

    keys = redis_handle.hkeys("ETO_RESOURCE")
    print("keys", keys)
    for i in keys:
        print("i", i)
        value = redis_handle.hget("ETO_RESOURCE", i)
        if redis_handle.hexists("ETO_RESOURCE_A", i):
            redis_handle.hset("ETO_RESOURCE_A", i, value)
    redis_handle.delete("ETO_RESOURCE")
    redis_handle.rename("ETO_RESOURCE_A", "ETO_RESOURCE")

    if redis_handle.hget(
        "CONTROL_VARIABLES",
            "ETO_RESOURCE_UPDATED") != "TRUE":
        redis_handle.hset("CONTROL_VARIABLES", "ETO_RESOURCE_UPDATED", "FALSE")
    #
    # delete process keys
    #
    keys = redis_handle.hkeys("WD_DIRECTORY")
    for i in keys:
        print("i", i)
        redis_handle.hdel("WD_DIRECTORY", i)

    redis_handle.hset(
        "SYS_DICT",
        "CONTROL_VARIABLES",
        "system control and status variables")
    redis_handle.hset(
        "SYS_DICT",
        "FILES:APP",
        "dictionary of application files")
    redis_handle.hset("SYS_DICT", "FILES:SYS", "dictionary of system files")
    redis_handle.hset("SYS_DICT", "ETO_RESOURCE", "dictionary of eto resource")
    redis_handle.hset(
        "SYS_DICT",
        "SCHEDULE_COMPLETED",
        "markers to prevent multiple keying of sprinklers")
    redis_handle.hset(
        "SYS_DICT",
        "OHM_MESS",
        "ohm measurement for active measurements")
    redis_handle.hset(
        "QUEUES_DICT",
        "QUEUES:SPRINKLER:PAST_ACTIONS",
        "QUEUE OF RECENT IRRIGATION EVENTS AND THEIR STATUS")
    redis_handle.hset(
        "QUEUES_DICT",
        "QUEUES:CLOUD_ALARM_QUEUE",
        "QUEUE OF EVENTS AND ACTIONS TO THE CLOUD")
    redis_handle.hset(
        "QUEUES_DICT",
        "QUEUES:SPRINKLER:FLOW:<schedule_name>",
        "QUEUE OF PAST FLOW DATA")
    redis_handle.hset(
        "QUEUES_DICT",
        "QUEUES:SPRINKLER:CURRENT:<schedule_name>",
        "QUEUE OF PAST CURRENT DATA")
    redis_handle.hset(
        "QUEUES_DICT",
        "QUEUES:SYSTEM:PAST_ACTIONS",
        "QUEUE OF RECENT SYSTEM EVENTS AND THEIR STATUS")
