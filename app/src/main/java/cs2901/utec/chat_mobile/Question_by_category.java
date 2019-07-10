package cs2901.utec.chat_mobile;
import android.app.Activity;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONException;
import org.json.JSONObject;

public class Question_by_category extends AppCompatActivity{

    public Activity getActivity(){
        return this;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_question_by_category);
        getQuestion();
    }
    public void getQuestion(){
        final String id = getIntent().getExtras().get("question_id").toString();
        String url = "http://3.130.238.73/get_question_by_id/<xid>";
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
                            TextView statment = (TextView) findViewById(R.id.statmentx);
                            TextView answer = (TextView) findViewById(R.id.answerx);
                            String statment1 = response.getString("statment");
                            String answer1 = response.getString("answer");
                            statment.setText(statment1);
                            answer.setText(answer1);
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