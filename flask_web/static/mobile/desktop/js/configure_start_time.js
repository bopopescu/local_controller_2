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


  
     function  set_start_end_dow(schedule_name )
     {  
         var temp_start_times;
	 var temp_end_times;
	 var temp_dow;
         var temp_index;
	
         temp_start_times = schedules_start_times[ schedule_name ];
	 temp_end_times = schedules_end_times[ schedule_name ];
	 temp_dow = schedules_dow[schedule_name];
	 temp_index = temp_start_times[0]*4;
	 temp_index += temp_start_times[1]/15;
	 $("#starting_time")[0].selectedIndex = temp_index;
	 $("#starting_time").selectmenu();
	 $("#starting_time").selectmenu("refresh")

	 temp_index = temp_end_times[0]*4;
	 temp_index += temp_end_times[1]/15;
	 $("#ending_time")[0].selectedIndex = temp_index;
	 $("#ending_time").selectmenu()
	 $("#ending_time").selectmenu("refresh")

         $("#sunday").checkboxradio();
	 $("#monday").checkboxradio();
	 $("#tuesday").checkboxradio();
	 $("#wednesday").checkboxradio();
	 $("#thursday").checkboxradio();
	 $("#friday").checkboxradio();
	 $("#saturday").checkboxradio();
         if( temp_dow[0] != 0 ){ $("#sunday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#sunday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[1] != 0 ){ $("#monday").prop( "checked", true ).checkboxradio( "refresh" );; } else {$("#monday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[2] != 0 ){ $("#tuesday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#tuesday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[3] != 0 ){ $("#wednesday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#wednesday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[4] != 0 ){ $("#thursday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#thursday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[5] != 0 ){ $("#friday").prop( "checked", true ).checkboxradio( "refresh" );} else {$("#friday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[6] != 0 ){ $("#saturday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#saturday").prop( "checked",false  ).checkboxradio( "refresh" ); }
 
        
     }
     
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
          initalize_schedules( "#starttime_schedule")
	  set_schedules("#starttime_schedule",0)
	
	   
	
	  set_start_end_dow(schedules[0])

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
     
     $( "#starttime_schedule" ).bind( "change", function(event, ui) 
     {  
         var temp_start_times;
	 var temp_end_times;
	 var temp_dow;
         var temp_index;
	
         temp_start_times = schedules_start_times[ $("#starttime_schedule").val()];
	 temp_end_times = schedules_end_times[ $("#starttime_schedule").val()];
	 temp_dow = schedules_dow[ $("#starttime_schedule").val()];
	 temp_index = temp_start_times[0]*4;
	 temp_index += temp_start_times[1]/15;
	 $("#starting_time")[0].selectedIndex = temp_index;
	 $("#starting_time").selectmenu("refresh")
	 temp_index = temp_end_times[0]*4;
	 temp_index += temp_end_times[1]/15;
	 $("#ending_time")[0].selectedIndex = temp_index;
	 $("#ending_time").selectmenu("refresh")

        
         if( temp_dow[0] != 0 ){ $("#sunday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#sunday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[1] != 0 ){ $("#monday").prop( "checked", true ).checkboxradio( "refresh" );; } else {$("#monday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[2] != 0 ){ $("#tuesday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#tuesday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[3] != 0 ){ $("#wednesday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#wednesday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[4] != 0 ){ $("#thursday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#thursday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[5] != 0 ){ $("#friday").prop( "checked", true ).checkboxradio( "refresh" );} else {$("#friday").prop( "checked", false ).checkboxradio( "refresh" ); }
         if( temp_dow[6] != 0 ){ $("#saturday").prop( "checked", true ).checkboxradio( "refresh" ); } else {$("#saturday").prop( "checked",false  ).checkboxradio( "refresh" ); }
 
        
     });
     
    
    
    
     $("#change_start_time_button").click(function (e) 
     {
       var schedule_name;
       var start_time;
       var end_time;
       var dow;
       
       schedule_name = $("#starttime_schedule").val()
       start_time = $("#starting_time").val()
       end_time = $("#ending_time").val()
       dow = []
       if( $("#sunday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) }
       if( $("#monday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) }
       if( $("#tuesday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) }
       if( $("#wednesday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) }
       if( $("#thursday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) }
       if( $("#friday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) }
       if( $("#saturday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) }
       var json_object = {}
       json_object["schedule_name"] = schedule_name
       json_object["start_time"] = JSON.parse(start_time)
       json_object["end_time"] = JSON.parse(end_time)
       json_object["dow"] = dow
       var json_string = JSON.stringify(json_object);

       
       
       var result = confirm("Do you want to make change start time");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/start_time_update.html',
                    dataType: 'json',
                    async: false,
	            contentType: "application/json",
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		        schedule_request();
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/start_time_update.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if
       
     });// change start time    
       
 
     $("#back").button();
     schedule_request();
        
     
  } // end of function
)



