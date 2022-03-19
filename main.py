import json
from Photo import Photo_Schema, Dict2Photo
from redis import Redis
import rq
import urllib.request as req
import os
from Functions import Education, downlodad_photos_from_json, deleting_old_dataset, set_dataset, model_save, Prediction, \
    do_photo_array

queue = rq.Queue('list0', connection=Redis.from_url('redis://'))

json_string = """[
    {
        "id": 55,
        "tag": "match",
        "image": "https://www.photostock.com.mx/stock-photo-preview/132507561/1000/inh_33594_320727.jpg",
        "description": "описание",
        "status": "b",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    },
    {
        "id": 54,
        "tag": "match",
        "image": "https://www.photostock.com.mx/stock-photo-preview/132507561/1000/inh_33594_320727.jpg",
        "description": "",
        "status": "n",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    },
    {
        "id": 53,
        "tag": "match",
        "image": "https://www.photostock.com.mx/stock-photo-preview/132507561/1000/inh_33594_320727.jpg",
        "description": "",
        "status": "n",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    },
    {
        "id": 52,
        "tag": "notmatch",
        "image": "https://www.photostock.com.mx/stock-photo-preview/132507561/1000/inh_33594_320727.jpg",
        "description": "",
        "status": "n",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    },
    {
        "id": 51,
        "tag": "notmatch",
        "image": "https://www.photostock.com.mx/stock-photo-preview/132507561/1000/inh_33594_320727.jpg",
        "description": "",
        "status": "n",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    },
    {
        "id": 50,
        "tag": "notmatch",
        "image": "https://www.photostock.com.mx/stock-photo-preview/132507561/1000/inh_33594_320727.jpg",
        "description": "",
        "status": "n",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    },
    {
        "id": 49,
        "tag": "notmatch",
        "image": "https://www.photostock.com.mx/stock-photo-preview/132507561/1000/inh_33594_320727.jpg",
        "description": "",
        "status": "n",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    }
]"""
job = queue.enqueue(Prediction, json_string, job_timeout=40000)
