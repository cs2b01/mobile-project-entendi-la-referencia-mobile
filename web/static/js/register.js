function EnviarDatos(){
            $.ajax({
                url: 'http://3.130.238.73/users',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                     "email":  $('#email').val(),
                     "username":  $('#username').val(),
                     "name":  $('#name').val(),
                     "lastname":  $('#lastname').val(),
                           "password":  $('#password').val()
                }),
                dataType: 'json',
                success: function(response){
                window.location.href="http://3.130.238.73/dologin"
                },
            error: function(response){
                if(response['status']==401){
                    $('#Ocupado').show();
                }
                 else{
                window.location.href="http://3.130.238.73/dologin"
                  }}
            });
        }
