import requests
import json
import time

class video:
    def __init__(self,code,num):
        # 定义请求头
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.43 Safari/537.36 Edg/81.0.416.28',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q = 0.9'}
        # 获取视频全部信息
        self.main_data = requests.get('https://api.bilibili.com/x/web-interface/view?{}={}'.format(code, num),headers=self.headers)
        # 获取请求资源码
        self.response_code = self.main_data.status_code
        self.main_data = json.loads(self.main_data.text)
        # 获取网站返回码
        self.return_code = self.main_data['code']

    def video_info(self):
        if self.return_code == -404 or self.return_code == -400 or self.return_code == 62002:
            return {'response_code': self.response_code, 'return_code': self.return_code, 'aid': '',
                    'bvid': '', 'owner': '', 'title': '', 'zone_name': '', 'copyrights': '', 'upload_time': ''}
        # 获取av，bv号
        video_aid = self.main_data['data']['aid'] # av号
        video_bvid = self.main_data['data']['bvid'] # bv号
        # 获取UP主名字，标题，视频分区
        video_owner = self.main_data['data']['owner']['name']  # 名字
        video_title = self.main_data['data']['title']  # 标题
        video_zone_name = self.main_data['data']['tname']  # 分区
        if self.main_data['data']['copyright'] == 1:  # 视频版权
            video_copyrights = '自制'
        else:
            video_copyrights = '转载'
        # 如果视频分区为空就返回未知
        if video_zone_name == '':
            video_zone_name = '未知'
        # 格式化Unix时间戳为正常时间
        video_upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.main_data['data']['pubdate']))  # 上传时间
        # 返回结果
        return {'response_code' : self.response_code, 'return_code' : self.return_code, 'aid' : video_aid,
                'bvid': video_bvid, 'owner': video_owner, 'title': video_title, 'zone_name': video_zone_name,
                'copyrights': video_copyrights, 'upload_time': video_upload_time}

    def introduction(self):
        if self.return_code == -404 or self.return_code == -400 or self.return_code == 62002:
            return {'response_code' : self.response_code, 'return_code' : self.return_code, 'introduction' : ''}
        # 获取简介
        video_introduction = self.main_data['data']['desc'].strip('\r')
        # 返回结果
        return {'response_code' : self.response_code, 'return_code' : self.return_code, 'introduction' : video_introduction}

    def video_data(self):
        if self.return_code == -404 or self.return_code == -400 or self.return_code == 62002:
            return {'response_code': self.response_code, 'return_code': self.return_code, 'view': '',
                    'danmaku': '', 'like': '', 'dislike': '', 'reply': '',
                    'coin': '', 'collect': '', 'share': ''}
        # 获取浏览，弹幕，评论，点赞，踩，硬币，收藏，分享
        video_view = self.main_data['data']['stat']['view']  # 浏览
        video_danmaku = self.main_data['data']['stat']['danmaku']  # 弹幕
        video_reply = self.main_data['data']['stat']['reply']  # 评论
        video_like = self.main_data['data']['stat']['like']  # 点赞
        video_dislike = self.main_data['data']['stat']['dislike']  # 踩
        video_coin = self.main_data['data']['stat']['coin']  # 硬币
        video_collect = self.main_data['data']['stat']['favorite']  # 收藏
        video_share = self.main_data['data']['stat']['share']  # 分享
        # 返回结果
        return {'response_code' : self.response_code, 'return_code' : self.return_code, 'view' : video_view,
                'danmaku' : video_danmaku, 'like' : video_like, 'dislike' : video_dislike, 'reply' : video_reply,
                'coin' : video_coin, 'collect' : video_collect, 'share' : video_share}

    def video_part(self):
        if self.return_code == -404 or self.return_code == -400 or self.return_code == 62002:
            return {'response_code': self.response_code, 'return_code': self.return_code,
                    'name': '', 'cid': '', 'length': ''}
        # 获取分P数
        # video_part = self.main_data['data']['videos']
        video_part_name = [] # 分P名称
        video_part_cid = [] # 分P cid
        video_part_length = [] # 分P视频长度
        # 开始循环访问字典添加数据
        for video_part in self.main_data['data']['pages']:
            video_part_name.append(video_part['part'])
            video_part_cid.append(video_part['cid'])
            # 处理时间戳
            video_part_length.append(
                ('{}:{}'.format(str((int(video_part['duration'] / 60))).zfill(2),
                                str(video_part['duration'] % 60).zfill(2))))
        # 返回数据
        return {'response_code' : self.response_code, 'return_code' : self.return_code,
                'name' : video_part_name, 'cid' : video_part_cid, 'length' :video_part_length}