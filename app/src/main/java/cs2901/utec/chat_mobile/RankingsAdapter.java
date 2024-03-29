package cs2901.utec.chat_mobile;

import android.content.Context;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RelativeLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


public class RankingsAdapter extends RecyclerView.Adapter<RankingsAdapter.ViewHolder> {
    public JSONArray elements;
    private Context context;

    public RankingsAdapter(JSONArray elements, Context context){
        this.elements = elements;
        this.context = context;
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        TextView first_line, second_line;
        RelativeLayout container;

        public ViewHolder(View itemView) {
            super(itemView);
            first_line = itemView.findViewById(R.id.element_view_first_line);
            second_line = itemView.findViewById(R.id.element_view_second_line);
            container = itemView.findViewById(R.id.element_view_container);
        }
    }

    @NonNull
    @Override
    public RankingsAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.element_view,parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull RankingsAdapter.ViewHolder holder, int position) {
        try {
            JSONObject element = elements.getJSONObject(position);
            String name = element.getString("name")+" "+element.getString("lastname");
            final String username = element.getString("username");
            final String id = element.getString("id");
            holder.first_line.setText(name);
            holder.second_line.setText(username);
            holder.container.setOnClickListener(new View.OnClickListener(){
                @Override public void onClick(View v) {
                    Intent intent = new Intent(context,ProfileActivity.class);
                    intent.putExtra("user_to_id",id);
                    context.startActivity(intent);
                }
            });
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    public int getItemCount() {
        return elements.length();
    }
}