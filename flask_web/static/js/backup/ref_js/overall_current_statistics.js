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
          
          $("#db_schedule_current").empty()
          for( var i = 0; i < schedules.length; i++ )
	  {
	
            $("#db_schedule_current").append('<option value='+schedules[i]+'>'+schedules[i]+'</option>');	
	
	  }
       
   	  $("#db_schedule_current")[0].selectedIndex = 0;
	  $("#db_schedule_current").selectmenu();
	  $("#db_schedule_current").selectmenu("refresh");
 
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
     
            

 
   $("#db_schedule_current").bind("change",function(event,ui)
   {
       var temp_val;
       
       temp_val = $("#db_schedule_current").val();
       
       localStorage.setItem("db_schedule_current", temp_val);
      
   });
   
   function update_current_data(data)
   {
     var temp;
     var i;
     
     
     temp =""
     $("#db_current_header").html("Composite Current Values");
    
    
     for( i = 0; i<data.length; i++)
     {
       
       temp = temp + generate_description( data[i].step , schedule_name)+ "\t\t average: "+data[i].avg+"\n"; //+ "\t\t std:  \t"+ data[i].std+"\n";
     }
     
     $("#display_current_area").val(temp).trigger('autosize.resize');
 
   }  
   

  $("#view_current_data").bind("click",function(event,ui)
   {
       var json_string;
       var json_data = {}

        
       schedule_name = $("#db_schedule_current").val();
 
  
       json_data = {}
       json_data.schedule = schedule_name;
  
       
       json_string = JSON.stringify(json_data)
 
       result = true
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/current/get/composite.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_current_data, 
		    
                    error: function () 
		    {
                       alert('/ajax/current/get/composite.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
       }// if    
	
     } );  
 
  function update_current_limit_data( data )
  {
     var temp;
     var i;
     
     
     temp =""
     $("#db_current_header").html("Current Limit Values");
    
    
     for( i = 0; i<data.length; i++)
     {
       
       temp = temp + generate_description( data[i].step , schedule_name)+ "\t\t average: "+data[i].avg+"\n"; //+ "\t\t std:  \t"+ data[i].std+"\n";
     }
     
     $("#display_current_area").val(temp).trigger('autosize.resize');
  }

  $("#view_current_limits").bind("click",function(event,ui)
  {
       var json_string;
       var json_data = {}

       
       schedule_name = $("#db_schedule_current").val();
      
       json_data = {}
       json_data.schedule = schedule_name;
       json_string = JSON.stringify(json_data)
       result = true
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/current/get/limits.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_current_limit_data,
	     
                    error: function () 
		    {
                       alert('/ajax/current/get/limits.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
       }// if    
	
     } );
  
  
  function update_variance_data( data )
  {
     var temp;
     var i;
     
     
     temp =""
     $("#db_current_header").html("Current Variance Values");
    
    
     for( i = 0; i<data.length; i++)
     {
       
       temp = temp + generate_description( data[i].step , schedule_name)+ "\t\t average: "+data[i].avg+"\n"; //+ "\t\t std:  \t"+ data[i].std+"\n";
     }
     
     $("#display_current_area").val(temp).trigger('autosize.resize');
  }
  
  $("#view_current_variances").bind("click",function(event,ui)
   {
       var json_string;
       var json_data = {}

       
       schedule_name = $("#db_schedule_current").val();

       json_data = {}
       json_data.schedule = schedule_name;

       json_string = JSON.stringify(json_data)
       result = true
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/current/get/variance.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_variance_data,
	     
                    error: function () 
		    {
                       alert( '/ajax/current/get/variance.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
       }// if    
	
     } );        
   
   
  
   schedule_request();
  
         
       
     
  } // end of function
)

