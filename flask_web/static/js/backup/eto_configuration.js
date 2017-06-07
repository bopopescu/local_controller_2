$(document).ready(
 function()
 {

    var holding_data;

    $( "#change_eto_setting" ).click( function(event, ui) 
    {   var i
        var jason_string;
	
        i = $("#select_index")[0].selectedIndex
       
	holding_data[i].recharge_eto = parseFloat( $("#select_eto_capacity")[0].selectedIndex)/100.
	holding_data[i].recharge_rate = parseFloat( $("#select_eto_recharge")[0].selectedIndex)/100.
        holding_data[i].seepage_rate = parseFloat( $("#select_drainage_rate")[0].selectedIndex)/100.
        var json_string = JSON.stringify( holding_data );
        $.ajax
        ({
                    type: "POST",
                    url: '/ajax/save_eto_configuration_data.html',
                    dataType: 'json',
                    async: false,
	            contentType: "application/json",
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		      
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/save_eto_configuration_data.html'+"  Server Error Change not made");
		       
		       
                    }
              })     

    });
    

    
    $( "#select_index" ).click(  function(event, ui) 
    {   var i
        
        i = $("#select_index")[0].selectedIndex
       
	$("#select_eto_capacity")[0].selectedIndex = (holding_data[i].recharge_eto*100)
	$("#select_eto_recharge")[0].selectedIndex = (holding_data[i].recharge_rate*100)
	$("#select_drainage_rate")[0].selectedIndex = (holding_data[i].seepage_rate*100)
        $("#select_eto_capacity").selectmenu()
        $("#select_eto_capacity").selectmenu("refresh")
        $("#select_eto_recharge").selectmenu()
        $("#select_eto_recharge").selectmenu("refresh")
        $("#select_drainage_rate").selectmenu()
        $("#select_drainage_rate").selectmenu("refresh")

        
     });   
 
     /*
      * data is an array of  {"controller":"satellite_1", "pin": 9,  "recharge_eto": 0.216, "recharge_rate":0.25   },
     */
     var ajax_schedule_success = function(data)
     {
          holding_data = data
       
          $("#select_index").empty()
          for( var i = 0; i < data.length; i++ )
	  {
             $("#select_index").append('<option value='+i+'> Controller:'+data[i].controller+' Valve:'+data[i].pin+'</option>');	
	  }
          $("#select_eto_recharge").empty()
          for( var i = 0; i <= 100; i++ )
	  {
             $("#select_eto_recharge").append('<option value='+i+'> ETO Recharge Rate GPH: '+parseFloat(i)/100+ ' </option>');	
	  }

          $("#select_eto_capacity").empty()
          for( var i = 0; i <= 100; i++ )
	  {
             $("#select_eto_capacity").append('<option value='+i+'> ETO Soil Capacity inch : '+parseFloat(i)/100+ ' </option>');	
	  }

	 $("#select_drainage_rate").empty()
          for( var i = 0; i <= 100; i++ )
	  {
             $("#select_drainage_rate").append('<option value='+i+'> ETO Drainage inch/day: '+parseFloat(i)/100+ ' </option>');	
	  }

	  $("#select_index")[0].selectedIndex = 0;
	  $("#select_index").selectmenu();
	  $("#select_index").selectmenu("refresh");
	  $("#controller_label").html("Controller: "+data[0].controller );
	  $("#pin_label").html("Pin: "+data[0].pin );
	  $("#select_eto_capacity")[0].selectedIndex = (data[0].recharge_eto*100)
	  $("#select_eto_recharge")[0].selectedIndex = (data[0].recharge_rate*100)
	  $("#select_drainage_rate")[0].selectedIndex = (data[0].seepage_rate*100)
	 
          $("#select_eto_capacity").selectmenu()
          $("#select_eto_capacity").selectmenu("refresh")
          $("#select_eto_recharge").selectmenu()
          $("#select_eto_recharge").selectmenu("refresh")
	  $("#select_drainage_rate").selectmenu()
          $("#select_drainage_rate").selectmenu("refresh")


     }
     

        
      schedule_request = function()
      {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/get_eto_configuration.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: ajax_schedule_success,
              
                    error: function () 
		    {
                       alert('/ajax/get_eto_configuration.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
      }
     

     

    
 
     
      

   
      $("#back").button();
      schedule_request();

 
     
  } // end of function
)



