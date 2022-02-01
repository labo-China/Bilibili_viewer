# coding: UTF-8
import requests
import json
from scripts.data_process import extractor
from math import ceil


class bangumi:

    @staticmethod
    def get_bangumi_info(media_id: int) -> dict:
        Data = requests.get(f'https://api.bilibili.com/pgc/review/user?media_id={media_id}')
        JsonData = json.loads(Data.text)
        InfoDict = {'title': 'title', 'season_id': 'season_id', 'new_ep': ['new_ep', 'id'],
                    'num': ['new_ep', 'index'], 'score': ['rating', 'score'], 'score_count': ['rating', 'count'],
                    'area': ['areas', 0, 'name']}
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                **extractor(data = JsonData['result']['media'], dicts = InfoDict)}

    @staticmethod
    def get_bangumi_data(season_id: int) -> dict:
        Data = requests.get(f'https://api.bilibili.com/pgc/web/season/stat?season_id={season_id}')
        JsonData = json.loads(Data.text)
        DataDict = {'view': 'views', 'coin': 'coins', 'danmaku': 'danmakus', 'follower': 'series_follow'}
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                **extractor(data = JsonData['result'], dicts = DataDict)}

    @staticmethod
    def get_bangumi_data_by_html(media_id: int) -> dict:
        # 由于某些信息在开播前就已确定,可能直接被B站写进了HTML里,暂时没有找到相关api
        Data = requests.get(f'https://www.bilibili.com/bangumi/media/md{media_id}')
        from re import findall, compile

        PublishPattern = compile(
            r'"publish":{"is_finish":(.),"is_started":(.),"pub_date":"(.*?)","pub_date_show":"(.*?)",'
            r'"release_date_show":"(.*?)","time_length_show":"(.*?)"}')
        PublishTuple = findall(PublishPattern, Data.text)[0]
        PublishData = {'finish': PublishTuple[0], 'start': PublishTuple[1], 'upload_time': PublishTuple[2],
                       'start_time': PublishTuple[3], 'update_time': PublishTuple[4]}

        TagTuple = findall('<span class="media-tag">(.*?)</span>+', Data.text)

        Introduction = findall('"evaluate":"(.*?)"', Data.text)[0]
        return {'response_code': Data.status_code, 'return_code': 0,
                **PublishData, 'tag_list': TagTuple, 'introduction': Introduction}

    @staticmethod
    def get_relate_video(tag_id: int, page_size: int = 10) -> dict:
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

    @staticmethod
    def get_tag_id(name: str) -> dict:
        Data = requests.get(f'https://api.bilibili.com/x/tag/info?tag_name={name}')
        JsonData = json.loads(Data.text)
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                'tag_id': JsonData['data']['tag_id']}

    @staticmethod
    def get_episodes(season_id: int) -> dict:
        Data = requests.get(f'https://api.bilibili.com/pgc/web/season/section?season_id={season_id}', )
        JsonData = json.loads(Data.text)
        if not JsonData['result']['section']:
            return {'response_code': Data.status_code, 'return_code': -1, 'main_episodes': [], 'other_episodes': []}
        EpisodeDict = {'aid': 'aid', 'title': 'long_title', 'episode_id': 'id', 'short_title': 'title'}
        MainEpisodes = []
        for MainEpisode in JsonData['result']['main_section']['episodes']:
            MainEpisodes.append(extractor(data = MainEpisode, dicts = EpisodeDict))
        OtherEpisodes = []  # 其它剧集的分支列表
        for OtherEpisode in JsonData['result']['section']:
            Episodes = []  # 剧集分支的具体剧集列表
            for range_var3 in OtherEpisode['episodes']:
                Episodes.append(extractor(data = range_var3, dicts = EpisodeDict))
            OtherEpisodes.append(Episodes)
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                'main_episodes': MainEpisodes, 'other_episodes': OtherEpisodes}

    @staticmethod
    def get_replies(media_id: int, reply_type: str = 'short', sort: 'int, str' = 0, page_size: int = 20):
        """
        获取番剧的长/短评\n
        :param media_id: 番剧的media_id
        :param reply_type: 获取的评论类型(short为短评,long为长评)(short)
        :param sort: 评论的排序(1为最新,0为默认)(0)
        :param page_size: 一次请求返回的评论数量(20)
        """
        BaseUrl = 'https://api.bilibili.com/pgc/review/{}/list?media_id={}&ps={}&sort={}'
        Page = ceil(
            json.loads(requests.get(BaseUrl.format(reply_type, media_id, page_size, sort)).text)['data']['total'] / 20)
        cursor = None
        ShortReplyDict = {'name': ['author', 'uname'], 'uid': 'mid', 'vip_status': ['vip', 'vipStatus'],
                          'content': 'content', 'upload_time': 'mtime', 'progress': 'progress', 'score': 'score',
                          'like': ['stat', 'likes']}
        LongReplyDict = {**ShortReplyDict, 'reply': ['stat', 'reply'], 'url': 'url'}

        for index in range(Page):
            Url = BaseUrl.format(reply_type, media_id, page_size, sort) + (f'&cursor={cursor}' if cursor else '')
            Data = requests.get(Url)
            JsonData = json.loads(Data.text)
            cursor = JsonData['data']['next']
            ReplyList = []

            for replies in JsonData['data']['list']:
                ReplyList.append(
                    extractor(data = replies, dicts = ShortReplyDict if reply_type == 'short' else LongReplyDict))
            yield {'response_code': Data.status_code, 'return_code': JsonData['code'],
                   'total': JsonData['data']['total'],
                   'cursor': JsonData['data']['next'], 'replies': ReplyList}

    @staticmethod
    def get_recommends(season_id: int) -> dict:
        Data = requests.get(f'https://api.bilibili.com/pgc/web/recommend/related/recommend?season_id={season_id}')
        JsonData = json.loads(Data.text)
        ReturnData = {'original': [], 'recommend': []}
        # 获取原作漫画
        OriginalDict = {'message1': 'desc1', 'message2': 'desc2', 'item_id': 'item_id',
                        'status': 'label', 'title': 'title', 'tname': 'tname', 'url': 'url'}
        for originals in JsonData['result']['relates']:
            original = extractor(data = originals, dicts = OriginalDict)
            original['messages'] = [original['message1'], original['message2']]
            del original['message1'], original['message2']
            ReturnData['original'].append(original)
        # 获取推荐番剧
        RecommendDict = {'title': 'title', 'season_id': 'season_id', 'new_ep': ['new_ep', 'id'],
                         'num': ['new_ep', 'index'], 'score': ['rating', 'score'], 'score_count': ['rating', 'count'],
                         'danmaku': ['stat', 'danmaku'], 'follow': ['stat', 'follow'], 'view': ['stat', 'view']}
        for recommend in JsonData['result']['season']:
            ReturnData['recommend'].append(extractor(data = recommend, dicts = RecommendDict))

        return {'response_code': Data.status_code, 'return_code': JsonData['code'], **ReturnData}

    @staticmethod
    def get_status(season_id: int) -> dict:
        Data = requests.get(f'https://api.bilibili.com/pgc/view/web/season/user/status?season_id={season_id}')
        JsonData = json.loads(Data.text)
        StatusDict = {'area_limit': 'area_limit', 'is_baned': 'ban_area_show', 'title': ['dialog', 'title'],
                      'aid': ['paster', 'aid'], 'cid': ['paster', 'cid'], 'length': ['paster', 'duration'],
                      'url': ['paster', 'url']}
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                **extractor(data = JsonData['result'], dicts = StatusDict)}
