$(document).ready(

 
 
  function()
  {  var g,h,i
     var alarm_data;
     var  queue_interval_id;
     var  nintervalId;
     var data = [];
     var conversion_factor_index;
     var conversion_factor;
     var conversion_factor_array;


     var ajax_success = function(data)
     {
       var temp
       var temp_1
       var tempDate
      
       tempDate = new Date()
       
       $("#time_stamp").html("Current Date/Time:  "+tempDate.toLocaleDateString() + "   " + tempDate.toLocaleTimeString() )

       $("#controller_time_stamp").html("Controller Time Stamp: "+data.controller_time_stamp)
       $("#flow_rate").html("Current Flow Rate GPM:  "+data.flow_rate*conversion_factor);
       $("#op_mode").html("Operating Mode: "+data.op_mode)
       $("#schedule").html("Sprinkler Schedule: "+data.schedule)
       $("#step").html("Sprinkler Step:   "+data.step)
       $("#time").html("Time Of Step:  "+data.time_of_step)
       $("#duration").html("Current Duration: "+data.current_duration) 
       $("#rain_day").html("Rain Day: "+data.rain_day)
       $("#plc_current").html("PLC Current: "+data.pcl_current)
       $("#coil_current").html("Coil Current: "+data.coil_current)
       $("#eto_yesterday").html("ETO Yesterday: "+data.eto_yesterday)
       $("#eto_current").html("ETO Current: "+ data.eto_current)
       $("#master_valve").html("Master Valve: "+data.eto_master_valve )
       $("#eto_management").html("ETO Management: "+data.eto_managment_flag )
       

     }

     var ajax_request = function()
     {
       
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/redis_get_status.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: ajax_success,
                    error: function () 
		    {
		      
                       alert('/ajax/redis_get_status.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
     }
 
     
   
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
                    url: '/ajax/get_irrigation_queue.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: working_queue_success,
                    error: function () 
		    {
		      
                       alert('/ajax/get_irrigation_queue.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	    
     }

  
 
     function flow_sensor_success( data )
     {
          
          var i;

	 
	  conversion_factor_array = []
	 
          for( i= 0; i < data.length; i++ )
          {
	    

	    conversion_factor_array.push(data[i][1])
          }
         
          conversion_factor_index = 0;
	  conversion_factor = conversion_factor_array[ conversion_factor_index ];

           ajax_request();
       
     }
     
    var flow_sensor_request = function()
     {
      
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/get_flow_sensor_name.html',
                    dataType: 'json',
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
     
      
   $("#refresh").bind("click",function(event,ui)
   {
       flow_sensor_request()
       queueRequest()
   });

     $("#back").button();
     // get flow sensors
     flow_sensor_request();
    
     queueRequest();
   

  } )


