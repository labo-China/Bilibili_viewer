import requests
import json
import time
from Plugin.tool import *


class video:
    """Get Bilibili video"""

    def __init__(self, code, num):
        # 获取视频全部信息
        self.MainData = requests.get(f'https://api.bilibili.com/x/web-interface/view?{code}={num}')
        # 获取请求资源码
        self.response_code = self.MainData.status_code
        self.MainData = json.loads(self.MainData.text)
        # 获取网站返回码
        self.return_code = self.MainData['code']

    def video_info(self) -> dict:
        """Return video info"""
        if self.return_code != 0 or self.response_code != 200:
            return {'response_code': self.response_code, 'return_code': self.return_code}
        VideoInfoDict = {'aid': 'aid', 'bvid': 'bvid', 'title': 'title', 'tname': 'tname',
                         'copyrights': 'copyright', 'upload_time': 'pubdate', 'owner': ['owner', 'name']}
        Data = extractor(data = self.MainData['data'], dicts = VideoInfoDict)
        Data['copyrights'] = '自制' if Data['copyrights'] == 1 else '转载'
        Data['upload_time'] = format_time(Data['upload_time'])
        return {'response_code': self.response_code, 'return_code': self.return_code, **Data}

    def introduction(self) -> dict:
        """Return video introduction"""
        if self.return_code != 0 or self.response_code != 200:
            return {'response_code': self.response_code, 'return_code': self.return_code}
        # 获取简介
        VideoIntroduction = self.MainData['data']['desc'].strip('\r')
        # 返回结果
        return {'response_code': self.response_code, 'return_code': self.return_code,
                'introduction': VideoIntroduction}

    def video_data(self) -> dict:
        """Return video data"""
        if self.return_code != 0 or self.response_code != 200:
            return {'response_code': self.response_code, 'return_code': self.return_code}
        VideoDataDict = {'view': 'view', 'danmaku': 'danmaku', 'like': 'like', 'dislike': 'dislike',
                         'reply': 'reply', 'coin': 'coin', 'collect': 'favorite', 'share': 'share'}
        return {'response_code': self.response_code, 'return_code': self.return_code,
                **extractor(data = self.MainData['data']['stat'], dicts = VideoDataDict)}

    def video_part(self) -> dict:
        if self.return_code != 0 or self.response_code != 200:
            return {'response_code': self.response_code, 'return_code': self.return_code}
        PartDict = {'name': 'part', 'cid': 'cid', 'length': 'duration'}
        PartList = []
        for Index in self.MainData['data']['pages']:
            Part = extractor(Index, PartDict)
            Part['length'] = TickToMinute(Part['length'])
            PartList.append(Part)
        return {'response_code': self.response_code, 'return_code': self.return_code, 'part': PartList}
    