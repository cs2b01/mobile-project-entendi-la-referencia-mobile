var uploads="Felicidades. Has subido ";
function Actual() {
    $.getJSON("/current", function (data) {
        if (data == null) {
            window.location.href = "http://3.130.238.73/dologin"
        }
        else {
            var x= data['uploads']+1;
            uploads = uploads + x + " preguntas. Sigue colaborando para obtener más puntos!";
            $('#h1').html(uploads)}
    });
}

function Subir_contenido(){
                window.location.href="http://3.130.238.73/subir_contenido"
    }
function Menu(){
                window.location.href="http://3.130.238.73/main_menu"
    }
