package cs2901.utec.chat_mobile;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;
public class MenuActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
        TextView editText = (TextView) findViewById(R.id.username_current);
        editText.setText(getIntent().getExtras().get("username").toString());

    }
    @Override
    protected void onResume(){
        super.onResume(); }


    public void Jugar(){
        Intent intent = new Intent(getActivity(), MenuActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public Activity getActivity(){
        return this;
    }


}
