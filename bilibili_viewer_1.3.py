import re
import time
import requests
import json
import you_get
import os

def video(av_num):
    global headers
    # 请求第一个视频信息
    data = requests.get('http://api.bilibili.com/archive_stat/stat?aid=' + str(av_num), headers=headers)
    code = json.loads(data.text)
    # 获取并判断运行码是否有错误，如果有就返回错误原因
    runcode = code['code']
    if runcode == 40001 or runcode == 40003:
        print('视频不存在')
        exit()
    # 获取浏览，弹幕，评论，点赞，踩，硬币，收藏，分享，版权
    view = code['data']['view'] # 浏览
    danmaku = code['data']['danmaku'] # 弹幕
    reply = code['data']['reply'] # 评论
    like = code['data']['like'] # 点赞
    dislike = code['data']['dislike'] # 踩
    coin = code['data']['coin'] # 硬币
    collect = code['data']['favorite'] # 收藏
    share = code['data']['share'] # 分享
    if code['data']['copyright'] == 1: # 视频版权
        made = '自制'
    else:
        made = '转载'
    # 请求第二个视频信息
    updata = requests.get('https://api.bilibili.com/x/web-interface/view?aid=' + str(av_num), headers=headers)
    upcode = json.loads(updata.text)
    # 获取UP主名字，标题，视频分区
    owner = upcode['data']['owner']['name'] # 名字
    title = upcode['data']['title'] # 标题
    tname = upcode['data']['tname'] # 分区
    # 如果视频分区为空就返回未知
    if tname == '':
        tname = '未知'
    # 格式化Unix时间戳为正常时间
    uploadtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(upcode['data']['ctime'])) # 上传时间
    # 请求UP主信息
    up = requests.get('https://search.bilibili.com/upuser?keyword=' + owner, headers=headers)
    upinfo = up.text
    # 获取UP主等级，个性签名/认证，稿件数量，粉丝数量
    lv = re.findall('"lv icon-lv(.*?)"',upinfo)[0] # 等级
    tag = re.findall('<div class="desc">\n(.*?)\n', upinfo)[0][6:] # 签名/认证
    videonum = re.findall('<span>稿件：(.*?)</span>', upinfo)[0] # 稿件数量
    fans = re.findall('<span>粉丝：(.*?)</span>', upinfo)[0] # 粉丝数量
    # 获取简介（B站能不能出一个完整的api啊喂，这都请求第四个了TAT）
    introduction_url = requests.get('https://api.bilibili.com/x/web-interface/archive/desc?&aid=' + av_num,headers = headers).text
    introduction = re.findall('data":"(.*?)"}',introduction_url)[0] # 简介
    # 打印信息
    print('————作品信息————')
    print('标题:', title)
    print('视频类型:', tname,made)
    print('上传时间:', uploadtime)
    print('av号:', av_num)
    print('url:https://www.bilibili.com/video/av{}'.format(av_num))
    print('简介:',end='')
    for x in range(int(len(introduction) / 45) + 1): # 45个字一行显示简介
        try:
            for local in range(45):
                print(introduction[local + (45 * x)],end='')
            print('')
            print('     ', end='')# 在第一行后每行前面缩进一个tab
        except IndexError: # 读取完成就退出
            break
    print('')
    print('浏览:', view)
    print('弹幕:', danmaku)
    print('点赞:', like)
    if int(dislike) >= 1:
        print('踩:', dislike)
    print('评论:', reply)
    print('硬币:', coin)
    print('收藏:', collect)
    print('分享:', share)
    print('————作者信息————')
    print('作者:', owner)
    print('等级: LV',lv)
    print('签名:', tag)
    print('稿件:', videonum)
    print('粉丝:', fans)

    if input('是否展示评论？（Y/Enter）') == 'Y':
        if input('请选择评论展示方式：按热度（H）/按时间（T）') == 'H': # 确定评论排序
            sort = '2'
        else:
            sort = '0'
        user_name = [] # 评论用户信息
        user_level = [] # 用户等级
        user_sex = [] # 用户性别
        user_offical = [] # 用户认证
        like_details = [] # 赞数
        reply_details = [] # 评论数
        reply_upload_time = [] #评论上传时间
        content = [] # 评论内容
        up_like = [] # UP主的赞
        up_reply = [] # UP主的评论

        about_reply = requests.get('https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={}&sort={}&_=1558948726737'.format(av_num,sort), headers = headers).text
        # 获取页数
        page = int(re.findall('"page":{"num":.*?,"size":.*?,"count":(.*?),', about_reply)[0]) // 20 + 1
        for i in range(page):
            print('正在爬取第{}页'.format(i))
            about_reply = requests.get(
                'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid={}&sort={}&_=1558948726737'.format(i,av_num, sort), headers=headers).text
            user_name += re.findall('"like":.*?,"action":.*?,"member":{"mid":".*?","uname":"(.*?)"',about_reply) # 匹配当前页所有的用户名
            user_name.append(re.findall('"uname":"(.*?)"', about_reply)[-1])
            user_level += re.findall('"current_level":(.*?),', about_reply) # 匹配当前页所有的用户等级
            user_sex += re.findall('"sex":"(.*?)"', about_reply) # 匹配当前页所有的用户性别
            user_offical += re.findall('"desc":"(.*?)"},', about_reply)[1:] # 匹配当前页所有的用户认证
            like_details += re.findall(',"like":(.*?),', about_reply) # 匹配当前页所有的赞数
            reply_details += re.findall('"rcount":(.*?),', about_reply) # 匹配当前页所有的评论数
            for utime in range(len(re.findall('"ctime":(.*?),', about_reply))): # 匹配当前页所有的评论上传时间并格式化
                reply_upload_time.append(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(re.findall('"ctime":(.*?),', about_reply)[utime])))))
            content += re.findall('{"message":"(.*?)"', about_reply) # # 匹配当前页所有的评论正文
            up_like += re.findall('"up_action":{"like":(.*?),"reply":.*?}', about_reply) # 匹配当前页所有的UP赞信息
            up_reply += re.findall('"up_action":{"like":.*?,"reply":(.*?)}', about_reply) # 匹配当前页所有的UP评论信息
            time.sleep(0.3) # 时停，避免访问量过大封IP
        y = 0 # 计评论数，10个一组
        for x in range(len(like_details)):
            # 按照列表打印评论详情
            y += 1
            print('————————————————————————')
            print(user_name[x],' LV',user_level[x],' 性别:',user_sex[x]) # 打印用户名称、姓名、等级
            if user_offical[x] != '': # 如果有认证就打印
                print('Bilibili认证:',user_offical[x])
            print(reply_upload_time[x]) # 打印上传时间
            for a in range(int(len(content[x]) / 45) + 1):  # 45个字一行显示评论
                try:
                    for local in range(45):
                        print(content[x][local + (45 * a)], end='')
                    print('')
                    print('     ', end='')  # 在第一行后每行前面缩进一个tab
                except IndexError:
                    break
            print('')
            print(like_details[x],'赞',reply_details[x],'评论')
            # 判断UP主是否与评论有互动
            if up_like[x] == 'True':
                print('UP主赞了')
            if up_reply[x] == 'False':
                print('UP主回复了')
            if y % 10 == 0: # 10个评论为一组显示
                if input('回车以查看下10个评论，输入exit退出评论:') == 'exit':
                    break

    if input('是否要下载视频？(Y/Enter)') != '':
        if input('选择你的下载方式:直接下载（D）/获取直链链接（G）') == 'D':
            path = input('请输入完整路径和文件名:')
            # 使用you-get下载
            os.system('you-get ' + '-O ' + path + ' https://www.bilibili.com/video/av{}'.format(av_num))
            input('下载成功')
        else:
            # 获取视频cid
            cid = re.findall('"cid":(.*?),',requests.get('https://api.bilibili.com/x/player/pagelist?aid={}'.format(av_num),headers=headers).text)[0]
            # 获取直链下载链接
            download_url = requests.get('http://www.xbeibeix.com/api/bilibiliapi.php?url=https://www.bilibili.com/&aid={}&cid={}'.format(av_num,cid))
            target_url = re.findall('"url": "(.*?)"', download_url.text)[0]
            print('直链:',target_url)


def person(uid):
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.43 Safari/537.36 Edg/81.0.416.28',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q = 0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'api.bilibili.com',
        'Cookie': r'_uuid=2B118F55-42AC-EEC0-5308-3DD0C0E9462721668infoc; buvid3=80EB36A3-ED3A-41F2-85CB-7CF9A2030209155836infoc;sid=m3uqaw2k; LIVE_BUVID=AUTO9015813863101871; CURRENT_FNVAL=16; rpdid=|(umu|RkYJll0J' + 'ul)uJ)YR~~; im_notify_type_439067826=0; dy_spec_agreed=1; INTVER=1; CURRENT_QUALITY=0; bili_jct=0796879f8f94b502cb421afedb6b46a6; SESSDATA=e98c43ab%2C1599531641%2Cdd890*31; DedeUserID__ckMd5=f0747ba893987099; DedeUserID=439067826; flash_player_gray=false; html5_player_gray=false; bp_t_offset_439067826=366026583373461264; PVID=1'}
    basic_data = json.loads(requests.get('https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(uid),headers = head).text) # 请求用户基础信息
    if basic_data['code'] == -404 or basic_data['code'] == -403: # 如果返回码错误，则退出
        print('用户不存在')
        exit()
    name = basic_data['data']['name'] # 名字
    sex = basic_data['data']['sex'] # 性别
    sign = basic_data['data']['sign'] # 签名
    level = basic_data['data']['level'] # 等级
    birthday = basic_data['data']['birthday'] # 生日
    coins = basic_data['data']['coins'] # 硬币
    official = basic_data['data']['official']['title'] # 认证
    vip = basic_data['data']['vip']['status'] # 会员状态
    fans_badge = basic_data['data']['fans_badge'] # 粉丝勋章状态
    # 置顶视频
    Top_video = json.loads(requests.get('https://api.bilibili.com/x/space/top/arc?vmid={}'.format(uid)).text)
    if Top_video['message'] == '没有置顶视频': # 判断是否有置顶视频
        print('当前用户没有置顶视频')
        exit()
    av_num = Top_video['data']['aid'] # av号
    tname = Top_video['data']['tname'] # 分区
    if Top_video['data']['copyright'] == 1: # 版权
        made = '自制'
    else:
        made = '转载'
    title = Top_video['data']['title'] # 标题
    upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(Top_video['data']['ctime'])) # 上传时间
    introduction = Top_video['data']['desc'] # 简介
    view = Top_video['data']['stat']['view'] # 浏览
    danmaku = Top_video['data']['stat']['danmaku'] # 弹幕
    reply = Top_video['data']['stat']['reply'] # 评论
    like = Top_video['data']['stat']['like'] # 赞
    dislike = Top_video['data']['stat']['dislike'] # 踩
    coin = Top_video['data']['stat']['coin'] # 硬币
    collect = Top_video['data']['stat']['favorite'] # 收藏
    share = Top_video['data']['stat']['share'] # 分享


    print('————用户信息————')
    print('昵称:',name)
    print('LV',level,end=' ')
    if vip == 1: # 判断是否有大会员
        print('大会员')
    else:
        print('')
    print('性别:',sex)
    if official != '': # 判断是否有认证
        print('Bilibili认证:',official)
    print('个性签名:',sign)
    if fans_badge:
        print('开通了粉丝勋章')
    print('硬币:',coins)
    if birthday != '': # 判断是否有生日
        print('生日:',birthday)

    check = json.loads(requests.get('http://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&'.format(uid), headers=headers).text)
    if check['data']['count'] == 0: # 检测用户是否有视频
        print('当前用户没有投稿视频')
        exit()

    print('————置顶信息————')
    print('标题:',title,' ',tname,' av',av_num)
    print('上传时间:',upload_time,made)
    print('简介:')
    if '\n' not in introduction:
        for x in range(int(len(introduction) / 45) + 1):  # 45个字一行显示简介
            try:
                for local in range(45):
                    print(introduction[local + (45 * x)], end='')
                print('')
                print('     ', end='')  # 在第一行后每行前面缩进一个tab
            except IndexError:
                print('')
                break
    else:
        print('     ' + introduction)
    print('浏览:',view,' 弹幕:',danmaku,' 评论',reply,' 赞:',like,' 踩',dislike,' 硬币',coin,' 收藏:',collect,' 分享:',share)
    print('————————————————')
    if input('是否展示视频信息？（Y/N）') == 'Y':
        video_list = requests.get('http://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&'.format(uid),headers = headers).text
        page = int(re.findall('"pages":(.*?)}', video_list)[-1]) # 获取页数
        video_title = [] # 标题
        video_reply = [] # 评论
        video_upload_time = [] # 视频上传时间
        video_danmaku = [] # 弹幕
        video_view = [] # 浏览
        video_introduction =[] # 简介
        video_len = [] # 视频长度
        video_collect = [] # 收藏
        video_avnum = [] # 视频av号
        for data in range(page):
            video_data = json.loads(requests.get('http://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pn={}'.format(uid,data),headers = headers).text)
            for video_detail in range(20):
                try:
                    video_title.append(video_data['data']['vlist'][video_detail]['title'])
                    video_reply.append(video_data['data']['vlist'][video_detail]['comment'])
                    video_upload_time.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(video_data['data']['vlist'][video_detail]['created'])))
                    video_danmaku.append(video_data['data']['vlist'][video_detail]['video_review'])
                    video_view.append(video_data['data']['vlist'][video_detail]['play'])
                    video_introduction.append(video_data['data']['vlist'][video_detail]['description'])
                    video_len.append(video_data['data']['vlist'][video_detail]['length'])
                    video_collect.append(video_data['data']['vlist'][video_detail]['favorites'])
                    video_avnum.append(video_data['data']['vlist'][video_detail]['aid'])
                except IndexError:
                    break
        for z in range(len(video_title)):
            print('————————————————')
            print('标题:', video_title[z])
            print('av',video_avnum[z],' 上传时间:',video_upload_time[z],' 时长:',video_len[z])
            print('简介:',end='')
            if '\n' not in video_introduction[z]:
                for x in range(int(len(video_introduction[z]) / 45) + 1):  # 45个字一行显示简介
                    try:
                        for local in range(45):
                            print(video_introduction[z][local + (45 * x)], end='')
                        print('')
                        print('     ', end='')  # 在第一行后每行前面缩进一个tab
                    except IndexError:
                        print('')
                        break
            else:
                print('     ' + video_introduction[z])
            print(video_view[z],'浏览',video_reply[z],'评论',video_danmaku[z],'弹幕',video_collect[z],'收藏')
        input('运行结束，按回车退出')

# 设置User-Agent
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/81.0.4044.43 Safari/537.36 Edg/81.0.416.28',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-CN,zh;q = 0.9'}
item = input('输入你要爬取信息的号码（用户uid/视频av/文章cv）,示例：uid:439067826:').split(':')
# 按照信息前缀判断信息类型
if item[0] == 'av':
    video(item[1])
elif item[0] == 'uid':
    person(item[1])
