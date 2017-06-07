#import urllib
import urllib2
import json
import datetime
import time

ONE_DAY = 24*3600


class CIMIS_ETO():
  #fetch from cimis site
  def __init__( self, access_data, app_key = "e1d03467-5c0d-4a9b-978d-7da2c32d95de", cimis_url="http://et.water.ca.gov/api/data" ):
     
     self.cimis_data = access_data["cimis_eto"]
     self.app_key = "appKey="+self.cimis_data["api-key"]
     self.cimis_url = self.cimis_data["url"]
     self.station   = self.cimis_data["station"]

  def get_eto( self,  time=time.time()-1*ONE_DAY  ): # time is in seconds for desired day
     date =  datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d')
     url = self.cimis_url+"?"+self.app_key+"&targets="+str(self.station)+"&startDate="+date+"&endDate="+date
     print "url",url
     req = urllib2.Request(url)
     response = urllib2.urlopen(req)
     temp = response.read()
     data = json.loads(temp)
     #print "data",data
     return {"eto":float(data["Data"]["Providers"][0]["Records"][0]['DayAsceEto']["Value"]), "rain":float(data["Data"]["Providers"][0]["Records"][0]['DayPrecip']["Value"])}

#http://et.water.ca.gov/api/data?appKey=e1d03467-5c0d-4a9b-978d-7da2c32d95de&targets=lat=33.578156,lng=-117.299459&startDate=2015-07-07&endDate=2015-07-07&dataItems=day-asce-eto&unitOfMeasure=E

class CIMIS_SPATIAL():
  #fetch from cimis site
  def __init__( self,access_data, app_key = "e1d03467-5c0d-4a9b-978d-7da2c32d95de", cimis_url="http://et.water.ca.gov/api/data" ):
     self.cimis_data = access_data["cimis_spatial"]
     self.app_key = "appKey="+self.cimis_data["api-key"]
     self.cimis_url = self.cimis_data["url"]
     self.latitude   = self.cimis_data["latitude"]
     self.longitude  = self.cimis_data["longitude"]

  def get_eto( self, time=time.time()-1*ONE_DAY  ): # time is in seconds for desired day

     date =  datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d')
     lat_long = "lat="+str(self.latitude)+",lng="+str(self.longitude)      
     url = self.cimis_url+"?"+self.app_key+"&targets="+lat_long+"&startDate="+date+"&endDate="+date
     print "url",url
     req = urllib2.Request(url)
     

     response = urllib2.urlopen(req)
     
     temp = response.read()
     #print temp
     data = json.loads(temp)
     return float(data["Data"]["Providers"][0]["Records"][0]['DayAsceEto']["Value"])


class Messo_ETO():
   def __init__( self,access_data, app_key="8b165ee73a734f379a8c91460afc98a1" , meso_url = "http://api.mesowest.net/v2/stations/timeseries?" ):
       self.messo_data = access_data["messo_eto"] 
       self.app_key             =   self.messo_data["api-key"]
       self.url                 =   self.messo_data["url"]
       self.station             =   self.messo_data["station"]
       self.token               =   "&token="+self.app_key

   def get_daily_data( self, time = time.time()  ):
     date_1 =  datetime.datetime.fromtimestamp(time-1*ONE_DAY).strftime('%Y%m%d')
     date_2 =  datetime.datetime.fromtimestamp(time-0*ONE_DAY).strftime('%Y%m%d')
     start_time = "&start="+date_1+"0800"
     end_time   = "&end="+date_2+"0900"

     
     url =   self.url+ "stid="+self.station+self.token+start_time+end_time+"&vars=relative_humidity,air_temp,solar_radiation,peak_wind_speed,wind_speed&obtimezone=local"
    
     print "url",url
     req = urllib2.Request(url) 
     print "req",req
     response = urllib2.urlopen(req)
     temp = response.read()
     data = json.loads(temp)
     #print "data",data
     station = data["STATION"]
     #print data.keys()
     #print data["UNITS"]
     station = station[0]
     station_data = station["OBSERVATIONS"]
    
     keys = station_data.keys()
     #print "keys",keys
     return_value = []
 
     
     #print "len",len(station_data["wind_speed_set_1"])
     for i in range(0,24):
       temp                              = {}
       temp["wind_speed"]                = station_data["wind_speed_set_1"][i]
       temp["peak_wind_speed"]           = station_data["peak_wind_speed_set_1"][i]
       temp["Humidity"]                  = station_data["relative_humidity_set_1"][i]
       temp["SolarRadiationWatts/m^2"]   = station_data["solar_radiation_set_1"][i]
       temp["TC"]                        = station_data["air_temp_set_1"][i]
       return_value.append(temp)
     return return_value


class Messo_Precp():
   def __init__( self, access_data,app_key="8b165ee73a734f379a8c91460afc98a1" , meso_url = "http://api.mesowest.net/v2/stations/precip?" ):
       self.messo_data          = access_data["messo_precp"] 
       self.app_key             =   self.messo_data["api-key"]
       self.url                 =   self.messo_data["url"]
       self.station             =   self.messo_data["station"]
       self.token               =   "&token="+self.app_key


   def get_daily_data( self,  time = time.time()):
     date_1 =  datetime.datetime.fromtimestamp(time-1*ONE_DAY).strftime('%Y%m%d')
     date_2 =  datetime.datetime.fromtimestamp(time-0*ONE_DAY).strftime('%Y%m%d')
     start_time = "&start="+date_1+"0800"
     end_time   = "&end="+date_2+"0900"

     
     url =   self.url+"stid="+self.station+self.token+start_time+end_time+"&obtimezone=local"
    
     
     req = urllib2.Request(url) 
     response = urllib2.urlopen(req)
     temp = response.read()
     data = json.loads(temp)
     station = data["STATION"]
     station = station[0]
     station_data = station["OBSERVATIONS"]
    
     
     rain = float(station_data["total_precip_value_1"])/25.4
     return rain
     
     #print "len",len(station_data["wind_speed_set_1"])
     for i in range(0,24):
       temp                              = {}
       temp["wind_speed"]                = station_data["wind_speed_set_1"][i]
       temp["peak_wind_speed"]           = station_data["peak_wind_speed_set_1"][i]
       temp["Humidity"]                  = station_data["relative_humidity_set_1"][i]
       temp["SolarRadiationWatts/m^2"]   = station_data["solar_radiation_set_1"][i]
       temp["TC"]                        = station_data["air_temp_set_1"][i]
       return_value.append(temp)
     return return_value
     

#http://et.water.ca.gov/api/data?appKey=e1d03467-5c0d-4a9b-978d-7da2c32d95de&targets=lat=33.578156,lng=-117.299459&startDate=2015-07-07&endDate=2015-07-07&dataItems=day-asce-eto&unitOfMeasure=E


if __name__ == "__main__":
#  x = Web_ETO( "e1d03467-5c0d-4a9b-978d-7da2c32d95de" )
#  x.get_eto(time.time()-24*3600,62)
#   x = Messo_ETO()
#   print x.get_daily_data( )
    x = CIMIS_SPATIAL() 
    print x.get_eto( 33.578156,-117.299459  ) 
 
"""
http://api.mesowest.net/v2/stations/timeseries?stid=SRUC1&token=1234567890&start=201506170000&end=201506180000&vars=relative_humidity,air_temp,solar_radiation,peak_wind_speed,wind_speed&obtimezone=local 
"""
#url = "http://et.water.ca.gov/api/data?appKey=e1d03467-5c0d-4a9b-978d-7da2c32d95de&targets=62&startDate=2014-10-26&endDate=2014-10-26"
#headers = { 'User-Agent' : user_agent }

#data = urllib.urlencode(values)
#req = urllib2.Request(url, data, headers)
#req = urllib2.Request(url)
#response = urllib2.urlopen(req)
#temp = response.read()
#data = json.loads(temp)
#print float(data["Data"]["Providers"][0]["Records"][0]['DayAsceEto']["Value"])


