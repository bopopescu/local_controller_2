$(document).ready($(function()
{
   var current_row = -1;
   var current_column = -1;
   var table_number = -1;
   var data_array
   var ref_row = null
   var ref_column = null

   var schedule_data

   function update_success()
   {
      schedule_request();  
     
   }
   
   
   
  function check_for_duplicate_name( text )
  {
    
    for( i = 0; i < table_number; i++ )
    {
       if( text == schedule_data[i].name )
       {
	 
	 return false;
       }
    }
    
    
    return true;
  }
  
   function insert_schedule_do()
   {

    var text;
    var json_object;
    var json_string;
    
    text = $("#copy_name").val();
    if( text=="" ){ alert("Please enter insert name"); return; }
    
    if( check_for_duplicate_name( text ) == true )
    {
      json_object = {}
      json_object.insert_schedule = text;
      json_string = JSON.stringify(json_object);
      $.ajax({
                    type: "POST",
                    url: '/ajax/insert_schedule.html',
	            contentType: "application/json",
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_success,
	     
                    error: function () 
		    {
                       alert('/ajax/insert_schedule.html'+"  Server Error Change not made");
		       
		       
                    }
              });
    }
    else
    {
      alert("selected name "+text+" already exists ");
    }
    $( this ).dialog( "close" );
  }   
   
   
   
  function copy_schedule_do()
  {
    var text;
    var json_object;
    var json_string;
    
    text = $("#copy_name").val();
    if( text=="" ){ alert("Please enter copy name"); return; }
    
    if( check_for_duplicate_name( text ) == true )
    {
      json_object = {}
      json_object.copy_source = schedule_data[ref_row].name;
      json_object.copy_destination = text;
      json_string = JSON.stringify(json_object);
      $.ajax({
                    type: "POST",
                    url: '/ajax/copy_schedule.html',
	            contentType: "application/json",
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: update_success,
	     
                    error: function () 
		    {
                       alert('/ajax/copy_schedule.html'+"  Server Error Change not made");
		       
		       
                    }
              });
    }
    else
    {
      alert("selected name "+text+" already exists ");
    }
    $( this ).dialog( "close" );
  }
     
 
   function insert_schedule()
   {
          $( "#insert_schedule_form" ).dialog({
	  title:"Insert Schedule",
          resizable: false,
          height:300,
          width: 400,
          modal: true,
          buttons: 
          {
	     Insert: insert_schedule_do,
             Cancel: function() 
	     {
                $( this ).dialog( "close" );
             }
           }
        });

   }
   
   
   function insert_schedule_a()
   {
     insert_schedule();
     $( this ).dialog( "close" );
   }
   
   function delete_schedule()
   {
      var result;
      var json_object;
      var json_string;
      
     
        
	 result = confirm("do you wish to delete schedule "+ schedule_data[ref_row].name);
	 if( result == true )
	 {
	            json_object = {}
                    json_object.deleted_schedule = schedule_data[ref_row].name;
                    json_string = JSON.stringify(json_object);
                    $.ajax({
                       type: "POST",
                       url: '/ajax/delete_schedule.html',
		       contentType: "application/json",
                       dataType: 'json',
                       async: false,
                       //json object to sent to the authentication url
                       data: json_string,
                       success: update_success,
                       error: function () 
		       {
                          alert('/ajax/delete_schedule.html'+"  Server Error Change not made");
		       }
                       });
		    
	 }
	 $( this ).dialog( "close" );
   }
   
   function copy_schedule()
   {
        
         $( "#insert_schedule_form" ).dialog({
	  title:"Copy Schedule "+schedule_data[ref_row].name,
          resizable: false,
          height:300,
          width: 400,
          modal: true,
          buttons: 
          {
	     Copy:   copy_schedule_do,
             Cancel: function() 
	     {
                $( this ).dialog( "close" );
             }
           }
        });
        $( this ).dialog( "close" );
   }
   
   function edit_schedule()
   {
      localStorage.setItem("edit_schedule_name",schedule_data[ref_row].name );
      window.location='/full_site_configuration_detail.html';
      $( this ).dialog( "close" );
   }
   
   function cell_select( iRow,iCol)
   {
	  
	  ref_column = parseInt(iCol,10);
          ref_row    = parseInt(iRow,10);
	  
	  temp = parseInt(ref_row,10);
	  $("#edit_schedule_data_name").html("Current Station is: "+schedule_data[temp].name);
          $( "#edit_schedule_data" ).dialog({
	  title:"Insert/Delete/Copy/Edit Schedule",
          resizable: false,
          height:300,
          width: 400,
          modal: true,
          buttons: 
          {
	     Insert:  insert_schedule_a,
	     Delete:  delete_schedule,
             Copy:    copy_schedule,
	     Edit:    edit_schedule,
             Cancel: function() 
	     {
                $( this ).dialog( "close" );
             }
           }
        });
      }       

   function grid_setup()
   {
      $("#grid_array").jqGrid(
     {
	onCellSelect: cell_select,
        rowNum:20,
	datatype: "local",
   	data: data_array, 
   	colModel:[
   	        {name:'name',label:'schedule  name'},
   		{name:'start_time',label:'start time'},
   		{name:'end_time',label:'end time'},
   		{name:'sunday',label:'sun'},
   		{name:'monday',label:'mon'},
   		{name:'tuesday',label:'tues'},		
   		{name:'wednesday',label:'wed'},		
    		{name:'thursday',label:'thurs'},
   		{name:'friday',label:'fri'},		
   		{name:'saturday',label:'sat'}		
  				
   	],
   	
        caption:"List of Schedules"
      });
      $("#grid_array").jqGrid('setGridHeight',800);

   }
    
     var ajax_schedule_success = function(data)
     {
          schedule_data = data;
          var table_data
          var element  
          
          grid_setup();
	  $("#grid_array").clearGridData(false);
          table_data = []
          table_number = data.length;
          for (var i = 0; i < data.length; i++) 
          {
	     element = {}
	    
	     element.name       =  data[i].name;
	     element.start_time =  data[i].start_time[0]+":"+data[i].start_time[1];
	     element.end_time   =  data[i].end_time[0]+":"+data[i].end_time[1];
	     element.sunday     =  data[i].dow[0];
	     element.monday     =  data[i].dow[1];
	     element.tuesday    =  data[i].dow[2];
	     element.wednesday  =  data[i].dow[3];
	     element.thursday   =  data[i].dow[4];
	     element.friday     =  data[i].dow[5];
	     element.saturday   =  data[i].dow[6];
	     table_data.push(element)
	     $("#grid_array").addRowData(i,element, "", i);
                  
          }
          grid_setup(table_data)

     }
 
    
        
      schedule_request = function()
      {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/schedule_data.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    success: ajax_schedule_success,
              
                    error: function () 
		    {
                       alert('/ajax/schedule_data.html' +"   "+"Server Error Change not made");
		       schedule_request();
		       
                    }
         });
      }
      
  $('#back').click(function() {
      window.location='/index.html';
   });
    
  
   
  
  $("#insert_schedule").click(function()
  {
     insert_schedule();
     
  });
  
  
 
  
  


  
  $("#insert_schedule_form").hide();
  $("#edit_schedule_data").hide();
  schedule_request();
    
})); 
