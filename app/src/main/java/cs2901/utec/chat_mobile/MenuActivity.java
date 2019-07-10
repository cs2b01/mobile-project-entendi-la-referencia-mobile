package cs2901.utec.chat_mobile;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.TextView;
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


    public void Jugarx(View v) {
        Jugar();
    }
    public void Jugar(){
        Intent intent = new Intent(getActivity(), Jugar_x.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public void Aprenderx(View v) {
        Aprender();
    }
    public void Aprender(){
        Intent intent = new Intent(getActivity(), Aprender.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public void Rankingsx(View v) {
        Rankings();
    }
    public void Rankings(){
        Intent intent = new Intent(getActivity(), RankingsActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public void Settingsx(View v) {
        Settings();
    }
    public void Settings(){
        Intent intent = new Intent(getActivity(), SettingsActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public void Subircontenidox(View v) {
        Subircontenido();
    }
    public void Subircontenido(){
        Intent intent = new Intent(getActivity(), SubirContenidoActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public Activity getActivity(){
        return this;
    }


}
