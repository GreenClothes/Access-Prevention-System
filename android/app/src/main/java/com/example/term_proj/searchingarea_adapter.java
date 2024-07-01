package com.example.term_proj;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.TextView;

import java.util.ArrayList;

public class searchingarea_adapter extends BaseAdapter implements Filterable {
    private LayoutInflater inflater;
    private ArrayList<searchingarea_item> data = new ArrayList<searchingarea_item>(); //Item 목록을 담을 배열
    private ArrayList<searchingarea_item> filtereditem = data;
    private int layout;

    Filter listFilter;

    public searchingarea_adapter(){

    }

    @Override
    public int getCount(){
        return filtereditem.size();
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent){
        final int pos = position;
        final Context context = parent.getContext();

        if (convertView == null){
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            convertView = inflater.inflate(R.layout.searchingarea_list,parent,false);
        }
        TextView spot = (TextView) convertView.findViewById(R.id.spot);
        TextView name = (TextView) convertView.findViewById(R.id.name);
        TextView phone = (TextView) convertView.findViewById(R.id.phone);

        searchingarea_item item = filtereditem.get(position);

        spot.setText(item.getSpot());
        name.setText(item.getName());
        phone.setText(item.getPhone());

        return convertView;
    }
    @Override
    public long getItemId(int position){
        return position;
    }

    @Override
    public Object getItem(int position){
        return filtereditem.get(position);
    }

    public void addItem(String spot, String name, String phone){
        searchingarea_item item = new searchingarea_item();

        item.setSpot(spot);
        item.setName(name);
        item.setPhone(phone);

        data.add(item);
    }

    @Override
    public Filter getFilter(){
        if(listFilter == null){
            listFilter = new ListFilter();
        }
        return listFilter;
    }

    private class ListFilter extends Filter {
        @Override
        protected FilterResults performFiltering(CharSequence constraint) {
            FilterResults results = new FilterResults();

            if (constraint == null || constraint.length() == 0){
                results.values = data;
                results.count = data.size();
            }
            else {
                ArrayList<searchingarea_item> itemArrayList = new ArrayList<searchingarea_item>();

                for (searchingarea_item item : data){
                    if (item.getSpot().toUpperCase().contains(constraint.toString().toUpperCase()) ||
                    item.getName().toUpperCase().contains(constraint.toString().toUpperCase()))
                    {
                        itemArrayList.add(item);
                    }
                }
                results.values = itemArrayList;
                results.count = itemArrayList.size();
            }
            return results;
        }
        @Override
        protected void publishResults(CharSequence constraint, FilterResults results){
            filtereditem = (ArrayList<searchingarea_item>) results.values;

            if (results.count > 0){
                notifyDataSetChanged();
            }
            else {
                notifyDataSetInvalidated();
            }
        }
    }
}