# -*- coding: UTF-8 -*-


# using-functions
def bv2av(x):
    alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    r = 0
    for i, v in enumerate([11, 10, 3, 8, 4, 6]):
        r += alphabet.find(x[v]) * 58 ** i
    return (r - 0x2_0840_07c0) ^ 0x0a93_b324


def av2bv(x):
    alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    x = (x ^ 0x0a93_b324) + 0x2_0840_07c0
    r = list('BV1**4*1*7**')
    for v in [11, 10, 3, 8, 4, 6]:
        x, d = divmod(x, 58)
        r[v] = alphabet[d]
    return ''.join(r)


def ceil(x: float) -> int:
    return int(x) if int(x) == x else int(x + 1)


def ReplaceByDict(string: str, replace_list: dict) -> str:
    for replace_str in replace_list:
        string = string.replace(replace_str, replace_list[replace_str])
    return string


def replace_for_web(string: str):
    ReplaceDict = {'&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt': '>', '&nbsp;': ' '}
    return ReplaceByDict(string = string, replace_list = ReplaceDict)


def replace_for_highlight(string: str):
    return string.replace('<em class="keyword">', '<').replace('</em>', '>')


def format_time(time_tick: 'int, float') -> str:
    """
    格式化时间戳为具体日期,例\n
    >>> format_time(123456789)\n
    >>> '1973-11-30 05:33:09'\n
    :param time_tick: 时间戳
    :return: 具体日期
    """
    from time import strftime, localtime
    return strftime('%Y-%m-%d %H:%M:%S', localtime(time_tick))


def TickToMinute(tick: int, minute_time: int = 60) -> str:
    """
    将时间戳转换为分:秒\n例:\n
    >>> TickToMinute(123)\n
    >>> '02:03'\n
    :param tick: 时间戳
    :param minute_time: 每分钟的时间(60)
    :return: 转换后的时间戳
    """
    return f'{str((int(tick / minute_time))).zfill(2)}:{str(tick % minute_time).zfill(2)}'


def extractor(data: dict, dicts: dict = None, copy_list: list = None) -> dict:
    if copy_list is None:
        copy_list = []
    if dicts is None:
        dicts = {}
    try:
        iter(data)  # 检测一个对象是否为可迭代对象，不是就返回
    except TypeError:
        return {}
    return_data = {}
    for copy in copy_list:
        if copy in data.keys():
            return_data.update({copy: data[copy]})
    for x in dicts:  # 遍历dicts的项，获得key
        if type(dicts[x]) is list:  # 如果key的值是一个列表，那么就递归处理
            for key in dicts[x]:
                if key in data:
                    local = extractor(data[key], {x: dicts[x][1:] if len(dicts[x][1:]) != 1 else dicts[x][1:][0]})
                    return_data.update(local if local else {})
        elif x in dicts.keys():  # 如果key的值不是列表且在data的键中，就直接键值对应
            if dicts[x] in data:
                return_data.update({x: data[dicts[x]]})
            else:
                return_data.update({x: None})
    return return_data


def fill(target: dict, fill_list: list, fill_object: any = None) -> dict:
    """
    使用列表来填充字典,例:\n
    >>> fill({1:3}, [1,2,3,4], 5)\n
    >>> {1:3,2:5,3:5,4:5}\n
    :param target: 需要填充的字典
    :param fill_list: 需要填充的键的列表
    :param fill_object: 用于填充空键的对象(None)
    :return: 填充后的字典
    """
    dictionary = target
    for fill_index in set(fill_list):
        dictionary.setdefault(fill_index, fill_object)
    return dictionary


def console(prefix: str = 'Console:', exit_key: str = 'EXIT_CONSOLE') -> None:
    """
    创建一个调试环境\n
    例：\n
    >>> console(prefix = '>>> Console:')\n
    >>> Console: print('hello world!')\n
    >>> Console: hello world!\n
    >>> Console: EXIT_CONSOLE\n
    >>>\n
    :param prefix: 调试环境的前缀(默认'Console: ')
    :param exit_key: 用于退出调试环境的命令（默认'EXIT_CONSOLE'）
    """
    from types import TracebackType
    while True:
        command = input(prefix)
        if command:
            if command == exit_key:
                return
            try:
                command = compile(command, 'input', 'single')
                exec(command)
            except BaseException as Error:
                print('Error:', Error)
                continue


# dev-functions
def replace_for_NTFS(string: str):
    ReplaceDict = {'/': '-', '\\': '-', ':': '-', '*': '-', '<': '-', '>': '-', '?': ''}
    ReplaceByDict(string, ReplaceDict)
    return string


def requests():
    import requests
    requests.old_get = requests.get

    def new_get(url, params = None, **kwargs):
        from time import time
        start_time = time()
        print(f'Requests starts at {format_time(start_time)}. Url:{url}, Other kwargs:{params, kwargs}')
        response = requests.old_get(url = url, params = params, **kwargs)
        print(f'Response at {format_time(time())}. Time:{"{:.3f}".format(time() - start_time)}sec '
              f'Code:{response.status_code}')
        return response

    requests.get = new_get
    return requests


def get(url: str, headers: dict = None, decode: bool = False):
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
    request = Request(url = url, headers = headers if headers else {})
    try:
        req = urlopen(request)
    except HTTPError:
        return {'data': b'', 'complete': False}
    else:
        return {'data': (req.read().decode() if decode else req.read()), 'complete': True}


def simple_request_generator(init, url: str, dicts: dict, extract_data = None, header: dict = None) -> dict:
    from requests import get
    from json import loads
    exec(init)
    Data = get(url, headers = header if header else {})
    JsonData = loads(Data.text)
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            **extractor(data = eval(extract_data) if extract_data else JsonData['data'], dicts = dicts)}


# modules
video_module = [
    'aid', 'bvid', 'owner', 'length', 'upload_time', 'tname', 'copyright', 'introduction',
    'title', 'view', 'danmaku', 'like', 'reply', 'coin', 'collect', 'share']

bangumi_module = ['title', 'score', 'score_count', 'tag_list', 'view', 'danmaku', 'coin', 'start_time', 'new_ep',
                  'season_id', 'num', 'area', 'follower', 'finish', 'start', 'upload_time', 'introduction']

user_module = [
    'name', 'level', 'uid', 'sex', 'vip', 'official', 'fans_badge',
    'birthday', 'sign', 'video_count', 'fans', 'follower', 'following', 'black'
]

reply_module = [
    'name', 'level', 'sex', 'official', 'upload_time',
    'content', 'like', 'reply', 'up_like', 'up_reply', 'replies', 'progress',
    'url', 'score', 'level'
]
