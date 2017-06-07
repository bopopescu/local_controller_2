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
     
     function clean_filter_request()
     {
       var result = confirm("Do you want clean filter");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/clean_filter_request.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: null,
                    success: function () 
		    {
                       alert("Changes Made");
		      
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/clean_filter_request.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if
     } 
     
     
     
     var mode_request_success = function(data)
     {
         
	$("#op_mode")[0].selectedIndex = data.mode;
	$("#op_mode").selectmenu();
	$("#op_mode").selectmenu("refresh");
	$("#manual_schedule")[0].selectedIndex = data.schedule;
	$("#manual_schedule").selectmenu("refresh");
	$("#manual_schedule").selectmenu("refresh");
	$("#manual_step")[0].selectedIndex = data.step;
        $("#manual_step").selectmenu();
	$("#manual_step").selectmenu("refresh");
	$("#run_time")[0].selectedIndex = data.run_time
        $("#run_time").selectmenu();
	$("#run_time").selectmenu("refresh");
     }
     
     
     
     
     
     
      mode_request = function()
      {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/mode_request.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: mode_request_success,
              
                    error: function () 
		    {
                       alert( '/ajax/mode_request.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
      }     
      
    function generate_description( index , schedule_name)
    {
      var temp_string;
     
      temp_string = "step "+index+" controller/pins  --->";
      index = index -1;
      if( index >= schedules_pins[schedule_name].length){ temp_string = "undefined"; return temp_string; }
      for( i = 0; i < schedules_pins[schedule_name][index].length;i++)
      {
	temp_string = temp_string + "   "+ schedules_pins[schedule_name][index][i];
 	
      }
      return temp_string;
    }
    
     function set_step(index)
     {
        var schedule_name;
	var temp_string;
	
	schedule_name = schedules[index];
        $("#manual_step").empty()
        for( var i = 1; i <= schedules_step[schedule_name].length; i++ )
	{
	  temp_string = generate_description( i , schedule_name)
          $("#manual_step").append('<option value='+i+'>'+temp_string+'</option>');	
	
	}

        $("#manual_step")[0].selectedIndex = 0;
	$("#manual_step").selectmenu();
	$("#manual_step").selectmenu("refresh");
 
       
       
       
     }
 
    var ajax_rain_schedule_flags_success = function(data)
    {
      var rain_flag;
      var schedule_correction;
      
      rain_flag = data.rain_flag;
      schedule_correction = data.schedule_correction;
      $("#rain_flag")[0].selectedIndex = rain_flag;
      $("#rain_flag").selectmenu();
      $("#rain_flag").selectmenu("refresh");      
      $("#time_correction")[0].selectedIndex = parseInt(schedule_correction*100) -1;
      $("#time_correction").selectmenu();
      $("#time_correction").selectmenu("refresh");
	
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
        localStorage.setItem("db_flow_sensor",$("#db_flow_sensor").val() )
        localStorage.setItem("db_schedule",$("#db_schedule").val() )
	
         $("#db_schedule_current").empty()
         for( var i = 0; i < schedules.length; i++ )
	 {
	
          $("#db_schedule_current").append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	 }
       
   	$("#db_schedule_current")[0].selectedIndex = 0;
	$("#db_schedule_current").selectmenu();
	$("#db_schedule_current").selectmenu("refresh");
        localStorage.setItem("db_schedule_current",$("#db_schedule_current").val() )
	
	
	
	
         $("#manual_schedule").empty()
         for( var i = 0; i < schedules.length; i++ )
	 {
	
          $("#manual_schedule").append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	 }
       
   	$("#manual_schedule")[0].selectedIndex = 0;
	$("#manual_schedule").selectmenu();
	$("#manual_schedule").selectmenu("refresh");
        set_step( 0 );
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/rain_schedule_flags.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: ajax_rain_schedule_flags_success,
              
                    error: function () 
		    {
                       alert('/ajax/rain_schedule_flags.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });       
 
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
     
            
     $("#schedule_div").hide()
     $("#manual_div").hide()
     $("#run_div").hide()
	

     $("#run_time").empty()
      for( var i = 1; i <= 60; i++ )
      {
          $("#run_time").append('<option value='+i+'>'+i+'  minutes </option>');	
	
      }

      $("#run_time")[0].selectedIndex = 9;
      $("#run_time").selectmenu();
      $("#run_time").selectmenu("refresh")
   
     $( "#op_mode" ).bind( "change", function(event, ui) 
     {  
        var temp_index
        
	temp_index = $("#op_mode")[0].selectedIndex;
	
	switch( temp_index)
	{
	  case 0:  // Auto Mode
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
	    break;
	    
	  case 1:  // Offline
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
	    
	    break;
	    
	  case 2:  // Queue Schedule
	      $("#schedule_div").show()
              $("#manual_div").hide()
              $("#run_div").hide()

	    break;
	    
	  case 3: // Queue Mode Schedule Step
	      $("#schedule_div").show()
              $("#manual_div").show()
              $("#run_div").hide()

	    break;

	  case 4: // Queue Mode Schedule Step Time
	      $("#schedule_div").show()
              $("#manual_div").show()
              $("#run_div").show()

	    break;
	    
	    
	  case 5:  // Manual Mode Schedule
	      $("#schedule_div").show()
              $("#manual_div").hide()
              $("#run_div").hide()

	    break;
	    
	  case 6: // Manual Mode Schedule Step
	      $("#schedule_div").show()
              $("#manual_div").show()
              $("#run_div").hide()

	    break;
	    
	  case 7: // Manual Mode Schedule Step 
	      $("#schedule_div").show()
              $("#manual_div").show()
              $("#run_div").show()

	    break;
	    

	}
     });
   

      $( "#manual_schedule" ).bind( "change", function(event, ui) 
     {  
    
         set_step($("#manual_schedule")[0].selectedIndex )
     });
 
 

     $( "#change_mode" ).bind( "click", function(event, ui) 
     {
       var mode;
       var schedule_name;
       var step;
       var run_time;
       
       
       mode           = $("#op_mode").val()
       schedule_name =  $("#manual_schedule").val()
       step           = $("#manual_step").val() 
       run_time      = $("#run_time").val()
       
       alert("mode is "+mode)
      
       var json_object = {}
       json_object["mode"] = mode;
       json_object["schedule_name"] = schedule_name;
       json_object["step"] = step;
       json_object["run_time"] = run_time;
       var json_string = JSON.stringify(json_object);

       
       
       var result = confirm("-----Do you want to make mode change ----------------");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/mode_change.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		      
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/mode_change.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if
       
     });// change start time
     // attach event to change_mode
     $("#time_correction").empty()
      for( var i = 1; i <=200; i++ )
      {
          $("#time_correction").append('<option value='+i/100.+'>'+i+'  percent </option>');	
	
      }

      $("#time_correction")[0].selectedIndex = 99;
      $("#time_correction").selectmenu();
      $("#time_correction").selectmenu("refresh")         
 
     $( "#reset_factor" ).bind( "click", function(event, ui) 
     {
       var result = confirm("Do you want to make reset rain flag and time correction factor?");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/reset_factor.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: "[]",
                    success: function () 
		    {
                       alert("Changes Made");
		       
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/reset_factor.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if    
	
     });

     $( "#change_rain_flag" ).bind( "click", function(event, ui) 
     {
       
       var json_data = {}
       
       json_data["rain_flag"]= $("#rain_flag").val();
       var json_string = JSON.stringify(json_data);

       var result = confirm("Do you want to make reset rain flag and time correction factor?");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/change_rain_flag.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/change_rain_flag.html'+"  Server Error Change not made");
		      
		       
                    }
              })
       }// if    
	
     } );
     
     $( "#change_factor" ).bind( "click", function(event, ui) 
     {
       
       var json_data = {}
       
       json_data["time_correction"]= $("#time_correction").val();
       var json_string = JSON.stringify(json_data);

       var result = confirm("Do you want to make reset rain flag and time correction factor?");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/change_sprinkler_schedule.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/change_sprinkler_schedule.html'+"  Server Error Change not made");
		     
		       
                    }
              })
       }// if    
	
     } );   
     
     
   $("#clear_redis").bind("click",function(event, ui) 
   {
       
       var json_data = {}
       
       var result = confirm("Do you want to clear memory db?");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/clear_redis.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: {},
                    success: function () 
		    {
                       alert("Changes Made");
		       
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/clear_redis.html'+"  Server Error Change not made");
		   
		       
                    }
              })
       }// if    
	
     } );   

      $( "#trim_db" ).bind( "click", function(event, ui) 
     {
       
       
       var json_data = {}
       
       json_data["days_to_trim"]= $("#days_to_trim").val();
       var json_string = JSON.stringify(json_data);

       var result = confirm("Do you want to trim db back to "+$("#days_to_trim").val()+" days");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/trim_db.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/trim_db'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if    
	
     } ); 
      




   
   function update_flow_data(data)
   {
     var temp;
     var i;
     temp =""
     $("#db_header").html("Composite Flow Data Values");

     
     for( i = 0; i<data.length; i++)
     {
       
       temp = temp +  generate_description( data[i].step , schedule_name)+ "\t\t average: "+Math.round(data[i].avg) + "\t\t std:  \t"+ Math.round(data[i].std)+"\n";
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
       temp = temp  +  generate_description( data[i].step , schedule_name)+ "\t\t average: "+Math.round(data[i].avg) + "\t\t std:  \t"+ Math.round(data[i].std)+"\n";
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
       temp = temp +  generate_description( data[i].step , schedule_name)+ "\t\t average: "+Math.round(data[i].avg) + "\t\t std:  \t"+ Math.round(data[i].std)+"\n";
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
  
    $("#controller_run_time").empty()
    for( var i = 1; i <= 60; i++ )
    {
          $("#controller_run_time").append('<option value='+i+'>'+i+'  minutes </option>');	
	
    }

  
   $("#controller_pin_turn_off").bind("click",function(event,ui)
   {
       
  
      
       var result = confirm("Do you want to make mode change");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/controller_pin_turn_off.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: "[]",
                    success: function () 
		    {
                       alert("Changes Made");
		      
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/controller_pin_turn_off.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }
     
       
   });// change start time     
   
   $("#controller_select").bind("click",function(event,ui)
   {
        var index;
	
	index = $("#controller_select")[0].selectedIndex;
        populate_pins( index );
   });
   
   
   $("#controller_pin_turn_on").bind("click",function(event,ui)
   {
       
  
       var controller;
       var pin;
       var run_time;
       
       
    
       controller    =  $("#controller_select").val()
       pin           =  $("#select_pin").val() 
       run_time      =  $("#controller_run_time").val()
       
     
      
       var json_object = {}
     
       json_object["controller"] = controller;
       json_object["pin"] = pin;
       json_object["run_time"] = run_time;
       var json_string = JSON.stringify(json_object);

       
       
       var result = confirm("Do you want to make mode change");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/controller_pin_turn_on.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		      
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/controller_pin_turn_on.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }
     
       
   });// change start time 
     
   function populate_pins( index )
   {
     var pins;
     
     pins = controller_pin_data[index].pins;
     $("#select_pin").empty()
     for( var i = 1; i <= pins.length; i++ )
     {
          $("#select_pin").append('<option value='+i+'>pin: '+i+' cable bundle: '+pins[i-1].cable_bundle+' wire color: '+pins[i-1].wire_color+ '</option>');	
	
     }
     $("#select_pin")[0].selectedIndex = 0;
     $("#select_pin").selectmenu();
     $("#select_pin").selectmenu("refresh");
   }
   
   
   function controller_pins_success( data )
   {
  
     controller_pin_data = data;
     $("#controller_select").empty()
     for( var i = 0; i < controller_pin_data.length; i++ )
     {
        $("#controller_select").append('<option value='+controller_pin_data[i].name+'>'+controller_pin_data[i].name+'</option>');	
     }
     $("#controller_select")[0].selectedIndex = 0;
     $("#controller_select").selectmenu();
     $("#controller_select").selectmenu("refresh");
     
     populate_pins( 0)

   }
   
   
   
   load_controller_pins = function()
   {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/load_controller_pins.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: controller_pins_success,
              
                    error: function () 
		    {
                       alert('/ajax/load_controller_pins.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
   }
    
    
   $("#db_schedule").bind("change",function(event,ui)
   {
       var temp_val;
       temp_val = $("#db_schedule").val();
     
       localStorage.setItem("db_schedule", temp_val);
       
   });
  
   $("#db_flow_sensor").bind("change",function(event,ui)
   {
       var temp_val;
       temp_val = $("#db_flow_sensor").val();
       
       localStorage.setItem("db_flow_sensor", temp_val);
      
   });
 
   $("#db_schedule_current").bind("change",function(event,ui)
   {
       var temp_val;

       temp_val = $("#db_schedule_current").val();
       
       localStorage.setItem("db_schedule_current", temp_val);
      
   });
   
   
   
   // fix me
  $("#view_current_data").bind("change",function(event,ui)
   {
       var json_string;
       var json_data = {}
   
       alert("view current data");
       return;
       
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
 
  
///// fix me
  $("#view_current_limits").bind("change",function(event,ui)
  {
       var json_string;
       var json_data = {}
 
       alert("view current limits");
       return;
       
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
  // -------------Fix me
  $("#view_current_variances").bind("change",function(event,ui)
   {
       var json_string;
       var json_data = {}
 
       alert("view current variances");
       return;
       
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
   
   
  
   schedule_request();
   mode_request();
   load_controller_pins()
   
         
       
     
  } // end of function
)

