package cs2901.utec.chat_mobile;
import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import java.lang.*;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class ProfileActivity extends AppCompatActivity{

    public Activity getActivity(){
        return this;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
        getInformation();
    }
    public void getInformation(){
        final String id = getIntent().getExtras().get("user_to_id").toString();
        final int uID = Integer.parseInt(id);
        String url = "http://3.130.41.244/user_mobile/<xid>";
        url = url.replace("<xid>", id);
        RequestQueue queue = Volley.newRequestQueue(this);
        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            TextView username = (TextView) findViewById(R.id.username_current);
                            TextView name = (TextView) findViewById(R.id.current);
                            String username1 = response.getString("username");
                            String curent_information= "Nombre: "+response.getString("name")+"\n\nApellido: "+response.getString("lastname")+"\n\nRecord: "+response.getString("record")+"\t\t\t\t\t\t\tUploads: "+response.getString("uploads");
                            username.setText(username1);
                            name.setText(curent_information);
                            username.setVisibility(View.VISIBLE);
                            name.setVisibility(View.VISIBLE);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        error.printStackTrace();
                    }
                }
        );
        queue.add(request);
    }

}