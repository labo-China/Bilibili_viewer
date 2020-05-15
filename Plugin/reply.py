import requests
import json
from Plugin.tool import tool
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
            self.num = tool.bv2av('BV' + self.num)
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