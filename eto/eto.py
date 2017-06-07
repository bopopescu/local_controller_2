import time
import string
import urllib2
import math
import redis
import json
import base64
import datetime
from fetch_cimis import *
from cimis_request import *



class ETO():
   def __init__(self,alt,access_codes):  #"alt is in feet"
       self.alt = alt*0.3048
       self.pressure = 101.3*(((293-.0065*alt)/293)**5.26)
       self.gamma = .000665*self.pressure
       self.reflect = .23
       self.access_codes = access_codes


 
   
   def calculate_eto( self, hourly_results):
         ETod = 0
         day_of_year = time.localtime().tm_yday
         dr = 1+.033*math.cos(2*3.14159/365*day_of_year)
         delta = .409*math.sin(2*3.14159/365*day_of_year-1.39) 
         lat  = 3.14159/180*33.2
         omega = math.acos( -math.tan(lat)*math.tan(delta))
         ra = 24*60/3.14159*.0820*dr*((omega*math.sin(delta)*math.sin(lat))+(math.cos(delta)*math.cos(lat)*math.sin(omega) ))
         rso = (.75+2e-5*self.alt)*ra

         for i in hourly_results:
             #ETo COMPUTATIONAL PROCEDURE 
             #The CIMIS Penman Equation was developed for use with hourly weather data. Required input data for the ETo computation include hourly means of air temperature (Ta; units of degrees C), vapor  
             #pressure deficit (VPD; units of kilopascals: kPa), wind speed (U2; units of m/s), and net radiation (Rn: units of mm/hr of equivalent evaporation). Hourly values of ETo (EToh) in mm/hr are   
             #computed using the following: 
             #EToh = W*Rn + (1-W)*VPD*FU2              (1) 
             #where W is a dimensionless partitioning factor, and FU2 is an empirical wind function (units: mm/hr/kPa). Daily values of ETo are computed by simply summing the twenty-four hourly EToh 
             #values computed from Eq. 1 for the period ending at midnight (end of AZMET day). Specific computational procedures used to obtain the required parameters for Eq. 1 are provided below. 
             #Net Radiation (Rn) 
             #CIMIS originally measured Rn using instruments known as net radiometers. CIMIS abandoned the use of net radiometers in the early 1990s for a variety of reasons. AZMET chose not use net  
             #radiometers and has computed hourly net radiation since network inception (1986) using a simple, clear sky estimation procedure that uses solar radiation (SR) expressed in units of MJ/m*m/hr 
             #and mean hourly vapor pressure (ea; units: kPa). The procedure is provided below: 
            P = self.pressure
            U2 = i["wind_speed"]
           
            tc = i["TC"]
            es = .6108*math.exp(17.27*tc/(tc+273.3))
            ea = es*i["Humidity"]/100.
            VPD  = es- ea
            
            #For Daytime Conditions (SR>=0.21 MJ/m*m/hr): 
            
            SR  = i["SolarRadiationWatts/m^2"] 
            if SR > 10:
                FU2 = 0.03 + 0.0576*U2
                
                         
            else:  #For Nighttime Conditions (SR<0.21 MJ/m*m/hr): 
                
                
                FU2 = 0.125 + 0.0439*U2
                             
            
            SR = .72*SR
            Rn = SR/(694.5*(1-0.000946*tc))
            S = es*(597.4-0.571*tc)/(0.1103*(tc+273.16)**2)
            G = 0.000646*P*(1+0.000949*tc)
            W = S/(S+G)
         
            
            RL = 4.903*(10 **-9)*(.34-.14*math.sqrt(ea))*((i["TC"]+273.3)**4)*277.8/24
            RL = RL/(694.5*(1-0.000946*tc))
            ETRL = -W*RL
            ETR  = W*Rn
            EHUM = (1-W)*VPD*FU2
           
            ETH  = ETRL+ETR+EHUM
            #print ETH/25.4,EHUM,ETR,ETRL
            ETod = ETod+ETH
            
         return ETod/25.4


   def integrate_eto_data(self ):
       rain = {}
       eto = {}
       print "made it here1"
       
       try:
           messo_eto            = Messo_ETO(self.access_codes)
           messo_results        = messo_eto.get_daily_data(time = time.time())
          
           eto["messo"]         = self.calculate_eto( messo_results)

       except:
          print "exception messo eto"
          #raise
       print "made it here2"
       try:
          messo_precp                      =  Messo_Precp(self.access_codes)
          rain["messo"]                    = messo_precp.get_daily_data(time = time.time())
       except:
           print "exception messo rain"

       print "made it here3"
       
       try:
           cimis_eto         = CIMIS_ETO( self.access_codes )
           cimis_results     = cimis_eto.get_eto(time = time.time()-24*3600)
           
           #eto["cimis"]      = cimis_results["eto"]
           #rain["cimis"]     = cimis_results["rain"]
       except:
          print "exception cimis"

       print "made it here 4"
       try:
          spatial                = CIMIS_SPATIAL(self.access_codes) 
          eto["cimis_spatial"]   = spatial.get_eto( time = time.time()-24*3600  ) 
       except:
           print "exception spatial"

       try:
          eto_values = eto.values()
          print "eto_values",eto_values
          eto_avg = ( reduce(lambda x, y: x+y, eto_values ))/len(eto_values)
          print "eto_avg",eto_avg
       except:
          eto_avg = 0
       try:
          rain_values = rain.values()
          rain_avg = ( reduce(lambda x, y: x+y, rain_values ))/len(rain_values)
          print "rain_avg",rain_avg
       except:
          rain_avg = 0

       return { "eto":eto_avg,"rain":rain_avg }, json.dumps(eto),json.dumps(rain)
        

if __name__ == "__main__":
   redis        = redis.StrictRedis( host = 'localhost', port=6379, db = 0 )
   data         = redis.hget("FILES:SYS","eto_api_setup.json")
   json_data    = base64.b64decode(data)
   #print "json_data",json_data
   access_data  = json.loads(json_data )
   print access_data
   eto = ETO(2400,access_data)
   print eto.integrate_eto_data()
  


#        imap_username = 'lacima.ranch@gmail.com'
#        imap_password = 'Gr1234gfd'
##
        #try:
           #eto_data = calculate_site_eto( sites, alt, time.time() -24*3600 )
           #print("made it here ",eto_data)
           #redis.set("YESTERDAY_ETO", eto_data["net_et"] )
           #redis.set("YESTERDAY_WIND_GUST",eto_data["wind_gust"])
           #redis.set("YESTERDAY_WIND_GUST_TIME_STAMP",eto_data["wind_gust_time_stamp"])
           #redis.set("YESTERDAY_ETO_DATA",eto_data)
        #except:
        
           #eto_data                            = {}
           #eto_data["net_et"]                  = 0
           #eto_data["wind_gust"]               = 0
           #eto_data["wind_gust_time_stamp"]   = 0
           #redis.set("YESTERDAY_ETO", eto_data["net_et"] )
           #redis.set("YESTERDAY_WIND_GUST",eto_data["wind_gust"])
           #redis.set("YESTERDAY_WIND_GUST_TIME_STAMP",eto_data["wind_gust_time_stamp"])
           #redis.set("YESTERDAY_ETO_DATA",eto_data)
        #print("eto_data"),eto_data
#        try:
#          cimis_data = process_cimis_data( imap_username, imap_password )
#        except:
#          cimis_data = [0,.5] # force eto_base data to be value
        #cimis_data.append( eto_data["net_et"] )
#        cimis_data.append(.25) 
#        print("cimis_data",cimis_data)
       
#        if cimis_data[0] > cimis_data[1] :  # doing a quick median filter
#           temp = cimis_data[0]
#           cimis_data[0] = cimis_data[1]
#           cimis_data[1] = temp
#        if cimis_data[1] > cimis_data[2] :
#           temp = cimis_data[1]
#           cimis_data[1] = cimis_data[2]
#           cimis_data[2] = temp
#        if cimis_data[0] > cimis_data[1] :
#           temp = cimis_data[0]
#           cimis_data[0] = cimis_data[1]
#           cimis_data[1] = temp
#        if cimis_data[1] > cimis_data[2] :
#           temp = cimis_data[1]
#          cimis_data[1] = cimis_data[2]
#           cimis_data[2] = temp
#        print("cimis_data",cimis_data)
#        print("official cimis data is ",cimis_data[1])
#        try:
#           redis.set("YESTERDAY_ETO", cimis_data[1] )
           #redis.set("YESTERDAY_WIND_GUST",eto_data["wind_gust"])
           #redis.set("YESTERDAY_WIND_GUST_TIME_STAMP",eto_data["wind_gust_time_stamp"])
#        except:
#           os.system("reboot ")
#        return cimis_data[1]

