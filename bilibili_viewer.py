# -*- coding: UTF-8 -*-
from Plugin.video import video
from Plugin.user import user
from Plugin.reply import reply
from Plugin.download import download
from Plugin.search import search
from Plugin.search import new_search
# add plugin at here
import re
import time
import requests
import json

class shower:
    @staticmethod
    def print_video(data : dict,slice_char='\r\n'):
        try:
            print(data['copyrights'], data['tname'], end=' ')
        except KeyError:
            pass
        print(data['title'],end=' ')
        try:
            print('作者:' + data['owner'])
        except KeyError:
            print('')
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
        shower.print_introduction({'introduction' : data['introduction']},slice_char=slice_char)
        print(data['view'], '浏览', data['danmaku'], '弹幕',end=' ')
        try:
            print(data['like'], '点赞',end=' ')
        except KeyError:
            pass
        try:
            print(data['reply'], '评论',end=' ')
        except KeyError:
            pass
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
    def print_introduction(data : dict,chars_limit=55,slice_char='\r\n',hand_char=' '*5):
        introduction = data['introduction'].split(slice_char)
        for range_var1 in introduction:
            for range_var2 in range(int(len(range_var1) / chars_limit) + 1):  # 45个字一行显示评论
                try:
                    print(hand_char, end = '')
                    for local in range(chars_limit):
                        print(range_var1[local + (chars_limit * range_var2)], end = '')
                    print('')
                except IndexError:
                    print('')
                    break
    @staticmethod
    def print_user(data : dict):
        print(data['name'], end = ' ')
        print('LV', data['level'], end = ' ')
        try:
            print('uid:', data['uid'])
        except KeyError:
            pass
        try:
            if data['sex'] != '保密':
                print(data['sex'], end = ' ')
            if data['vip'] == 1:
                print('大会员',end = ' ')
            if data['official'] != '':
                print('Bilibili认证:' + data['official'])
            if data['fans_badge']:
                print('粉丝勋章已开通',end=' ')
            if data['birthday'] != '':
                print('生日:', data['birthday'])
        except KeyError:
            pass
        print('个性签名:', data['sign'])
        try:
            print('稿件:', data['video_count'])
            print('粉丝:', data['fans'])
        except KeyError:
            pass

class viewer:
    def __init__(self,code,num):
        self.code = code
        self.num = num
        if code == 'aid':
            self.easy_code = 'av'
        elif code == 'bvid':
            self.easy_code = 'BV'

    def view_video(self):
        video_response = video(self.code,self.num)
        # 获取并打印视频基本信息
        video_info = video_response.video_info()
        introduction = video_response.introduction()
        video_data = video_response.video_data()
        if video_info['response_code'] != 200 or video_info['return_code'] != 0:
            print('网络连接错误或无此视频')
            return
        if video_data['response_code'] != 200 or video_data['return_code'] != 0:
            print('网络连接错误或无此视频')
            return
        print('————作品信息————')
        data = video_info
        data.update(video_data)
        data.update(introduction)
        shower.print_video(data)
        # 获取并打印UP主的基本信息
        print('————作者信息————')
        up_data = new_search(keyword = video_info['owner'], search_type = 'bili_user')
        shower.print_user(up_data.get_user()[0])
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
                        content = replys['content'][range_var2]
                        shower.print_introduction(data={'introduction':content},slice_char='\n',hand_char = ' '*5*replys['is_double_reply'][range_var2]+' ')
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
                    downloads.merge_video_part(inputs = download_part_name['filename'], output = filename[range_var5].replace('/','-') + '.flv')
                    downloads.xml2ass(filename[range_var5].replace('/','-'))
                downloads.del_file()
        return

    def view_user(self):
        user_response = user(self.num)
        user_info = user_response.user_info()
        if user_info['response_code'] != 200 or user_info['return_code'] != 0:
            print('网络连接错误或无此用户')
            return
        print('————用户信息————')
        shower.print_user(user_info)

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

    def view_search(self):
        name = {'video' : 'video','user' : 'bili_user'}
        search_type = input('请输入搜索类型')
        data = new_search(keyword = self.num,search_type = name[search_type])
        for range_var in range(data.get_pages()):
            data = new_search(keyword = self.num,page = (range_var + 1),search_type = name[search_type])
            if search_type == 'video':
                videos = data.get_video()
                for video in videos:
                    shower.print_video(video)
            if search_type == 'user':
                users = data.get_user()
                for user in users:
                    shower.print_user(user)
                    print('————————————————')
                    for user_video in user['top_video']:
                        shower.print_video(user_video,slice_char = '\n')
                        print('————————————————')
            if input('按回车查看下一页,按exit退出') == 'exit':
                break

if __name__ == '__main__':
    while True:
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
            run = viewer('search', item[1])
            run.view_search()
        else:
            print('输入错误')
            print('用法: code:num\n例:')
            print('支持的code类型:av,bv,uid')