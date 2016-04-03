package com.example.prashant.castledefencecontroller;

import android.content.Intent;
import android.graphics.Color;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.RelativeLayout;

public class ControllerActivity extends AppCompatActivity {
    Handler connectHandler = ReadyActivity.connectHandler;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        setContentView(R.layout.activity_controller);

        Intent intent = getIntent();
        String color = intent.getStringExtra(ReadyActivity.COLOR);
        RelativeLayout rl = (RelativeLayout) findViewById(R.id.cview);
        rl.setBackgroundColor(Color.parseColor(color));

        Button a_button = (Button) findViewById(R.id.a);
        a_button.setOnTouchListener(new View.OnTouchListener() {

            private Handler mHandler;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        if (mHandler != null) return true;
                        mHandler = new Handler();
                        mHandler.postDelayed(mAction, 250);
                        break;
                    case MotionEvent.ACTION_UP:
                        if (mHandler == null) return true;
                        mHandler.removeCallbacks(mAction);
                        mHandler = null;
                        break;
                }
                return false;
            }

            Runnable mAction = new Runnable() {
                @Override
                public void run() {
                    System.out.println("Performing action...");
                    if (connectHandler != null) {
                        Message msg = connectHandler.obtainMessage();
                        Bundle bundle = new Bundle();
                        bundle.putString("move", "A");
                        msg.setData(bundle);
                        connectHandler.sendMessage(msg);
                    }
                    mHandler.postDelayed(this, 250);
                }
            };

        });

        Button b_button = (Button) findViewById(R.id.b);
        b_button.setOnTouchListener(new View.OnTouchListener() {

            private Handler mHandler;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        if (mHandler != null) return true;
                        mHandler = new Handler();
                        mHandler.postDelayed(mAction, 250);
                        break;
                    case MotionEvent.ACTION_UP:
                        if (mHandler == null) return true;
                        mHandler.removeCallbacks(mAction);
                        mHandler = null;
                        break;
                }
                return false;
            }

            Runnable mAction = new Runnable() {
                @Override
                public void run() {
                    System.out.println("Performing action...");
                    if (connectHandler != null) {
                        Message msg = connectHandler.obtainMessage();
                        Bundle bundle = new Bundle();
                        bundle.putString("move", "B");
                        msg.setData(bundle);
                        connectHandler.sendMessage(msg);
                    }
                    mHandler.postDelayed(this, 250);
                }
            };

        });

        Button up_button = (Button) findViewById(R.id.up);
        up_button.setOnTouchListener(new View.OnTouchListener() {

            private Handler mHandler;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        if (mHandler != null) return true;
                        mHandler = new Handler();
                        mHandler.postDelayed(mAction, 100);
                        break;
                    case MotionEvent.ACTION_UP:
                        if (mHandler == null) return true;
                        mHandler.removeCallbacks(mAction);
                        mHandler = null;
                        break;
                }
                return false;
            }

            Runnable mAction = new Runnable() {
                @Override
                public void run() {
                    System.out.println("Performing action...");
                    if (connectHandler != null) {
                        Message msg = connectHandler.obtainMessage();
                        Bundle bundle = new Bundle();
                        bundle.putString("move", "Up");
                        msg.setData(bundle);
                        connectHandler.sendMessage(msg);
                    }
                    mHandler.postDelayed(this, 100);
                }
            };

        });

        Button down_button = (Button) findViewById(R.id.down);
        down_button.setOnTouchListener(new View.OnTouchListener() {

            private Handler mHandler;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        if (mHandler != null) return true;
                        mHandler = new Handler();
                        mHandler.postDelayed(mAction, 100);
                        break;
                    case MotionEvent.ACTION_UP:
                        if (mHandler == null) return true;
                        mHandler.removeCallbacks(mAction);
                        mHandler = null;
                        break;
                }
                return false;
            }

            Runnable mAction = new Runnable() {
                @Override
                public void run() {
                    System.out.println("Performing action...");
                    if (connectHandler != null) {
                        Message msg = connectHandler.obtainMessage();
                        Bundle bundle = new Bundle();
                        bundle.putString("move", "Down");
                        msg.setData(bundle);
                        connectHandler.sendMessage(msg);
                    }
                    mHandler.postDelayed(this, 100);
                }
            };

        });

        Button left_button = (Button) findViewById(R.id.left);
        left_button.setOnTouchListener(new View.OnTouchListener() {

            private Handler mHandler;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        if (mHandler != null) return true;
                        mHandler = new Handler();
                        mHandler.postDelayed(mAction, 100);
                        break;
                    case MotionEvent.ACTION_UP:
                        if (mHandler == null) return true;
                        mHandler.removeCallbacks(mAction);
                        mHandler = null;
                        break;
                }
                return false;
            }

            Runnable mAction = new Runnable() {
                @Override
                public void run() {
                    System.out.println("Performing action...");
                    if (connectHandler != null) {
                        Message msg = connectHandler.obtainMessage();
                        Bundle bundle = new Bundle();
                        bundle.putString("move", "Left");
                        msg.setData(bundle);
                        connectHandler.sendMessage(msg);
                    }
                    mHandler.postDelayed(this, 100);
                }
            };

        });

        Button right_button = (Button) findViewById(R.id.right);
        right_button.setOnTouchListener(new View.OnTouchListener() {

            private Handler mHandler;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        if (mHandler != null) return true;
                        mHandler = new Handler();
                        mHandler.postDelayed(mAction, 100);
                        break;
                    case MotionEvent.ACTION_UP:
                        if (mHandler == null) return true;
                        mHandler.removeCallbacks(mAction);
                        mHandler = null;
                        break;
                }
                return false;
            }

            Runnable mAction = new Runnable() {
                @Override
                public void run() {
                    System.out.println("Performing action...");
                    if (connectHandler != null) {
                        Message msg = connectHandler.obtainMessage();
                        Bundle bundle = new Bundle();
                        bundle.putString("move", "Right");
                        msg.setData(bundle);
                        connectHandler.sendMessage(msg);
                    }
                    mHandler.postDelayed(this, 100);
                }
            };

        });
    }

    public void moveup(View v) {
        if (connectHandler != null) {
            Message msg = connectHandler.obtainMessage();
            Bundle bundle = new Bundle();
            bundle.putString("move", "Up");
            msg.setData(bundle);
            connectHandler.sendMessage(msg);
        }
    }
    public void movedown(View v) {
        if (connectHandler != null) {
            Message msg = connectHandler.obtainMessage();
            Bundle bundle = new Bundle();
            bundle.putString("move", "Down");
            msg.setData(bundle);
            connectHandler.sendMessage(msg);
        }
    }
    public void moveleft(View v) {
        if (connectHandler != null) {
            Message msg = connectHandler.obtainMessage();
            Bundle bundle = new Bundle();
            bundle.putString("move", "Left");
            msg.setData(bundle);
            connectHandler.sendMessage(msg);
        }
    }
    public void moveright(View v) {
        if (connectHandler != null) {
            Message msg = connectHandler.obtainMessage();
            Bundle bundle = new Bundle();
            bundle.putString("move", "Right");
            msg.setData(bundle);
            connectHandler.sendMessage(msg);
        }
    }
    public void a(View v) {
        if (connectHandler != null) {
            Message msg = connectHandler.obtainMessage();
            Bundle bundle = new Bundle();
            bundle.putString("move", "A");
            msg.setData(bundle);
            connectHandler.sendMessage(msg);
        }
    }
    public void b(View v) {
        if (connectHandler != null) {
            Message msg = connectHandler.obtainMessage();
            Bundle bundle = new Bundle();
            bundle.putString("move", "B");
            msg.setData(bundle);
            connectHandler.sendMessage(msg);
        }
    }

}
