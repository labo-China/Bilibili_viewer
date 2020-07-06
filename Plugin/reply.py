import requests
import json
from Plugin.tool import av2bv, bv2av, extractor


class reply:
    """Get Bilibili replies"""
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

    @staticmethod
    def video_reply(types, num, pn, sort):
        """Return video replies"""
        if types == 'bvid':
            num = bv2av('BV' + num)
        data = requests.get(f'http://api.bilibili.com/x/v2/reply?pn={pn}&type=1&sort={sort}&oid={num}',
                            headers = reply.headers)
        response_code = data.status_code
        data = json.loads(data.text)
        return_code = data['code']
        all_page = int(data['data']['page']['count'])
        # 获得页数（向上取整）
        if not all_page / 20 == int(all_page / 20):
            all_page = int(all_page / 20) + 1
        else:
            all_page = all_page / 20
        replies = []
        ReplyDict = {'name': ['member', 'uname'], 'level': ['member', 'level_info', 'current_level'],
                     'sex': ['member', 'sex'], 'official': ['member', 'official_verify', 'desc'],
                     'like': 'like', 'reply': 'rcount', 'upload_time': 'ctime', 'content': ['content', 'message'],
                     'up_like': ['up_action', 'like'], 'up_reply': ['up_action', 'reply']}
        for Reply in data['data']['replies']:
            replies.append({**extractor(data = Reply, dicts = ReplyDict), 'replies': []})
            if Reply['replies']:
                for range_var1 in Reply['replies']:
                    replies[len(replies) - 1]['replies'].append(
                        {**extractor(data = range_var1, dicts = ReplyDict), 'replies': []})
        # 返回数据
        return {'return_code': return_code, 'response_code': response_code, 'replies': replies, 'all_page': all_page}
