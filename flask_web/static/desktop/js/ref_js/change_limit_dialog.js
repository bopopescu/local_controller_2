$(document).ready(
 function()
 {
     var result;
     var schedule_name;
     var flow_sensor;
     var composite_limit_values;
     var json_string;
     var conversion_factor;
     

   
     $("#save_limits").bind("click",function(event,ui)
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
	 json_object.sensor = flow_sensor;
	 json_object.schedule = schedule_name
	 json_object.step_number = composite_limit_values.length
         json_string = JSON.stringify(json_object);
	
         result = confirm("Do you want to make change selected flow limits");
	 
         if( result == true )
         { 
	  
	   
	   // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/change_flow_limits.html',
                    dataType: 'json',
                    async: false,
	            contentType: "application/json",
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       window.location.replace( "manual_flow_limit.html" )
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/change_flow_limits.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if     
   
  
});


     
     
     
     function composite_limits_success( data )
     {
        var temp_index
        composite_limit_values = data
        $("#limit_data").empty();
      
     
        var html = "";
          html +=  "<h3>Selects limits to change for Schedule ----> "+schedule_name+"  and Flow Sensor ----> "+flow_sensor+ "</h3>";
	  html += '<div data-role="controlgroup">';
           for( i = 0; i < data.length; i++ )
          { 
	    
	    data[i].limit_std = parseInt( data[i].limit_std*conversion_factor*100)/100
	    data[i].limit_avg = parseInt( data[i].limit_avg*conversion_factor*100)/100
	    data[i].composite_avg = parseInt( data[i].composite_avg*conversion_factor*100)/100
	    data[i].composite_std = parseInt( data[i].composite_std*conversion_factor*100)/100
            temp_index = i +1;    
	    html +=   '<label for=id'+i+'  >Station '+temp_index+" Replace (mean , std) "+data[i].limit_avg+" , "+data[i].limit_std+" With "+data[i].composite_avg+" , "+data[i].composite_std +"</label>"
	    html +=   '<input type=checkbox   id=id'+i+' />';
             
           }
 
      html += "</div>";
     
      $("#limit_data").append (html)
      for( i = 0; i < data.length; i++ )
      {
        $("#id"+i).checkboxradio();
        $("#id"+i).checkboxradio("refresh");	 
      }
          
   }     
      
   function load_data(event, ui) 
   {
     
 
      
      
       var json_string;
       var json_data;
       var step_number
       
       
       
       json_data = {}
       schedule_name = localStorage.getItem("db_schedule" );
       flow_sensor = localStorage.getItem("db_flow_sensor" );
       conversion_factor = localStorage.getItem("db_conversion_factor");
       step_number = localStorage.getItem("db_step_number");
       json_data = {}
       json_data.schedule = schedule_name;
       json_data.sensor = flow_sensor;
       json_data.step_number = parseInt(step_number);
       
       
       json_string = JSON.stringify(json_data)
       
       
       
      $.ajax
      ({
	
                    type: "GET",
                    url: '/ajax/get_limit_and_composite.html',
                    dataType: 'json',
                    async: false,
                    contentType: "application/json",
                    //json object to sent to the authentication url
                    data: json_string,
                    success: composite_limits_success, 
		   
                    error: function () 
		    {
                       alert('/ajax/get_limit_and_composite.html'+"  Server Error Change not made");
		   
		       
                    }
      })
          
	
   }
  
   $("#back").button();
   load_data();
 });
