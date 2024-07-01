package com.example.term_proj;

public class searchingarea_item {
    private String stringspot; // 수색 구역
    private String stringname; // 담당 교직원 목록
    private String stringphone; // 대표자 연락처

    public void setSpot(String spot){
        stringspot = spot;
    }

    public void setName(String name){
        stringname = name;
    }

    public void setPhone(String phone){
        stringphone = phone;
    }

    public String getSpot(){
        return this.stringspot;
    }
    public String getName(){
        return this.stringname;
    }
    public String getPhone(){
        return this.stringphone;
    }
}