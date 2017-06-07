
 function eto_functions()
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
	            contentType: "application/json",
                    success: function () 
		    {
                       alert("Changes Made");
		       
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/change_eto_flag.html'+"Server error");
		      
		       
                    }
              })
       }// if    
	
     } );
     
 
      

	
 
     
    var ajax_eto_flag_success = function(data)
    {
    
      var eto_flag;

      
      
      eto_flag = data.eto_flag;
      $("#eto_flag")[0].selectedIndex = eto_flag;
      $("#eto_flag").selectmenu();
      $("#eto_flag").selectmenu("refresh");      

       
    }
    
    function get_rain_eto_data()
    {
      
    $.ajax(
         {
                    type: "GET",
                    url: '/ajax/eto_flag.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: ajax_eto_flag_success,
              
                    error: function () 
		    {
                       alert('/ajax/eto_flag.html' +"   "+"access unsuccessfull");
		       
		       
                    }
       }); 
 
    }
    
    get_rain_eto_data();
   


 

       
     
  } // end of function


