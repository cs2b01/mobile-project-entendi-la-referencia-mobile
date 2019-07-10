$.getJSON("/current", function(data){
         if(data==null){
          window.location.href="http://3.130.238.73/dologin"
         }
             });

$.getJSON("/current", function(data){
    document.getElementById("username").value = data['username'];
    document.getElementById("name").value = data['name'];
    document.getElementById("lastname").value = data['lastname'];
    document.getElementById("password").value = data['password'];});

function Actualizar(){
            $('#success').show();
            $.ajax({
                url: 'http://3.130.238.73/users',
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({
                     "username":  $('#username').val(),
                     "name":  $('#name').val(),
                     "lastname":  $('#lastname').val(),
                     "password":  $('#password').val()
                }),
                dataType: 'json',
                success: function(response){
                    $('#success').show();
                },
            error: function(response){
                if(response['status']==401){}
                 else{
                 window.location.href="http://3.130.238.73/main_menu"
                  }}
            });
        }

function Borracuenta(){
                $.ajax({
                url: 'http://3.130.238.73/users',
                type: 'DELETE',
                success: function(response){
                    window.location.href="http://3.130.238.73/dologin"
                },
            error: function(response){
                if(response['status']==401){}
                 else{
                window.location.href="http://3.130.238.73/dologin"
                  }}
            });

}
