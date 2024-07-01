package com.example.term_proj;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import java.util.ArrayList;

public class StudentList extends Activity implements View.OnClickListener {

    private ArrayList<std_list_item> data = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_student_list);

        ListView listView = (ListView) findViewById(R.id.std_listView);

        data = new ArrayList<>();
        std_list_item student1 = new std_list_item(R.drawable.ic_launcher_foreground, "김땡땡", "초 1-1","교출 횟수 : 3회","최근 발견 장소 : 2층 남자 화장실");
        std_list_item student2 = new std_list_item(R.drawable.ic_launcher_foreground, "이땡땡", "중 2-1","교출 횟수 : 1회","최근 발견 장소 : 중 1-2 교실");
        std_list_item student3 = new std_list_item(R.drawable.ic_launcher_foreground, "박땡땡", "유치원 훈민반","교출 횟수 : 3회","최근 발견 장소 :교외(학교 정문)");
        std_list_item student4 = new std_list_item(R.drawable.ic_launcher_foreground, "최땡땡", "고 3-2","교출 횟수 : 5회","최근 발견 장소 : 중 1-2 교실");
        std_list_item student5 = new std_list_item(R.drawable.ic_launcher_foreground, "정땡땡", "초 4-1","교출 횟수 : 2회","최근 발견 장소 : 초 6-1 교실");
        std_list_item student6 = new std_list_item(R.drawable.ic_launcher_foreground, "주땡땡", "중 2-3","교출 횟수 : 1회","최근 발견 장소 : 3층 과학실");
        std_list_item student7 = new std_list_item(R.drawable.ic_launcher_foreground, "장땡땡", "중 1-2","교출 횟수 : 4회","최근 발견 장소 : 2층 음악실");
        std_list_item student8 = new std_list_item(R.drawable.ic_launcher_foreground, "윤땡땡", "전공 1-1","교출 횟수 : 3회","최근 발견 장소 : 고 1-3 교실");
        std_list_item student9 = new std_list_item(R.drawable.ic_launcher_foreground, "손땡땡", "중 1-3","교출 횟수 : 3회","최근 발견 장소 : 2층 놀이파크");
        std_list_item student10 = new std_list_item(R.drawable.ic_launcher_foreground, "한땡땡", "고 1-2","교출 횟수 : 3회","최근 발견 장소 : 4층 심리안정실");
        // 위의 std_list_item과 아래의 data.add에 추가 정보만 입력하면 쉽게 학생 추가 및 수정 가능

        data.add(student1);
        data.add(student2);
        data.add(student3);
        data.add(student4);
        data.add(student5);
        data.add(student6);
        data.add(student7);
        data.add(student8);
        data.add(student9);
        data.add(student10);

        /* 리스트 속의 아이템 연결 */
        std_list_adapter adapter = new std_list_adapter(this, R.layout.students_list, data);
        listView.setAdapter(adapter);

        /* 아이템 클릭시 작동 */
        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView parent, View v, int position, long id) {
                Intent intent = new Intent(getApplicationContext(), std_list_clicked.class);
                /* putExtra의 첫 값은 식별 태그, 뒤에는 다음 화면에 넘길 값 */
                intent.putExtra("photo", Integer.toString(data.get(position).getPhoto()));
                intent.putExtra("name", data.get(position).getName());
                intent.putExtra("grade",data.get(position).getGrade());
                intent.putExtra("times", data.get(position).getTimes());
                intent.putExtra("spot",data.get(position).getSpot());
                startActivity(intent);
            }
        });
    }

    @Override
    public void onClick(View v) {
    }

}



