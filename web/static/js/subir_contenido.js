$.getJSON("/current", function(data){
         if(data==null){
          window.location.href="http://3.130.238.73/dologin"
         }
             });

var data_images = new Array();
data_images[0] = "/static/images/marvel.jpg";
data_images[1] = "/static/images/starwars.jpg";
data_images[2] = "/static/images/anime.jpg";
data_images[3] = "/static/images/deportes.jpg";
data_images[4] = "/static/images/meme.gif";
var category=1;
var indice=0;

var data_categories= new Array();
data_categories[0]="Marvel";
data_categories[1]="Star Wars";
data_categories[2]="Anime";
data_categories[3]="Deportes";
data_categories[4]="Memes";

function Avanzar() {
    indice=indice+1;
    if(indice>=data_categories.length)
        indice=0;
    category=indice+1;
    $('#imagen').attr("src",data_images[indice]);
    document.getElementById("content").innerText =data_categories[indice];
}

function Retroceder() {
    indice=indice-1;
    if(indice<0)
        indice=data_categories.length-1;
    category=indice+1;
    $('#imagen').attr("src",data_images[indice]);
    document.getElementById("content").innerText =data_categories[indice];
}


function SeleccionarCategoria(){
        var message = JSON.stringify({
                "id": category,
            });

        $.ajax({
            url:'/set_category',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            success: function(response){
                },
            error: function(response){
                if(response['status']==401){
                    }
                 else{
                window.location.href="http://3.130.238.73/subir_pregunta"
                  }}
        });
    }
