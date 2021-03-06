#!/Users/zhenghongwang/.pyenv/shims/python3

from typing import *
import os
import time
import urllib.request
import json
import hashlib

raw_data_file_path = 'raw_data.json'

mod_data = []

with open(raw_data_file_path, 'r') as json_file:
    data = json.load(json_file)
    for img_entry in data['img_data']:
        local_path = img_entry['local_path']
        if not img_entry['md5']:
            # calc md5
            with open(local_path, "rb") as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            img_entry['md5'] = file_hash.hexdigest()
        if not img_entry['size']:
            img_entry['size'] = os.stat(local_path).st_size
        img_entry['img_url'] = "https://zh-wang.github.io/right_brain_training_data/%s" % local_path
    mod_data = data

with open(raw_data_file_path, 'w') as json_file:
    json_file.write(json.dumps(mod_data, ensure_ascii=False, indent=4))
