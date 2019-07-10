$.getJSON("/current", function(data){
   if(data==null){
   window.location.href="http://3.130.238.73/dologin"
      }
   else{record = data['record']}
        });



const esperar = 3500,
  random = 1000,
  extra = 2000,
  pregunta = 8000,
  resultado = 2000,
  cantidad = 5,
  sprite_inicial = 0;

let c = document.getElementById("app");
let ctx = c.getContext("2d");
let elemento = [
  document.getElementById("fondo0"),
  document.getElementById("fondo1"),
  document.getElementById("fondo2"),
  document.getElementById("fondo3"),
  document.getElementById("fondo4")
];
let cuadro = document.getElementById("pregunta");
let mal = document.getElementById("mal");
let bien = document.getElementById("bien");
let error = document.getElementById("error");
let i = sprite_inicial,
  max = cantidad - 1;
let spins,
  tiempo_frame,
  tiempo_anterior,
  tiempo_anterior_e,
  tiempo_anterior_ex,
  tiempo_anterior_pr,
  tiempo_anterior_rs;
let tiempo_espera,
  tiempo_espera_extra,
  tiempo_espera_pregunta,
  tiempo_espera_resultado;
let w = 0,
  h = 0;

let rodar = true,
  preguntar = false,
  corregir = false,
  correcta = false,
  con_pregunta = true;
let statment;
let respuesta_orden = [0, 1, 2, 3];
let respuestas_texto = ["", "", "", ""];

function escribir_texto(t, f, s, i, j) {
  ctx.font = f + "px " + s;
  ctx.fillStyle = "white";
  let x = (i * window.innerWidth) / 1600;
  let y = (j * window.innerHeight) / 900;
  ctx.fillText(t, x, y);
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function establecer_pregunta(r) {
  statment = r.statment;
  respuestas_texto[0] = r.answer;
  respuestas_texto[1] = r.wrong1;
  respuestas_texto[2] = r.wrong2;
  respuestas_texto[3] = r.wrong3;
  shuffleArray(respuesta_orden);
}

function siguiente_pregunta() {
  let id_ = JSON.stringify({ "id": (i+1) });
  $.ajax({
    url: "/set_category_and_random_question",
    type: "POST",
    contentType: "application/json",
    data: id_,
    dataType: "json",
      success: function(response) {
      establecer_pregunta(response);
    },
    error: function(response) {
      con_pregunta = false;
    }
  });
  let ejemplo = {
    statment: "Hola",
    answer: "esta es la respuesta",
    wrong1: "esta es wrong 1",
    wrong2: "esta es wrong 2",
    wrong3: "esta es wrong 3"
  };
}

function tiempo_aleatorio() {
  tiempo_espera = esperar + Math.random() * random;
  tiempo_espera_extra = extra + tiempo_espera;
  tiempo_espera_pregunta = pregunta + tiempo_espera_extra;
  tiempo_espera_resultado = resultado + tiempo_espera_pregunta;
  tiempo_frame = 0;
  spins = 0;
}

function start() {
  tiempo_aleatorio();
  requestAnimationFrame(loop);
}

function siguiente_sprite() {
  if (i < max) {
    i = i + 1;
  } else {
    i = 0;
  }
}

function actualizar_elemento(tiempo) {
  if (!tiempo_anterior) {
    tiempo_anterior = tiempo;
    tiempo_anterior_e = tiempo;
    tiempo_anterior_ex = tiempo;
    tiempo_anterior_pr = tiempo;
    tiempo_anterior_rs = tiempo;
  }
  if (rodar) {
    if (tiempo - tiempo_anterior > tiempo_frame) {
      siguiente_sprite();
      spins += 0.1;
      tiempo_anterior = tiempo;
      tiempo_frame = spins * spins;
    }
    if (tiempo - tiempo_anterior_e > tiempo_espera) {
      rodar = false;
    }
  } else {
    if (!preguntar) {
      if (tiempo - tiempo_anterior_ex > tiempo_espera_extra) {
        preguntar = true;
        siguiente_pregunta();
      }
    } else {
      if (!corregir) {
        if (tiempo - tiempo_anterior_pr > tiempo_espera_pregunta) {
          corregir = true;
        }
      } else {
        if (tiempo - tiempo_anterior_rs > tiempo_espera_resultado) {
          tiempo_anterior = tiempo;
          tiempo_anterior_e = tiempo;
          tiempo_anterior_ex = tiempo;
          tiempo_anterior_pr = tiempo;
          tiempo_anterior_rs = tiempo;
          tiempo_aleatorio();
          rodar = true;
          preguntar = false;
          corregir = false;
          correcta = false;
          con_pregunta = true;
        }
      }
    }
  }
}

function borrar() {
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
}

function restablecer_escalado() {
  var widthToHeight = 16 / 9;
  var newWidth = window.innerWidth;
  var newHeight = window.innerHeight;
  var newWidthToHeight = newWidth / newHeight;

  if (newWidthToHeight < widthToHeight) {
    newWidth = newHeight * widthToHeight;
  } else {
    newHeight = newWidth / widthToHeight;
  }
  w = newWidth;
  h = newHeight;
  c.width = newWidth;
  c.height = newHeight;
}

function dibujar(e) {
  ctx.drawImage(e, 0, 0, w, h);
}

function loop(tiempo) {
  actualizar_elemento(tiempo);
  borrar();
  restablecer_escalado();
  dibujar(elemento[i]);
  if (preguntar) {
    if (con_pregunta) {
      if (!corregir) {
        dibujar(cuadro);
        escribir_texto(statment, "25", "Arial", 420, 200);
        escribir_texto(
          respuestas_texto[respuesta_orden[0]],
          "30",
          "Arial",
          445,
          520
        );
        escribir_texto(
          respuestas_texto[respuesta_orden[1]],
          "30",
          "Arial",
          445,
          630
        );
        escribir_texto(
          respuestas_texto[respuesta_orden[2]],
          "30",
          "Arial",
          445,
          740
        );
        escribir_texto(
          respuestas_texto[respuesta_orden[3]],
          "30",
          "Arial",
          445,
          890
        );
        /*escribir_texto(
          respuestas_texto['a'],
          "50",
          "Arial",
          1000,
          400
        );*/
      } else {
        if (correcta) {
          dibujar(bien);
        } else {
          dibujar(mal);
        }
      }
    } else {
      dibujar(error);
    }
  }
  requestAnimationFrame(loop);
}

function añadir_puntos() {
  $.ajax({
    url: "/users",
    type: "PUT",
    contentType: "application/json",
    data: JSON.stringify({
      "record": (record + 1)
    }),
    dataType: "json"
  });
}

function corregir_respuesta(r) {
  if (r) {
    r = r - 49;
    if (respuesta_orden[r] === 0) {
      correcta = true;
      añadir_puntos();
    }
    tiempo_espera_pregunta = 0;
  }
}

document.addEventListener("keydown", event => {
  if (preguntar && con_pregunta && !corregir) {
    if (event.keyCode < 53 && event.keyCode > 48) {
      corregir_respuesta(event.keyCode);
    }
  }
});

start();
