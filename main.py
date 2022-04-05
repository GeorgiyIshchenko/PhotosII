import json
from Photo import Photo_Schema, Dict2Photo
from redis import Redis
import rq
import urllib.request as req
import os
import time
from Functions import Education, downlodad_photos_from_json, deleting_old_dataset, set_dataset, model_save, Prediction, \
    do_photo_array, dataset_by_filenames

queue = rq.Queue('list0', connection=Redis.from_url('redis://'))


json_string = """[
    {
        "id": 55,
        "tag": "notmatch",
        "image": "0.jpg",
        "description": "описание",
        "status": "b",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    },
    {
        "id": 54,
        "tag": "match",
        "image": "1.jpg",
        "description": "",
        "status": "n",
        "created_at": "21.02.2022 13:25",
        "is_ai_tag": false,
        "user": 13
    }
]"""

print(Prediction(json_string))
'''
job = queue.enqueue(Education, json_string, job_timeout=40000)
while job.is_finished==False:
    job.refresh()
    time.sleep(1)

print(job.result)
'''
