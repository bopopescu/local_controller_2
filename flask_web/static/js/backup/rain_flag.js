
function rain_day_functions()
{
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
                    contentType: "application/json",
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
     
 
	
 
     
    var rain_flag_success = function(data)
    {
      var rain_flag;
    
      rain_flag = data.rain_flag;
    
      $("#rain_flag")[0].selectedIndex = rain_flag;
      $("#rain_flag").selectmenu();
      $("#rain_flag").selectmenu("refresh");  
           
    }

    function get_rain_data()
    {
      
    $.ajax(
         {
                    type: "GET",
                    url: '/ajax/rain_flag.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: rain_flag_success,
              
                    error: function () 
		    {
                       alert('/ajax/rain_flag.html' +"   "+"access unsuccessfull");
		       
		       
                    }
       }); 
 
    }
    get_rain_data();

}
