# -*- coding: UTF-8 -*-
import requests
import json
from Plugin.tool import extractor


def get_default_search_word() -> dict:
    Data = requests.get('https://api.bilibili.com/x/web-interface/search/default')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            **extractor(data = JsonData['data'], dicts = {'name': 'show_name', 'url': 'url'})}


def get_danmaku_preview(aid: int) -> dict:
    Data = requests.get(f'https://api.bilibili.com/x/v2/dm/ajax?aid={aid}')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'danmaku_list': JsonData['data']}


def get_background_image() -> dict:
    Data = requests.get('https://api.bilibili.com/x/web-show/res/locs?pf=0&ids=142')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            'background': JsonData['data']['142'][0]['pic'], 'title': JsonData['data']['142'][0]['litpic']}
