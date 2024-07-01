package com.example.term_proj;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;


public class std_list_adapter extends BaseAdapter {
    private LayoutInflater inflater;
    private ArrayList<std_list_item> data; //Item 목록을 담을 배열
    private int layout;

    public std_list_adapter(Context context, int layout, ArrayList<std_list_item> data) {
        this.inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        this.data = data;
        this.layout = layout;
    }

    @Override
    public int getCount() { //리스트 안 Item의 개수를 센다.
        return data.size();
    }

    @Override
    public String getItem(int position) {
        return data.get(position).getName();
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = inflater.inflate(layout, parent, false);
        }
        std_list_item friendsItem = data.get(position);

        //학생 사진
        ImageView profile = (ImageView) convertView.findViewById(R.id.photo);
        profile.setImageResource(friendsItem.getPhoto());

        //학생 이름
        TextView name = (TextView) convertView.findViewById(R.id.name);
        name.setText(friendsItem.getName());

        //학생 학년 반
        TextView grade = (TextView) convertView.findViewById(R.id.grade);
        grade.setText(friendsItem.getGrade());

        //학생 교출 횟수
        TextView times = (TextView) convertView.findViewById(R.id.times);
        times.setText(friendsItem.getTimes());

        //학생 교출 시 최근 발견 장소
        TextView spot = (TextView) convertView.findViewById(R.id.spot);
        spot.setText(friendsItem.getSpot());

        return convertView;
    }
}