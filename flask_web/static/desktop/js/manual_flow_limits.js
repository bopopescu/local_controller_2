$(document).ready(
 function()
 {
     var nintervalId;
     var schedules_pins = {}
     var schedules = []
     var schedules_steps = {}
     var schedules_start_times = {}
     var schedules_end_times = {}
     var schedules_dow = {}
     var controller_pin_data = {}
     var composite_limit_values = {}
     var schedule_name;
     var conversion_factor_array;
     var conversion_factor_index;
     var conversion_factor;
     
  
     
     function generate_description( index , schedule_name)
    {
      var temp_string;
      var i;
     
      temp_string = "Schedule Step:   "+index+"       Controller:Valves  --->";
      index = index ;
      if( index >= schedules_pins[schedule_name].length){ temp_string = "undefined"; return temp_string; }

      temp_string = temp_string + schedules_pins[schedule_name][index];
      
      // padding string to 30 characters
      // this is bad hack needs to be replaced in future
      for(i = 0;i<100;i++)
      {
	if( temp_string.length > 60)
	{
	  break;
	  
	}
	else
	{
	  temp_string = temp_string+" ";
	}
      }
      return temp_string;
    }
       
  
 


           
  
  
	
	
 

    
   $("#db_schedule").bind("change",function(event,ui)
   {
       var temp_val;
       temp_val = $("#db_schedule").val();
       
       localStorage.setItem("db_schedule", temp_val);
      
       localStorage.setItem("db_step_number",schedules_pins[temp_val].length);
       get_limit_and_composite();
   });
  
   $("#db_flow_sensor").bind("change",function(event,ui)
   {
       var temp_val;
       
       temp_val = $("#db_flow_sensor").val();
       conversion_factor_index = $("#db_flow_sensor")[0].selectedIndex;
       conversion_factor = conversion_factor_array[ conversion_factor_index ];
       localStorage.setItem("db_conversion_factor",  conversion_factor )
       localStorage.setItem("db_flow_sensor",$("#db_flow_sensor").val() )
       get_limit_and_composite();
   });






/*
**
*                                   These functions fetch configurations data 
* 
* 
* 
**
*/


     function limit_and_composite( data )
     {
        var temp_index
      
      
        $("#listview").empty();
          for( i = 0; i < data.length; i++ )
          {
	    data[i].limit_std = parseInt( data[i].limit_std*conversion_factor*100)/100
	    data[i].limit_avg = parseInt( data[i].limit_avg*conversion_factor*100)/100
	    data[i].composite_avg = parseInt( data[i].composite_avg*conversion_factor*100)/100
	    data[i].composite_std = parseInt( data[i].composite_std*conversion_factor*100)/100
	    $("#listview").append('<li><h5>'+generate_description( i , schedule_name)+"<br>Flow Limits Avg: "+data[i].limit_avg+"  Std: "+data[i].limit_std+"<br>Last Value Avg: "+data[i].composite_avg+
	      "   Std: "+data[i].composite_std +"</h5>  </li>")
      
	  }
          $("#listview").listview("refresh"); 
    }

   
   function get_limit_and_composite() 
   {
       var json_string;
       var json_data = {}
 
       
       schedule_name = $("#db_schedule").val();
      
       flow_sensor = $("#db_flow_sensor").val();
       
       json_data = {}
       json_data.schedule = schedule_name;
       json_data.sensor = flow_sensor;
       json_data.step_number = schedules_pins[schedule_name].length
       json_string = JSON.stringify(json_data)
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/get_limit_and_composite.html',
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: limit_and_composite,
	     
                    error: function () 
		    {
                       alert('/ajax/get_limit_and_composite.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
     
	
     }  



     function flow_sensor_success( data )
     {
          var length;
          var i;
	  var flow_meter
	  
	  flow_meter = $("#db_flow_sensor");
          length = data.length;
          flow_meter.empty()
          ref_flow_meter = 1;
	  conversion_factor_array = []
	 
          for( i= 0; i < length; i++ )
          {
	    
            flow_meter.append('<option value='+data[i][0]+'>Select Flow Sensor ----------> '+data[i][0]+'</option>');
	    conversion_factor_array.push(data[i][1])
          }
         
          conversion_factor_index = 0;
	  conversion_factor = conversion_factor_array[ conversion_factor_index ];

	  localStorage.setItem("db_conversion_factor",  conversion_factor )
	  
          flow_meter.selectedIndex = 0;
	  flow_meter.selectmenu();
          flow_meter.selectmenu("refresh");
          get_limit_and_composite()
       
       
     }
     
    
    var flow_sensor_request = function()
     {
      
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/get_flow_sensor_name.html',
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: flow_sensor_success,
                    error: function () 
		    {
		      
                       alert('/ajax/get_flow_sensor_name.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
     }
      
    var ajax_schedule_success = function(data)
     {
         
          schedules = []
          schedules_step = {}
          schedules_start_times = {}
          schedules_end_times = {}
          schedules_dow = {}
          schedules_pins = {}
          for (var i = 0; i < data.length; i++) 
          {
	     
	     schedules.push(data[i].name)
	     schedules_step[data[i].name]            = data[i].steps
             schedules_start_times[data[i].name]     = data[i].start_time
             schedules_end_times[data[i].name]       = data[i].end_time   
             schedules_dow[data[i].name]             = data[i].dow
             schedules_pins[data[i].name]            = data[i].controller_pins     
          }
          

          $("#db_schedule").empty()
	 
         for( var i = 0; i < schedules.length; i++ )
	 {
	
          $("#db_schedule").append('<option value='+schedules[i]+'>Select Irrigation Schedule ------------> '+schedules[i]+'</option>');	
	
	 }
       
   	$("#db_schedule")[0].selectedIndex = 0;
	$("#db_schedule").selectmenu();
	$("#db_schedule").selectmenu("refresh");
        localStorage.setItem("db_flow_sensor",$("#db_flow_sensor").val() )
        localStorage.setItem("db_schedule",$("#db_schedule").val() )
	 localStorage.setItem("db_step_number",schedules_pins[$("#db_schedule").val()].length);
         $("#db_schedule_current").empty()
         for( var i = 0; i < schedules.length; i++ )
	 {
	
          $("#db_schedule_current").append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	 }
	 flow_sensor_request();  
       
 
     }
 
    
        
      schedule_request = function()
      {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/schedule_data.html',
                    dataType: 'json',
		    contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    success: ajax_schedule_success,
              
                    error: function () 
		    {
                       alert('/ajax/schedule_data.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
      }
     

     
  
   schedule_request();
   $("#back").button();

   

   
 
   
         
       
     
  } // end of function
)

