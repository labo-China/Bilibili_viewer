from Plugin.tool import *
import time
import requests
import json
import re


class new_search:
    def __init__(self, keyword: str, search_type: str = 'all', page: int = 1, highlignt: int = 1):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        if search_type == 'all':
            self.main_data = requests.get(
                f'https://api.bilibili.com/x/web-interface/search/all/v2?'
                f'page={page}&keyword={keyword}&highlight={highlignt}',
                headers = self.headers)
        else:
            self.main_data = requests.get(
                f'https://api.bilibili.com/x/web-interface/search/type?'
                f'search_type={search_type}&page={page}&keyword={keyword}&highlight={highlignt}',
                headers = self.headers)
        self.search_type = search_type
        self.response_code = self.main_data.status_code
        self.main_data = json.loads(self.main_data.text)
        self.return_code = self.main_data['code']

    def get_pages(self):
        return self.main_data['data']['numPages']

    def get_video(self):
        VideoList = []
        Data = self.__get_data__('video')
        for Videos in Data:
            Video = {'title': replace_for_web(replace_for_highlight(Videos['title'])), 'aid': Videos['aid'],
                     'bvid': Videos['bvid'], 'danmaku': Videos['video_review'],
                     'introduction': replace_for_web(Videos['description']), 'length': Videos['duration'],
                     'collect': Videos['favorites'], 'view': Videos['play'], 'reply': Videos['review'],
                     'upload_time': format_time(Videos['pubdate']),
                     'tag': Videos['tag'], 'tname': Videos['typename']}
            VideoList.append(Video)
        return VideoList

    def get_user(self):
        result_data = self.__get_data__('bili_user')
        return_data = []
        for range_var in result_data:
            user_data = {'name': range_var['uname'], 'level': range_var['level'], 'uid': range_var['mid'],
                         'official': range_var['official_verify']['desc'], 'fans': range_var['fans'],
                         'video_count': range_var['videos'], 'sign': range_var['usign']}
            if range_var['gender'] == 1:
                user_data['sex'] = '男'
            elif range_var['gender'] == 2:
                user_data['sex'] = '女'
            else:
                user_data['sex'] = '保密'
            if range_var['is_live'] == 1:
                user_data['live'] = True
            else:
                user_data['live'] = False
            if range_var['is_upuser'] == 1:
                user_data['upuser'] = True
            else:
                user_data['upuser'] = False
            user_data['top_video'] = []
            for top_videos in range_var['res']:
                top_video = {'aid': top_videos['aid'], 'bvid': top_videos['bvid'], 'title': top_videos['title'],
                             'coin': top_videos['coin'], 'introduction': top_videos['desc'],
                             'collect': top_videos['fav'],
                             'length': top_videos['duration'], 'view': top_videos['play'], 'danmaku': top_videos['dm'],
                             'upload_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(top_videos['pubdate']))}
                user_data['top_video'].append(top_video)
            return_data.append(user_data)
        return return_data

    def __get_data__(self, data_type):
        if self.search_type == 'all':
            for range_var in self.main_data['data']['result']:
                if range_var['result_type'] == data_type:
                    return range_var['data']
            return None
        else:
            return self.main_data['data']['result']
