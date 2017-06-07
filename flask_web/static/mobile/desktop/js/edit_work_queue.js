
 function load_irrigation_queue_data()
 {
     var result;
     var schedule_name;
     var flow_sensor;
     var queue_values;
     var json_string;
     

   
     $("#delete_limits").bind("click",function(event,ui)
     {
       
         var mask;
	 var update_flag;
	 var status;
	 var json_object;
	 var json_string;
	 
         status = [];
	 update_flag = 0;
         for( i=0;i<queue_values.length;i++)
	 {
	   
	   if( $("#qid"+i).is(":checked") == true )
	   {
	     
             
	     status.push(1);
	     update_flag = 1;
	   }
	   else
	   {
	     
	     status.push(0);
	   }
	 }
         if( update_flag == 0 ){ alert("no changes selected"); return; }   
         json_string = JSON.stringify(status);
	
         result = confirm("Do you want to make change selected flow limits");
	 
         if( result == true )
         { 
	  
	   
	   // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/delete_queue_element.html',
                    dataType: 'json',
                    async: false,
	            contentType: "application/json",
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       load_data();
                    },
                    error: function () 
		    {
                       alert('/ajax/delete_queue_element.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if     
   
  
});


     
     
     
     function getQueueEntries( data )
     {

        var temp_index;
        var html;
       queue_values = data
       
        $("#queue_elements").empty();
      
       if( data.length == 0 )
       {
        var html = "";
          html +=  "<h3>No Elements in Work Queue </h3>";
	  html += '<div data-role="controlgroup">';
	 
	 
       }
       else
       {
        var html = "";
          html +=  "<h3>Selects select elements to be deleted from queue </h3>";
	  html += '<div data-role="controlgroup">';

          for( i = 0; i < data.length; i++ )
          {
	    data[i].value = parseInt( data[i].value)
            temp_index = i +1;    
	    html +=   '<label for=qid'+i+'  >Queue Element '+temp_index+" Name "+data[i].name+" Total Time "+data[i].value +"</label>"
	    html +=   '<input type=checkbox   id=qid'+i+' />';
             
           }
       } // else
      html += "</div>";
     
      $("#queue_elements").append (html)

      for( i = 0; i < data.length; i++ )
      {
        $("#qid"+i).checkboxradio();
        $("#qid"+i).checkboxradio("refresh");	 
      }
          
   }     
      
   function load_data(event, ui) 
   {
     
 
        
       
      $.ajax
      ({
	
                    type: "GET",
                    url: '/ajax/get_queue_entry.html',
                    dataType: 'json',
                    async: false,

                    success: getQueueEntries, 
		   
                    error: function () 
		    {
                       alert('/ajax/get_queue_entry.html'+"  Server Error Change not made");
		   
		       
                    }
      })
          
	
   }
   load_data();
   $("#refresh_b").bind("click",function(event,ui)
   {
     
      load_data();
      
   });
  
}
