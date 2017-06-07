
/*
	    <option selected value=0>Zero Selected ETO Data</option>
	    <option value=1>Subtract .05 inch from ETO Data</option>
	    <option value=2>Add .05 inch from ETO Data</option>
	    <option value=3>Select All Elements</option>
	    <option value=4>Unselect All Elememts</option>
*/

  
  
 function load_eto_data()
 {
     var result;
     var json_object;
     var json_string;
     var eto_ref_data;
     var eto_current_data;
     var check_status;

     function save_data()
     {
       var schedule_name;
       var schedule_step;
       var runtime_step;
       
      
            
       var json_string = JSON.stringify(eto_current_data);
   
       
       
       var result = confirm("Do you want to change eto");
       if( result == true )
       {    // making update
	    uncheck_elements()
	    save_check_state();
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/save_eto_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
	            contentType: "application/json",
                    success: function () 
		    {
                       alert("Changes Made");
		       load_data()
		       
                    },
                   error: function () 
		    {
                       alert('/ajax/save_eto_data.html '+"Server Error Change not made");
		      
		       
                    }

              });
        }
               
       
       
       
       
       
       
       
     }

     $("#eto_op_mode").bind('click change',function(event,ui)
     {
       
       save_check_state()
       for( i= 0; i<eto_current_data.length; i++ )
       {
             
           if( $("#id"+i).is(":checked") == true )
	   {
             
	       process_data(i);
	    
	   }
	   else
	   {
	      ; // do nothing
	   }       
       }
       
       process_end_results();
       restore_check_state();
       $("#eto_op_mode")[0].selectedIndex = 0 
       $("#eto_op_mode").refresh()
     });
     
   function process_end_results()
   {
     switch( $("#eto_op_mode")[0].selectedIndex )
     {

		
	 case 4: 
	        
	        check_elements();
	        save_check_state();
		break;
		
	 case 5:
	       
	        uncheck_elements()
	        save_check_state();
	        break;
	
	 case 7: save_data()
		break;
     }
   
     display_data( eto_current_data );
     
   }
     
   function process_data(i)
   {
     
     switch( $("#eto_op_mode")[0].selectedIndex )
     {
	 case 0: 
	        break;
	 
	 
	 case 1:
	        
		eto_current_data[i].data = 0;
		break;
		  
	 case 2:
	        
		eto_current_data[i].data = eto_current_data[i].data -.05;
		break;
		
	 case 3:
	        
		eto_current_data[i].data = eto_current_data[i].data +.05;   
		break;
		
	 case 6: 
	        
	        eto_current_data[i].data = eto_ref_data[i];
		break;
	 
       }
       
   }


     function display_data( data )
     {
           var html = "";
	   
	   $("#eto_list").empty();
            for( i = 0; i < data.length; i++ )
            {
	      data[i].data = parseFloat( data[i].data)
              temp_index = i +1;    
	      html +=   '<label for=id'+i+"> "+data[i].name+"    ---   Water Deficient (inch) -->"+data[i].data +"</label>"
	      html +=   '<input type=checkbox   id=id'+i+' />';
             
             }
             html += "</div>";
             $("#eto_list").append (html)
             for( i = 0; i < data.length; i++ )
             {
               $("#id"+i).checkboxradio();
               $("#id"+i).checkboxradio("refresh");	 
             }     
     
        
     }
     
     function save_check_state()
     {
       
         check_status = [];
	
         for( i=0;i<eto_current_data.length;i++)
	 {
	   
	   if( $("#id"+i).is(":checked") == true )
	   {
             
	     check_status.push(1);
	     update_flag = 1;
	   }
	   else
	   {
	     check_status.push(0);
	   }
	 }

       
     }
     
     function restore_check_state()
     {
         for( i=0;i<eto_current_data.length;i++)
	 {
	   
	   if( check_status[i] |= 0 )
	   {
	    $("#id"+i).prop('checked', true).checkboxradio('refresh');
	   }
	   else
	   {
	     $("#id"+i).prop('checked', false).checkboxradio('refresh');
	     
	   }
	  
	 }

       
     }
     
     
     
     function uncheck_elements()
     {
        
         for( i=0;i<eto_current_data.length;i++)
	 {
	     $("#id"+i).prop('checked', false).checkboxradio('refresh');
	  
	 }

       
     }
     
     function check_elements()
     {
        
         for( i=0;i<eto_current_data.length;i++)
	 {
	    $("#id"+i).prop('checked', true).checkboxradio('refresh');
	  
	 }

       
     }
     
     function getQueueEntries( data )
     {
         var temp_index;
         var html;
	 var i;
	 
         eto_current_data   = data
         eto_ref_data = [];
         $("#eto_list").empty();
      
         if( data.length == 0 )
         {
            var html = "";
            html +=  "<h3>No ETO Setups</h3>";
	 
         }
         else
         {
	    display_data( eto_current_data);
	    for( i= 0; i < eto_current_data.length ;i++)
	    {
	         eto_ref_data.push(eto_current_data[i].data);
	    }
	    uncheck_elements()
	    
	    save_check_state();

	 }
   }     
      
   function load_data(event, ui) 
   {
     
 
        
       
      $.ajax
      ({
	
                    type: "GET",
                    url: '/ajax/get_eto_entries.html',
                    dataType: 'json',
                    async: false,

                    success: getQueueEntries, 
		   
                    error: function () 
		    {
                       alert('/ajax/get_eto_entries.html'+"  Server Error Change not made");
		   
		       
                    }
      })
          
	
   }
   load_data();
   $("#refresh_c").bind("click",function(event,ui)
   {
     
      load_data();
      
   });
 }
