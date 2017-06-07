$(document).ready(
 function()
 {
     var remote_units
     var remote_index = 0

     var remote_unit_list_success = function(data)
     {   
         remote_units = data
         $("#select_remote_units").empty()
         for( var i = 0; i < data.length; i++ )
	 {
	
          $("#select_remote_units").append('<option value='+i+'>'+data[i].name+'</option>');	
	
	 }
       

         
	$("#select_remote_units")[0].selectedIndex = 0;
        $("#select_remote_units").selectmenu();
	$("#select_remote_units").selectmenu("refresh");
     }
     
     
    
     $( "#select_remote_units" ).bind( "click", function(event, ui) 
     {  
             var json_string = JSON.stringify(  $("#select_remote_units")[0].selectedIndex )
             remote_index = $("#select_remote_units")[0].selectedIndex;
             $("#main_header").html("Cloud Controller for Remote Unit: "+remote_units[remote_index].name)
             $.ajax
            ({
                    type: "POST",
                    url: '/ajax/select_remote_units.html',
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		      
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/select_remote_units.html'+"  Server Error Change not made");
		       
		       
                    }
              })
     })

   $( "#ping_remote" ).bind( "click", function(event, ui) 
     {  
             var json_string = JSON.stringify(  $("#select_remote_units")[0].selectedIndex )
             $.ajax
            ({
                    type: "POST",
                    url: '/ajax/ping_remote.html',
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function (data) 
		    {
                       alert(data)
                       if( data == true )
                       {
                          alert("Remote Unit "+remote_units[remote_index].name +" Pinged");
                       }
                       else
                       {
		          alert(remote_units[remote_index].name+"  Not Pinged");
                       }
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/ping_remote.html'+"  Server Error Change not made");
		       
		       
                    }
              })
     })     
   $( "#tr_to_host" ).bind( "click", function(event, ui) 
     {  

            result = confirm("Do you want to transfer remote files to host?");
            if( result != true )
            { 
	       return;
            }

             var json_string = JSON.stringify(  $("#select_remote_units")[0].selectedIndex )
             $.ajax
            ({
                    data: json_string,
                    type: "POST",
                    url: '/ajax/transfer_files_to_host.html',
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url

                    success: function (data) 
		    {
                       alert("Transfered Files to Cloud Server")
                 
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/transfer_files_to_host.html'+"  Server Error Change not made");
		       
		       
                    }
              })
     })          

     $( "#tr_to_remote" ).bind( "click", function(event, ui) 
     {  

            result = confirm("Do you want to transfer host files to remote?");
            if( result != true )
            { 
	       return;
            }

             var json_string = JSON.stringify(  $("#select_remote_units")[0].selectedIndex )
             $.ajax
            ({
                    data: json_string,
                    type: "POST",
                    url: '/ajax/transfer_files_to_remote.html',
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url

                    success: function (data) 
		    {
                       alert("Transfered Files to Remote Units")
                 
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/transfer_files_to_remote"transfer_files_to_remote.html".html'+"  Server Error Change not made");
		       
		       
                    }
              })
     })          
     
     
      remote_unit_load = function()
      {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/get_remote_units.html',
                    dataType: 'json',
                    async: false,
                 
                    success: remote_unit_list_success,
              
                    error: function () 
		    {
                       alert( '/ajax/get_remote_units.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
      }  
  
      remote_unit_load();
      $("#main_header").html("Cloud Controller for Remote Unit: "+remote_units[remote_index].name)


  } // end of function
  

 
)

