package com.example.term_proj;

public class std_list_item {
    private int photo; // 학생 사진
    private String name; // 학생 이름
    private String times; // 교출 횟수
    private String grade; // 학년 반
    private String spot; // 최근 발견 장소

    public int getPhoto() {
        return photo;
    }

    public String getName() {
        return name;
    }
    public String getGrade() {
        return grade;
    }
    public String getTimes() {
        return times;
    }
    public String getSpot() {
        return spot;
    }


    public std_list_item(int photo, String name, String grade, String times, String spot) {
        this.photo = photo;
        this.name = name;
        this.grade = grade;
        this.times = times;
        this.spot = spot;

    }
}