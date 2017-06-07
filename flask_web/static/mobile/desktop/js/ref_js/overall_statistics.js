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
     
      temp_string = "step "+index+" controller/pins  --->";
      index = index -1;
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
	
          $("#db_schedule").append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	 }
       
   	$("#db_schedule")[0].selectedIndex = 0;
	$("#db_schedule").selectmenu();
	$("#db_schedule").selectmenu("refresh");
        localStorage.setItem("db_schedule_current",$("#db_schedule")[0].selectedIndex )
	localStorage.setItem("db_step",0 )
 
	
         $("#db_schedule_current").empty()
         for( var i = 0; i < schedules.length; i++ )
	 {
	
          $("#db_schedule_current").append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	 }
       
 
     }
 
    
        
      schedule_request = function()
      {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/schedule_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: ajax_schedule_success,
              
                    error: function () 
		    {
                       alert('/ajax/schedule_data.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
      }
     
            

 


   
   function update_flow_data(data)
   {
     var temp;
     var i;
     temp =""
     $("#db_header").html("Composite Flow Data Values");

     
     for( i = 0; i<data.length; i++)
     {
       
       
       temp = temp +  generate_description( data[i].step , schedule_name)+ "--->average gpm: "+Math.round(data[i].avg*conversion_factor*100)/100 + "  std gpm: "+ Math.round(data[i].std*conversion_factor*100)/100+"\n";
     }
     $("#display_area").val(temp).trigger('autosize.resize');
 
   }
      
   $("#view_data").bind("click",function(event, ui) 
   {
       var json_string;
       var json_data = {}
   
  
       
       schedule_name = $("#db_schedule").val();
       flow_sensor = $("#db_flow_sensor").val()

       json_data = {}
       json_data.schedule = schedule_name;
       json_data.sensor = flow_sensor;
       
       json_string = JSON.stringify(json_data)
 //      var result = confirm("Do you want to view data for schedule "+schedule_name+"  ?");
       result = true
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/view_composite_flow_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_flow_data, 
		    
                    error: function () 
		    {
                       alert('/ajax/view_composite_flow_data'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
       }// if    
	
     } );  
 
   
   
   function update_limit_data(data)
   {
     var temp;
     var i;
     temp =""
     $("#db_header").html("Limit Values");

     
     for( i = 0; i<data.length; i++)
     {
        temp = temp +  generate_description( data[i].step , schedule_name)+ "--->average gpm: "+Math.round(data[i].avg*conversion_factor*100)/100 + "  std gpm: "+ Math.round(data[i].std*conversion_factor*100)/100+"\n";
     }
     $("#display_area").val(temp).trigger('autosize.resize');
 
   } 
   
  $("#view_limits").bind("click",function(event, ui) 
   {
       var json_string;
       var json_data = {}
 
     
       
       schedule_name = $("#db_schedule").val();
       flow_sensor = $("#db_flow_sensor").val();
       json_data = {}
       json_data.schedule = schedule_name;
       json_data.sensor = flow_sensor;
       json_string = JSON.stringify(json_data)
       result = true
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/view_flow_limits.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_limit_data,
	     
                    error: function () 
		    {
                       alert('/ajax/view_flow_limits.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
       }// if    
	
     } );
  
  
  function update_variance_data(data)
   {
     var temp;
     var i;
     temp =""
     $("#db_header").html("Variance Data");
     temp = "Time of Variance Measurement\n"
     temp = temp + "Year "+data[0].year+" Month "+data[0].month+" Day "+data[0].day+" Hour "+data[0].hour+" Minute "+data[0].minute+" \n"
     for( i = 0; i<data.length; i++)
     {
        temp = temp +  generate_description( data[i].step , schedule_name)+ "--->average gpm: "+Math.round(data[i].avg*conversion_factor*100)/100 + "  std gpm: "+ Math.round(data[i].std*conversion_factor*100)/100+"\n";
     }
     $("#display_area").val(temp).trigger('autosize.resize');
 
   } 
   
  $("#view_variances").bind("click",function(event, ui) 
   {
       var json_string;
       var json_data = {}
 
       
       schedule_name = $("#db_schedule").val();
       flow_sensor = $("#db_flow_sensor").val();
       
       json_data = {}
       json_data.schedule = schedule_name;
       json_data.sensor = flow_sensor;
       json_string = JSON.stringify(json_data)
       result = true
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/view_flow_variance_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_variance_data,
	     
                    error: function () 
		    {
                       alert( '/ajax/view_flow_variance_data.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
       }// if    
	
     } );              
  
  
  
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
	    
            flow_meter.append('<option value='+data[i][0]+'>'+data[i][0]+'</option>');
	    conversion_factor_array.push(data[i][1])
          }
         
          conversion_factor_index = 0;
	  conversion_factor = conversion_factor_array[ conversion_factor_index ];
	  
          flow_meter.selectedIndex = 0;
	  flow_meter.selectmenu();
          flow_meter.selectmenu("refresh");
      
       
       
     }
     
     $("#db_flow_sensor" ).bind( "change", function(event, ui)
     {

       ref_flow_meter = $("#db_flow_sensor")[0].selectedIndex +1;
       conversion_factor_index = $("#db_flow_sensor")[0].selectedIndex;
       
       conversion_factor = conversion_factor_array[ conversion_factor_index ];
       
       
     });
     
    var flow_sensor_request = function()
     {
      
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/flow_sensor/get/flow_sensor_name.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: flow_sensor_success,
                    error: function () 
		    {
		      
                       alert('/ajax/flow_sensor/get/flow_sensor_name.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
     }
     flow_sensor_request();
      
   

    
     
   
   
  
   schedule_request();
   

   
         
       
     
  } // end of function
)

