$(document).ready(
 function()
 {
 
     $( "#change_eto_flag" ).bind( "click", function(event, ui) 
     {
       
       var json_data = {}
       
       json_data["eto_flag"]= $("#eto_flag").val();
       var json_string = JSON.stringify(json_data);

       var result = confirm("Do you want to make reset eto management flag ?");
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/change_eto_flag.html',
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
                       alert('/ajax/change_eto_flag.html'+"  Server Error");
		      
		       
                    }
              })
       }// if    
	
     } );
     
 
      
 
 




     $( "#change_rain_flag" ).bind( "click", function(event, ui) 
     {
       
       var json_data = {}
       
       json_data["rain_flag"]= $("#rain_flag").val();
       var json_string = JSON.stringify(json_data);

       var result = confirm("Do you want to make reset rain flag ?");
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
     
 
	
 
     
    var ajax_rain_schedule_flags_success = function(data)
    {
      var rain_flag;
      var eto_flag;
      
      rain_flag = data.rain_flag;
      eto_flag = data.eto_flag;
      $("#rain_flag")[0].selectedIndex = rain_flag;
      $("#rain_flag").selectmenu();
      $("#rain_flag").selectmenu("refresh");  
      $("#eto_flag")[0].selectedIndex = eto_flag;
      $("#eto_flag").selectmenu();
      $("#eto_flag").selectmenu("refresh");      

       
    }
    function get_rain_eto_data()
    {
      
    $.ajax(
         {
                    type: "GET",
                    url: '/ajax/rain_eto_flags.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: ajax_rain_schedule_flags_success,
              
                    error: function () 
		    {
                       alert('/ajax/rain_eto_flags.html' +"   "+"access unsuccessfull");
		       
		       
                    }
       }); 
 
    }
    
    get_rain_eto_data();
   


 

       
     
  } // end of function
)

