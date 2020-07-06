import hashlib
import requests
import re
import json
import os
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
        self.save_path = save_path.replace('/','\\')
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
            print('下载中...[{}/{}]'.format(range_var + 1, len(url)))
            # 获取分段文件
            data = requests.get(url[range_var],headers=self.headers)
            # 写入数据
            if not os.path.exists(self.save_path):
                os.system('mkdir ' + self.save_path)
                print('mkdir ' + self.save_path)
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
        os.system('DanmakuFactory\DanmakuFactory.exe -i "{}danmaku.xml" -o "{}{}.ass"'.format(self.save_path, self.save_path, filename.replace('/','\\\\')))
        return

    def merge_video_part(self,inputs, output):
        print('正在合并视频分段...')
        # 根据写入的视频分段名称把名字写入filelist.txt
        with open(self.save_path + 'filelist.txt', 'w', encoding = 'utf-8') as file:
            for filename in inputs:
                file.write('file \'{}\'\n'.format(self.save_path + filename))
        # 使用FFmpeg读取filelist.txt并合并其中的文件
        os.system('ffmpeg.exe -f concat -safe 0 -i {}filelist.txt -c copy "{}{}"'.format(self.save_path, self.save_path, output))

    def flush_ass_to_video(self,filename):
        # 获取合成后的文件分辨率并写入quality.txt
        os.system(r'ffmpeg.exe -i {}full.flv 2> {}quality.txt'.format(self.save_path, self.save_path))
        # 获取视频分辨率
        quality = re.findall(r'(\d*x\d*)',open(self.save_path + 'quality.txt').read())[0]
        print('正在冲入ASS字幕...')
        # 使用ffmpeg将ass字幕打入视频流中
        os.system(r'/ffmpeg.exe -i {}full.flv -i {}danmaku.ass -vf ass=\'{}danmaku.ass\' -strict -2 -s {}.flv'.format(
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