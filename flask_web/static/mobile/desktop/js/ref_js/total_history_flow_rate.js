$(document).ready(
 function()
 {
   // flow meter variables
   var ref_flow_meter;
   var conversion_factor_array;
   var conversion_factor_index;
   var conversion_factor;
   
   // schedule/ step variables
   var schedules = []
   var schedules_step = {}
   var schedules_start_times = {}
   var schedules_end_times = {}
   var schedules_dow = {}
   var schedules_pins = {}

 
   var $flow_sensor = $("#Flow_Flow_Sensor");
   var $schedule = $("#Flow_Schedule");
   var $step = $("#Flow_Step");

   
   // graphic
   var g_flow;
   var strip_chart_update;
   var limit_flag;
   
/*
--------------------------------------------------------------------------------------------------------------------------------------------------
Generate Graph
--------------------------------------------------------------------------------------------------------------------------------------------------
*/
  

   function strip_chart_update(data)
   {
        g_flow.updateOptions( { 'file': data } );
   }





  function initialize_flow_graph()
  {
     
    var data = [];
     
 
       var t = new Date();
       for (var i = 100; i >= 0 ; i--)
       {
          var x = new Date(t.getTime() - i * 60000);
          data.push([x,0]);
       }

       g_flow = new Dygraph(document.getElementById("div_g_flow"), data,
                          {
                            pointSize:     3,
			    logscale:   true,
                            drawPoints: true,
                            showRoller: true,
                            valueRange: [1,10000],
                            labels: ['Time', 'Gallons']
                          });

   

  }

  
  function draw_graph( data )
  {
       var i;
       var graph_data;
       var x;
       var limit;
       var limit_std;
       var limit_std_hi;
       var limit_std_low
       
       graph_data = [];
       
       var t = new Date(data.time*1000);
 
       


          for( i = data.data.length-1; i >= 0; i--  )
          {
	  
          
             var x = new Date(data.data[i][0]*1000);

            graph_data.push([x,data.data[i][1]*conversion_factor ]);
	    
	  }
          strip_chart_update( graph_data );
      
       
   }

  function filter_graph_data(data)
  {
     initialize_flow_graph()
      
       draw_graph( data );
       
    
  }




  function generate_graph()
   {
 

            json_object = {}
            json_object.schedule = $("#Flow_Schedule").val()
            json_object.step = $("#Flow_Step").val()
	    json_object.flow_sensor = $("#Flow_Flow_Sensor").val()

            json_string = JSON.stringify(json_object);
            $.ajax
            ({
                    url: '/ajax/get_total_flow_data.html',
	            type: "GET",
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    data: json_string,
                    success: filter_graph_data,
                    error: function () 
		    {
		      
                       alert('/ajax/get_total_flow_data.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })

   }    
    
/*
 * 
*/


  
   
     
/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------
Build Index Select
*/






   
/*
----------------------------------------------------------------------------------------------------------------------------------------------------------------
Build Schedule
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

     $("#Flow_Schedule" ).bind( "change", function(event, ui)
     {
        build_step_list( $step,schedules_step,$("#Flow_Schedule").val())
	localStorage.setItem("db_schedule_current",$("#Flow_Schedule")[0].selectedIndex);

	generate_graph()
     });
     
     
      $("#Flow_Step").bind("change", function(event,ui)
     {
       
       localStorage.setItem("db_step",$("#Flow_Step")[0].selectedIndex);

       generate_graph()
     });
      

    function generate_description( index , schedule_name)
    {
      var temp_string;
      var temp_index
      temp_index = index;
      index = index -1
      temp_string = "step "+temp_index+" controller/pins  --->";
      for( i = 0; i < schedules_pins[schedule_name][index].length;i++)
      {
	temp_string = temp_string + "   "+ schedules_pins[schedule_name][index][i];
 	
      }
      return temp_string;
    }   
   
   
     function build_step_list( element,count_dictionary,key)
     {   
          
          var i
          var limit = count_dictionary[key]
          var temp;
          limit = limit.length;
          element.empty()
          for( i= 1; i < limit+1; i++ )
          {
	    temp =generate_description( i , key)
            element.append('<option value='+(i-1)+'>Select Step --------->  '+temp+'</option>');	
          }
          element.selectedIndex = 0;
	  element.selectmenu();
          element.selectmenu("refresh");
     }
 
     function  build_choice_list( element, element_list )
     {
          element.empty();
          $.each(element_list, function(index, value) 
                     {  
		        if( index == 0 )
                        {
                           
                           //<option selected value=1>1</option>
                          element.append("<option selected value="+value+">Select Schedule ----------------> "+value+ "</option>")
                        }
                        else
                        {
			 
			  element.append("<option value="+value+">Select Schedule ---------->  " + value + "</option>");
                        }
		     });
          element.selectedIndex = 0;
	  element.selectmenu();
          element.selectmenu("refresh");
     }

  function build_schedule()
  {
        $.getJSON('/ajax/schedule_data.html', function(data) 
	{
          for (var i = 0; i < data.length; i++) 
          {
	     
	     schedules.push(data[i].name)
	     schedules_step[data[i].name]            = data[i].steps
             schedules_start_times[data[i].name]     = data[i].start_time
             schedules_end_times[data[i].name]       = data[i].end_time   
             schedules_dow[data[i].name]             = data[i].dow
             schedules_pins[data[i].name]            = data[i].controller_pins   
          }

           build_choice_list( $schedule, schedules ) 
	   if( localStorage.getItem("db_schedule_current") != null )
	   {
	         $schedule[0].selectedIndex = localStorage.getItem("db_schedule_current")
	   }
	   else
	   {
	       $schedule[0].selectedIndex = 0
	   }
	   $schedule.selectmenu();
	   $schedule.selectmenu("refresh")
	   build_step_list( $step,schedules_step,$("#Flow_Schedule").val())
	   if( localStorage.getItem("db_step") != null )
	   {
	       $step[0].selectedIndex = localStorage.getItem("db_step")
	   }
	   else
	   {
	      $step[0].selectedIndex = 0
	   }
	   $step.selectmenu();
	   $step.selectmenu("refresh")
           generate_graph();
        });
	

  }
 
  
   
   
   
/*
----------------------------------------------------------------------------------------------------------------------------------------------------------------
Flow Sensor Stuff
----------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

  $("#Flow_Flow_Sensor" ).bind( "change", function(event, ui)
  {
       

       ref_flow_meter = $("#Flow_Flow_Sensor")[0].selectedIndex;
       conversion_factor_index = $("#Flow_Flow_Sensor")[0].selectedIndex;
       
       conversion_factor = conversion_factor_array[ conversion_factor_index ];
       generate_graph()
       
  });

   function flow_sensor_success( data )
     {
          var length;
          var i;
	  var flow_meter
	  
	  flow_meter = $("#Flow_Flow_Sensor");
          length = data.length;
          flow_meter.empty()
          ref_flow_meter = 0;
	  conversion_factor_array = []
	 
          for( i= 0; i < length; i++ )
          {
	    
            flow_meter.append('<option value='+data[i][0]+'>Select Flow Sensor ------>  '+data[i][0]+'</option>');
	    conversion_factor_array.push(data[i][1])
          }
         
          conversion_factor_index = 0;
	  conversion_factor = conversion_factor_array[ conversion_factor_index ];
	  
          flow_meter.selectedIndex = 0;
	  flow_meter.selectmenu();
          flow_meter.selectmenu("refresh");
     
       
       
     }
     
  function flow_sensor_request()
  {
      
     
            $.ajax
            ({
                    url: '/ajax/get_flow_sensor_name.html',
	            type: "GET",
                    dataType: 'json',
	            contentType: "application/json",
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: flow_sensor_success,
                    error: function () 
		    {
		      
                       alert('/ajax/get_flow_sensor_name.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
  }

 flow_sensor_request();
 build_schedule();
}) 
