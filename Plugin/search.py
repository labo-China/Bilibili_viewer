import time
import requests
import json
import re
class new_search:
    def __init__(self,keyword : str, search_type : str = 'all', page : int = 1):
        if search_type == 'all':
            self.main_data = requests.get('https://api.bilibili.com/x/web-interface/search/all/v2?page={}&keyword={}&highlight=1&jsonp=jsonp'.format(page,keyword))
        else:
            self.main_data = requests.get('https://api.bilibili.com/x/web-interface/search/type?search_type={}&page={}&keyword={}&jsonp=jsonp'.format(search_type,page,keyword))
        self.search_type = search_type
        self.response_code = self.main_data.status_code
        self.main_data = json.loads(self.main_data.text)
        self.return_code = self.main_data['code']

    def get_pages(self):
        return self.main_data['data']['numPages']

    def get_video(self):
        return_data = []
        result_data = self.__get_data__('video')
        for range_var in result_data:
            video_data = {}
            title = range_var['title'].replace('<em class="keyword">', '<')
            video_data['title'] = title.replace('</em>', '>')
            video_data['aid'] = range_var['aid']
            video_data['bvid'] = range_var['bvid']
            video_data['danmaku'] =range_var['video_review']
            video_data['introduction'] = range_var['description']
            video_data['length'] = range_var['duration']
            video_data['collect'] = range_var['favorites']
            video_data['view'] = range_var['play']
            video_data['reply'] = range_var['review']
            video_data['upload_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(range_var['pubdate']))
            video_data['tag'] = range_var['tag']
            video_data['tname'] = range_var['typename']
            return_data.append(video_data)
        return return_data

    def get_user(self):
        result_data = self.__get_data__('bili_user')
        return_data = []
        for range_var in result_data:
            user_data = {'name': range_var['uname'], 'level': range_var['level'], 'uid': range_var['mid'],
                         'official': range_var['official_verify']['desc'], 'fans': range_var['fans'],
                         'video_count': range_var['videos'], 'sign': range_var['usign']}
            if range_var['gender'] == 1: user_data['sex'] = '男'
            elif range_var['gender'] == 2: user_data['sex'] = '女'
            else: user_data['sex'] = '保密'
            if range_var['is_live'] == 1: user_data['live'] = True
            else: user_data['live'] = False
            if range_var['is_upuser'] == 1: user_data['upuser'] = True
            else: user_data['upuser'] = False
            user_data['top_video'] = []
            for top_videos in range_var['res']:
                top_video = {'aid': top_videos['aid'], 'bvid': top_videos['bvid'], 'title' : top_videos['title'],
                             'coin': top_videos['coin'], 'introduction': top_videos['desc'], 'collect': top_videos['fav'],
                             'length': top_videos['duration'], 'view': top_videos['play'], 'danmaku': top_videos['dm'],
                             'upload_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(top_videos['pubdate']))}
                user_data['top_video'].append(top_video)
            return_data.append(user_data)
        return return_data

    def __get_data__(self,data_type):
        if self.search_type == 'all':
            for range_var in self.main_data['data']['result']:
                if range_var['result_type'] == data_type:
                    return range_var['data']
            return None
        else:
            return self.main_data['data']['result']
class search:
    def __init__(self,search_word,search_type='all'):
        # 定义请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.43 Safari/537.36 Edg/81.0.416.28',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'}
        # 初始化各方法搜索状态
        self.video_detect = False
        self.bangumi_detect = False
        self.pgc_detect = False
        self.live_detect = False
        self.article_detect = False
        self.topic_detect = False
        self.photo_detect = False
        self.upuser_detect = False
        # 请求搜索结果
        self.main_data = requests.get('https://search.bilibili.com/{}?keyword={}'.format(search_type, search_word), headers = self.headers)
        # 获取请求资源码
        self.response_code = self.main_data.status_code
        self.main_data = self.main_data.text

    def all_search(self):
        return_data = {'detect_list' : []}
        # 综合搜索结果
        search_user = self.upuser_search()
        if self.upuser_detect:
            return_data['detect_list'].append('upuser')
            return_data.update({'upuser' : search_user})

        search_bangumi = self.bangumi_search()
        if self.bangumi_detect:
            return_data['detect_list'].append('bangumi')
            return_data.update({'bangumi' : search_bangumi})

        search_live = self.live_search()
        if self.live_detect:
            return_data['detect_list'].append('live')
            return_data.update({'live' : search_live})

        search_video = self.video_search()
        if self.video_detect:
            return_data['detect_list'].append('video')
            return_data.update({'video' : search_video})

        search_article = self.article_search()
        if self.article_detect:
            return_data['detect_list'].apend('article')
            return_data.update({'article' : search_article})
        return_data.update({'response_code' : self.response_code})
        return return_data

    def video_search(self):
        # 获取搜索到的视频标题、id、浏览、弹幕、作者、作者uid、视频长度、上传时间
        search_video_title = re.findall('<a href="//www.bilibili.com/video/.*?" title="(.*?)"', self.main_data) # 标题
        if len(search_video_title) == 0:
            return {'response_code' : self.response_code, 'title' : [], 'id' :[], 'view' : [], 'danmaku' : [],
                    'owner' : [], 'owner_uid' : [], 'length' : [], 'upload_time' : []}
        else:
            self.video_detect = True
        search_video_id = re.findall('<a href="//www.bilibili.com/video/(BV.{10})\?from=search" title=".*?"', self.main_data) # id
        search_video_view = re.findall('<i class="icon-playtime"></i>\n\s*(.*?)\n\s*"', self.main_data) # 浏览
        search_video_danmaku = re.findall('<i class="icon-subtitle"></i>\n\s*(.*?)\n\s*"', self.main_data) # 弹幕
        search_video_owner = re.findall('<a href="//space.bilibili.com/.*?from=search.*?" target="_blank" class="up-name">(.*?)</a>', self.main_data) # 作者
        search_video_owner_uid = re.findall('<a href="//space.bilibili.com/(.*?)\?from=search.*?" target="_blank" class="up-name">.*?</a>', self.main_data) # 作者uid
        search_video_length = re.findall('<span class="so-imgTag_rb">(.*?)</span>', self.main_data) # 视频长度
        search_video_upload_time = re.findall('<i class="icon-date"></i>\n\s*(.*?)\n\s*"', self.main_data) # 上传时间
        # 返回数据
        return {'response_code' : self.response_code, 'title' : search_video_title, 'id' :search_video_id, 'view' : search_video_view,
                'danmaku' : search_video_danmaku, 'owner' : search_video_owner, 'owner_uid' : search_video_owner_uid,
                'length' : search_video_length, 'upload_time' : search_video_upload_time}

    def bangumi_search(self):
        # 获取番剧/纪录片片名、评分、评分人数、自定义数据、简介、分集列表
        search_bangumi_title = re.findall('<a href="//www.bilibili.com/bangumi/media/md.*?/?from=search&amp;seid=>.*?" title="(.*?)" target="_blank"',seld.main_data) # 名称
        if len(search_bangumi_title) == 0:
            return {'response_code' : self.response_code, 'title' : [], 'score' : [], 'score_num' : [], 'data' : [],
                    'introduction' : [], 'ep' : []}
        else:
            self.video_detect = True
        search_bangumi_score = re.findall('<div class="score-num">\n\s*(.*?)\n', self.main_data) # 评分
        search_bangumi_score_num = re.findall('<div class="user-count">\n\s*(.*?)点评\n\s*</div>', self.main_data) # 评分人数
        search_bangumi_data = re.findall('<span class="label">(.*?)：</span>\n<span class="value">(.*?)</span>', self.main_data) # 所有自定义数据
        for range_var in range(len(search_bangumi_data)):
            search_bangumi_data[range_var][1] = search_bangumi_data[range_var][1].replace('" class="value"', '\n')
        search_bangumi_introduction = re.findall('<div class="desc">\n\s*(.*?)\n\s*</div>', self.main_data) # 简介
        search_bangumi_ep_list = re.findall('<div title="(.*?)" class="ep-item">.*?</div>', self.main_data) # 分集列表
        # 返回数据
        return {'response_code' : self.response_code, 'title' : search_bangumi_title, 'score' : search_bangumi_score,
                'score_num' : search_bangumi_score_num, 'data' : search_bangumi_data,
                'introduction' : search_bangumi_introduction, 'ep' : search_bangumi_ep_list}

    def live_search(self):
        # 获取直播间标题、所属用户、观看人数、房间号码
        search_live_title = re.findall('<p title="(.*?)" class="item-title">', self.main_data) # 标题
        if len(search_live_title) == 0:
            return {'response_code' : self.response_code, 'title' : [], 'owner' : [], 'watch' : [], 'num' : []}
        else:
            self.live_detect = True
        search_live_owner = re.findall('<div title="(.*?)" class="uname">\n<i class="icon-live-up">', self.main_data) # 所属用户
        search_live_watch = re.findall('<i class="icon-live-watch"></i>\n<span>(.*?)</span>', self.main_data) # 观看人数
        search_live_num = re.findall('<a href="//live.bilibili.com/(.*?)\?from=search&amp;seid=.*?" target="_blank" class="item-wrapper">', self.main_data) # 直播房间号
        # 返回数据
        return {'response_code' : self.response_code, 'title' : search_live_title, 'owner' : search_live_owner,
                'watch' : search_live_watch, 'num' : search_live_num}

    def article_search(self):
        # 获取文章标题、cv号、作者、作者uid、分区、浏览、点赞、评论、一行预览
        search_article_title = re.findall('<em class="keyword">(.*?)</em>', self.main_data) # 标题
        if len(search_article_title) == 0:
            return {'response_code' : self.response_code, 'title' : [], 'num' : [], 'owner' : [], 'owner_uid' : [],
                    'tname' : [], 'introduction' : [], 'view' : [], 'like' : [], 'reply' : []}
        else:
            self.article_detect = True
        search_article_num = re.findall('<a title=".*?" href="//www.bilibili.com/read/cv(.*?)\?from=search" target="_blank" class="title">', self.main_data) # cv号
        search_article_owner = re.findall('<a href="//space.bilibili.com/.*?\?from=search&amp;seid=.*?" target="_blank" class="up-name oneline">(.*?)</a>', self.main_data) # 作者
        search_article_owner_uid = re.findall('<a href="//space.bilibili.com/(.*?)\?from=search&amp;seid=.*?" target="_blank" class="up-name oneline">.*?</a>', self.main_data) # 作者uid
        search_article_tname = re.findall('<a href="//www.bilibili.com/read/.*? target="_blank">(.*?)</a>', self.main_data) # 分区
        search_article_view = re.findall('<i class="icon-view"></i>\n\s*(.*?)\n\s*', self.main_data) # 浏览
        search_article_like = re.findall('<i class="icon-like"></i>\n\s*(.*?)\n\s*', self.main_data) # 点赞
        search_article_reply = re.findall('<i class="icon-reply"></i>\n\s*(.*?)\n\s*', self.main_data) # 评论
        search_article_introduction = re.findall('<p class="desc oneline">\n(.*?)\n', self.main_data) # 一行正文预览
        # 返回数据
        return {'response_code' : self.response_code, 'title' : search_article_title, 'num' : search_article_num, 'owner' : search_article_owner,
                'owner_uid' : search_article_owner_uid, 'tname' : search_article_tname, 'introduction' : search_article_introduction,
                'view' : search_article_view, 'like' : search_article_like, 'reply' : search_article_reply}

    def upuser_search(self):
        if len(re.findall('"//space.bilibili.com/(.*?)?from=search"', self.main_data)) == 0:
            return {'name' : [], 'uid' : [],'level' : [], 'tag' : [], 'video_count' : [], 'fans' : []}
        else:
            self.upuser_detect = True
        search_user_name = re.findall('title="(.*?)" target="_blank" class="face-img">', self.main_data)
        search_user_uid = re.findall('//space.bilibili.com/(\d{1,10})\?from=search', self.main_data)  # uid
        search_user_level = re.findall('"lv icon-lv(.*?)"', self.main_data)  # 等级
        search_user_tag = re.findall('<div class="desc">\n(.*?)\n', self.main_data)  # 签名/认证
        for tags in range(len(search_user_tag)):
            search_user_tag[tags] = search_user_tag[tags][6:]
        search_user_video_count = re.findall('<span>稿件：(.*?)</span>', self.main_data)  # 稿件数量
        search_user_fans = re.findall('<span>粉丝：(.*?)</span>', self.main_data)  # 粉丝数量
        return {'response_code' : self.response_code, 'name' : search_user_name, 'uid' : search_user_uid, 'level' : search_user_level,
                'sign' : search_user_tag, 'video_count' : search_user_video_count, 'fans' : search_user_fans}

