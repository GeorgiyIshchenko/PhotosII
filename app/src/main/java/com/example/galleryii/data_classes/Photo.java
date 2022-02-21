package com.example.galleryii.data_classes;

import android.net.Uri;

import java.io.File;

public class Photo {

    public long id;
    public String url;
    public String description;
    public String createdAt;
    public String tagName;
    public boolean match;
    public File file;
    public Uri uri;

    public Photo(long id, String url, String description, String createdAt, String tagName, boolean match, File file, Uri uri) {
        this.id = id;
        this.url = url;
        this.description = description;
        this.createdAt = createdAt;
        this.match = match;
        this.tagName = tagName;
        this.file = file;
        this.uri = uri;
    }

    public Photo() {
    }

    public String getTagName() {
        return tagName;
    }

    public void setTagName(String tagName) {
        this.tagName = tagName;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public boolean isMatch() {
        return match;
    }

    public String getStatus() {
        if (this.match) return "n";
        return "b";
    }

    public void setMatch(boolean match) {
        this.match = match;
    }

    public File getFile() {
        return file;
    }

    public void setFile(File file) {
        this.file = file;
    }

    public Uri getUri() {
        return uri;
    }

    public void setUri(Uri uri) {
        this.uri = uri;
    }
}
