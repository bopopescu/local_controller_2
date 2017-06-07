$(document).ready(
 function()
 {
     var result;
     var schedule_name;
     var flow_sensor;
     var composite_limit_values;
     var json_string;
     var conversion_factor;
     

   
     $("#clear_modbus_counter").bind("click",function(event,ui)
     {
       
         var mask;
	 var update_flag;
	 var status;
	 var json_object;
	 var json_string;
	 
         status = [];
	 update_flag = 0;
         for( i=0;i<composite_limit_values.length;i++)
	 {
	   
	   if( $("#id"+i).is(":checked") == true )
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
         json_object = {}
         json_object.mask = status;
         json_string = JSON.stringify(json_object);
	
         result = confirm("Do You Wish to Clear Modbus Error Counters ?");
	 
         if( result == true )
         { 
	  
	   
	   // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/clear_modbus_counters.html',
	            contentType: "application/json",
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       load_data() 
                    },
                    error: function () 
		    {
                       alert('/ajax/clear_modbus_counters.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if     
   
  
});


     
     
     
     function modbus_statistics_success( data )
     {
        var temp_index
        composite_limit_values = data
        $("#modbus_counter").empty();
      
        
        var html = "";
          html +=  "<h3>Select to clear  </h3>";
	  html += '<div data-role="controlgroup">';
          
          for( i = 0; i < data.length; i++ )
          {
	    data[i].count = parseInt( data[i].count)
	    if( data[i].count == 0 ){ data[i].count = 1; data[i].success = 1; }
	    data[i].success = parseInt( data[i].success);
	    data[i].failed = parseInt((data[i].count-data[i].success)*100/data[i].count)/100
            temp_index = i +1;    
	    html +=   '<label for=id'+i+'  >Station '+data[i].name+" Total Msg -->"+data[i].count+" Failed Msg Rate ---->"+data[i].failed+"%   Modbus Errors -->"+data[i].error+" " +"</label>"
	    html +=   '<input type=checkbox   id=id'+i+' />';
             
           }
 
      html += "</div>";
     
      $("#modbus_counter").append (html)
      for( i = 0; i < data.length; i++ )
      {
        $("#id"+i).checkboxradio();
        $("#id"+i).checkboxradio("refresh");	 
      }
          
   }     
      
   function load_data(event, ui) 
   {
     
 
      
      
       
       
       
      $.ajax
      ({
	
                    type: "GET",
                    url: '/ajax/modbus_statistics.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    
                    success: modbus_statistics_success, 
		   
                    error: function () 
		    {
                       alert('/ajax/modbus_statistics.html'+"  Server Error Change not made");
		   
		       
                    }
      })
          
	
   }
       

   load_data();
   $("#refresh").bind("click",function(event,ui)
   {
     
      load_data();
      
   });
 });
