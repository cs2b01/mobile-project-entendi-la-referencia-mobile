    var category_id;
    $.getJSON("/current_category", function(data){
                category_id = data['id']
        });
    $.getJSON("/current", function(data){
          if(data==null){
          window.location.href="http://3.130.238.73/dologin"
         }
          else{uploads = data['uploads']}
        });


    function Enviar(){
            $.ajax({
                url: 'http://3.130.238.73/questions',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                     "statment": $('#statment').val(),
                     "answer":$('#answer').val(),
                     "wrong1":$('#wrong1').val(),
                     "wrong2":$('#wrong2').val(),
                     "wrong3":$('#wrong3').val(),
                     "category_id":category_id
                }),
                dataType: 'json',
                success: function(response){
                    AumentoUploads();
                window.location.href="http://3.130.238.73/gracias"
                },
                error: function(response){
                if(response['status']==401){
                }
                 else{
                 AumentoUploads();
                window.location.href="http://3.130.238.73/gracias"
                  }}
            });
        }
        function AumentoUploads() {
            $.ajax({
                url: 'http://3.130.238.73/users',
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({
                     "uploads":(uploads+1)
                }),
                dataType: 'json'
            });
        }
