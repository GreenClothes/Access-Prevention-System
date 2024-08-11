package com.example.term_proj;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.annotation.NonNull;

import android.app.NotificationManager;
import android.content.Intent;
import android.os.Bundle;
import android.os.Build;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.os.Handler;
import android.os.Looper;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.ByteBuffer;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;


public class MainActivity extends AppCompatActivity {

    private static Button button_sbm;
    private Button button;
    private SocketThread socketThread;
    private ImageView imageView1;
    private TextView textView1;
    PrintWriter sendWriter;
    String sendmsg;
    private Socket socket;


    // 알림 권한 설정 관련
    private PermissionSupport permission;
    // 알림 전송 관련 부분
    private final String DEFAULT = "DEFAULT";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        onClickButtonListener_searchingArea();
        onClickButtonListener_stdlist();
        onClickButtonListener_monitoring();

        imageView1 = findViewById(R.id.main_photo);
        textView1 = findViewById(R.id.school);
        button = findViewById(R.id.alert_btn);

        // 서버와의 소켓 통신을 위한 스레드 생성 및 시작
        socketThread = new SocketThread();
        socketThread.start();

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    sendWriter = new PrintWriter(socket.getOutputStream());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                sendmsg = "end";
                new Thread() {
                    @Override
                    public void run() {
                        super.run();
                        try {
                            sendWriter.println(sendmsg);
                            sendWriter.flush();
                            //message.setText("");
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }.start();
            }
        });

        //createNotification(DEFAULT, 1, "교출 상황 발생!!!!", "현재 교출 상황이 발생했으니 수업 중이지 않은 선생님들께서는 학생을 찾아주시기 바랍니다.", noti_intent);

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // 액티비티가 종료될 때 스레드 중지
        socketThread.interrupt();
    }

    public void onClickButtonListener_stdlist(){
        button_sbm = (Button) findViewById(R.id.student_list_btn);
        button_sbm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent("com.example.term_proj.StudentList");
                startActivity(intent);
            }
        });
    }

    public void onClickButtonListener_searchingArea(){
        button_sbm = (Button) findViewById(R.id.searching_area);
        button_sbm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent("com.example.term_proj.searchingArea");
                startActivity(intent);
            }
        });
    }

    public void onClickButtonListener_monitoring(){
        button_sbm = (Button) findViewById(R.id.monitoring);
        button_sbm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent("com.example.term_proj.monitoring");
                startActivity(intent);
            }
        });
    }

    private class SocketThread extends Thread {
        private Handler handler1;

        @Override
        public void run() {
            try {
                // 서버에 연결
                String serverIP = "SERVER_IP";
                int port = PORT;
                socket = new Socket(serverIP, port);
                while(true) {
                    // 이미지 데이터 수신
                    InputStream inputStream = socket.getInputStream();
                    if (inputStream != null) {
                        // 이미지 데이터 길이 수신
                        byte[] imgLengthBytes = new byte[4];
                        inputStream.read(imgLengthBytes);
                        int imgLength = ByteBuffer.wrap(imgLengthBytes).getInt();

                        // 이미지 데이터 수신
                        byte[] imgBytes = new byte[imgLength];
                        int totalBytesRead = 0;
                        int bytesRead;
                        while (totalBytesRead < imgLength && (bytesRead = inputStream.read(imgBytes, totalBytesRead, imgLength - totalBytesRead)) != -1) {
                            totalBytesRead += bytesRead;
                        }
                        final Bitmap imageBitmap = BitmapFactory.decodeByteArray(imgBytes, 0, imgBytes.length);

                        // 문자열 데이터 수신
                        byte[] textLengthBytes = new byte[4];
                        inputStream.read(textLengthBytes);
                        int textLength = ByteBuffer.wrap(textLengthBytes).getInt();

                        byte[] textBytes = new byte[textLength];
                        int totalBytesRead1 = 0;
                        while (totalBytesRead1 < textLength) {
                            int bytesRead1 = inputStream.read(textBytes, totalBytesRead1, textLength - totalBytesRead1);
                            if (bytesRead1 == -1) {
                                // 읽을 데이터가 없는 경우 종료
                                break;
                            }
                            totalBytesRead1 += bytesRead1;
                        }
                        final String textData = new String(textBytes);


                        // UI 업데이트를 위해 핸들러 사용
                        handler1 = new Handler(Looper.getMainLooper());
                        handler1.post(new Runnable() {
                            @Override
                            public void run() {
                                // 이미지를 ImageView에 표시
                                imageView1.setImageBitmap(imageBitmap);
                                // 문자열을 TextView에 표시
                                textView1.setText(textData);
                            }
                        });

                        // 알림 권한 설정 관련
                        permissionCheck();
                        // 알림 전송 관련 부분
                        createNotificationChannel(DEFAULT, "default channel", NotificationManager.IMPORTANCE_HIGH);

                        Intent noti_intent = new Intent(MainActivity.this, SocketThread.class);       // 클릭시 실행할 activity를 지정
                        noti_intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP);
                        createNotification(DEFAULT, 1, "교출 상황 발생!!!!", "현재 교출 상황이 발생했으니 수업 중이지 않은 선생님들께서는 학생을 찾아주시기 바랍니다.", noti_intent);
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // 알림 권한 설정 관련
    private void permissionCheck(){
        permission = new PermissionSupport(this, this);
        if (!permission.checkPermission()){
            //권한 요청
            permission.requestPermission();
        }
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        //여기서도 리턴이 false로 들어온다면 (사용자가 권한 허용 거부)
        if (!permission.permissionResult(requestCode, permissions, grantResults)) {
            // 다시 permission 요청
            permission.requestPermission();
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    // 알림 전송 관련 부분
    void createNotificationChannel(String channelId, String channelName, int importance)
    {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
        {
            NotificationManager notificationManager = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
            notificationManager.createNotificationChannel(new NotificationChannel(channelId, channelName, importance));
        }
    }

    void createNotification(String channelId, int id, String title, String text, Intent intent)
    {
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent, PendingIntent.FLAG_IMMUTABLE);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, channelId)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setSmallIcon(R.drawable.warning)
                .setContentTitle(title)
                .setContentText(text)
                .setContentIntent(pendingIntent)    // 클릭시 설정된 PendingIntent가 실행된다
                .setAutoCancel(true)                // true이면 클릭시 알림이 삭제된다
                //.setTimeoutAfter(1000)
                //.setStyle(new NotificationCompat.BigTextStyle().bigText(text))
                .setDefaults(Notification.DEFAULT_SOUND | Notification.DEFAULT_VIBRATE);

        NotificationManager notificationManager = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        notificationManager.notify(1, builder.build());
    }

    void destroyNotification(int id)
    {
        NotificationManager notificationManager = (NotificationManager)getSystemService(NOTIFICATION_SERVICE);
        notificationManager.cancel(id);
    }


}