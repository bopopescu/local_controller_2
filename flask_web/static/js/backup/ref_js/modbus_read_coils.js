$(document).ready(
 function()
 {
     var result;
     var schedule_name;
     var flow_sensor;
     var composite_limit_values;
     var json_string;
     var conversion_factor;
     
     function display_results( data )
     {
         $("#result").html("Result--->  "+JSON.stringify(data)); 
     }

   
     $("#read_coil").bind("click",function(event,ui)
     {
       
         var json_object;
	
         json_object = {}
         json_object.controller  = $("#select_controller").val();
         json_object.coil        = $("#select_coil").val();
         json_string = JSON.stringify(json_object);
	
         result = confirm("Do you want to read modbus register");
	 
         if( result == true )
         { 

	   
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/read_modbus_coil.html',
	            contentType: "application/json",
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function (data) 
		    {
                     
		       display_results( data ); 
                    },
                    error: function () 
		    {
                       alert('/ajax/read_modbus_coil.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if     
   
  
       });


     
     
     

      
   function controller_pins_success( data )
   {
  
     controller_pin_data = data;
     $("#select_controller").empty()
     for( var i = 0; i < controller_pin_data.length; i++ )
     {
        $("#select_controller").append('<option value='+controller_pin_data[i].name+'>'+controller_pin_data[i].name+'</option>');	
     }
     $("#select_controller")[0].selectedIndex = 0;
     $("#select_controller").selectmenu();
     $("#select_controller").selectmenu("refresh");
     


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
       

    $("#select_coil").empty()
    for( var i = 1; i <= 200; i++ )
    {
          $("#select_coil").append('<option value='+i+'>'+i+'</option>');	
	
    }
     $("#select_coil")[0].selectedIndex = 0;
     $("#select_coil").selectmenu();
     $("#select_coil").selectmenu("refresh");

  
   load_controller_pins();
      
   
 });
