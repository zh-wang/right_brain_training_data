#!/Users/zhenghongwang/.pyenv/shims/python3

from typing import *
import os
import time
import urllib.request
import json
import requests
import base64
import urllib.parse

def fetch_audio(text):
    url = 'https://www.google.com/async/translate_tts?ei=mDBEYPyoI8jN-QbyiZuYCQ&yv=3&ttsp=tl:ja,txt:{}&async=_fmt:jspb'
    with requests.Session() as s:
        res = s.get(url.format(urllib.parse.quote(text)))
        if res.status_code == 200:
            s = res.content.decode()
            i = s.index('{"translate_tts')
            audio_base64_raw = json.loads(s[i:])['translate_tts'][0]
            with open('audio/%s.mp3' % text, 'wb') as f:
                f.write(base64.b64decode(audio_base64_raw))
