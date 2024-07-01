package com.example.term_proj;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import android.widget.ListView;
import androidx.appcompat.app.AppCompatActivity;

public class searchingArea extends AppCompatActivity {
    ListView listView = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_searching_area);

        searchingarea_adapter adapter;

        adapter = new searchingarea_adapter();

        listView = (ListView) findViewById(R.id.listView_searching);
        listView.setAdapter(adapter);

        adapter.addItem("교내 1층","유재석, 강호동, 이수근, 박명수","유재석 : 010-0000-0000");
        adapter.addItem("교내 2층","강동원, 이병헌, 전지현, 김태희","강동원 : 010-1111-1111");
        adapter.addItem("교내 3층","공유, 현빈, 손예진","공유 : 010-2222-2222");
        adapter.addItem("교내 4층","송혜교, 이도현, 임지연, 박성훈","송혜교 : 010-3333-3333");
        adapter.addItem("교내 건물 외부","박효신, 김범수, 나얼, 이수","박효신 : 010-4444-4444");
        adapter.addItem("교외 시화공단 방향"," 이승기, 정승환, 권진아, 이홍기","이승기 : 010-5555-5555");
        adapter.addItem("교외 배곧 방향","안유진, 장원영, 김채원, 권은비, 최예나","안유진 : 010-6666-6666");
        adapter.addItem("교외 오이도 방향","이상혁, 이민형, 류민석, 최우제, 문현준","이상혁 : 010-7777-7777");
        adapter.addItem("교외 정왕역 방향","김석진, 민윤기, 정호석, 김남준, 박지민, 김태형, 전정국","김석진 : 010-8888-8888");
        adapter.addItem("교외 안산 방향","손흥민, 이강인, 김민재, 황희찬, 박지성","손흥민 : 010-9999-9999");
        adapter.addItem("교내 상황실 담당","교무부장, 유초등교육부장, 중등교육부장, 고등교육부장","교무부장 : 010-1234-1234");


        EditText editTextFilter = (EditText) findViewById(R.id.searchEditText);
        editTextFilter.addTextChangedListener(new TextWatcher() {
            @Override
            public void afterTextChanged(Editable edit){
                String filterText = edit.toString();
                ((searchingarea_adapter)listView.getAdapter()).getFilter().filter(filterText);
            }

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after){

            }
            @Override
            public void onTextChanged(CharSequence charSequence, int start, int before, int count) {

            }

        });
    }
}