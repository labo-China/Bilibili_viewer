# coding: UTF-8
import requests
import json
from scripts.tool import extractor, TickToMinute, bv2av, ceil
from scripts.tool import parseable as psb


def get_raw(code: psb, num: psb) -> dict:
    code = 'av' if code == 'aid' else ('bv' if code == 'bvid' else code)
    req = requests.get(f'http://www.bilibili.com/video/{code}{num}')
    return {'response_code': req.status_code, 'return_code': 0, 'raw_content': req.text}


def get_info(code: psb, num: psb) -> dict:
    """Return video info"""
    Data = requests.get(f'https://api.bilibili.com/x/web-interface/view?{code}={num}')
    JsonData = json.loads(Data.text)
    if JsonData['code'] != 0 or Data.status_code != 200:
        return {'response_code': JsonData['code'], 'return_code': Data.status_code, 'url': Data.url}
    VideoInfoDict = {'upload_time': 'pubdate', 'owner': ['owner', 'name']}
    VideoInfoList = ['aid', 'bvid', 'title', 'tname', 'copyright']
    ReturnData = extractor(data = JsonData['data'], dicts = VideoInfoDict, copy_list = VideoInfoList)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], **ReturnData, 'url': Data.url}


def get_introduction(code: psb, num: psb) -> dict:
    """Return video introduction"""
    Data = requests.get(f'https://api.bilibili.com/x/web-interface/archive/desc?{code}={num}')
    JsonData = json.loads(Data.text)
    if JsonData['code'] != 0 or Data.status_code != 200:
        return {'response_code': JsonData['code'], 'return_code': Data.status_code, 'url': Data.url}
    ReturnData = {'introduction': JsonData['data']}  # 这里数据不复杂,就不用extractor了
    return {'response_code': JsonData['code'], 'return_code': Data.status_code, **ReturnData, 'url': Data.url}


def get_data(code: psb, num: psb) -> dict:
    """Return video data"""
    Data = requests.get(f'https://api.bilibili.com/x/web-interface/archive/stat?{code}={num}')
    JsonData = json.loads(Data.text)
    if JsonData['code'] != 0 or Data.status_code != 200:
        return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'url': Data.url}
    VideoDataDict = {'view': 'view', 'danmaku': 'danmaku', 'like': 'like', 'dislike': 'dislike',
                     'reply': 'reply', 'coin': 'coin', 'collect': 'favorite', 'share': 'share'}
    ReturnData = extractor(data = self.JsonData['data'], dicts = VideoDataDict)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], **ReturnData, 'url': Data.url}


def get_part(code: psb, num: psb) -> dict:
    Data = requests.get(f'https://api.bilibili.com/x/player/pagelist?{code}={num}')
    JsonData = json.loads(Data.text)
    if JsonData['code'] != 0 or Data.status_code != 200:
        return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'url': Data.url}
    PartDict = {'name': 'part', 'cid': 'cid', 'length': 'duration'}
    PartList = []
    for Index in JsonData['data']:
        Part = extractor(Index, PartDict)
        Part['length'] = TickToMinute(Part['length'])
        PartList.append(Part)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'part': PartList, 'url': Data.url}


def get_reply(aid: psb, page: psb, sort: psb):
    Data = requests.get(f'http://api.bilibili.com/x/v2/reply?pn={page}&type=1&sort={sort}&oid={aid}')
    JsonData = json.loads(Data.text)
    if Data.status_code != 200 or JsonData['code'] != 0:
        return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'url': Data.url}
    ReplyDict = {'name': ['member', 'uname'], 'level': ['member', 'level_info', 'current_level'],
                 'sex': ['member', 'sex'], 'official': ['member', 'official_verify', 'desc'],
                 'like': 'like', 'reply': 'rcount', 'upload_time': 'ctime', 'content': ['content', 'message'],
                 'up_like': ['up_action', 'like'], 'up_reply': ['up_action', 'reply']}
    ReplyList = []

    for Replies in JsonData['data']['replies']:
        ReplyList.append({**extractor(data = Replies, dicts = ReplyDict), 'replies': []})
        if Replies['replies']:
            for ChildReplies in Replies['replies']:
                ReplyList[len(ReplyList) - 1]['replies'].append(
                    {**extractor(data = ChildReplies, dicts = ReplyDict), 'replies': []})
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'replies': ReplyList, 'url': Data.url}


def get_tags(code: psb, num: psb) -> dict:
    Data = requests.get(f'https://api.bilibili.com/x/web-interface/view/detail/tag?{code}={num}')
    JsonData = json.loads(Data.text)
    TagList = []
    TagDict = {'upload_time': 'ctime', 'dislike': 'hates', 'like': 'likes', 'content': 'short_content',
               'follower': 'subscribed_count', 'tag_id': 'tag_id', 'name': 'tag_name', 'type': 'tag_type'}
    if JsonData['data']:
        for tags in JsonData['data']:
            TagList.append(extractor(data = tags, dicts = TagDict))
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'tag_list': TagList, 'url': Data.url}


def get_questions(aid: psb, bvid: psb, edge_id: psb = None) -> dict:
    from re import findall
    cid = get_part(code = 'aid', num = aid)['part'][0]['cid']
    graph_url = 'https://api.bilibili.com/x/player.so?id=cid%3A{}&aid={}&bvid={}'
    graph_resp = requests.get(graph_url.format(cid, aid, bvid), headers = {'referer': 'https://www.bilibili.com/'})
    if 'graph_version' not in graph_resp.text:
        return {'response_code': graph_resp.status_code, 'return_code': -1}
    graph_version = findall('\"graph_version\":(.*?),', graph_resp.text)[0]
    Url = f'https://api.bilibili.com/x/stein/edgeinfo_v2?aid={aid}&graph_version={graph_version}' + \
          (f'&edge_id={edge_id}' if edge_id else '')
    Data = requests.get(Url)
    JsonData = json.loads(Data.text)
    QuestionList = []

    QuestionDict = {'cid': 'cid', 'edge_id': 'id', 'is_default': 'is_default', 'content': 'option'}
    if 'questions' in JsonData['data']['edges']:
        for Questions in JsonData['data']['edges']['questions']:
            ChoiceList = []
            for Choices in Questions['choices']:
                ChoiceList.append(extractor(data = Choices, dicts = QuestionDict))
            QuestionList.append(ChoiceList)
    else:
        QuestionList = []
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            'question_list': QuestionList, 'url': Url}


def get_video_download_url(code: psb, num: psb, quality: psb = 80) -> dict:
    import hashlib
    part_dict = get_part(code = code, num = num)['part']
    cid_list = [part['cid'] for part in part_dict]
    for cid in cid_list:
        params = 'appkey=iVGUTjsxvpLeuDCf&cid=%s&otype=json&qn=%s&quality=%s&type=' % (cid, quality, quality)
        chksum = hashlib.md5(bytes(params + 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt', 'utf8')).hexdigest()
        url = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
        referer = f'https://www.bilibili.com/video/{"av" if code == "aid" else "bvid"}{num}'
        url_dict = json.loads(requests.get(url).text)['durl']
        return_url, return_size = [urls['url'] for urls in url_dict], [size['size'] for size in url_dict]
        yield {'url': return_url, 'size': return_size, 'referer': referer, 'cid': cid}


def get_danmaku_download_url(cid: psb) -> dict:
    return {'url': f'https://comment.bilibili.com/{cid}.xml'}


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

    def get_replies(self, sort) -> dict:
        num = bv2av('BV' + self.num) if self.code == 'bvid' else self.num
        BaseUrl = 'http://api.bilibili.com/x/v2/reply?pn={}&type=1&sort={}&oid={}'
        Page = ceil(json.loads(requests.get(BaseUrl.format(1, sort, num)).text)['data']['page']['acount'] / 20)
        ReplyDict = {'name': ['member', 'uname'], 'level': ['member', 'level_info', 'current_level'],
                     'sex': ['member', 'sex'], 'official': ['member', 'official_verify', 'desc'],
                     'like': 'like', 'reply': 'rcount', 'upload_time': 'ctime', 'content': ['content', 'message'],
                     'up_like': ['up_action', 'like'], 'up_reply': ['up_action', 'reply']}

        for Index in range(1, Page + 1):
            Data = requests.get(BaseUrl.format(Index, sort, num))
            JsonData = json.loads(Data.text)
            ReplyList = []

            for Replies in JsonData['data']['replies']:
                ReplyList.append({**extractor(data = Replies, dicts = ReplyDict), 'replies': []})
                if Replies['replies']:
                    for ChildReplies in Replies['replies']:
                        ReplyList[len(ReplyList) - 1]['replies'].append(
                            {**extractor(data = ChildReplies, dicts = ReplyDict), 'replies': []})
            yield {'response_code': Data.status_code, 'return_code': JsonData['code'],
                   'replies': ReplyList, 'page': Page}

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
        Url = f'https://api.bilibili.com/x/stein/edgeinfo_v2?{self.code}={num}&graph_version=303884' + \
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
