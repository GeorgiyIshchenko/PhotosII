package com.example.galleryii;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.Manifest;
import android.app.AlertDialog;
import android.content.ContentValues;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.example.galleryii.adapters.TagsAdapter;
import com.example.galleryii.auth.AuthActivity;
import com.example.galleryii.data_classes.Photo;
import com.example.galleryii.data_classes.Tag;
import com.example.galleryii.data_set_creation.DataSetCreationActivity;
import com.example.galleryii.data_set_creation.SinglePhotoCreationActivity;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.jetbrains.annotations.NotNull;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private static final int PERMISSION_CODE = 1001;
    private static final int IMAGE_CAPTURE_CODE = 1002;
    private static final int IMAGE_PICK_CODE = 1003;

    public static final String AUTH_PREFERENCES = "auth";
    public static final String USER_LOGIN = "login";
    public static final String USER_PASSWORD = "password";
    public static final String USER_TOKEN = "token";
    public static final String USER_ID = "user_id";

    public static String DEVELOP_URL = "http://192.168.8.3:8000";

    SharedPreferences sp;

    Uri image_uri;
    File photo;

    String url;

    FloatingActionButton buttonAdd;
    FloatingActionButton buttonGallery;
    FloatingActionButton buttonExit;

    ArrayList<Tag> tags;
    TagsAdapter adapter;
    RecyclerView recyclerView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sp = getSharedPreferences(AUTH_PREFERENCES, Context.MODE_PRIVATE);
        String id = sp.getString(USER_ID, null);
        if (id == null) {
            startActivity(new Intent(this, AuthActivity.class));
            finish();
        }

        buttonAdd = findViewById(R.id.button_photo_add);
        buttonGallery = findViewById(R.id.button_gallery_add);
        buttonExit = findViewById(R.id.button_exit);
        recyclerView = findViewById(R.id.rv_tags);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        url = DEVELOP_URL+"/api/" + id + "/tags";
        Log.d("request", url);

        CheckPermissions();

        GetPhotoList getPhotoList = new GetPhotoList();
        getPhotoList.execute();

        buttonAdd.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCamera();
            }
        });
        buttonGallery.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(MainActivity.this, DataSetCreationActivity.class));
            }
        });
        buttonExit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                builder.setTitle("Выход");  // заголовок
                builder.setMessage("Вы уверены что хотите выйти?"); // сообщение
                builder.setPositiveButton("Да", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {
                        SharedPreferences.Editor editor = sp.edit();
                        editor.putString(USER_ID, null);
                        editor.apply();
                        startActivity(new Intent(MainActivity.this, AuthActivity.class));
                        finish();
                    }
                });
                builder.setNegativeButton("Нет", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int id) {

                    }
                });
                builder.setCancelable(true);
                builder.create();
                builder.show();
            }
        });
    }

    class GetPhotoList extends AsyncTask<String, String, String> {

        @Override
        protected String doInBackground(String... strings) {
            try {
                OkHttpClient client = new OkHttpClient();
                Request request = new Request.Builder().url(new URL(url)).build();
                Response response = client.newCall(request).execute();
                String s = response.body().string();
                Log.d("request", s);
                return s;
            } catch (IOException e) {
                Log.d("request", e.getMessage());
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPostExecute(String s) {
            try {
                JSONArray tagsJSON = new JSONArray(s);
                tags = new ArrayList<>();
                int JSONArraySize = tagsJSON.length();
                for (int i = 0; i < JSONArraySize; i++) {
                    JSONObject tagJSON = tagsJSON.getJSONObject(i);
                    Tag tag = new Tag();
                    tag.name = tagJSON.getString("name");
                    if (tag.name.length() > 0)
                        tag.name = tag.name.substring(0, 1).toUpperCase() + tag.name.substring(1);
                    JSONArray photosJSON = tagJSON.getJSONArray("photos");
                    ArrayList<Photo> photos = new ArrayList<>();
                    int JSONPhotosSize = photosJSON.length();
                    for (int j = 0; j < JSONPhotosSize; j++) {
                        JSONObject photoJSON = photosJSON.getJSONObject(j);
                        Photo photo = new Photo();
                        photo.id = photoJSON.getInt("id");
                        photo.url = photoJSON.getString("image");
                        photo.description = photoJSON.getString("description");
                        photo.match = photoJSON.getString("status").equals("n");
                        photo.createdAt = photoJSON.getString("created_at");
                        photo.tagName = tag.name;
                        photos.add(photo);
                    }
                    tag.photos = photos;
                    tags.add(tag);
                    Log.d("request", photosJSON.toString());
                }
                adapter = new TagsAdapter(tags);
                recyclerView.setAdapter(adapter);
            } catch (JSONException e) {
                e.printStackTrace();
            }
            super.onPostExecute(s);
        }
    }

    private void CheckPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.CAMERA) ==
                    PackageManager.PERMISSION_DENIED ||
                    checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) ==
                            PackageManager.PERMISSION_DENIED ||
                    checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) ==
                            PackageManager.PERMISSION_DENIED) {
                String[] permissions = {Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.READ_EXTERNAL_STORAGE};
                requestPermissions(permissions, PERMISSION_CODE);
            }
        }
    }

    public String getRealPathFromURI(Uri uri) {
        Cursor cursor = getContentResolver().query(uri, null, null, null, null);
        cursor.moveToFirst();
        int id_uri = cursor.getColumnIndex(MediaStore.Images.ImageColumns.DATA);
        return cursor.getString(id_uri);
    }

    private void openCamera() {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.TITLE, "New Picture");
        values.put(MediaStore.Images.Media.DESCRIPTION, "From the camera");
        image_uri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);

        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, image_uri);
        startActivityForResult(cameraIntent, IMAGE_CAPTURE_CODE);
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Log.d("single_photo", image_uri.getPath());
        if (resultCode == RESULT_OK && requestCode == IMAGE_CAPTURE_CODE) {
            Log.d("request", getRealPathFromURI(image_uri));
            photo = new File(getRealPathFromURI(image_uri));
            Intent intent = new Intent(MainActivity.this, SinglePhotoCreationActivity.class);
            intent.putExtra("fileUri", photo.getAbsolutePath());
            startActivity(intent);
            finish();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull @NotNull String[] permissions, @NonNull @NotNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case PERMISSION_CODE: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    openCamera();
                } else {
                    Toast.makeText(this, "Permission denied", Toast.LENGTH_SHORT).show();
                }
            }
        }
    }
}