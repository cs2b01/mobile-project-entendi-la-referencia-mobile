package cs2901.utec.chat_mobile;
import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.SimpleItemAnimator;
import android.view.View;
import android.widget.EditText;
import java.lang.Thread;
import java.lang.*;
import java.lang.Object;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import android.support.v7.widget.RecyclerView.ItemAnimator;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MessageActivity extends AppCompatActivity{
    RecyclerView mRecyclerView;
    RecyclerView.Adapter mAdapter;
     int contador=0;
    public Activity getActivity(){
        return this;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_message);
        String username = getIntent().getExtras().get("username").toString();
        setTitle("Chat con "+username);
        mRecyclerView = findViewById(R.id.main_recycler_view);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
    }

    @Override
    protected void onResume(){
        super.onResume();
        getChats();
        Runnable runnable = new Runnable() {
            @Override
            public void run() {
                while (true) {
                  try {Thread.sleep(1000); getChats(); }
                catch (InterruptedException e) { e.printStackTrace(); }
                }
            }
        };
        Thread hilo = new Thread(runnable);
        hilo.start();
    }

    public void onClickBtnSend(View v) {
        postMessage();
    }

    public void getChats(){
        final String userFromId = getIntent().getExtras().get("user_from_id").toString();
        String userToId = getIntent().getExtras().get("user_to_id").toString();
        String url = "http://192.168.1.8:8080/chats/<user_from_id>/<user_to_id>";
        final int uID = Integer.parseInt(userFromId);
        url = url.replace("<user_from_id>", userFromId);
        url = url.replace("<user_to_id>", userToId);
        RequestQueue queue = Volley.newRequestQueue(this);
        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            JSONArray data = response.getJSONArray("response");
                            if(contador==0){
                            mAdapter = new MyMessageAdapter(data, getActivity(), uID); contador+=1;
                            mRecyclerView.setAdapter(mAdapter);
                            mRecyclerView.smoothScrollToPosition(mRecyclerView.getAdapter().getItemCount());
                            }
                            else{
                                if(mAdapter.getItemCount()!=data.length()){
                                    mAdapter = new MyMessageAdapter(data, getActivity(), uID);
                                    mRecyclerView.setAdapter(mAdapter);
                                    mAdapter.notifyDataSetChanged();
                                    mRecyclerView.smoothScrollToPosition(mRecyclerView.getAdapter().getItemCount());
                                    }}
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

    public void postMessage(){
        String url = "http://192.168.1.8:8080/messages";
        RequestQueue queue = Volley.newRequestQueue(this);
        Map<String, String> params = new HashMap();
        final String user_from_id = getIntent().getExtras().get("user_from_id").toString();
        final String user_to_id = getIntent().getExtras().get("user_to_id").toString();
        final String content = ((EditText)findViewById(R.id.txtMessage)).getText().toString();
        params.put("user_from_id",user_from_id);
        params.put("user_to_id", user_to_id);
        params.put("content", content);
        JSONObject parameters = new JSONObject(params);
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.POST,
                url,
                parameters,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // TODO
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                // TODO: Handle error
                error.printStackTrace();

            }
        });
        queue.add(jsonObjectRequest);
        EditText editText = (EditText)findViewById(R.id.txtMessage);
        editText.setText("");
    }


}