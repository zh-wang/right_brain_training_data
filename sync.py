#!/Users/zhenghongwang/.pyenv/shims/python3

from typing import *
import os
import time
import urllib.request
import json
import hashlib
from fetch_audio import fetch_audio

raw_data_file_path = 'raw_data.json'

mod_data = []

# read audio file in local
audio_files = os.listdir('audio')

def calc_md5(path):
    with open(path, 'rb') as f:
        file_hash = hashlib.md5()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)
    return file_hash.hexdigest()

def fetch_audio_file(text, checker, li):
    fetch_audio(text)
    checker.append(text)
    audio_file_local_path = "audio/%s.mp3" % text
    new_entry = {
            "text": text,
            "path": audio_file_local_path,
            "md5": calc_md5(audio_file_local_path),
            "size": os.stat(audio_file_local_path).st_size
            }
    li.append(new_entry)

with open(raw_data_file_path, 'r') as json_file:
    data = json.load(json_file)
    # read audio files
    audio_already_exists = []
    for audio_entry in data['audio_data']:
        audio_already_exists.append(audio_entry['text'])

    # prepare image files
    for img_entry in data['img_data']:
        local_path = img_entry['local_path']
        if not img_entry['md5']:
            img_entry['md5'] = calc_md5(local_path)
        if not img_entry['size']:
            img_entry['size'] = os.stat(local_path).st_size
        if not img_entry['img_url']:
            img_entry['img_url'] = "https://zh-wang.github.io/right_brain_training_data/%s" % local_path
        # prepare audio file for 'name_ja'
        if img_entry['name_ja'] not in audio_already_exists:
            fetch_audio_file(img_entry['name_ja'], audio_already_exists, data['audio_data'])
    mod_data = data

with open(raw_data_file_path, 'w') as json_file:
    json_file.write(json.dumps(mod_data, ensure_ascii=False, indent=4))
