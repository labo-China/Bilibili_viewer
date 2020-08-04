# -*- coding: UTF-8 -*-
from Plugin.user import user
from Plugin.video import video
from Plugin.search import new_search
from Plugin.bangumi import bangumi
from Plugin.download import download
from Plugin.background import *
from Plugin.tool import *


class shower:
    """按格式打印获取的数据"""

    @staticmethod
    def PrintIntroduction(data: dict, chars_limit = 55, hand_char = '\t'):
        """按格式打印简介/长文字\n
            :param data: 文字数据
            :param chars_limit: 一行文字数量限制
            :param hand_char: 每行文字的缩进"""
        Line = data['introduction'].split()
        for Char in Line:
            for Indexer in range(int(len(Char) / chars_limit) + 1):
                try:
                    print(hand_char, end = '')
                    for local in range(chars_limit):
                        print(Char[local + (chars_limit * Indexer)], end = '')
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
        shower.TryPrint('大会员' if data['vip'] else '', ' ', change_line = False)
        shower.TryPrint('关注了', data["following"], '人')
        shower.TryPrint('Bilibili认证:' + data['official'] if data['official'] else '', ' ')
        shower.TryPrint('粉丝勋章已开通' if data['fans_badge'] else '', ' ', change_line = False)
        shower.TryPrint('生日:', data['birthday'] if data['birthday'] else '')
        print('个性签名:', data['sign'])
        shower.TryPrint('稿件:', data['video_count'], change_line = False)
        shower.TryPrint('粉丝:', data['fans'] if data['fans'] else data['follower'])

    @staticmethod
    def PrintReply(data: dict, print_line = False, reply_depth = 0, head_char = '\t'):
        Header = head_char * reply_depth
        print(Header + data['name'], end = ' ')
        shower.TryPrint('LV', data['level'], ' 性别:', data['sex'])
        shower.TryPrint(Header + 'Bilibili认证:' + data['official'] if data['official'] else '')
        print(Header + format_time(data['upload_time']))
        shower.TryPrint('文章url:', data['url'])
        shower.TryPrint(data['progress'], ' ', f'给这部番打了{data["score"]}分')
        shower.PrintIntroduction(data = {'introduction': data['content']}, hand_char = Header)
        print(Header + str(data['like']), '赞', end = ' ')
        shower.TryPrint(data['reply'], ' ', '评论' if reply_depth == 0 else '', other = '')
        shower.TryPrint(Header + 'UP主赞了' if data['up_like'] else '', change_line = False)
        shower.TryPrint(Header + 'UP主回复了' if data['up_reply'] else '', change_line = False)
        print(Header + '————————————————') if print_line else None
        if data['replies']:
            for ChildReply in data['replies']:
                shower.PrintReply(data = fill(ChildReply, reply_module), reply_depth = reply_depth + 1,
                                  print_line = print_line)

    @staticmethod
    def PrintVideo(data: dict):
        shower.TryPrint('自制' if data['copyright'] == '1' else ('转载' if data['copyright'] == 2 else None),
                        ' ', change_line = False)
        shower.TryPrint(data['tname'], ' ', change_line = False)
        print(data['title'], end = ' ')
        shower.TryPrint('作者:', data['owner'], other = '')
        shower.TryPrint('av', data['aid'], change_line = False)
        shower.TryPrint('/', data['bvid'], ' ', change_line = False)
        print(format_time(data['upload_time']), end = ' ')
        shower.TryPrint('时长: ', data['length'], other = '')
        print('简介:')
        shower.PrintIntroduction({'introduction': data['introduction']})
        shower.TryPrint(data['view'], ' 浏览 ', change_line = False)
        shower.TryPrint(data['danmaku'], ' 弹幕 ', change_line = False)
        shower.TryPrint(data['like'], ' 点赞 ', change_line = False)
        shower.TryPrint(data['reply'], ' 评论 ', change_line = False)
        shower.TryPrint(data['coin'], ' 硬币 ', change_line = False)
        shower.TryPrint(data['collect'], ' 收藏 ', change_line = False)
        shower.TryPrint(data['share'], ' 分享 ', other = '')

    @staticmethod
    def PrintBangumi(data: dict):
        print(data['title'], f'{data["score"]}分', *data['tag_list'], f'{data["score_count"]}人评价了此部番剧')
        print(f'{data["view"]}播放 {data["danmaku"]}弹幕 {data["coin"]}硬币 {data["follower"]}人追了此部番')
        print(data['start_time'], data['update_time'], f'已更新至{data["num"]}集')
        print('简介:')
        shower.PrintIntroduction({'introduction': data['introduction']})

    @staticmethod
    def PrintEpisodes(data: dict, header: str = ''):
        print(header + data['short_title'], data['title'])
        print(header + f'ep{data["episode_id"]} av{data["aid"]}')

    @staticmethod
    def PrintLongReply(data: dict):
        print(data['name'], data['uid'])
        shower.TryPrint('文章Url', data['url'])
        print(format_time(data['upload_time']), data['progress'], f'给这部番打了{data["score"]}分')
        shower.PrintIntroduction(data = {'introduction': data['content'] + '...'})
        print(str(data['like']) + '赞', str(data['reply']) + '评论')

    @staticmethod
    def TryPrint(*args, change_line: bool = True, other: str = None) -> None:
        """
        如果args里的值全为真就打印args\n
        :param args: 要检测真伪的值
        :param change_line: 在结尾是否输出\n
        :param other: 如果不打印args时要打印的字符串
        """
        for arg in args:
            if arg is None or arg == '':
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
            Sort = input('选择你的评论排序方式(0=按时间，2=按热度)')
            try:
                Page = 1
                while True:
                    VideoReply = VideoResponse.get_replies(pn = Page, sort = Sort)
                    for Replies in VideoReply['replies']:
                        shower.PrintReply(data = fill(Replies, reply_module), print_line = True)
                    Choice = input('回车以查看下一页评论，输入exit退出:')
                    if Choice == 'exit':
                        raise IndexError
                    else:
                        if Page == VideoReply['all_page']:
                            raise IndexError
                        Page += 1
                        continue
            except IndexError:
                pass

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
            VideoDownload = download(Path, self.code, self.num)
            for DownloadIndex in range(len(Part['part'])):
                Url = VideoDownload.get_video_download_urls(DownloadIndex, Quality)
                DownloadPartName = VideoDownload.video_downloader(Url['url'], Url['referer'])
                VideoDownload.danmaku_downloader(Url['cid'])
                VideoDownload.merge_video_part(inputs = DownloadPartName['filename'],
                                               output = FileName[DownloadIndex].replace('/', '-') + '.flv')
                VideoDownload.xml2ass(FileName[DownloadIndex].replace('/', '-'))
                VideoDownload.del_file()
        return

    def view_user(self):
        UserResponse = user(self.num)
        UserInfo = fill({**UserResponse.user_info(), **UserResponse.user_follows()}, user_module)
        if self.CheckForResponse(UserInfo):
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
                if Index == Page:
                    break
                elif input('是否查看下一页?(Enter/exit)') == 'exit':
                    break
                else:
                    Index += 1
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
        BangumiInfo = bangumi.get_bangumi_info(self.num)
        SeasonId = BangumiInfo['season_id']
        BangumiData = bangumi.get_bangumi_data(SeasonId)
        BangumiHTMLData = bangumi.get_bangumi_data_by_html(self.num)
        BangumiTagId = bangumi.get_tag_id(BangumiInfo['title'])
        BangumiStatus = bangumi.get_status(SeasonId)
        Data = {**BangumiInfo, **BangumiData, **BangumiHTMLData}
        if self.CheckForResponse(Data):
            return
        print('------番剧信息------')
        shower.PrintBangumi(fill(Data, bangumi_module))
        if BangumiStatus['area_limit']:
            if input('当前番剧可能受到地区限制,访问可能出现异常,是否继续(Enter/Y)') == '':
                return

        if input('是否查看具体剧集列表?(Y/Enter)').upper() == 'Y':
            EpisodesList = bangumi.get_episodes(SeasonId)
            print('------正片------')
            for MainEpisode in EpisodesList['main_episodes']:
                shower.PrintEpisodes(MainEpisode, '\t')
                print('\t------------------')
            print('------附加------') if EpisodesList['other_episodes'] else None
            for OtherEpisodes in EpisodesList['other_episodes']:
                shower.PrintEpisodes(OtherEpisodes, '\t')
                print('\t------------------')

        def reply_(reply_type: str, page_size: int):
            if input(f'是否获取{"长" if reply_type == "long" else "短"}评列表?(Y/Enter)').upper() == 'Y':
                Sort = input('选择你的评论排序方式(1=按时间，0=按用户评分)')
                RepliesList = bangumi.get_replies(self.num, reply_type = reply_type, sort = Sort, page_size = page_size)
                Page = ceil(RepliesList['total'] / page_size)
                print('total', Page)
                for index in range(Page):
                    if len(RepliesList['replies']) == 0:
                        break
                    for Replies in RepliesList['replies']:
                        shower.PrintReply(fill(Replies, reply_module))
                        print('----------------')
                    if input('回车以查看下一页评论,输入exit退出') == 'exit':
                        raise BaseException
                    cursor = RepliesList['cursor']
                    RepliesList = bangumi.get_replies(self.num, reply_type = reply_type, sort = Sort, cursor = cursor,
                                                      page_size = page_size)

        reply_('short', 20)
        reply_('long', 1)

        if input('是否查看相关视频?(Y/Enter)').upper() == 'Y':
            RelateVideoList = bangumi.get_relate_video(BangumiTagId['tag_id'])
            Index = 1
            while not self.CheckForResponse(RelateVideoList, error = ''):
                for Video in RelateVideoList['videos']:
                    print('----------------')
                    shower.PrintVideo(fill(Video, video_module))
                if input('回车以查看下一页视频,输入exit退出') == 'exit':
                    break
                Index += 1
                RelateVideoList = bangumi.get_relate_video(BangumiTagId['tag_id'], page = Index)
            # print('----------------')

    @staticmethod
    def CheckForResponse(data: dict, error = '请求的资源不存在或连接错误') -> bool:
        print(error) if (data['response_code'] != 200 or data['return_code'] != 0) and error else None
        return data['response_code'] != 200 or data['return_code'] != 0


def main(item: list, error_message: str = '输入错误 例:\nav:2\nuid:2\nbv:1xx411c7mD\nsearch:bilibili\nconsole\nexit'):
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
    elif item[0] == 'md':
        run = viewer('md', item[1])
        run.view_bangumi()
    elif item[0] == 'search':
        run = viewer('search', item[1])
        run.view_search()
    elif item[0] == 'debug':
        print('####################')
        print('#   Debugging...   #')
        print('#   Item:Bangumi   #')
        print('####################')
        print('------info------')
        info = bangumi.get_bangumi_info(28222671)
        print(info)
        print('------data------')
        DataA = bangumi.get_bangumi_data(info['season_id'])
        print(DataA)
        print('------html_data------')
        print(bangumi.get_bangumi_data_by_html(28222671))
        print('------tag_id------')
        tag_id = bangumi.get_tag_id(info['title'])
        print(tag_id)
        print('------top_video------')
        top_video = bangumi.get_top_video(tag_id['tag_id'])
        for x in top_video['videos']:
            print(x)
        print('------episodes------')
        print(bangumi.get_episodes(info['season_id']))
        print('------short_reply------')
        print(bangumi.get_replies(28222671))
        print('------long_reply------')
        print(bangumi.get_replies(media_id = 28222671, reply_type = 'long'))
    elif item[0] == 'console':
        print('已进入调试模式，输入EXIT_CONSOLE以退出')
        console()
    elif item[0] == 'exit':
        from sys import exit
        exit()
    else:
        print(error_message)
    return


if __name__ == '__main__':
    while True:
        print('--------------------')
        message = input('输入你要爬取信息的特征码\n例：uid:439067826:\n').split(':')
        main(item = message)
