# -*- coding: UTF-8 -*-
import Plugin.video as video
import Plugin.user as user
import Plugin.reply as reply
import Plugin.download as download
# add plugin at here
import re
import time
import requests
import json
import os

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
class shower:
    @staticmethod
    def print_video(data : dict):
        try:
            print(data['copyrights'], data['tname'], end=' ')
        except KeyError:
            pass
        print(data['title'])
        print('av' + str(data['aid']),end='')
        try:
            print('/' + data['bvid'],end=' ')
        except KeyError:
            pass
        print(data['upload_time'],end=' ')
        try:
            print('时长:', data['length'],end=' ')
        except KeyError:
            print('')
        else:
            print('')
        print('简介:')
        shower.print_introduction({'introduction' : data['introduction']})
        print(data['view'], '浏览', data['danmaku'], '弹幕',end=' ')
        try:
            print(data['like'], '点赞',end=' ')
        except KeyError:
            pass
        print(data['reply'], '评论',end=' ')
        try:
            print(data['coin'], '硬币',end=' ')
        except KeyError:
            pass
        print(data['collect'], '收藏', end=' ')
        try:
            print(data['share'], '分享')
        except KeyError:
            print('')
    @staticmethod
    def print_introduction(data : dict,chars_limit=55):
        introduction = data['introduction'].split('\r\n')
        for range_var1 in introduction:
            for range_var2 in range(int(len(range_var1) / chars_limit) + 1):  # 45个字一行显示评论
                try:
                    print('     ', end = '')
                    for local in range(chars_limit):
                        print(range_var1[local + (chars_limit * range_var2)], end = '')
                    print('')
                except IndexError:
                    print('')
                    break
class viewer:
    def __init__(self,code,num):
        self.code = code
        self.num = num
        if code == 'aid':
            self.easy_code = 'av'
        elif code == 'bvid':
            self.easy_code = 'BV'

    def view_video(self):
        video_response = video.video(self.code,self.num)
        # 获取并打印视频基本信息
        video_info = video_response.video_info()
        if video_info['response_code'] != 200 or video_info['return_code'] != 0:
            print('网络连接错误或无此视频')
            return
        '''
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
        '''
        video_data = video_response.video_data()
        if video_data['response_code'] != 200 or video_data['return_code'] != 0:
            print('网络连接错误或无此视频')
            return
        video_info = video_info.update(video_data)
        shower.print_video(video_info)
        '''
        print('浏览:', video_data['view'])
        print('弹幕:', video_data['danmaku'])
        print('点赞:', video_data['like'])
        if int(video_data['dislike']) >= 1:
            print('踩:', video_data['dislike'])
        print('评论:', video_data['reply'])
        print('硬币:', video_data['coin'])
        print('收藏:', video_data['collect'])
        print('分享:', video_data['share'])
        '''
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
                    replys = reply.reply(self.code,self.num,page,sort)
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
            downloads = download.download(path,self.code,self.num)
            for range_var5 in range(len(part['cid'])):
                url = downloads.get_video_download_urls(range_var5, quality)
                download_part_name = downloads.video_downloader(url['url'],url['referer'])
                downloads.danmaku_downloader(url['cid'])
                if download_type == '2':
                    downloads.merge_video_part(inputs = download_part_name['filename'], output = 'full.flv')
                    downloads.xml2ass()
                    downloads.flush_ass_to_video(filename[range_var5])
                else:
                    downloads.merge_video_part(inputs = download_part_name['filename'], output = filename[range_var5].replace('/','-') + '.flv')
                    downloads.xml2ass(filename[range_var5].replace('/','-'))
                downloads.del_file()

        input('程序运行完毕，按Enter退出...')

    def view_user(self):
        user_response = user.user(self.num)
        user_info = user_response.user_info()
        if user_info['response_code'] != 200 or user_info['return_code'] != 0:
            print('网络连接错误或无此用户')
            return
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
            shower.print_video(user_top_video)
            print('————————————————')

        choice = input('是否查看用户视频列表(Y/Enter)?')
        if choice == 'Y' or choice == 'y':
            pn = 1
            while True:
                user_video_list = user_response.user_video(pn)
                pages = user_video_list['pages']
                if pn > pages:
                    break
                for range_var in user_video_list['data']:
                    shower.print_video(range_var)
                    print('————————————————')
                pn += 1
                if input('是否查看下一页?(Enter/exit)') == 'exit':
                    break

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
    elif item[0] == 'search':
        if len(item) == 2:
            run = viewer('search', item[1])
    else:
        print('输入错误')
        print('用法: code:num\n例:')
        print('支持的code类型:av,bv,uid')