package cs2901.utec.chat_mobile; //AQUI FALTA CAMBIAR POR OTRO NOMBRE DE PROYECTO

import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;

import android.support.v7.app.AppCompatActivity;
import java.util.ArrayList;
public class Jugar_x extends AppCompatActivity {
    //Fondo
    private static Integer[] secciones =
            {R.drawable.m_spin_anime, R.drawable.m_spin_futbol,
                    R.drawable.m_spin_marvel, R.drawable.m_spin_meme};
    private int seccion = 0;
    private static int max_seccion = 3;
    private RelativeLayout fondo;
    private static Integer[] resultados =
            {R.drawable.m_error, R.drawable.m_wrong, R.drawable.m_check};

    //Texto y botones
    private TextView txtPreg;
    private ArrayList<Button> btnResp = new ArrayList<>();


    //Bucle recursivo
    private Handler handler = new Handler();
    private Runnable runnable;
    private int delay = 100; //Un ciclo de reloj en milisegundos

    //Giro
    private int ciclosGiro = 0;
    private static int max_ciclosGiro = 30;

    //Pregunta
    private String pregunta;
    private String[] alternativas = {"", "", "", ""};
    private Integer[] orden = {1, 0, 2, 3};
    private static int alternativa_correcta = 0; //Índice de la respuesta correcta
    private boolean no_en_pregunta = true;

    //Resultado
    private int ciclosResultado = 0;
    private static int max_ciclosResultado = 30;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_jugar_x);
        Obtener_elementos();
        Anadir_accion_btn();
        Comenzar_juego();
    }

    private void Obtener_elementos(){
        fondo = findViewById(R.id.bg);
        txtPreg = findViewById(R.id.preg);
        Button btn0 = findViewById(R.id.button);
        Button btn1 = findViewById(R.id.bB);
        Button btn2 = findViewById(R.id.bC);
        Button btn3 = findViewById(R.id.bD);
        btnResp.add(btn0);
        btnResp.add(btn1);
        btnResp.add(btn2);
        btnResp.add(btn3);
    }

    private void Comenzar_juego(){
        ciclosGiro = max_ciclosGiro;
        ciclosResultado = max_ciclosResultado;
        Ocultar_pregunta();
        Dibujar_fondo(seccion);
        onResume();
    }

    private void Anadir_accion_btn(){
        btnResp.get(0).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Responder_pregunta(0);
            }
        });
        btnResp.get(1).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Responder_pregunta(1);
            }
        });
        btnResp.get(2).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Responder_pregunta(2);
            }
        });
        btnResp.get(3).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Responder_pregunta(3);
            }
        });

    }


    //EN ESTA FUNCION FALTA UN AJAX Y UN RANDOM
    private void Obtener_pregunta(){

        //AJAX GET: pregunta y alternativas
        //Qué valor le corresponde a cada categoría lo determina el servidor
        //En esta versión no se muestra un fondo correspondiente a la categoría
        //Por lo que no necesitamos saber la categoría

        onPause();
        int random = (int) (Math.random() * (4)); //RANDOM de 0 a 4

        pregunta = "Ejemplo";
        alternativas[0] = "Respuesta correcta";
        alternativas[1] = "Respuesta incorrecta";
        alternativas[2] = "Respuesta incorrecta";
        alternativas[3] = "Respuesta incorrecta";
        Mostrar_pregunta(); //Si el servidor responde
        //Mostrar_resultado(0); //Si el servidor no responde
    }

    private void Mostrar_resultado(int i){
        fondo.setBackgroundResource(resultados[i]);
        Ocultar_pregunta();
        no_en_pregunta = true;
        onResume();
    }

    private void Ocultar_pregunta(){
        txtPreg.setVisibility(View.INVISIBLE);
        for(Button btn : btnResp){
            btn.setVisibility(View.INVISIBLE);
        }
    }

    private void Mostrar_pregunta(){
        Reordenar_alternativas();
        no_en_pregunta = false;
        txtPreg.setVisibility(View.VISIBLE);
        txtPreg.setText(pregunta);
        int i = 0;
        for(Button btn : btnResp){
            btn.setVisibility(View.VISIBLE);
            btn.setText(alternativas[orden[i]]);
            i++;
        }
    }

    private void Reordenar_alternativas(){
        ArrayList<Integer> temp = new ArrayList<>();
        temp.add(0);
        temp.add(1);
        temp.add(2);
        temp.add(3);
        int random;
        for (int i = 0; i<4; i++){
            random = (int) (Math.random() * (3-i)); //RANDOM de 0 a (3-i)
            orden[i] = temp.get(random);
            temp.remove(random);
        }
    }


    //EN ESTA FUNCION FALTA UN AJAX
    private void Responder_pregunta(int seleccionado){
        if(orden[seleccionado] == alternativa_correcta){
            //AJAX POST
            Mostrar_resultado(2);
        }else{
            Mostrar_resultado(1);
        }
    }

    private void Dibujar_fondo(int i){
        fondo.setBackgroundResource(secciones[i]);
    }

    private void Seleccionar_siguiente_seccion(){
        if(seccion<max_seccion){
            seccion++;
        }else{
            seccion = 0;
        }
        Dibujar_fondo(seccion);
    }

    @Override
    protected void onResume() {
        handler.postDelayed( runnable = new Runnable() {
            public void run() {
                if(no_en_pregunta){
                    if(ciclosGiro>0){
                        Seleccionar_siguiente_seccion();
                        ciclosGiro--;
                        if(ciclosGiro==0){
                            Obtener_pregunta();

                        }
                    }else{
                        if(ciclosResultado>0){
                            ciclosResultado--;
                        }else{
                            ciclosResultado = max_ciclosResultado;
                            ciclosGiro = max_ciclosGiro;
                        }
                    }
                }
                handler.postDelayed(runnable, delay);
            }
        }, delay);

        super.onResume();
    }

    @Override
    protected void onPause() {
        handler.removeCallbacks(runnable);
        super.onPause();
    }
}