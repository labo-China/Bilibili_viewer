import requests
import json
import time
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
        import Plugin.tool as tool
        bv_coverter = tool.tool()
        returns = []
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
            returns.append({'title' : range_var['title'], 'reply' : range_var['comment'], 'view' : range_var['play'],
                            'upload_time' : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(range_var['created'])),
                            'danmaku' : range_var['video_review'], 'introduction' : range_var['description'],
                            'length' : range_var['length'], 'collect' : range_var['favorites'], 'aid' : range_var['aid'],
                            'bvid' : bv_coverter.av2bv(range_var['aid'])})
            user_video_title.append(range_var['title'])
            user_video_reply.append(range_var['comment'])
            user_video_upload_time.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(range_var['created'])))
            user_video_danmaku.append(range_var['video_review'])
            user_video_view.append(range_var['play'])
            user_video_introduction.append(range_var['description'])
            user_video_length.append(range_var['length'])
            user_video_collect.append(range_var['favorites'])
            user_video_aid.append(range_var['aid'])
        return {'pages' : user_video_pages,'data' : returns}
        # 返回数据
        #return {'title' : user_video_title, 'reply' : user_video_reply, 'upload_time' : user_video_upload_time,
        #        'danmaku' : user_video_danmaku, 'view' : user_video_view, 'introduction' : user_video_introduction,
        #        'length' : user_video_length, 'collect' : user_video_collect, 'aid' : user_video_aid, 'pages' : user_video_pages}