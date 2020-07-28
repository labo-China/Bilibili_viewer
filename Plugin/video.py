# -*- coding: UTF-8 -*-
import requests
import json
import time
from Plugin.tool import extractor, format_time, TickToMinute, av2bv


class video:
    """Get Bilibili video"""

    def __init__(self, code, num):
        # 获取视频全部信息
        self.MainData = requests.get(f'https://api.bilibili.com/x/web-interface/view?{code}={num}')
        self.code = code
        self.num = num
        # 获取请求资源码
        self.response_code = self.MainData.status_code
        self.MainData = json.loads(self.MainData.text)
        # 获取网站返回码
        self.return_code = self.MainData['code']

    def video_info(self) -> dict:
        """Return video info"""
        if self.return_code != 0 or self.response_code != 200:
            return {'response_code': self.response_code, 'return_code': self.return_code}
        VideoInfoDict = {'upload_time': 'pubdate', 'owner': ['owner', 'name']}
        VideoInfoList = ['aid', 'bvid', 'title', 'tname', 'copyright']
        Data = extractor(data = self.MainData['data'], dicts = VideoInfoDict, copy_list = VideoInfoList)
        Data['copyright'] = '自制' if Data['copyright'] == 1 else '转载'
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

    def get_replies(self, sort, pn) -> dict:
        num = bv2av('BV' + self.num) if self.code == 'bvid' else self.num
        Data = requests.get(f'http://api.bilibili.com/x/v2/reply?pn={pn}&type=1&sort={sort}&oid={num}')
        JsonData = json.loads(Data.text)
        all_page = int(JsonData['data']['page']['count'])
        all_page = all_page / 20 if all_page / 20 == int(all_page / 20) else int(all_page / 20) + 1

        ReplyList = []
        ReplyDict = {'name': ['member', 'uname'], 'level': ['member', 'level_info', 'current_level'],
                     'sex': ['member', 'sex'], 'official': ['member', 'official_verify', 'desc'],
                     'like': 'like', 'reply': 'rcount', 'upload_time': 'ctime', 'content': ['content', 'message'],
                     'up_like': ['up_action', 'like'], 'up_reply': ['up_action', 'reply']}
        for Replies in JsonData['data']['replies']:
            ReplyList.append({**extractor(data = Replies, dicts = ReplyDict), 'replies': []})
            if Replies['replies']:
                for ChildReplies in Replies['replies']:
                    ReplyList[len(ReplyList) - 1]['replies'].append(
                        {**extractor(data = ChildReplies, dicts = ReplyDict), 'replies': []})
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                'replies': ReplyList, 'all_page': all_page}

    def get_tags(self) -> dict:
        Data = requests.get(f'https://api.bilibili.com/x/web-interface/view/detail/tag?{self.code}={self.num}')
        JsonData = json.loads(Data.text)
        TagList = []
        TagDict = {'upload_time': 'ctime', 'dislike': 'hates', 'like': 'likes', 'content': 'short_content',
                   'follower': 'subscribed_count', 'tag_id': 'tag_id', 'name': 'tag_name', 'type': 'tag_type'}
        for tags in JsonData['data']:
            TagList.append(extractor(data = tags, dicts = TagDict))
        return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'tag_list': TagList}

    def get_questions(self, edge_id: int = None) -> dict:
        num = 'BV' + self.num if self.code == 'bvid' else self.num
        Url = f'https://api.bilibili.com/x/stein/edgeinfo_v2?{self.code}={num}&graph_version=303884' +\
              (f'&edge_id={edge_id}' if edge_id else '')
        Data = requests.get(Url)
        JsonData = json.loads(Data.text)
        QuestionList = []

        QuestionDict = {'cid': 'cid', 'edge_id': 'id', 'is_default': 'is_default', 'content': 'option'}
        for Questions in JsonData['data']['edges']['questions']:
            ChoiceList = []
            for Choices in Questions['choices']:
                ChoiceList.append(extractor(data = Choices, dicts = QuestionDict))
            QuestionList.append(ChoiceList)
        return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'question_list': QuestionList}
