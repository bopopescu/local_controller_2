


$(document).ready(
 function()
 {
  var alarm_data;
  var alarm_display;
  
  
  function parse_incomming_data( data )
  {
     var i;
     var returnValue;
     var alarm_type;
     returnValue = []
     alarm_type = $("#Alarm_Types").val();
     alarm_type = parseInt( alarm_type);
     if( alarm_type == 0 ){ return data; }
     for( i=0; i < data.length; i++ )
     {
       
       temp = data[i][0].split("|");
       
       temp_int = parseInt(temp[0]);
       
       if( temp_int == alarm_type )
       {
	 returnValue.push( data[i] ) 
	 
	 
       }
       
       
     }
    
     return returnValue;
    
  }
 
  function alarm_data_list( data )
    {
        var temp_index;
        var temp_data;
        
	alarm_data = data;
	// parse by display type
        data = parse_incomming_data( data );
        alarm_display = data;
        
       
        $("#alarm_display").empty();
      
      
        var html = "";
        
	  html += '<div data-role="controlgroup">';

          for( i = 0; i < data.length; i++ )
          {
            temp_index = i +1;    
	    html +=   '<label for=id'+i+'  >Alarm Name--> '+data[i][0]+' ----Value--> '+data[i][1]+' ----Time--> '+data[i][2] +"</label>"
	    html +=   '<input type=checkbox   id=id'+i+' />';
             
           }
 
      html += "</div>";
      $("#alarm_display").empty()
      $("#alarm_display").append (html)
      for( i = 0; i < data.length; i++ )
      {
        $("#id"+i).checkboxradio();
        $("#id"+i).checkboxradio("refresh");	 
      }
          
               
       
  }
     
     function getAlarmData()
     {
       
        $.ajax
            ({
                    type: "GET",
                    url: '/ajax/get_alarm_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: alarm_data_list,
                    error: function () 
		    {
		      
                       alert('/ajax/get_alarm_data.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	    
     }
     
     function delete_alarms()
     {
       
         var mask;
	 var update_flag;
	 var status;
	 var json_object;
	 var json_string;
	 
         status = [];
	 update_flag = 0;
         for( i=0;i<alarm_data.length;i++)
	 {
	   
	   if( $("#id"+i).is(":checked") == true )
	   {
             
	     status.push(alarm_display[i][0])
	     update_flag = 1;
	   }
	   else
	   {
	     status.push(null);
	   }
	 }
         if( update_flag == 0 ){ alert("no changes selected"); return; }   
      
         json_string = JSON.stringify(status);
	
         result = confirm("Do you want to delete selected alarm limits");
	 
         if( result == true )
         { 
	  
	   
	   // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/delete_alarm_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       getAlarmData();
                    },
                    error: function () 
		    {
                       alert('/ajax/delete_alarm_data.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if     
     }
  
     $( "#Alarm_Types" ).bind( "change", function(event, ui) 
     { 
       alarm_data_list( alarm_data ); 
  
     } );
 
     $( "#Alarm_Actions" ).bind( "change", function(event, ui) 
     { 
       
       switch( $("#Alarm_Actions")[0].selectedIndex )
       {
	 case 0:
	          // do no actions
		  break;
		  
	 case 1:
	        check_alarm();
	
		break;
		
	 case 2: 
	        uncheck_alarm();
	
		break;
		
	 case 3:
	        delete_alarms();
		break;
	 
       }
        
  
     } );

     function check_alarm()
     {
       
         var mask;
	 var update_flag;
	 var status;
	 var json_object;
	 var json_string;
	 
         status = [];
	 update_flag = 0;
        
         for( i=0;i<alarm_data.length;i++)
	 {
	
               $("#id"+i).prop("checked", true).checkboxradio("refresh");	
	   
	}
     }	 
    
     function uncheck_alarm()
     {
         var mask;
	 var update_flag;
	 var status;
	 var json_object;
	 var json_string;
	 
         status = [];
	 update_flag = 0;

         for( i=0;i<alarm_data.length;i++)
	 {
	   $("#id"+i).prop("checked", false).checkboxradio("refresh");
	   
	 }
     }	 
       
       
       
       
       
     
     $("#AlarmPag").on('pageint',function () {
          
           ajax_request();
     });
     

     
     
     // get flow sensors
      getAlarmData();
  

  } )


