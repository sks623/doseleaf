package com.doseleaf.app;
import android.content.*;
public class BootReceiver extends BroadcastReceiver{public void onReceive(Context c,Intent i){PendingResult r=goAsync();new Thread(()->{try{Scheduler.all(c);}finally{r.finish();}}).start();}}
