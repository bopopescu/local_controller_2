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
     var alarm_data_setup = {}
     var alarm_meta_data = {}
     var alert_index = 0;
     var ref_schedule = null;
     var ref_step = null;


 
	 
          
       

   
   
     
 
 
     
     function initalize_schedules( schedule_id )
     {
       $(schedule_id).empty()
       for( var i = 0; i < schedules.length; i++ )
	{
	
          $(schedule_id).append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	}
	set_schedules( schedule_id, 0 )

     }
     
     function set_schedules( schedule_id, index )
     {
       
   	$(schedule_id)[0].selectedIndex = index;
	$(schedule_id).selectmenu();
	$(schedule_id).selectmenu("refresh");
        
     }
    
    
 
    function generate_description( index , schedule_name)
    {
      var temp_string;
      var temp_index
      temp_index = index + 1;
      temp_string = "step "+temp_index+" controller/pins  --->";
    
      for( i = 0; i < schedules_pins[schedule_name][index].length;i++)
      {
	temp_string = temp_string + "   "+ schedules_pins[schedule_name][index][i];
 	
      }
      return temp_string;
    }
    
     function set_step( index, schedule_name )
     {
       var temp
       var temp_string

       $("#run_time").empty()
       $("#run_time").append('<option value='+0+'>'+0+'</option>');
       for( var i = 5; i <= 400; i++ )
	{
	  
	 
	  
          $("#run_time").append('<option value='+i+'>'+i+'</option>');	
	
	}
      
       $("#runtime_step").empty()
       for( var i = 0; i < schedules_step[schedule_name].length; i++ )
	{
	  temp = i + 1
	  temp_string = generate_description( i , schedule_name)
	 
          $("#runtime_step").append('<option value='+i+'>'+temp_string+'</option>');	
	
	}
        
       $("#runtime_step")[0].selectedIndex = index;
       if( schedules_step[schedule_name][index] == 0)
       {
	 $("#run_time")[0].selectedIndex = 0;
       }
       else
       {
	 $("#run_time")[0].selectedIndex = schedules_step[schedule_name][index] -4;
       }
       
       

       $("#runtime_step").selectmenu()
       $("#runtime_step").selectmenu("refresh")
       $("#run_time").selectmenu()
       $("#run_time").selectmenu("refresh")
      
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
          initalize_schedules( "#runtime_schedule")
	  set_schedules("#runtime_schedule",0)
	
	  if( ref_schedule != null )
	  {
	    
	    $("#runtime_schedule")[0].selectedIndex = ref_schedule;
            $("#runtime_schedule").selectmenu("refresh");
	    temp_index = $("#runtime_schedule")[0].selectedIndex;
     	    temp_name =  schedules[temp_index];
	    if( ref_step != null )
	    {
	      
              set_step( ref_step,temp_name);
	    }
	    else
	    {
	      set_step( 0, temp_name);
	    }
	  }
	  else
	  {
	       
	      temp_name =  schedules[0];
              set_step( 0, temp_name);
	  }

	  $("#runtime_step").selectmenu("refresh") 
	  $("#run_time").selectmenu("refresh")

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
		       schedule_request();
		       
                    }
         });
      }
     

     
    $( "#runtime_schedule" ).bind( "change", function(event, ui) 
    {  
        var temp_name;
	var temp_index;
	temp_index
	
	temp_index = $("#runtime_schedule")[0].selectedIndex;
	temp_name =  schedules[temp_index];
        set_step( 0,temp_name)
	$("#runtime_step").selectmenu("refresh") 
	$("#run_time").selectmenu("refresh")
        
     });   
 
    $( "#runtime_step" ).bind( "change", function(event, ui) 
    {  
        var temp_name;
	var temp_index;
	temp_index
	
	temp_name  = schedules[ $("#runtime_schedule")[0].selectedIndex ];
	temp_index = $("#runtime_step")[0].selectedIndex;
        if( schedules_step[temp_name][temp_index] == 0)
        {
	 $("#run_time")[0].selectedIndex = 0;
        }
        else
        {
	 $("#run_time")[0].selectedIndex = schedules_step[temp_name][temp_index] -4;
        }
       
      
	$("#run_time").selectmenu("refresh")
        
     }); 
    
 
     
     $("#change_run_time").click(function (e) 
     {
       var schedule_name;
       var schedule_step;
       var runtime_step;
       
      
       schedule_name     = $("#runtime_schedule").val()
       schedule_step     = $("#runtime_step").val()
       runtime_step      = $("#run_time").val()
       ref_schedule      = $("#runtime_schedule")[0].selectedIndex;
       ref_step          = $("#runtime_step")[0].selectedIndex;
      
       var json_object = {}
       json_object["schedule_name"] = schedule_name
       json_object["schedule_step"] = schedule_step;
       json_object["runtime_step"] = runtime_step
       
       var json_string = JSON.stringify(json_object);
   
       
       
       var result = confirm("Do you want to make change run time");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/run_time_update.html',
                    dataType: 'json',
	             contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       schedule_request();
		       
                    },
                   error: function () 
		    {
                       alert('/ajax/run_time_update.html  '+"Server Error Change not made");
		       schedule_request();
		       
                    }

              });
        }
        
 
  
   }); // end of change run time click
   

   
   $("#back").button();
   schedule_request();
       
     
  } // end of function
)



