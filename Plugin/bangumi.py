from Plugin.tool import extractor
import requests
import json


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
        DataDict = {'coin': 'coins', 'danmaku': 'danmakus', 'watching': 'series_follow'}
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                **extractor(data = JsonData['result'], dicts = DataDict)}

    @staticmethod
    def get_top_video(tag_id: int, page: int = 1, page_size: int = 10) -> dict:
        Data = requests.get(f'https://api.bilibili.com/x/web-interface/tag/top?pn={page}&ps={page_size}&tid={tag_id}')
        JsonData = json.loads(Data.text)
        VideoInfoDict = {'aid': 'aid', 'bvid': 'bvid', 'title': 'title', 'tname': 'tname',
                         'copyrights': 'copyright', 'upload_time': 'pubdate'}
        VideoDataDict = {'view': 'view', 'danmaku': 'danmaku', 'like': 'like', 'dislike': 'dislike',
                         'reply': 'reply', 'coin': 'coin', 'collect': 'favorite', 'share': 'share'}
        VideoList = []
        for Video in JsonData['data']:
            VideoList.append({**extractor(data = Video, dicts = VideoInfoDict),
                              **extractor(data = Video['stat'], dicts = VideoDataDict)})
        return {'return_code': Data.status_code, 'response_code': JsonData['code'], 'videos': VideoList}

    @staticmethod
    def get_tag_id(name: str) -> dict:
        Data = requests.get(f'https://api.bilibili.com/x/tag/info?tag_name={name}')
        JsonData = json.loads(Data.text)
        return {'response_code': Data.status_code, 'return_code': JsonData['code'],
                'tag_id': JsonData['data']['tag_id']}

    @staticmethod
    def get_episodes(season_id: int) -> dict:
        Data = requests.get(f'https://api.bilibili.com/pgc/web/season/section?season_id={season_id}', )
        JsonDATA = json.loads(Data.text)
        EpisodeDict = {'aid': 'aid', 'title': 'long_title', 'episode_id': 'id', 'short_title': 'title'}
        MainEpisodes = []
        for MainEpisode in JsonDATA['result']['main_section']['episodes']:
            MainEpisodes.append(extractor(data = MainEpisode, dicts = EpisodeDict))
        OtherEpisodes = []  # 其它剧集的分支列表
        for OtherEpisode in JsonDATA['result']['section']:
            Episodes = []  # 剧集分支的具体剧集列表
            for range_var3 in OtherEpisode['episodes']:
                Episodes.append(extractor(data = range_var3, dicts = EpisodeDict))
            OtherEpisodes.append(Episodes)
        return {'response_code': Data.status_code, 'return_code': JsonDATA['code'],
                'main_episodes': MainEpisodes, 'other_epidoses': OtherEpisodes}
