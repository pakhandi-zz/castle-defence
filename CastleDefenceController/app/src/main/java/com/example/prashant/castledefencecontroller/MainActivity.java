package com.example.prashant.castledefencecontroller;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {
    public final static String IP_ADDR = "com.example.prashant.castledefencecontroller.IP_ADDR";
    public final static String PORT = "com.example.prashant.castledefencecontroller.PORT";
    private Button bt;
    private EditText ip;
    private EditText port;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        bt = (Button) findViewById(R.id.button);
        ip = (EditText) findViewById(R.id.ip);
        port = (EditText) findViewById(R.id.port);

    }

    public void submit(View v) {
        Intent intent = new Intent(this, ReadyActivity.class);
        String ip_addr = ip.getText().toString();
        intent.putExtra(IP_ADDR, ip_addr);
        String port_no = port.getText().toString();
        intent.putExtra(PORT, port_no);
        startActivity(intent);
    }


}
