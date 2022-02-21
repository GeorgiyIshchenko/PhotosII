package com.example.galleryii.data_set_creation;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.galleryii.R;
import com.example.galleryii.data_classes.Photo;

import java.util.ArrayList;

public class CheckSelectFragment extends Fragment {

    CheckSelectFragment(ArrayList<Photo> photos, boolean match){

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_check_select, container, false);
    }
}