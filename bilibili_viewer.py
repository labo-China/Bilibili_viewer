# -*- coding: UTF-8 -*-
from Plugin.video import video
from Plugin.bangumi import bangumi
from Plugin.user import user
from Plugin.reply import reply
from Plugin.download import download
from Plugin.search import new_search
from Plugin.tool import *


class shower:
    """按格式打印获取的数据"""

    @staticmethod
    def print_introduction(data: dict, chars_limit = 55, hand_char = '\t'):
        """按格式打印简介/长文字\n
            :param data: 文字数据
            :param chars_limit: 一行文字数量限制
            :param hand_char: 每行文字的缩进"""
        introduction = data['introduction'].split()
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
    def PrintUser(data: dict):
        print(data['name'], end = ' ')
        shower.TryPrint(data['sex'] if data['sex'] != '保密' else '', ' ', change_line = False)
        print('LV', data['level'], end = ' ')
        shower.TryPrint('Uid:', data['uid'])
        shower.TryPrint('大会员' if data['vip'] else '', ' ')
        shower.TryPrint('Bilibili认证:' + data['official'] if data['official'] else '', ' ')
        shower.TryPrint('粉丝勋章已开通' if data['fans_badge'] else '', ' ')
        shower.TryPrint('生日:', data['birthday'] if data['birthday'] else '')
        print('个性签名:', data['sign'])
        shower.TryPrint('稿件:', data['video_count'], '\n', '粉丝:', data['fans'])

    @staticmethod
    def PrintReply(data: dict, print_line = False, reply_depth = 0, head_char = '\t'):
        Header = head_char * reply_depth
        print(Header + data['name'], 'LV', data['level'], ' 性别:', data['sex'])
        shower.TryPrint(Header + 'Bilibili认证:' + data['official'] if data['official'] else '')
        print(Header + format_time(data['upload_time']))
        shower.print_introduction(data = {'introduction': data['content']}, hand_char = Header)
        print(Header + str(data['like']), '赞', str(data['reply']) + '评论' if reply_depth == 0 else '')
        shower.TryPrint(Header + 'UP主赞了' if data['up_like'] else '', change_line = False)
        shower.TryPrint(Header + 'UP主回复了' if data['up_reply'] else '', change_line = False)
        print(Header + '————————————————') if print_line else None
        for ChildReply in data['replies']:
            shower.PrintReply(data = ChildReply, reply_depth = reply_depth + 1, print_line = print_line)
    
    @staticmethod
    def PrintVideo(data: dict):
        shower.TryPrint(data['copyrights'], ' ', change_line = False)
        shower.TryPrint(data['tname'], ' ', change_line = False)
        print(data['title'], end = ' ')
        shower.TryPrint('作者:', data['owner'], other = '')
        shower.TryPrint('av', data['aid'], change_line = False)
        shower.TryPrint('/', data['bvid'], ' ', change_line = False)
        print(data['upload_time'], end = ' ')
        shower.TryPrint('时长: ', data['length'], other = '')
        print('简介:')
        shower.print_introduction({'introduction': data['introduction']})
        shower.TryPrint(data['view'], ' 浏览 ', change_line = False)
        shower.TryPrint(data['danmaku'], ' 弹幕 ', change_line = False)
        shower.TryPrint(data['like'], ' 点赞 ', change_line = False)
        shower.TryPrint(data['reply'], ' 评论 ', change_line = False)
        shower.TryPrint(data['coin'], ' 硬币 ', change_line = False)
        shower.TryPrint(data['collect'], ' 收藏 ', change_line = False)
        shower.TryPrint(data['share'], ' 分享 ', other = '')

    @staticmethod
    def TryPrint(*args, change_line: bool = True, other: str = None) -> None:
        for arg in args:
            if not bool(arg):
                if other is not None:
                    print(other)
                return
        else:
            for arg in args:
                print(arg, end = '')
            print('') if change_line else None
        return


class viewer:
    def __init__(self, code, num):
        self.code = code
        self.num = num

    def view_video(self):
        VideoResponse = video(self.code, self.num)
        # 获取并打印视频基本信息
        VideoInfo = VideoResponse.video_info()
        VideoData = VideoResponse.video_data()
        Introduction = VideoResponse.introduction()
        if self.CheckForResponse(VideoInfo) or self.CheckForResponse(VideoData) or self.CheckForResponse(Introduction):
            return
        Data = fill({**VideoInfo, **VideoData, **Introduction}, video_module)
        print('------作品信息------')
        shower.PrintVideo(Data)
        # 获取并打印UP主的基本信息
        print('------作者信息------')
        OwnerData = new_search(keyword = VideoInfo['owner'], search_type = 'bili_user')
        shower.PrintUser(fill(OwnerData.get_user()[0], user_module))
        print('-------------------')
        # 获取并打印视频分P(如果没有就不打印)
        Part = VideoResponse.video_part()
        if self.CheckForResponse(Part):
            return
        elif len(Part['part']) > 1:
            print('————分P信息————')
            for Index, Parts in enumerate(Part['part']):
                print(str(Index + 1) + 'P:', Parts['name'])
                print(f'     cid:{Parts["cid"]}')
                print(f'     长度:{Parts["length"]}')
                print('-------------------')

        # 获取并打印评论
        Choice = input('是否查看视频评论？(Y/Enter):').upper()
        if Choice == 'Y':
            Sort = str(input('选择你的评论排序方式(0=按时间，2=按热度)'))
            try:
                Page = 1
                while True:
                    VideoReply = reply.video_reply(types = self.code, num = self.num, pn = Page, sort = Sort)
                    for Replies in VideoReply['replies']:
                        shower.PrintReply(data = Replies, print_line = True)
                    Choice = input('回车以查看下一页评论，输入exit退出评论:')
                    if Choice == 'exit':
                        raise IndexError
                    else:
                        if Page == VideoReply['all_page']:
                            raise IndexError
                        Page += 1
                        continue
            except IndexError:
                print('评论查看完毕')

        Choice = input('是否下载视频和弹幕？(Y/Enter):').upper()
        if Choice == 'Y':
            # 生成最终文件名
            FileName = []
            for Index, Name in enumerate(Part['part']):
                FileName.append(VideoInfo['title'] + f'P{(Index + 1)}-{Name["name"]}')
            # 获取清晰度并转换成网站的标准
            QualityDict = {
                '1080': 80,
                '720': 64,
                '480': 32,
                '360': 16}
            Quality = input('请输入所需清晰度(1080/720/480/360):')
            Quality = QualityDict[Quality] if Quality in QualityDict.keys() else 80
            Path = input('输入视频和弹幕的保存路径，例:E:/video:')
            DownloadType = input('请选择弹幕下载方式:\n1,下载为ASS字幕(推荐)\n2,强行嵌入视频中')
            VideoDownload = download(Path, self.code, self.num)
            for DownloadIndex in range(len(Part['part'])):
                Url = VideoDownload.get_video_download_urls(DownloadIndex, Quality)
                DownloadPartName = VideoDownload.video_downloader(Url['url'], Url['referer'])
                VideoDownload.danmaku_downloader(Url['cid'])
                if DownloadType == '2':
                    VideoDownload.merge_video_part(inputs = DownloadPartName['filename'], output = 'full.flv')
                    VideoDownload.xml2ass()
                    VideoDownload.flush_ass_to_video(FileName[DownloadIndex])
                else:
                    VideoDownload.merge_video_part(inputs = DownloadPartName['filename'],
                                                   output = FileName[DownloadIndex].replace('/', '-') + '.flv')
                    VideoDownload.xml2ass(FileName[DownloadIndex].replace('/', '-'))
                VideoDownload.del_file()
        return

    def view_user(self):
        UserResponse = user(self.num)
        UserInfo = fill(UserResponse.user_info(), user_module)
        if self.CheckForResponse(UserInfo, ''):
            return
        print('————用户信息————')
        shower.PrintUser(fill(UserInfo, user_module))
        UserTopVideo = fill(UserResponse.user_top_video(), video_module)
        if self.CheckForResponse(UserTopVideo, '当前用户无置顶视频'):
            return
        else:
            print('------置顶视频------')
            shower.PrintVideo(UserTopVideo)
            print('-------------------')

        Choice = input('是否查看用户视频列表(Y/Enter)?').upper()
        if Choice == 'Y':
            Index = 1
            while True:
                UserVideoList = fill(UserResponse.user_video(Index), video_module)
                Page = UserVideoList['pages']
                if Index > Page:
                    break
                for Video in UserVideoList['data']:
                    Video = fill(Video, video_module)
                    shower.PrintVideo(Video)
                    print('-------------------')
                Index += 1
                if input('是否查看下一页?(Enter/exit)') == 'exit':
                    break
                else:
                    continue

    def view_search(self):
        Name = {'video': 'video', 'user': 'bili_user'}
        SearchType = input('请输入搜索类型')
        Data = new_search(keyword = self.num, search_type = Name[SearchType])
        for Index in range(Data.get_pages()):
            Data = new_search(keyword = self.num, page = (Index + 1), search_type = Name[SearchType])
            if SearchType == 'video':
                VideoList = Data.get_video()
                for Video in VideoList:
                    Video = fill(Video, video_module)
                    shower.PrintVideo(Video)
                    print('-------------------')
            if SearchType == 'user':
                UserList = Data.get_user()
                for User in UserList:
                    shower.PrintUser(fill(User, user_module))
                    print('-------------------')
                    # 展示用户视频
                    # for UserVideo in User['top_video']:
                    #     shower.PrintVideo(UserVideo, slice_char = '\n')
                    #     print('-------------------')
            if input('按回车查看下一页,按exit退出') == 'exit':
                break

    def view_bangumi(self):
        pass

    @staticmethod
    def CheckForResponse(data: dict, error = '请求的资源不存在或连接错误') -> bool:
        print(error) if (data['response_code'] != 200 or data['return_code'] != 0) and error else None
        return data['response_code'] != 200 or data['return_code'] != 0


def main(item: list, error_message: str = '输入错误 \n用法: code:num \n例: \n支持的code类型:av,bv,uid'):
    if item[0] == 'av':
        run = viewer('aid', item[1])
        run.view_video()
    elif item[0] == 'bv':
        run = viewer('bvid', item[1])
        run.view_video()
    elif item[0] == 'uid':
        run = viewer('uid', item[1])
        run.view_user()
    elif item[0] == 'cv':
        pass
    elif item[0] == 'search':
        run = viewer('search', item[1])
        run.view_search()
    elif item[0] == 'debug':
        info = bangumi.get_bangumi_info(28224095)
        print(info)
        DataA = bangumi.get_bangumi_data(info['season_id'])
        print(DataA)
        tag_id = bangumi.get_tag_id(info['title'])
        print(tag_id)
        top_video = bangumi.get_top_video(tag_id['tag_id'])
        for x in top_video['videos']:
            print(x)
        print(bangumi.get_episodes(29325))
    elif item[0] == 'console':
        print('已进入调试模式，输入EXIT_CONSOLE以退出')
        console()
    else:
        print(error_message)
    return


if __name__ == '__main__':
    while True:
        message = input('输入你要爬取信息的特征码\n例：uid:439067826:\n').split(':')
        main(item = message)
