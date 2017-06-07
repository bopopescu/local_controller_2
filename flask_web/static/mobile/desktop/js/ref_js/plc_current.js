$(document).ready(

 
 
  function()
  {  var g,h,i
     var alarm_data;
     var  queue_interval_id;
     var  nintervalId;
     var data = [];
     var t = new Date();
     for (var i = 100; i >= 0 ; i--)
     {
        var x = new Date(t.getTime() - i * 60000);
        data.push([x,0]);
     }
     

 
         var hh = new Dygraph(document.getElementById("div_plc"), data,
                          {
                            drawPoints: true,
                            showRoller: true,
                            valueRange: [-.5, 1.0 ],
                            labels: ['Time', 'Current']
                          });
     
     
   
     var strip_chart_update = function(data)
     {
            
	hh.updateOptions( { 'file': data } );

      }



     var ajax_success = function(data)
     {
       var temp
       var temp_1
       var tempDate
       
       tempDate = new Date()
       
 

       temp = data.plc_current_queue;
       temp_2 = [];
       var t = new Date();
       for ( i = temp.length-1; i >= 0 ; i--)
       {
        var x = new Date(t.getTime() - i * 60000);
        temp_2.push([x,Number(temp[i]) ]);
       }

       strip_chart_update( temp_2 )
    
       

     }

     var ajax_request = function()
     {
       
     
            $.ajax
            ({
                    type: "GET",
                    url: '/ajax/recent_plc.html',
                    dataType: 'json',
                    async: false,
                    //json object to sent to the authentication url
                    data: [],
                    success: ajax_success,
                    error: function () 
		    {
		      
                       alert('/ajax/recent_plc.html'+"  Server Error Request Not Successful");
		   
		       
                    }
              })
	  
     }
 
     nintervalId =window.setInterval(ajax_request, 300 );
   

     


     
     // get flow sensors
     ajax_request();
     $("#back").button();
     $("#refresh").bind("click",function(event,ui)
     {
 
       ajax_request();
     });

  

  } )

