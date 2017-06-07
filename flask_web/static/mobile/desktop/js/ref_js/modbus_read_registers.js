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

   
     $("#read_register").bind("click",function(event,ui)
     {
       
         var json_object;
	
         json_object = {}
         json_object.controller = $("#select_controller").val();
         json_object.register   = $("#select_register").val();
         // construct json object
         json_string = JSON.stringify(json_object);
	
         result = confirm("Do you want to read modbus register");
	 
         if( result == true )
         { 
	   $("#result").html("Awaiting Results");
	   
	   // making update
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/read_modbus_register.html',
	            contentType: "application/json",
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function ( data ) 
		    {
                      
		       display_results( data ); 
                    },
                    error: function () 
		    {
                       alert('/ajax/read_modbus_register.html'+"  Server Error Change not made");
		       
		       
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

         data = {}
	 data.register    = $("#select_register")[0].selectedIndex;
	 data.controller  = $("#select_controller")[0].selectedIndex;

         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/load_controller_pins.html',
                    dataType: 'json',
                    async: false,
		    data: json_string,
                    //json object to sent to the authentication url
                    success: controller_pins_success,
              
                    error: function () 
		    {
                       alert('/ajax/load_controller_pins.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
   }
       

    $("#select_register").empty()
    for( var i = 1; i <= 200; i++ )
    {
          $("#select_register").append('<option value='+i+'>'+i+'</option>');	
	
    }
     $("#select_register")[0].selectedIndex = 0;
     $("#select_register").selectmenu();
     $("#select_register").selectmenu("refresh");

  
   load_controller_pins();
      
   
 });
