# -*- coding: UTF-8 -*-
import re
import time
import requests
import json
import os

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

class user:
    def __init__(self,user_uid):
        # 定义请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.43 Safari/537.36 Edg/81.0.416.28',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'}
        # 定义uid
        self.user_uid = user_uid

    def user_info(self):
        # 请求用户基础信息
        user_info = requests.get('https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(self.user_uid),headers = self.headers)
        # 获取请求资源码
        response_code = user_info.status_code
        user_info = json.loads(user_info.text)
        # 获取网站返回码
        return_code = user_info['code']
        if response_code != 200 or return_code != 0:  # 如果返回码错误，则返回空数据
            return {'response_code': response_code, 'return_code': return_code, 'name': '',
                    'sex': '', 'sign': '', 'level': '', 'birthday': '',
                    'offical': '', 'live_url': '', 'vip': '', 'fans_badge': ''}
        # 获取用户名字、性别、签名、等级、生日、认证、粉丝勋章状态、直播间码
        user_name = user_info['data']['name']  # 名字
        user_sex = user_info['data']['sex']  # 性别
        user_sign = user_info['data']['sign']  # 签名
        user_level = user_info['data']['level']  # 等级
        user_birthday = user_info['data']['birthday']  # 生日
        # user_coins = user_info['data']['coins']  # 硬币(未实现调用cookie所以隐藏)
        user_official = user_info['data']['official']['title']  # 认证
        user_vip = user_info['data']['vip']['status']  # 会员状态
        user_fans_badge = user_info['data']['fans_badge']  # 粉丝勋章状态
        return {'response_code' : response_code, 'return_code' : return_code, 'name' : user_name,
                'sex' : user_sex, 'sign' : user_sign, 'level' : user_level, 'birthday' : user_birthday,
                'official' : user_official, 'vip' : user_vip, 'fans_badge' : user_fans_badge}

    def user_top_video(self):
        # 请求用户置顶视频
        top_video = requests.get('https://api.bilibili.com/x/space/top/arc?vmid={}'.format(self.user_uid),headers=self.headers)
        # 获取请求资源码
        response_code = top_video.status_code
        top_video = json.loads(top_video.text)
        # 获取网站返回码
        return_code  = top_video['code']
        if return_code != 0 or return_code != 0:  # 判断是否有置顶视频
            return {'response_code' : response_code, 'return_code' : return_code, 'aid': '', 'bvid': '', 'tname': '',
                    'copyrights': '', 'title': '', 'upload_time': '', 'introduction': '', 'view': '', 'danmaku': '',
                    'reply': '', 'like': '', 'dislike': '', 'coin': '', 'collect': '', 'share': ''}
        top_video_aid = top_video['data']['aid']  # av号
        top_video_bvid = top_video['data']['bvid'] # bv号
        top_video_tname = top_video['data']['tname']  # 分区
        if top_video['data']['copyright'] == 1:  # 版权
            top_video_copyrights = '自制'
        else:
            top_video_copyrights = '转载'
        top_video_title = top_video['data']['title']  # 标题
        top_video_upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(top_video['data']['ctime']))  # 上传时间
        top_video_introduction = top_video['data']['desc']  # 简介
        top_video_view = top_video['data']['stat']['view']  # 浏览
        top_video_danmaku = top_video['data']['stat']['danmaku']  # 弹幕
        top_video_reply = top_video['data']['stat']['reply']  # 评论
        top_video_like = top_video['data']['stat']['like']  # 赞
        top_video_dislike = top_video['data']['stat']['dislike']  # 踩
        top_video_coin = top_video['data']['stat']['coin']  # 硬币
        top_video_collect = top_video['data']['stat']['favorite']  # 收藏
        top_video_share = top_video['data']['stat']['share']  # 分享
        return {'response_code' : response_code, 'return_code' : return_code, 'aid' : top_video_aid,
                'bvid' : top_video_bvid, 'tname' : top_video_tname, 'copyrights' : top_video_copyrights,
                'title' : top_video_title, 'upload_time' : top_video_upload_time,'introduction' : top_video_introduction,
                'view' : top_video_view, 'danmaku' : top_video_danmaku,'reply' : top_video_reply,'like' : top_video_like,
                'dislike' : top_video_dislike, 'coin' : top_video_coin, 'collect' : top_video_collect, 'share' : top_video_share}

    def user_video(self,pn):
        user_video_title = []  # 标题
        user_video_reply = []  # 评论
        user_video_upload_time = []  # 视频上传时间
        user_video_danmaku = []  # 弹幕
        user_video_view = []  # 浏览
        user_video_introduction = []  # 简介
        user_video_length = []  # 视频长度
        user_video_collect = []  # 收藏
        user_video_aid = []  # 视频av号
        # 获取用户视频列表
        video_data = json.loads(requests.get('http://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&page={}'.format(
            self.user_uid, pn),headers=self.headers).text)
        # 获取数据
        user_video_pages = video_data['data']['pages']
        for range_var in video_data['data']['vlist']:
            user_video_title.append(range_var['title'])
            user_video_reply.append(range_var['comment'])
            user_video_upload_time.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(range_var['created'])))
            user_video_danmaku.append(range_var['video_review'])
            user_video_view.append(range_var['play'])
            user_video_introduction.append(range_var['description'])
            user_video_length.append(range_var['length'])
            user_video_collect.append(range_var['favorites'])
            user_video_aid.append(range_var['aid'])
        # 返回数据
        return {'title' : user_video_title, 'reply' : user_video_reply, 'upload_time' : user_video_upload_time,
                'danmaku' : user_video_danmaku, 'view' : user_video_view, 'introduction' : user_video_introduction,
                'length' : user_video_length, 'collect' : user_video_collect, 'aid' : user_video_aid, 'pages' : user_video_pages}

class reply:
    def __init__(self,types,num,pn,sort):
        # 定义请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.43 Safari/537.36 Edg/81.0.416.28',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'}
        self.types = types
        self.num = str(num)
        self.page = pn
        self.sort = sort
        # 根据类型请求对应的评论
        if types == 'aid':
            self.main_data = requests.get('http://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&sort={}&oid={}'.format(pn, sort, num),headers=self.headers)
        elif types == 'bvid':
            tools = tool()
            self.num = tools.bv2av('BV' + self.num)
            self.main_data = requests.get('http://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&sort={}&oid={}'.format(pn, sort, self.num, headers=self.headers))
        # 获取请求资源码
        self.response_code = self.main_data.status_code
        self.main_data = json.loads(self.main_data.text)
        # 获取网站返回码
        self.return_code = self.main_data['code']

    def video_reply(self):
        # 如果返回码异常返回空数据，减少时间
        if self.response_code != 200 or self.return_code != 0:
            return{'response_code' : self.response_code, 'return_code' : self.return_code, 'type' : self.types,
                   'num' : self.num, 'page' : self.page, 'sort' : self.sort, 'user_name' : [],'user_level' : [],
                   'user_sex' : [], 'user_official' : [], 'like' : [], 'reply' : [], 'content' : [], 'upload_time' : [],
                   'up_like' : [], 'up_reply' : [], 'is_double_reply' : []}
        reply_user_name = [] # 用户名称
        reply_user_level = [] # 用户等级
        reply_user_sex = [] # 用户性别
        reply_user_official = [] # 用户认证
        reply_like_num = [] # 评论赞数
        reply_reply_num = [] # 评论回复数
        reply_upload_time = [] # 评论上传时间
        reply_content = [] # 评论正文
        reply_up_like = [] # UP是否点赞
        reply_up_reply = [] # UP是否评论
        is_double_reply = [] # 是否是第二层评论
        all_page = int(self.main_data['data']['page']['count'])
        # 获得页数（向上取整）
        if not all_page / 20 == int(all_page / 20):
            all_page = int(all_page / 20) + 1
        else:
            all_page = all_page / 20
        # 遍历字典，获得数据
        for range_var0 in self.main_data['data']['replies']:
            reply_user_name.append(range_var0['member']['uname'])
            reply_user_level.append(range_var0['member']['level_info']['current_level'])
            reply_user_sex.append(range_var0['member']['sex'])
            reply_user_official.append(range_var0['member']['official_verify']['desc'])
            reply_like_num.append(range_var0['like'])
            reply_reply_num.append(range_var0['rcount'])
            reply_upload_time.append(range_var0['ctime'])
            reply_content.append(range_var0['content']['message'])
            for range_var1 in range(len(reply_content)):
                reply_content[range_var1] = reply_content[range_var1].replace('\r', '')
            reply_up_like.append(range_var0['up_action']['like'])
            reply_up_reply.append(range_var0['up_action']['reply'])
            is_double_reply.append(0)
            if not range_var0['replies'] is None:
                # 获取评论回复
                for range_var2 in range_var0['replies']:
                    reply_user_name.append(range_var2['member']['uname'])
                    reply_user_level.append(range_var2['member']['level_info']['current_level'])
                    reply_user_sex.append(range_var2['member']['sex'])
                    reply_user_official.append(range_var2['member']['official_verify']['desc'])
                    reply_like_num.append(range_var2['like'])
                    reply_reply_num.append(range_var2['rcount'])
                    reply_upload_time.append(range_var2['ctime'])
                    reply_content.append(range_var2['content']['message'])
                    for range_var1 in range(len(reply_content)):
                        reply_content[range_var1] = reply_content[range_var1].replace('\r', '')
                    reply_up_like.append(range_var2['up_action']['like'])
                    reply_up_reply.append(range_var2['up_action']['reply'])
                    is_double_reply.append(1)
        # 返回数据
        return{'response_code' : self.response_code, 'return_code' : self.return_code, 'type' : self.types,
               'num' : self.num, 'page' : self.page, 'sort' : self.sort, 'all_page' : all_page, 'user_name' : reply_user_name,
               'user_level' : reply_user_level, 'user_sex' : reply_user_sex, 'user_official' : reply_user_official,
               'like' : reply_like_num, 'reply' : reply_reply_num, 'content' : reply_content, 'upload_time' : reply_upload_time,
               'up_like' : reply_up_like, 'up_reply' : reply_up_reply, 'is_double_reply' : is_double_reply}

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
        search_video_id = re.findall('<a href="//www.bilibili.com/video/(.*?)" title=".*?"', self.main_data) # id
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
        search_user_uid = re.findall('<a href="//space.bilibili.com/(.*?)/video', self.main_data)  # uid
        search_user_level = re.findall('"lv icon-lv(.*?)"', self.main_data)  # 等级
        search_user_tag = re.findall('<div class="desc">\n(.*?)\n', self.main_data)  # 签名/认证
        for tags in range(len(search_user_tag)):
            search_user_tag[tags] = search_user_tag[tags][6:]
        search_user_video_count = re.findall('<span>稿件：(.*?)</span>', self.main_data)  # 稿件数量
        search_user_fans = re.findall('<span>粉丝：(.*?)</span>', self.main_data)  # 粉丝数量
        return {'response_code' : self.response_code, 'name' : search_user_name, 'uid' : search_user_uid, 'level' : search_user_level,
                'tag' : search_user_tag, 'video_count' : search_user_video_count, 'fans' : search_user_fans}

class download:
    def __init__(self,save_path,code,num):
        # 定义请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.43 Safari/537.36 Edg/81.0.416.28',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9',
            'Cache-Control' : 'max-age=0',
            'Connection' : 'keep-alive'
            }
        self.save_path = save_path
        if code == 'aid':
            self.zipname = 'av'
            self.basicname = 'aid'
            self.fullname = 'avid'
        elif code == 'bvid':
            self.zipname = 'bv'
            self.basicname = 'bvid'
            self.fullname = 'bvid'
        self.num = num

    def get_video_download_urls(self,part,quality = 80):
        print('正在获取下载链接...')
        import hashlib
        url_list = []
        size_list = []
        # 取得并访问可以获取URL的网址
        cid = re.findall('"cid":(.*?),', requests.get('https://api.bilibili.com/x/player/pagelist?{}={}'.format(self.basicname,self.num)).text)[part]
        entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
        appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
        params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
        chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
        url= 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
        # 设置referer项
        referer = 'https://www.bilibili.com/video/{}{}'.format(self.zipname, self.num)
        return_url = json.loads(requests.get(url).content.decode())['durl']
        for urls in return_url:
            url_list.append(urls['url'])
            size_list.append(urls['size'])
        # 返回数据
        return {'url' : url_list, 'referer' : referer, 'cid' : cid}

    def video_downloader(self,url,referer):
        # 更新请求头，加上referer
        self.headers.update({'Referer' : referer})
        video_download_name = []
        for range_var in range(len(url)):
            print('下载中...[{}/{}]'.format(range_var + 1, len(url)),end='\r')
            # 获取分段文件
            data = requests.get(url[range_var],headers=self.headers)
            # 写入数据
            with open(self.save_path + 'part' + str(range_var + 1),'wb') as file:
                video_download_name.append('part' + str(range_var + 1))
                file.write(data.content)
                file.flush()
        # 返回下载的视频分段文件名列表
        return {'filename' : video_download_name}

    def danmaku_downloader(self,cid):
        print('下载弹幕中...')
        danmaku_download_name = []
        # 获取弹幕
        danmaku_file = requests.get('https://comment.bilibili.com/{}.xml'.format(cid))
        # 写入数据
        with open(self.save_path + 'danmaku.xml','wb') as file:
            danmaku_download_name.append('danmaku')
            file.write(danmaku_file.content)
            file.flush()
        # 返回写入的弹幕名称
        return {'filename' : danmaku_download_name}

    def xml2ass(self,filename='danmaku'):
        # 使用DanmakuFactory将弹幕XML文件转换为字幕ASS文件
        os.system('DanmakuFactory\DanmakuFactory.exe -i "{}danmaku.xml" -o "{}{}.ass"'.format(self.save_path, self.save_path, filename))
        return

    def merge_video_part(self,inputs, output):
        print('正在合并视频分段...')
        # 根据写入的视频分段名称把名字写入filelist.txt
        with open(self.save_path + 'filelist.txt', 'w', encoding = 'utf-8') as file:
            for filename in inputs:
                file.write('file \'{}\'\n'.format(filename))
        # 使用FFmpeg读取filelist.txt并合并其中的文件
        os.system('ffmpeg.exe -f concat -safe 0 -i {}filelist.txt -c copy {}{}'.format(self.save_path, self.save_path, output))

    def flush_ass_to_video(self,filename):
        # 获取合成后的文件分辨率并写入quality.txt
        os.system(r'ffmpeg.exe -i {}full.flv 2> {}quality.txt'.format(self.save_path, self.save_path))
        # 获取视频分辨率
        quality = re.findall(r'(\d*x\d*)',open(self.save_path + 'quality.txt').read())[0]
        print('正在冲入ASS字幕...')
        # 使用ffmpeg将ass字幕打入视频流中
        os.system(r'ffmpeg.exe -i {}full.flv -i {}danmaku.ass -vf ass=\'{}danmaku.ass\' -strict -2 -s {}.flv'.format(
            self.save_path,self.save_path ,self.save_path, (quality + ' "' + self.save_path + filename)))

    def del_file(self):
        part = 1
        # 移除多余文件
        # 移除记录视频分段文件列表的文件
        os.remove(self.save_path + 'filelist.txt')
        while os.path.exists(self.save_path + 'part{}'.format(part)):
            # 重复移除视频分段文件
            os.remove(self.save_path + 'part{}'.format(part))
            part += 1
        # 尝试移除只有把ass文件打入视频流时才产生的文件
        try:
            os.remove(self.save_path + 'danmaku.ass')
            os.remove(self.save_path + 'quality.txt')
            os.remove(self.save_path + 'full.flv')
        except FileNotFoundError:
            pass
        # 移除弹幕XML文件
        os.remove(self.save_path + 'danmaku.xml')

class viewer:
    def __init__(self,code,num):
        self.code = code
        self.num = num
        if code == 'aid':
            self.easy_code = 'av'
        elif code == 'bvid':
            self.easy_code = 'BV'

    def view_video(self):
        video_response = video(self.code, self.num)
        # 获取并打印视频基本信息
        video_info = video_response.video_info()
        if video_info['response_code'] != 200 or video_info['return_code'] != 0:
            print('网络连接错误或无此视频')
            exit(0)
        print('————作品信息————')
        print('标题:', video_info['title'])
        print('作者:', video_info['owner'])
        print('视频类型:', video_info['zone_name'], video_info['copyrights'])
        print('上传时间:', video_info['upload_time'])
        print('av号:', video_info['aid'])
        print('av:url:https://www.bilibili.com/video/av{}'.format(video_info['aid']))
        print('bv号:', video_info['bvid'])
        print('bv:url:https://www.bilibili.com/video/{}'.format(video_info['bvid']))
        # 获取并打印视频简介
        introduction = video_response.introduction()['introduction'].split('\n')
        print('简介:', end='')
        for range_var0 in introduction:
            for range_var1 in range(int(len(range_var0) / 55) + 1):  # 45个字一行显示评论
                try:
                    for local in range(55):
                        print(range_var0[local + (55 * range_var1)], end='')
                    print('')
                except IndexError:
                    break
        print('')
        # 获取并打印视频数据
        video_data = video_response.video_data()
        if video_data['response_code'] != 200 or video_data['return_code'] != 0:
            print('网络连接错误或无此视频')
            exit(0)
        print('浏览:', video_data['view'])
        print('弹幕:', video_data['danmaku'])
        print('点赞:', video_data['like'])
        if int(video_data['dislike']) >= 1:
            print('踩:', video_data['dislike'])
        print('评论:', video_data['reply'])
        print('硬币:', video_data['coin'])
        print('收藏:', video_data['collect'])
        print('分享:', video_data['share'])
        # 获取并打印UP主的基本信息
        up = search(video_info['owner'],'upuser')
        up_data = up.upuser_search()
        print('————作者信息————')
        print('作者:', up_data['name'][0])
        if len(up_data['uid']) >= 1:
            print('uid:', up_data['uid'][0])
        print('等级: LV', up_data['level'][0])
        print('签名:', up_data['tag'][0])
        print('稿件:', up_data['video_count'][0])
        print('粉丝:', up_data['fans'][0])
        # 获取并打印视频分P(如果没有就不打印)
        part = video_response.video_part()
        if not len(part['name']) == 1:
            print('————分P信息————')
            for part_num in range(len(part['name'])):
                print(str(part_num + 1) + 'P:', part['name'][part_num])
                print('     cid:{}'.format(part['cid'][part_num]))
                print('     长度:{}'.format(part['length'][part_num]))
                print('————————————————')
        # 获取并打印评论
        choice = input('是否查看视频评论？(Y/Enter):')
        if choice == 'Y' or choice == 'y':
            sort = str(input('选择你的评论排序方式(0=按时间，2=按热度)'))
            try:
                page = 1
                while True:
                    replys = reply(self.code,self.num,page,sort)
                    replys = replys.video_reply()
                    for range_var2 in range(len(replys['user_name'])):
                        # 按照列表打印评论详情
                        # '     ' * replys['is_double_reply'][range_var2] ：按照父评论层数打印缩进
                        print('     ' * replys['is_double_reply'][range_var2],replys['user_name'][range_var2], ' LV', replys['user_level'][range_var2], ' 性别:', replys['user_sex'][range_var2])  # 打印用户名称、姓名、等级
                        if replys['user_official'][range_var2] != '':  # 如果有认证就打印
                            print('     ' * replys['is_double_reply'][range_var2], 'Bilibili认证:', replys['user_official'][range_var2])
                        print('     ' * replys['is_double_reply'][range_var2], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(replys['upload_time'][range_var2])))  # 打印上传时间
                        content = replys['content'][range_var2].split('\n')
                        for range_var3 in content:
                            for range_var4 in range(int(len(range_var3) / 55) + 1):  # 55个字一行显示评论
                                print('     ' * replys['is_double_reply'][range_var2], '', end='')
                                try:
                                    for local in range(55):
                                        print(range_var3[local + (55 * range_var4)], end='')
                                    print('')
                                except IndexError:
                                    break
                            print('')
                        print('     ' * replys['is_double_reply'][range_var2], replys['like'][range_var2], '赞', replys['reply'][range_var2], '评论')
                        # 判断UP主是否与评论有互动
                        if replys['up_like'][range_var2]:
                            print('     ' * replys['is_double_reply'][range_var2], 'UP主赞了')
                        if replys['up_reply'][range_var2]:
                            print('     ' * replys['is_double_reply'][range_var2], 'UP主回复了')
                        print('     ' * replys['is_double_reply'][range_var2], '————————————————————————')
                    choice = input('回车以查看下一页评论，输入exit退出评论:')
                    if  choice == 'exit':
                        raise IndexError
                    else:
                        if page == replys['all_page']:
                            raise IndexError
                        page += 1
                        continue

            except IndexError:
                print('评论查看完毕')

        choice = input('是否下载视频和弹幕？(Y/Enter):')
        if choice == 'Y' or choice == 'y':
            # 生成最终文件名
            filename = []
            for range_var4 in range(len(part['name'])):
                filename.append(video_info['title'] + 'P{}-{}'.format(range_var4 + 1, part['name'][range_var4]))
            # 获取清晰度并转换成网站的标准
            quality = input('请输入所需清晰度(1080/720/480/360):')
            if quality == '1080':
                quality = 80
            elif quality == '720':
                quality = 64
            elif quality == '480':
                quality = 32
            elif quality == '360':
                quality = 16
            else:
                quality = 80
            path = input('输入视频和弹幕的保存路径，例:E:/video:')
            download_type = input('请选择弹幕下载方式:\n1,下载为ASS字幕(推荐)\n2，强行嵌入视频中')
            downloads = download(path,self.code,self.num)
            for range_var5 in range(len(part['cid'])):
                url = downloads.get_video_download_urls(range_var5, quality)
                download_part_name = downloads.video_downloader(url['url'],url['referer'])
                downloads.danmaku_downloader(url['cid'])
                if download_type == '2':
                    downloads.merge_video_part(inputs = download_part_name['filename'], output = 'full.flv')
                    downloads.xml2ass()
                    downloads.flush_ass_to_video(filename[range_var5])
                else:
                    downloads.merge_video_part(inputs = download_part_name['filename'], output = filename[range_var5] + '.flv')
                    downloads.xml2ass(filename[range_var5])
                downloads.del_file()

        input('程序运行完毕，按Enter退出...')

    def view_user(self):
        user_response = user(self.num)
        user_info = user_response.user_info()
        if user_info['response_code'] != 200 or user_info['return_code'] != 0:
            print('网络连接错误或无此用户')
            exit(0)
        print(user_info['name'], end=' ')
        if user_info['sex'] != '保密':
            print(user_info['sex'], end=' ')
        print('LV', user_info['level'], end=' ')
        if user_info['vip'] == 1:
            print('大会员')
        else:
            print('')
        if user_info['official'] != '':
            print('Bilibili认证', user_info['official'])
        if user_info['fans_badge']:
            print('开通了粉丝勋章')
        if user_info['birthday'] != '':
            print('生日:', user_info['birthday'])
        print('个性签名:', user_info['sign'])

        user_top_video = user_response.user_top_video()
        if user_top_video['response_code'] != 200 or user_top_video['return_code'] != 0:
            print('当前用户暂无置顶视频')
        else:
            print('——————置顶视频——————')
            print(user_top_video['copyrights'], user_top_video['tname'], user_top_video['title'])
            print('av' + str(user_top_video['aid']) + '/' + user_top_video['bvid'], user_top_video['upload_time'])
            introduction = user_top_video['introduction'].split('\n')
            print('简介:', end='')
            for range_var0 in introduction:
                for range_var1 in range(int(len(range_var0) / 55) + 1):  # 45个字一行显示评论
                    try:
                        for local in range(55):
                            print(range_var0[local + (55 * range_var1)], end = '')
                        print('')
                    except IndexError:
                        break
            print('')
            print(user_top_video['view'], '浏览', user_top_video['danmaku'], '弹幕', user_top_video['like'], '点赞',
                  user_top_video['reply'], '评论', user_top_video['coin'], '硬币', user_top_video['collect'], '收藏', user_top_video['share'], '分享')
            print('————————————————')

        choice = input('是否查看用户视频列表(Y/Enter)?')
        if choice == 'Y' or choice == 'y':
            pn = 1
            while True:
                user_video_list = user_response.user_video(pn)
                pages = user_video_list['pages']
                if pn > pages:
                    break
                user_video_title = user_video_list['title']
                user_video_reply = user_video_list['reply']
                user_video_upload_time = user_video_list['upload_time']
                user_video_danmaku = user_video_list['danmaku']
                user_video_view = user_video_list['view']
                user_video_introduction = user_video_list['introduction']
                user_video_length = user_video_list['length']
                user_video_collect = user_video_list['collect']
                user_video_aid = user_video_list['aid']
                for range_var2 in range(20):
                    try:
                        print(user_video_title[range_var2])
                        print('av' + str(user_video_aid[range_var2]), user_video_upload_time[range_var2], '时长:', user_video_length[range_var2])
                        introduction = user_video_introduction[range_var2].split('\r\n')
                        print('简介:')
                        for range_var3 in introduction:
                            for range_var4 in range(int(len(range_var3) / 55) + 1):  # 45个字一行显示评论
                                try:
                                    print('     ', end='')
                                    for local in range(55):
                                        print(range_var3[local + (55 * range_var4)], end = '')
                                except IndexError:
                                    print('')
                                    break
                        print(user_video_view[range_var2], '浏览', user_video_danmaku[range_var2], '弹幕',
                              user_video_reply[range_var2], '评论', user_video_collect[range_var2], '收藏')
                        print('————————————————')
                    except IndexError:
                        break
                pn += 1
                if input('是否查看下一页?(Enter/exit)') == 'exit':
                    break

class tool:
    def __init__(self):
        # av2bv bv2av
        self.alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'

    def bv2av(self,x):
        r = 0
        for i, v in enumerate([11, 10, 3, 8, 4, 6]):
            r += self.alphabet.find(x[v]) * 58 ** i
        return (r - 0x2_0840_07c0) ^ 0x0a93_b324

    def av2bv(self,x):
        x = (x ^ 0x0a93_b324) + 0x2_0840_07c0
        r = list('BV1**4*1*7**')
        for v in [11, 10, 3, 8, 4, 6]:
            x, d = divmod(x, 58)
            r[v] = self.alphabet[d]
        return ''.join(r)

if __name__ == '__main__':
    item = input('输入你要爬取信息的特征码（uid/av/bv/cv）,示例：uid:439067826:').split(':')
    # 按照信息前缀判断信息类型
    if item[0] == 'av':
        run = viewer('aid',item[1])
        run.view_video()
    elif item[0] == 'bv':
        run = viewer('bvid', item[1])
        run.view_video()
    elif item[0] == 'uid':
        run = viewer('uid', item[1])
        run.view_user()
    elif item[0] == 'cv':
        # pessage(item[1])
        pass