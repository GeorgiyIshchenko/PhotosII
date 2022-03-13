import json
from Photo import Photo_Schema, Dict2Photo
from redis import Redis
import rq
import urllib.request as req
from Functions import Education, download_photo, downlodad_photo_from_json

queue = rq.Queue('list0', connection=Redis.from_url('redis://'))
args = []
job = queue.enqueue(Education())

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

job = queue.enqueue(downlodad_photo_from_json, json_string = json_string)