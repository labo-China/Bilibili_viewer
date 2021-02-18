# coding: UTF-8
from scripts.tool import extractor, replace_for_web, replace_for_highlight
import requests
import json


class new_search:
    def __init__(self, keyword: str, search_type: str = 'all', page: int = 1, highlignt: int = 1):
        if search_type == 'all':
            self.main_data = requests.get(
                f'https://api.bilibili.com/x/web-interface/search/all/v2?'
                f'page={page}&keyword={keyword}&highlight={highlignt}')
        else:
            self.main_data = requests.get(
                f'https://api.bilibili.com/x/web-interface/search/type?'
                f'search_type={search_type}&page={page}&keyword={keyword}&highlight={highlignt}')
        self.search_type = search_type
        self.response_code = self.main_data.status_code
        self.main_data = json.loads(self.main_data.text)
        self.return_code = self.main_data['code']

    def get_pages(self):
        return self.main_data['data']['numPages']

    def get_video(self):
        VideoList = []
        Data = self.__get_data__('video')
        VideoDict = {'title': 'title', 'aid': 'aid', 'bvid': 'bvid', 'danmaku': 'video_review', 'length': 'duration',
                     'introduction': 'description', 'collect': 'favorites', 'view': 'play', 'reply': 'review',
                     'upload_time': 'pubdate', 'tag': 'tag', 'tname': 'typename'}
        for Videos in Data:
            Video = extractor(data = Videos, dicts = VideoDict)
            Video['title'] = replace_for_web(replace_for_highlight(Video['title']))
            Video['introduction'] = replace_for_web(Video['introduction'])
            VideoList.append(Video)
        return VideoList

    def get_user(self):
        ResultData = self.__get_data__('bili_user')
        UserDict = {'name': 'uname', 'level': 'level', 'uid': 'mid', 'official': ['official', 'desc'], 'fans': 'fans',
                    'video_count': 'videos', 'sign': 'usign'}
        ReturnData = []
        for Users in ResultData:
            UserData = extractor(data = Users, dicts = UserDict)
            if Users['gender'] == 1:
                UserData['sex'] = '男'
            elif Users['gender'] == 2:
                UserData['sex'] = '女'
            else:
                UserData['sex'] = '保密'
            if Users['is_live'] == 1:
                UserData['live'] = True
            else:
                UserData['live'] = False
            if Users['is_upuser'] == 1:
                UserData['upuser'] = True
            else:
                UserData['upuser'] = False
            VideoDict = {'view': 'play', 'bvid': 'bvid', 'title': 'title', 'coin': 'coin', 'upload_time': 'pubdate',
                         'introduction': 'desc', 'collect': 'fav', 'length': 'duration', 'aid': 'aid', 'danmaku': 'dm'}
            UserData['top_video'] = []
            for TopVideos in Users['res']:
                UserData['top_video'].append(extractor(data = TopVideos, dicts = VideoDict))
            ReturnData.append(UserData)
        return ReturnData

    def __get_data__(self, data_type):
        if self.search_type == 'all':
            for range_var in self.main_data['data']['result']:
                if range_var['result_type'] == data_type:
                    return range_var['data']
            return None
        else:
            return self.main_data['data']['result']
