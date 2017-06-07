$(document).ready($(function()
{ 
    var ref_column;
    var ref_row;
    var ref_data;
    var grid_data;
    
    ref_row = 0;
    ref_column = 0;
    $( "#tabs" ).tabs();
    
    
   
     var ajax_schedule_success = function(data)
     {
       var i;
       var j;
       var temp_index;
       
    
       
      
       
       ref_data = data;
        
      
       $("#edit_schedule").html("<h2>Edit schedule for "+localStorage.getItem("edit_schedule_name" )+ " </h2>")
       $("#description").val(data.description);

       temp_index = data.start_time[0]*4;
       temp_index + data.start_time[1]/15;
       $("#starting_time")[0].selectedIndex = temp_index;

       temp_index = data.end_time[0]*4;
       temp_index += data.end_time[1]/15;
       $("#ending_time")[0].selectedIndex = temp_index;

       if( data.dow[0] != 0 ){ $("#sunday").prop( "checked", true ) } else {$("#sunday").prop( "checked", false ) }
       if( data.dow[1] != 0 ){ $("#monday").prop( "checked", true ) } else {$("#monday").prop( "checked", false ) }
       if( data.dow[2] != 0 ){ $("#tuesday").prop( "checked", true ) } else {$("#tuesday").prop( "checked", false ) }
       if( data.dow[3] != 0 ){ $("#wednesday").prop( "checked", true ) } else {$("#wednesday").prop( "checked", false ) }
       if( data.dow[4] != 0 ){ $("#thursday").prop( "checked", true ) } else {$("#thursday").prop( "checked", false ) }
       if( data.dow[5] != 0 ){ $("#friday").prop( "checked", true )} else {$("#friday").prop( "checked", false ) }
       if( data.dow[6] != 0 ){ $("#saturday").prop( "checked", true ) } else {$("#saturday").prop( "checked",false  ) }
       load_grid( data );
    
     }
    
      function load_grid( data )
      {
       var field_array = ["station_1","station_2","station_3","station_4","station_5"];
       var temp_element;
       
       $("#grid_array").jqGrid('clearGridData' );
       grid_data = []
       for( i = 0; i < data.controller_pins.length; i++)
       {

	 temp_element = {}
         temp_element.step = i+1;
	 temp_element.time = data.steps[i];
	
         for( j = 0; j < data.controller_pins[i].length; j++)
	 {
	   temp = {}
	   temp.controller = data.controller_pins[i][j][0]
	   temp.pins       = parseInt(data.controller_pins[i][j][1])
	
	   temp_element[field_array[j]] = (data.controller_pins[i][j][0]+":"+data.controller_pins[i][j][1]);
	 }
	 grid_data.push(temp_element);
	  $("#grid_array").addRowData(i,temp_element, "", i);
	 
       }
      
      } 
      
      function load_grid_a( data )
      {
       var field_array = ["station_1","station_2","station_3","station_4","station_5"];
       var temp_element;
  
       for( i = 0; i < data.length; i++)
       {
         data[i].step = i+1;
	 temp_element = {}
         temp_element.step = i+1;
	 temp_element.time = data[i].time;
	
         for( j = 0; j < field_array.length; j++)
	 {
	   if( data[i][field_array[j]] != null )
	   {
	      temp_element[field_array[j]] = data[i][field_array[j]];
	   }
	 }
	
	  $("#grid_array").addRowData(i,temp_element, "", i);
	 
       }
       return data;
      
      } 
      
      schedule_request = function()
      {
	 var json_object;
	 var json_string;
	 
	 json_object = {}
	 json_object.schedule_name = localStorage.getItem("edit_schedule_name" );
	
	 json_string = JSON.stringify(json_object);
         $.ajax(
         {        
                    type: "GET",
                    url: '/ajax/schedule_entry.html',
                    dataType: 'json',
		    contentType: "application/json",
                    async: false,
		    data: json_string,
                    //json object to sent to the authentication url
                    success: ajax_schedule_success,
              
                    error: function () 
		    {
                       alert('/ajax/schedule_entry.html' +"   "+"Server Error Change not made");
		       //schedule_request();
		       
                    }
         });
      }
      
      dataArray = []

      
      function cell_select( iRow,iCol)
      {
	  var value
	  ref_column = iCol;
          ref_row    = iRow;
	  //alert("ref_row is "+ref_row);
	  value = $("#grid_array").getCell(iRow,iCol)
	  if( ref_column > 1 )
	  {
	    open_edit_station(value);
	  }
	  else if( ref_column == 1 )
	  {
	   
	    open_edit_runtime(value);
	  }
	  else
	  {
	    open_edit_step_data(value);
	  }
	    

      }
      
      
      $("#grid_array").jqGrid({
	onCellSelect: cell_select,
        rowNum:0,
	datatype: "local",
   	data: dataArray, 
   	colModel:[
   	        {name:'step',label:'step'},
   		{name:'time',label:'time'},
   		{name:'station_1',label:'station 1'},
   		{name:'station_2',label:'station 2'},
   		{name:'station_3',label:'station 3'},
   		{name:'station_4',label:'station 4'},		
   		{name:'station_5',label:'station 5'}		
   				
   	],
   	
        caption:"Step List"
         });
      
       function open_edit_station(value)
      {
	  var temp1;
	  var temp2;
	  temp1 = parseInt(ref_row, 10) +1;
	  temp2 = parseInt(ref_column,10)-1;

	  $("#edit_station_label").html("Current Step is "+temp1+" Valve index is "+temp2);
	  $("#current_selection").html("Current Value is (Controller:Pin): "+value)
          $( "#edit_station" ).dialog({
          resizable: false,
	  title:"Add/Delete/Update Sprinkler Valve",
          height:500,
          width: 800,
          modal: true,
          buttons: 
          {
	     Save_Valve: save_valve,
	     Delete_Valve: delete_valve,
	     			      
             Cancel: function() 
	     {
                $( this ).dialog( "close" );
             }
           }
        });
      }
      
      function open_edit_runtime(value)
      {
	  var temp1;
	  var temp2;
	  temp1 = parseInt(ref_row, 10) +1;
	  temp2 = parseInt(ref_column,10)-1;
	  $("#current_runtime_selection").html("Current runtime setting for station "+temp1)
	  if( value > 0 )
	  {
	    $("#controller_run_time")[0].selectedIndex = value-4;
	  }
	  else
	  {
	    $("#controller_run_time")[0].selectedIndex  = 0;
	  }
	 
          $( "#edit_run_time" ).dialog({
	  title:"Change Sprinkler Runtime",
          resizable: false,
          height:300,
          width: 800,
          modal: true,
          buttons: 
          {
	     Save_Time: save_time,
             Cancel: function() 
	     {
                $( this ).dialog( "close" );
             }
           }
        });
      }
      
     function open_edit_step_data(value)
      {
	  var temp;
	  temp = parseInt(ref_row,10)+1;
	  $("#edit_step_data_label").html("Current Station is: "+temp);
          $( "#edit_step_data" ).dialog({
	  title:"Delete/Insert Step",
          resizable: false,
          height:300,
          width: 800,
          modal: true,
          buttons: 
          {
	     Insert_After:  insert_after,
	     Insert_Before: insert_before,
             Delete_Step: delete_step,
             Cancel: function() 
	     {
                $( this ).dialog( "close" );
             }
           }
        });
      }      
      function delete_valve()
      {
	
         var field_array = ["station_1","station_2","station_3","station_4","station_5"];
	 var temp1;
	 var temp2;
	 var temp;
	 var i;
	 
	 temp1 = parseInt(ref_row, 10);
	 temp2 = parseInt(ref_column,10);
         temp2 = temp2-2;
	 for( i = temp2; i<=field_array.length-1;i++)
	 {

	   grid_data[temp1][field_array[i]] = grid_data[temp1][field_array[i+1]]
	 }
	 grid_data[temp1][field_array.length-1] = undefined;
	 $("#grid_array").jqGrid('clearGridData' );
	 grid_data = load_grid_a( grid_data )
	 $( this ).dialog( "close" );
      }
      
      
      function save_time()
      {
	grid_data[ref_row].time = $("#controller_run_time").val()
        $("#grid_array").jqGrid('clearGridData' );
	grid_data = load_grid_a( grid_data )
	$( this ).dialog( "close" );

      }
      
      function check_for_duplicate_data( row, value )
      {
	var i;
	var field_array = ["station_1","station_2","station_3","station_4","station_5"];
        for( i = 0; i<field_array.length;i++)
	{
           if( value == grid_data[row][field_array[i]] )
	   {
	     return true;
	   }
	}
	return false;
      }
	
     function pack_value( row,value )
     {
	var i;
	var field_array = ["station_1","station_2","station_3","station_4","station_5"];
        for( i = 0; i<field_array.length;i++)
	{  
           if( grid_data[row][field_array[i]] == undefined )
	   {
	      
	      grid_data[row][field_array[i]] = value;     
	      return;
	   }
	}
	
      }
	
      function save_valve()
       {
	
         var field_array = ["station_1","station_2","station_3","station_4","station_5"];
	 var temp1;
	 var temp2;
	 var temp;
	 var temp3;
	 
	 temp3 = $("#controller_select").val()+":"+$("#select_pin").val();
	 

	 temp1 = parseInt(ref_row, 10);
	 temp2 = parseInt(ref_column,10);
         temp2 = temp2-2;
	 if( check_for_duplicate_data( temp1,temp3 ) == true ){ alert("valve "+temp3+" is defined in the step");return; }
	 if( grid_data[temp1][field_array[temp2]] != undefined )
	 {
	   grid_data[temp1][field_array[temp2]] = temp3;
	 }
	 else
	 {
	   pack_value( temp1,temp3);
	 }
	 
	 $("#grid_array").jqGrid('clearGridData' );
	 grid_data = load_grid_a( grid_data )

	 $( this ).dialog( "close" );
      }
      
      function insert_before()
      {
	 var row_count;
	 var temp_element;
	 var temp
	 temp_element = {}
	 temp_element.time = 10;
	 temp = parseInt(ref_row,10)+1;
	 
	 row_count = $("#grid_array").getGridParam("reccount");
	 if( row_count > 0 )
	 {
	    if( confirm("Do you wish to insert a row before current row "+temp)==false){ return; }
	    grid_data.splice(ref_row, 0, temp_element);
	    $("#grid_array").jqGrid('clearGridData' );
	    grid_data = load_grid_a( grid_data )
	    
	 }
	 else
	 {
	    grid_data.push(temp_element);
	    $("#grid_array").jqGrid('clearGridData' );
	    grid_data = load_grid_a( grid_data )

	 }
	 $( this ).dialog( "close" );
       }
            
      function insert_after()
      {
	 var row_plus_one
	 var temp;
	 var row_count;
	 var temp_element;
	 temp_element = {}
	 temp_element.time = 10;
	 temp = parseInt(ref_row,10)+1;
	 row_plus_one = parseInt(ref_row,10)+1;
	 
	 row_count = $("#grid_array").getGridParam("reccount");
	 if( row_count != 0 )
	 {
	    if( confirm("Do you wish to insert a row after current row "+temp)==false){ return; }
	   
	    grid_data.splice(row_plus_one, 0, temp_element);
	    $("#grid_array").jqGrid('clearGridData' );
	    grid_data = load_grid_a( grid_data )
	    
	 }
	 else
	 {
	    grid_data.push(temp_element);
	    $("#grid_array").jqGrid('clearGridData' );
	    grid_data = load_grid_a( grid_data )

	 }
	 $( this ).dialog( "close" );
       }
       
      function delete_step()
      {
	var row_count;
	if( confirm("Do you wish to delete row "+ref_row)==false){ return; }
	row_count = $("#grid_array").getGridParam("reccount");

	if( ref_row < 0 ){ return;}
	if( ref_row >= row_count){ return;}
	grid_data.splice(ref_row,1);
	$("#grid_array").jqGrid('clearGridData' );
	grid_data = load_grid_a( grid_data );
	$( this ).dialog( "close" );
      }
 
     

      
      $("#controller_run_time").empty()
      $("#controller_run_time").append('<option value='+0+'>'+0+'</option>');
      for( var i = 5; i <= 400; i++ )
      {
	    
          $("#controller_run_time").append('<option value='+i+'>'+i+'</option>');	
	
	}

      
      $("#controller_select").bind("click",function(event,ui)
       {
          var index;
	  index = $("#controller_select")[0].selectedIndex;
          populate_pins( index );
       });
      
      
      function populate_pins( index )
      {
         var pins;
         pins = controller_pin_data[index].pins;
         $("#select_pin").empty()
         for( var i = 1; i <= pins.length; i++ )
         {
             $("#select_pin").append('<option value='+i+'>pin: '+i+' cable bundle: '+pins[i-1].cable_bundle+' wire color: '+pins[i-1].wire_color+ '</option>');	
	
         }
         $("#select_pin")[0].selectedIndex = 0;
      }
   
   
   function controller_pins_success( data )
   {
  
     controller_pin_data = data;
     $("#controller_select").empty()
     for( var i = 0; i < controller_pin_data.length; i++ )
     {
        $("#controller_select").append('<option value='+controller_pin_data[i].name+'>'+controller_pin_data[i].name+'</option>');	
     }
     $("#controller_select")[0].selectedIndex = 0;
     
     populate_pins( 0)

   }
   
   
   
   load_controller_pins = function()
   {
	
         $.ajax(
         {
                    type: "GET",
                    url: '/ajax/load_controller_pins.html',
                    dataType: 'json',
		    contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    success: controller_pins_success,
              
                    error: function () 
		    {
                       alert('/ajax/load_controller_pins.html' +"   "+"Server Error Change not made");
		       
		       
                    }
         });
   }
    
   
     
 
    
    
    $("#insert_row").bind("click",function(event,ui)
     {
         var temp_element;
	 temp_element = {}
	 temp_element.time = 10;
         grid_data.push(temp_element);
	 $("#grid_array").jqGrid('clearGridData' );
	 grid_data = load_grid_a( grid_data );

     });

   $('#back').click(function() {
      window.location='/full_site_configuration.html';
   }); 
   
   $('#reset_changes').click(function() {
      schedule_request();
   });    
 
   function assemble_dow()
   {
     var returnValue;
     returnValue = [];
     
     
     return returnValue
   }
   
   
   
    $("#save_changes").bind("click",function(event,ui)
    {
        var json_object;
	var dow;
	var start_time;
	var end_time;
	var json_string;
	var result;
	

        start_time = $("#starting_time").val();
        end_time = $("#ending_time").val();
        dow = [];
        if( $("#sunday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) };
        if( $("#monday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) };
        if( $("#tuesday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) };
        if( $("#wednesday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) };
        if( $("#thursday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) };
        if( $("#friday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) };
        if( $("#saturday").prop( "checked") == true ){ dow.push(1) } else { dow.push(0) };
	
	json_object = {};
	json_object.schedule_name = localStorage.getItem("edit_schedule_name" );
	json_object.description = $("#description").val();
        json_object.dow = dow;
	json_object.start_time = JSON.parse(start_time)
        json_object.end_time = JSON.parse(end_time)
        json_object.grid_data = grid_data;
	json_string = JSON.stringify(json_object);
        alert(json_string)
       
       
       result = confirm("Do you want to make change schedule "+localStorage.getItem("edit_schedule_name" ));
       if( result == true )
       {    // making update
            $.ajax
            ({
                    type: "POST",
                    url: '/ajax/change_schedule.html',
                    dataType: 'json',
                    async: false,
	            contentType: "application/json",
                    //json object to sent to the authentication url
                    data: json_string,
                    success: function () 
		    {
                       alert("Changes Made");
		       
		       
                    },
                    error: function () 
		    {
                       alert('/ajax/change_schedule.html'+"  Server Error Change not made");
		       
		       
                    }
              })
       }// if
    });
    
    $("#edit_station").hide();
    $("#edit_run_time").hide();
    $("#edit_step_data").hide();

    load_controller_pins();
    schedule_request();

    
}));
