from Plugin.tool import *
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

    def user_top_video(self):
        """返回用户的置顶视频"""
        # 请求用户置顶视频
        TopVideo = requests.get(f'https://api.bilibili.com/x/space/top/arc?vmid={self.user_uid}',
                                headers = self.headers)
        # 获取请求资源码
        response_code = TopVideo.status_code
        TopVideo = json.loads(TopVideo.text)
        # 获取网站返回码
        return_code = TopVideo['code']
        if return_code != 0 or return_code != 0:  # 判断是否有置顶视频
            return {'response_code': response_code, 'return_code': return_code}
        TopVideoDict = {'aid': 'aid', 'bvid': 'bvid', 'tname': 'tname', 'copyright': 'copyright',
                        'title': 'title', 'upload_time': 'ctime', 'introduction': 'desc'}
        TopVideoData = {'view': 'view', 'danmaku': 'danmaku', 'reply': 'reply', 'like': 'like',
                        'dislike': 'dislike', 'coin': 'coin', 'collect': 'favorite', 'share': 'share'}
        TopVideo = {**extractor(TopVideo['data'], TopVideoDict), **extractor(TopVideo['data']['stat'], TopVideoData)}
        TopVideo['upload_time'] = format_time(TopVideo['upload_time'])
        return {'response_code': response_code, 'return_code': return_code, **TopVideo}

    def user_video(self, pn):
        """Return user`s video list"""
        VideoList = []
        # 获取用户视频列表
        VideoListData = json.loads(
            requests.get(f'http://space.bilibili.com/ajax/member/getSubmitVideos?mid={self.user_uid}&page={pn}',
                         headers = self.headers).text)
        # 获取数据
        Page = VideoListData['data']['pages']
        VideoDict = {'title': 'title', 'reply': 'comment', 'view': 'play', 'upload_time': 'created',
                     'danmaku': 'video_review', 'introduction': 'description', 'length': 'length',
                     'collect': 'favorites', 'aid': 'aid'}
        for Video in VideoListData['data']['vlist']:
            video = extractor(Video, VideoDict)
            video['bvid'] = av2bv(video['aid'])
            video['upload_time'] = format_time(video['upload_time'])
            VideoList.append(video)
        return {'pages': Page, 'data': VideoList}
