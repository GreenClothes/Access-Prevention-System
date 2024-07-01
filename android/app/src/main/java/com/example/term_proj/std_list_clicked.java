package com.example.term_proj;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

public class std_list_clicked extends Activity {

    private int img;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        /* xml과 연결 */
        setContentView(R.layout.std_list_clicked);

        Intent intent = getIntent();

        ImageView photo = (ImageView) findViewById(R.id.std_photo);
        TextView name=(TextView) findViewById(R.id.std_name);
        TextView grade=(TextView) findViewById(R.id.std_grade);
        TextView times=(TextView) findViewById(R.id.std_times);
        TextView spot=(TextView) findViewById(R.id.std_spot);

        img=Integer.parseInt(intent.getStringExtra("photo"));
        photo.setImageResource(img);
        name.setText(intent.getStringExtra("name"));
        grade.setText(intent.getStringExtra("grade"));
        times.setText(intent.getStringExtra("times"));
        spot.setText(intent.getStringExtra("spot"));

    }
}