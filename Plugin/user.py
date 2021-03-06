# -*- coding: UTF-8 -*-
from Plugin.tool import extractor, format_time, av2bv
import requests
import json


class user:
    """Get Bilibili User"""

    def __init__(self, user_uid):
        # 定义请求头
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
        # 定义uid
        self.user_uid = user_uid

    def user_info(self):
        """Return user`s basic info"""
        # 请求用户基础信息
        Data = requests.get(f'https://api.bilibili.com/x/space/acc/info?mid={self.user_uid}',
                            headers = self.headers)
        # 获取请求资源码
        response_code = Data.status_code
        Data = json.loads(Data.text)
        # 获取网站返回码
        return_code = Data['code']
        if response_code != 200 or return_code != 0:  # 如果返回码错误，则返回空数据
            return {'response_code': response_code, 'return_code': return_code}
        InfoDict = {'name': 'name', 'sex': 'sex', 'sign': 'sign', 'level': 'level', 'birthday': 'birthday',
                    'fans_badge': 'fans_badge', 'official': ['official', 'title'], 'vip': ['vip', 'status']}
        return {'response_code': response_code, 'return_code': return_code,
                **extractor(Data['data'], dicts = InfoDict)}
        # user_coins = user_info['data']['coins']  # 硬币(未实现调用cookie所以隐藏)

    def user_follows(self):
        Data = requests.get(f'https://api.bilibili.com/x/relation/stat?vmid={self.user_uid}')
        JsonData = json.loads(Data.text)
        FollowCopyList = ['black', 'follower', 'following']
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                **extractor(data = JsonData['data'], copy_list = FollowCopyList)}

    def user_top_video(self):
        """返回用户的置顶视频"""
        Data = requests.get(f'https://api.bilibili.com/x/space/top/arc?vmid={self.user_uid}', headers = self.headers)
        JsonData = json.loads(Data.text)
        if Data.status_code != 200 or JsonData['code'] != 0:  # 判断是否有置顶视频
            return {'response_code': Data.status_code, 'return_code': JsonData['code']}
        TopVideoDict = {'aid': 'aid', 'bvid': 'bvid', 'tname': 'tname', 'copyright': 'copyright', 'title': 'title',
                        'upload_time': 'ctime', 'introduction': 'desc', 'view': 'view', 'danmaku': 'danmaku',
                        'reply': 'reply', 'like': 'like', 'dislike': 'dislike', 'coin': 'coin', 'collect': 'favorite',
                        'share': 'share'}
        ReturnData = extractor(data = {**JsonData['data'], **JsonData['data']['stat']}, dicts = TopVideoDict)
        ReturnData['upload_time'] = int(ReturnData['upload_time'])
        return {'response_code': Data.status_code, 'return_code': JsonData['code'], **ReturnData}

    def user_video(self, pn):
        """Return user`s video list"""
        Data = requests.get(f'http://space.bilibili.com/ajax/member/getSubmitVideos?mid={self.user_uid}&page={pn}',
                            headers = self.headers)
        JsonData = json.loads(Data.text)
        VideoList = []
        Page = JsonData['data']['pages']
        VideoDict = {'title': 'title', 'reply': 'comment', 'view': 'play', 'upload_time': 'created',
                     'danmaku': 'video_review', 'introduction': 'description', 'length': 'length',
                     'collect': 'favorites', 'aid': 'aid'}
        for Video in JsonData['data']['vlist']:
            video = extractor(data = Video, dicts = VideoDict)
            video['bvid'] = av2bv(video['aid'])
            VideoList.append(video)
        return {'response_code': Data.status_code, 'return_code': 0 if JsonData['status'] else -1,
                'pages': Page, 'data': VideoList}
