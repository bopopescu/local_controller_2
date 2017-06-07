$(document).ready(
 function()
 {
   var g_flow;
   var strip_chart_update;
   var g_flow_1;
   var strip_chart_update_1;
   var g_flow_2;
   var strip_chart_update_2;
   var schedules = []
   var schedules_step = {}
   var schedules_start_times = {}
   var schedules_end_times = {}
   var schedules_dow = {}
   var schedules_pins = {}
   var ref_flow_meter;
   var conversion_factor_array;
   var conversion_factor_index;
   var conversion_factor;

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
   
   
  var initialize_flow_graph = function()
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
                            drawPoints: true,
                            showRoller: true,
                            valueRange: [0,40],
                            labels: ['Time', 'GPM']
                          });

     strip_chart_update = function(data)
     {
        g_flow.updateOptions( { 'file': data } );
      }





  }

   var flow = function()
   {

 
     var $flow_sensor = $("#Flow_Flow_Sensor");
     var $schedule = $("#Flow_Schedule");
     var $step = $("#Flow_Step");
     
     



     var build_step_list = function( element,count_dictionary,key)
     {   
          
          var i
          var limit = count_dictionary[key]
          var temp;
          limit = limit.length;
          element.empty()
          for( i= 1; i < limit+1; i++ )
          {
	    temp =generate_description( i , key)
            element.append('<option value='+i+'>'+temp+'</option>');	
          }
          element.selectedIndex = 0;
	  element.selectmenu();
          element.selectmenu("refresh");
     }
 
     var build_choice_list = function( element, element_list )
     {
          element.empty();
          $.each(element_list, function(index, value) 
                     {  
		        if( index == 0 )
                        {
                           
                           //<option selected value=1>1</option>
                          element.append("<option selected value="+value+"> "+value+ "</option>")
                        }
                        else
                        {
			  element.append("<option> " + value + "</option>");
                        }
		     });
          element.selectedIndex = 0;
	  element.selectmenu();
          element.selectmenu("refresh");
     }

     function generate_graph( data )
     {
       var i;
       var graph_data;
       graph_data = [];
       //alert(JSON.stringify(data))
       for( i = 0; i< data.length; i++ )
       {
	  var x = new Date(0);
          x.setUTCSeconds(data[i][0]);
          graph_data.push([x,data[i][1]*conversion_factor ]); 
	 
       }
       strip_chart_update( graph_data );
       
     }
     $("#graph_flow").click(function()
     {
         var data
        data = {}
        data["sensor"] =  $("#Flow_Flow_Sensor").val()
	
        data["schedule"] = $("#Flow_Schedule").val()
        data["step"] = $("#Flow_Step").val()
        data["days"] = $("#Flow_Relative_Day").val()
        $.getJSON('/ajax/get_flow_data.html',data, generate_graph )
     });
     
     var init_data = function()
     {
        $.getJSON('/ajax/graph_flow_set_up.html', function(data) 
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
	   $schedule[0].selectedIndex = localStorage.getItem("db_schedule_current")
	   $schedule.selectmenu();
	   $schedule.selectmenu("refresh")
	   build_step_list( $step,schedules_step,$("#Flow_Schedule").val())
	   $step[0].selectedIndex = localStorage.getItem("db_step")
	   $step.selectmenu();
	   $step.selectmenu("refresh")

        });
	

     }
    
     $("#Flow_Schedule" ).bind( "change", function(event, ui)
     {
        build_step_list( $step,schedules_step,$("#Flow_Schedule").val())
	localStorage.setItem("db_schedule_current",$("#Flow_Schedule")[0].selectedIndex);
     });
     
     
      $("#Flow_Step").bind("change", function(event,ui)
     {
       
       localStorage.setItem("db_step",$("#Flow_Step")[0].selectedIndex);
     
     });
      
     
 
     initialize_flow_graph()
     init_data()
     //
  }				
  
  $("#Flow_Flow_Sensor" ).bind( "change", function(event, ui)
  {

       ref_flow_meter = $("#Flow_Flow_Sensor")[0].selectedIndex +1;
       conversion_factor_index = $("#Flow_Flow_Sensor")[0].selectedIndex;
       
       conversion_factor = conversion_factor_array[ conversion_factor_index ];
      
       
  });

  flow() // initialize flow tab
  
   function flow_sensor_success( data )
     {
          var length;
          var i;
	  var flow_meter
	  
	  flow_meter = $("#Flow_Flow_Sensor");
          length = data.length;
          flow_meter.empty()
          ref_flow_meter = 1;
	  conversion_factor_array = []
	 
          for( i= 0; i < length; i++ )
          {
	    
            flow_meter.append('<option value='+data[i][0]+'>'+data[i][0]+'</option>');
	    conversion_factor_array.push(data[i][1])
          }
         
          conversion_factor_index = 0;
	  conversion_factor = conversion_factor_array[ conversion_factor_index ];
	  
          flow_meter.selectedIndex = 0;
	  flow_meter.selectmenu();
          flow_meter.selectmenu("refresh");
     
       
       
     }
     
  var flow_sensor_request = function()
  {
      
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/flow_sensor/get/flow_sensor_name.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: flow_sensor_success,
                    error: function () 
		    {
		      
                       alert('/ajax/flow_sensor/get/flow_sensor_name.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
  }
 flow_sensor_request();
})




