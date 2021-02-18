# coding: UTF-8
import requests
import json
from scripts.tool import extractor


# website-background
def get_default_search_word() -> dict:
    Data = requests.get('https://api.bilibili.com/x/web-interface/search/default')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            **extractor(data = JsonData['data'], dicts = {'name': 'show_name', 'url': 'url'})}


def get_background_image() -> dict:
    Data = requests.get('https://api.bilibili.com/x/web-show/res/locs?pf=0&ids=142')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            'background': JsonData['data']['142'][0]['pic'], 'title': JsonData['data']['142'][0]['litpic']}


# video-background
def get_danmaku_preview(aid: int) -> dict:
    Data = requests.get(f'https://api.bilibili.com/x/v2/dm/ajax?aid={aid}')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'danmaku_list': JsonData['data']}


# tag-api
def get_tag_id(name: str) -> dict:
    Data = requests.get(f'https://api.bilibili.com/x/tag/info?tag_name={name}')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            'tag_id': JsonData['data']['tag_id']}


def get_tag_video(tag_id: int, page_size: int = 10) -> dict:
    BaseUrl = 'https://api.bilibili.com/x/web-interface/tag/top?pn={}&ps={}&tid={}'
    Page = 1
    Data = requests.get(BaseUrl.format(Page, page_size, tag_id))
    VideoInfoDict = {'aid': 'aid', 'bvid': 'bvid', 'title': 'title', 'tname': 'tname',
                     'copyright': 'copyright', 'upload_time': 'pubdate', 'introduction': 'desc'}
    VideoDataDict = {'view': 'view', 'danmaku': 'danmaku', 'like': 'like', 'dislike': 'dislike',
                     'reply': 'reply', 'coin': 'coin', 'collect': 'favorite', 'share': 'share'}

    while Data.text != '':
        Page += 1
        JsonData = json.loads(Data.text)
        VideoList = []

        for Video in JsonData['data']:
            VideoList.append({**extractor(data = Video, dicts = VideoInfoDict),
                              **extractor(data = Video['stat'], dicts = VideoDataDict)})
        Data = requests.get(BaseUrl.format(Page, page_size, tag_id))
        yield {'response_code': Data.status_code, 'return_code': JsonData['code'], 'videos': VideoList}
