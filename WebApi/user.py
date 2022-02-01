# coding: UTF-8
import requests
import json
from scripts.data_process import extractor, av2bv
from scripts.tool import parseable as psb


def get_login_url():
    Data = requests.get('https://passport.bilibili.com/qrcode/getLoginUrl')
    JsonData = json.loads(Data.text)
    if Data.status_code != 200 or JsonData['code'] != 0:
        return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'url': Data.url}
    ReturnData = JsonData['data']['url']
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], 'url': ReturnData}


def get_login_info():
    Data = requests.post('https://passport.bilibili.com/qrcode/getLoginInfo')
    JsonData = json.loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData.get('code'), 'cookies': Data.cookies}


def tmp():
    import qrcode
    import PIL
    import io
    url = get_login_url()
    s = io.StringIO
    # a = qrcode.make(url).save(s)
    # print(a)


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
        # user_coins = user_info['data']['coins']  # 硬币(未实现获取SESSDATA所以隐藏)

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
        # Data = requests.get(f'http://space.bilibili.com/ajax/member/getSubmitVideos?mid={self.user_uid}&page={pn}',
        #                    headers = self.headers)
        Data = requests.get(f'https://api.bilibili.com/x/space/arc/search'
                            f'?mid={self.user_uid}&ps=30&tid=0&pn={pn}&keyword=&order=pubdate')
        response_code = Data.status_code
        JsonData = json.loads(Data.text)
        return_code = JsonData['code']
        VideoList = []
        Page = JsonData['data']['page']['count']
        VideoDict = {'title': 'title', 'reply': 'comment', 'view': 'play', 'upload_time': 'created',
                     'danmaku': 'video_review', 'introduction': 'description', 'length': 'length',
                     'collect': 'favorites', 'aid': 'aid'}
        for Video in JsonData['data']['list']['vlist']:
            video = extractor(data = Video, dicts = VideoDict)
            video['bvid'] = av2bv(video['aid'])
            VideoList.append(video)
        return {'response_code': response_code, 'return_code': return_code,
                'pages': Page, 'data': VideoList}
