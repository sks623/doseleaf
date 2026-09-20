package com.doseleaf.app;
import android.content.*;import android.database.*;import android.net.Uri;import android.os.*;import java.io.*;
public class PhotoProvider extends ContentProvider {
 public boolean onCreate(){return true;}
 private File file(Uri uri)throws FileNotFoundException{String name=uri.getLastPathSegment();if(!"camera.jpg".equals(name)&&!"reminders.ics".equals(name))throw new FileNotFoundException();return new File(getContext().getCacheDir(),name);}
 public ParcelFileDescriptor openFile(Uri uri,String mode)throws FileNotFoundException{File f=file(uri);int flags=mode.contains("w")?ParcelFileDescriptor.MODE_CREATE|ParcelFileDescriptor.MODE_TRUNCATE|ParcelFileDescriptor.MODE_READ_WRITE:ParcelFileDescriptor.MODE_READ_ONLY;return ParcelFileDescriptor.open(f,flags);}
 public String getType(Uri uri){return "reminders.ics".equals(uri.getLastPathSegment())?"text/calendar":"image/jpeg";}
 public Cursor query(Uri uri,String[] projection,String selection,String[] args,String sort){try{File f=file(uri);MatrixCursor c=new MatrixCursor(new String[]{"_display_name","_size"});c.addRow(new Object[]{f.getName(),f.length()});return c;}catch(Exception e){return null;}}
 public Uri insert(Uri u,ContentValues v){throw new UnsupportedOperationException();}public int delete(Uri u,String s,String[] a){throw new UnsupportedOperationException();}public int update(Uri u,ContentValues v,String s,String[] a){throw new UnsupportedOperationException();}
}
