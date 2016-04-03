package com.example.prashant.castledefencecontroller;

import android.content.Intent;
import android.graphics.Color;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.net.UnknownHostException;

public class ReadyActivity extends AppCompatActivity {
    TextView status_message;
    Button ready_button;
    public static Handler connectHandler;
    static Handler uiHandler;
    String bgcolor = "white";
    public final static String COLOR = "com.example.prashant.castledefencecontroller.COLOR";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ready);
        Intent intent = getIntent();
        String ip_addr = intent.getStringExtra(MainActivity.IP_ADDR);
        String port_no = intent.getStringExtra(MainActivity.PORT);

        Log.e("QWERTY", "ip:port " + ip_addr + ":" + port_no);
        status_message = (TextView) findViewById(R.id.status_message);
        status_message.setText("Connecting to " + ip_addr + ":" + port_no);

        ready_button = (Button) findViewById(R.id.ready_button);

        uiHandler = new Handler() {
            public void handleMessage(Message msg) {
                Bundle bundle = msg.getData();
                String connect_status = bundle.getString("connect_status");
                String color = bundle.getString("color");
                status_message.setText(connect_status);
                if (connect_status.compareTo("Connected") == 0) {
                    ready_button.setEnabled(true);
                    ready_button.setVisibility(View.VISIBLE);
                    RelativeLayout rl = (RelativeLayout) findViewById(R.id.view);
                    rl.setBackgroundColor(Color.parseColor(color));
                    bgcolor = color;
                }
            }
        };

        new Thread(new Connect(ip_addr, Integer.parseInt(port_no))).start();

        Log.e("QWERTY", "Thread started");
    }

    @Override
    protected void onDestroy() {
        if (connectHandler != null)
            connectHandler.getLooper().quit();
        super.onDestroy();
    }

    public void ready(View v) {
        if (connectHandler != null) {
            Message msg = connectHandler.obtainMessage();
            Bundle bundle = new Bundle();
            bundle.putString("move", "Ready");
            msg.setData(bundle);
            connectHandler.sendMessage(msg);
        }
        Intent intent = new Intent(this, ControllerActivity.class);
        intent.putExtra(COLOR, bgcolor);
        startActivity(intent);
    }

    private class Connect implements Runnable {
        Socket socket = null;
        DataOutputStream out = null;
        BufferedReader in = null;
        String ip_addr;
        int port_no;

        Connect(String ip_addr, int port_no) {
            this.ip_addr = ip_addr;
            this.port_no = port_no;
        }

        public void run() {
            try {
                socket = new Socket(ip_addr, port_no);
                out = new DataOutputStream(socket.getOutputStream());
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                out.writeUTF("Player connect");
                Log.e("QWERTY", "Message sent from app to server");
                String response = in.readLine();
                String color = in.readLine();
                Log.e("QWERTY", "Message received from server " + response);
                if (uiHandler != null) {
                    Message msg = uiHandler.obtainMessage();
                    Bundle bundle = new Bundle();
                    bundle.putString("connect_status", response);
                    bundle.putString("color", color);
                    msg.setData(bundle);
                    uiHandler.sendMessage(msg);
                    Log.e("QWERTY", "Message sent to ui");
                }
            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            Looper.prepare();

            connectHandler = new Handler() {
                @Override
                public void handleMessage(Message msg) {
                    Bundle bundle = msg.getData();
                    String move = bundle.getString("move");
                    Log.e("QWERTY", move);
                    try {
                        out.writeUTF(move);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            };

            Looper.loop();
        }
    }

}
