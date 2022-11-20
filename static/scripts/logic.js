
        function form_handler(event)
        {
            event.preventDefault();
        }
         function send_data()
         {
            document.querySelector('form').addEventListener("submit",form_handler);
            var fd=new FormData(document.querySelector('form'));
            var xhr=new XMLHttpRequest({mozSystem:true});
            xhr.open('POST','/predict',true);
            document.getElementById("prediction").innerHTML="Wait Predicting Price!...";
            // console.log(xhr.responseText);
            xhr.onreadystatechange = function(){
              // console.log(xhr.responseText);
        
                if(xhr.readyState==XMLHttpRequest.DONE){
                  // console.log(67);
                  console.log(typeof(xhr.responseText));
                  console.log(xhr.responseText);
                  var str=xhr.responseText;
                   
                    document.getElementById('prediction').innerHTML="Prediction: Rs."+str;
                      // document.getElementById('prediction').innerHTML=xhr.responseText;
                }
            };
            xhr.onload =function(){};
            xhr.send(fd);
         }
        

    