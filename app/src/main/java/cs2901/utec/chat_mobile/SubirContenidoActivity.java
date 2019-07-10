package cs2901.utec.chat_mobile;

import android.app.Activity;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class SubirContenidoActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_subir_contenido);
    }
    public Activity getActivity(){
        return this;
    }

    public void Enviarpregunta(View v) {
        Enviar();
    }


    public void showMessage(String message) {
        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
    }

    public void Enviar(){
        final String id_user = getIntent().getExtras().get("user_id").toString();
        final EditText statment = (EditText) findViewById(R.id.statment);final EditText answer = (EditText) findViewById(R.id.answer);final EditText wrong1 = (EditText) findViewById(R.id.wrong1);final EditText wrong2 = (EditText) findViewById(R.id.wrong2);final EditText wrong3 = (EditText) findViewById(R.id.wrong3);
        final RadioButton marvel= (RadioButton)findViewById(R.id.Marvel);
        final RadioButton star_wars= (RadioButton)findViewById(R.id.StarWars);
        final RadioButton anime= (RadioButton)findViewById(R.id.Anime);
        final RadioButton deportes= (RadioButton)findViewById(R.id.Deportes);
        final RadioButton memes= (RadioButton)findViewById(R.id.Memes);

        String STATMENT = statment.getText().toString();
        String ANSWER = answer.getText().toString();
        String WRONG1 = wrong1.getText().toString();
        String WRONG2 = wrong2.getText().toString();
        String WRONG3 = wrong3.getText().toString();

        Map<String, String> message = new HashMap<>();
        message.put("statment", STATMENT);
        message.put("answer", ANSWER);
        message.put("wrong1", WRONG1);
        message.put("wrong2", WRONG2);
        message.put("wrong3", WRONG3);

        // 3. Converting the message object to JSON string (jsonify)
        JSONObject jsonMessage = new JSONObject(message);

        // 4. Sending json message to Server

        String id_question="1";

        if(marvel.isChecked()){
            id_question="1";
        }
        else if(star_wars.isChecked()){
            id_question="2";
        }
        else if(anime.isChecked()){
            id_question="3";
        }
        else if(deportes.isChecked()){
            id_question="4";
        }
        else if(memes.isChecked()){
            id_question="5";
        }
        String url = "http://3.130.238.73/questions_mobile/<xid>";
        String url2 = "http://3.130.238.73/subir_upload/<xid>";
        url = url.replace("<xid>",id_question);
        url2 = url2.replace("<xid>",id_user);
        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                url,
                jsonMessage,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        //TODO
                        try{
                            String message = response.getString("message");
                            if(message.equals("Authorized")) {
                                statment.setText("");answer.setText("");wrong1.setText("");wrong2.setText("");wrong3.setText("");
                                marvel.setChecked(false); star_wars.setChecked(false);deportes.setChecked(false); anime.setChecked(false);memes.setChecked(false);
                           }
                            else {
                            }
                        }catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        error.printStackTrace();
                        if( error instanceof AuthFailureError){
                        }
                        else {
                        }
                    }
                }
        );

        JsonObjectRequest request2 = new JsonObjectRequest(
                Request.Method.PUT,
                url2,
                null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response2) {
                        //TODO
                        try{
                            String message2 = response2.getString("message");
                            if(message2.equals("Authorized")) {
                                showMessage("Éxito");
                           }
                            else {
                            }
                        }catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        error.printStackTrace();
                        if( error instanceof AuthFailureError){
                        }
                        else {
                        }
                    }
                }
        );


       RequestQueue queue = Volley.newRequestQueue(this);
        queue.add(request);
        queue.add(request2);




    }

}
