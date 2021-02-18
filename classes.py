from scripts.tool import parseable as psb
from scripts.tool import log_str


class Video:
    from WebApi import video

    def __init__(self, code: psb, num: psb, sort: psb = 0, quality: psb = 80):
        self.code = 'aid' if code == 'av' else ('bvid' if code == 'bv' else code)
        self.num = num
        self.sort = sort
        self.quality = quality

        self.video_type = ''
        self._data = {}
        self._raw = ''

        self.cid_list = [part['cid'] for part in Video.video.get_part(self.code, self.num)['part']]

    def load(self, data: dict = None):
        if data:
            # load given data
            self._data = data
        else:
            # load data from WebApi.video
            web_data = [
                Video.video.get_info(self.code, self.num),
                Video.video.get_introduction(self.code, self.num),
                Video.video.get_data(self.code, self.num),
                Video.video.get_part(self.code, self.num),
                Video.video.get_tags(self.code, self.num),
            ]
            for d in web_data:
                self._data.update(d)
                if d['response_code'] != 200 or d['return_code']:
                    print(log_str(f'Warning: The code of data from url "{d["url"]}" is unsafe!', 'warning'))
            self._data.pop('response_code')
            self._data.pop('return_code')

            if Video.video.get_questions(self._data['aid'], self._data['bvid'])['return_code'] != -1:
                self.video_type = 'interactive'
            else:
                self.video_type = 'normal'
