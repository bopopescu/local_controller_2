$(document).ready(
 function()
 {
 function schedule_setup()
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
          

  
	
	
         $("#manual_schedule").empty()
         for( var i = 0; i < schedules.length; i++ )
	 {
	
          $("#manual_schedule").append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	 }
       
   	$("#manual_schedule")[0].selectedIndex = 0;
	$("#manual_schedule").selectmenu();
	$("#manual_schedule").selectmenu("refresh");
        set_step( 0 );
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
	    
	  case  0:  // Offline
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
	    
	    break;
	    
	  case 1:  // Queue Schedule
	      $("#schedule_div").show()
              $("#manual_div").hide()
              $("#run_div").hide()

	    break;
	    
	  case 2: // Queue Mode Schedule Step
	      $("#schedule_div").show()
              $("#manual_div").show()
              $("#run_div").hide()

	    break;

	  case 3: // Queue Mode Schedule Step Time
	      $("#schedule_div").show()
              $("#manual_div").show()
              $("#run_div").show()

	    break;
	    
	    

	  case 4:  // Clean Filter
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
	    break;

          case 5:  // open Master Valve
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
	    break;

          case 6: // Close Master Valve
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
	    break;

          case 7: // Restart Program
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
	    break;

          case 8: // Reset Program
	      $("#schedule_div").hide()
              $("#manual_div").hide()
              $("#run_div").hide()
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
       
       
       mode            = $("#op_mode").val()
       schedule_name   =  $("#manual_schedule").val()
       step            = $("#manual_step").val() 
       run_time        = $("#run_time").val()
       
     
       
       var json_object = {}
       json_object["mode"] = mode;
       json_object["schedule_name"] = schedule_name;
       json_object["step"] = step;
       json_object["run_time"] = run_time;
       var json_string = JSON.stringify(json_object);
     
       
       
       var result = confirm("Do you want to make mode change");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/mode_change.html',
                    dataType: 'json',
	            contentType: "application/json",
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

   
   
   

   $("#back").button();
  
   schedule_request();
   mode_request();
   
   
         
       
     
  } // end of function
  
  $("#refresh_a").bind("click",function(event,ui)
  {
     //  schedule_setup();
     // controller_pin_control();
     // rain_day_functions();
     // eto_functions();
     // load_irrigation_queue_data();
     // load_eto_data();
      system_state_init();
   });

  schedule_setup();
  controller_pin_control();
  rain_day_functions();
  eto_functions();
  load_irrigation_queue_data();
  load_eto_data();
 
  system_state_init();
 }
)

