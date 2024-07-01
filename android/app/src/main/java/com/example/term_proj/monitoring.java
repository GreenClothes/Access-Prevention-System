package com.example.term_proj;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class monitoring extends AppCompatActivity {

    private WebView WebView;
    private WebSettings WebSettings;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_monitoring_list);

        WebView = (WebView)findViewById(R.id.webview);
        WebView.setWebViewClient(new WebViewClient());


        //layoutParams.height = 1000; // 원하는 높이 값으로 변경

        WebSettings = WebView.getSettings();
        WebSettings.setUseWideViewPort(true);
        WebSettings.setLoadWithOverviewMode(true);
        WebSettings.setJavaScriptEnabled(true);

        WebView.loadUrl("http://192.168.75.152:8081");
        //192.168.75.152:8081
    }
}