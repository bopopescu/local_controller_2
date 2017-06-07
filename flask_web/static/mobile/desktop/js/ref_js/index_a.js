


$(document).ready(

 
 
  function()
  {  var g,h,i
     var alarm_data;
     var  queue_interval_id;
     var  nintervalId;
     var data = [];




     var ajax_success = function(data)
     {
       var temp
       var temp_1
       var tempDate
      
       tempDate = new Date()
       
       $("#time_stamp").html("Current Date/Time:  "+tempDate.toLocaleDateString() + "   " + tempDate.toLocaleTimeString() )

       $("#controller_time_stamp").html("Controller Time Stamp: "+data.controller_time_stamp)
       $("#index_flow_rate").html("Current Flow Rate:  "+data.flow_rate)
       $("#index_op_mode").html("Operating Mode: "+data.op_mode)
       $("#index_sprinkler_schedule").html("Sprinkler Schedule: "+data.schedule)
       $("#index_sprinkler_step").html("Sprinkler Step:   "+data.step)
       $("#index_time_of_step").html("Time Of Step:  "+data.time_of_step)
       $("#index_current_duration").html("Current Duration: "+data.current_duration) 
       $("#index_rain_day").html("Rain Day: "+data.rain_day)
       $("#index_derating_factor").html("Derating Factor: "+data.derating_factor)
       $("#plc_current").html("PLC Current: "+data.pcl_current)
       $("#coil_current").html("Coil Current: "+data.coil_current)
       $("#eto_yesterday").html("ETO Yesterday_a: "+data.eto_yesterday)
       $("#eto_current").html("ETO Current_a: "+data.eto_current )
 

       nintervalId =window.setInterval(ajax_request, 30000 );  // important only enable on a success full transfer

     }

     var ajax_request = function()
     {
       window.clearInterval(nintervalId);
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/home.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: ajax_success,
                    error: function () 
		    {
		      
                       alert('/ajax/home.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
     }
 
     nintervalId =window.setInterval(ajax_request, 300 );
   
     function working_queue_success(data)
     {
       var dataArray;
       var element;
       var data_elements;
       var i;
       var j;
       var temp;
       var ii;
       
       
   
       dataArray = []
       for( i = 0; i < data.length; i++ )
       {
	
	 temp = data[i]; 
	 
	 data_element = [];
	 element = [];
	 for( j =0; j < temp.value.length; j++)
	 {
	   data_element.push( temp.value[j])
	 }  
	
	 element.push(data_element, temp.name);
	 dataArray.push(element)
       }
       
       $("#div_h").empty()
       
       if( dataArray.length == 0 )
       {
	  $("#queue_div").empty() 
	  $("#queue_div").html("<h3> No elements in the Work Queue <h3>");
       
       }
       else
       {
          $('#div_h').jqBarGraph({ data: dataArray,
                        height: 500,

		        colors: ['#000000','#437346'] 
          });
       }
       queue_interval_id =window.setInterval(queueRequest, 30000 );
     }
     
     function queueRequest()
     {
       window.clearInterval(queue_interval_id);
        $.ajax
            ({
                    type: "GET",
                    url: '/ajax/working_queue.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: working_queue_success,
                    error: function () 
		    {
		      
                       alert('/ajax/working_queue.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	    
     }

     queue_interval_id =window.setInterval(queueRequest, 30000 );
     function alarm_data_list( data, mask )
    {
        var temp_index
        alarm_data = data
        $("#alarm_display").empty();
      
      
        var html = "";
        
	  html += '<div data-role="controlgroup">';

          for( i = 0; i < data.length; i++ )
          {
            temp_index = i +1;    
	    html +=   '<label for=id'+i+'  >Alarm Name--> '+data[i][0]+' Value--> '+data[i][1]+' Time--> '+data[i][2] +"</label>"
	    html +=   '<input type=checkbox   id=id'+i+' />';
             
           }
 
      html += "</div>";
      $("#alarm_display").empty()
      $("#alarm_display").append (html)
      for( i = 0; i < data.length; i++ )
      {
        $("#id"+i).checkboxradio();
        $("#id"+i).checkboxradio("refresh");	 
      }
          
               
       
  }
     
     function getAlarmData()
     {
       
        $.ajax
            ({
                    type: "GET",
                    url: '/ajax/get_alarm_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: alarm_data_list,
                    error: function () 
		    {
		      
                       alert('/ajax/get_alarm_data.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	    
     }
     
     $("#delete_alarms").bind("click",function(event,ui)
     {
       
         var mask;
	 var update_flag;
	 var status;
	 var json_object;
	 var json_string;
	 
         status = [];
	 update_flag = 0;
         for( i=0;i<alarm_data.length;i++)
	 {
	   
	   if( $("#id"+i).is(":checked") == true )
	   {
             
	     status.push(alarm_data[i][0])
	     update_flag = 1;
	   }
	   else
	   {
	     status.push(null);
	   }
	 }
         if( update_flag == 0 ){ alert("no changes selected"); return; }   
      
         json_string = JSON.stringify(status);
	
         result = confirm("Do you want to delete selected alarm limits");
	 
         if( result == true )
         { 
	  
	   
	   // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/delete_alarm_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       getAlarmData();
                    },
                    error: function () 
		    {
                       alert('/ajax/delete_alarm_data.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if     
   
  
});
        
  
      
     
     $("#AlarmPag").on('pageint',function () {
          
           ajax_request();
     });
     
     $("#StatusPage").on('pageint',  function () {
           alert("made it here")
           ajax_request();
	    queueRequest();
     });
    

     function get_flow_sensor_success()
     {
       alert("now construct the flow sensors");
     }
      
     function get_flow_sensors()
     {
     
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/get_flow_sensors.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: get_flow_sensor_success,
                    error: function () 
		    {
		      
                       alert('/ajax/get_flow_sensors.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
     }
     
     // get flow sensors
     ajax_request();
     queueRequest();
     getAlarmData();
  

  } )

/*
       $("#flow_meter").empty()
       for( var i = 0; i < data.flow_meter_description.length; i++ )
       {
          $("flow_meter").append('<option value=i>'+data.flow_meter_description+'</option>');	
	
	}
	set_schedules( schedule_id, 0 )

       #flow_meter
*/
