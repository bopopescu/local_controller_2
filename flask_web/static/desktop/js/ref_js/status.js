$(document).ready(
 function()
 {

	 
 
       

       
     var alert_fetch_success = function(data)
     {
          
        var temp;
	temp = []
	

	temp.push("Start of Alarm Data \n")
        for( i = 0; i<data.length; i++)
        {
	
         temp.push( JSON.stringify(data[i]) +"\n"); 
        }
        temp.push("End of Alarm Data \n");
        $("#alarm_display").val( temp.join("") ).trigger('autosize.resize');  

      


     }
 
    
        
      alert_fetch = function(data)
      {
	 var json_string;
	 json_string = JSON.stringify(data);
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/alert_fetch.html',
                    dataType: 'json',
                    async: false,
		    data: json_string,
                    //json object to sent to the authentication url
                    success: alert_fetch_success,
              
                    error: function () 
		    {
                       alert('/ajax/alert_fetch.html' +"   "+"Server Error Change not made");
		    
		       
                    }
         });

    }
     $("#get_alarm_history").click( function(e)
       {
	 var data;
	 data = {}
	 data.days = $("#alarm_history_day").val()
	 alert_fetch(data);
	 
       });


     var event_fetch_success = function(data)
     {
        var temp;
	temp = []
	

	temp.push("Start of Event Data\n")
        for( i = 0; i<data.length; i++)
        {
	
         temp.push( JSON.stringify(data[i]) +"\n"); 
        }
        temp.push("End of Event Data");
        $("#event_display").val( temp.join("") ).trigger('autosize.resize');  

     }
 
    
        
      event_fetch = function(data)
      {
	 var json_string;
	 json_string = JSON.stringify(data);
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/event_fetch.html',
                    dataType: 'json',
                    async: false,
		    data: json_string,
                    //json object to sent to the authentication url
                    success: event_fetch_success,
              
                    error: function () 
		    {
                       alert('/ajax/event_fetch.html' +"   "+"Server Error Change not made");
		      
		       
                    }
         });
      }       
              
       $("#get_event_history").click( function(e)
       {
	 var data;
	 data = {}
	 data.days = $("#event_history_day").val()
	
	 event_fetch(data);
	 
       });
       
             
       
     
  } // end of function
)



