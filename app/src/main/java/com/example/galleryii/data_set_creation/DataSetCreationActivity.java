package com.example.galleryii.data_set_creation;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.Notification;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.FileUriExposedException;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Toast;

import com.example.galleryii.FileUtil;
import com.example.galleryii.MainActivity;
import com.example.galleryii.R;
import com.example.galleryii.data_classes.Photo;

import org.jetbrains.annotations.NotNull;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DataSetCreationActivity extends AppCompatActivity {

    private static final int PICK_IMAGES_CODE = 501;

    boolean match;
    Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_data_set_creation);
        getSupportFragmentManager().beginTransaction().replace(R.id.data_set_creation, new MatchPhotoCreationFragment()).commit();
    }

    class SendPhotos extends AsyncTask<String, String, String> {

        private final ArrayList<Photo> taskPhotos;

        public SendPhotos(ArrayList<Photo> photos) {
            this.taskPhotos = photos;
        }

        @Override
        protected String doInBackground(String... strings) {
            SharedPreferences sp = getSharedPreferences(MainActivity.AUTH_PREFERENCES, Context.MODE_PRIVATE);
            String id = sp.getString(MainActivity.USER_ID, null);
            String url = MainActivity.DEVELOP_URL + "/api/photos/post/";
            OkHttpClient client = new OkHttpClient.Builder().connectTimeout(10, TimeUnit.SECONDS).writeTimeout(180, TimeUnit.SECONDS).readTimeout(180, TimeUnit.SECONDS).build();
            for (Photo photo : taskPhotos) {
                RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
                        .addFormDataPart("image", photo.getFile().getName(), RequestBody.create(MediaType.parse("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), photo.getFile()))
                        .addFormDataPart("description", "")
                        .addFormDataPart("status", photo.getStatus())
                        .addFormDataPart("user", id)
                        .addFormDataPart("is_ai_tag", "false")
                        .build();
                Request request = new Request.Builder().url(url).post(body).build();
                try {
                    client.newCall(request).execute();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return null;
        }

    }

    public void pickImagesIntent(Boolean match, Context context) {
        this.match = match;
        this.context = context;

        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("image/*");
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
        startActivityForResult(Intent.createChooser(intent, "Выберите изображения (не менее 10)"), PICK_IMAGES_CODE);
    }

    protected void onActivityResult(int requestCode, int resultCode, @Nullable @org.jetbrains.annotations.Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_IMAGES_CODE) {
            if (resultCode == Activity.RESULT_OK) {
                ArrayList<Photo> photos = new ArrayList<>();
                assert data != null;
                if (data.getClipData() != null){
                    int size = data.getClipData().getItemCount();
                    for (int i = 0; i < size; i++) {
                        Uri imageUri = data.getClipData().getItemAt(i).getUri();
                        File file = null;
                        try {
                            file = FileUtil.from(this,imageUri);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        Log.d("file", "File...:::: uti - "+file .getPath()+" file -" + file + " : " + file .exists());
                        Photo photo = new Photo();
                        photo.match = this.match;
                        photo.uri = imageUri;
                        photo.file = file;
                        photos.add(photo);
                    }
                }
                else{
                    Uri imageUri = data.getData();
                    File file = null;
                    try {
                        file = FileUtil.from(this,imageUri);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    Photo photo = new Photo();
                    photo.match = this.match;
                    photo.uri = imageUri;
                    photo.file = file;
                    photos.add(photo);
                }
                SendPhotos sendPhotos = new SendPhotos(photos);
                sendPhotos.execute();
            }
        }
    }
}