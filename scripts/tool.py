# coding: UTF-8
from typing import Union


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


def format_time(time_tick: Union[int, float]) -> str:
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
    copy_list = [] if copy_list is None else copy_list
    dicts = {} if dicts is None else dicts
    try:
        iter(data)  # 检测一个对象是否为可迭代对象，不是就返回
    except TypeError:
        return {}
    return_data = {}
    for copy in copy_list:
        return_data.update({copy: data[copy]} if copy in data else set())
    for x in dicts:  # 遍历dicts的项，获得key
        if type(dicts[x]) is list:  # 如果key的值是一个列表，那么就递归处理
            for key in dicts[x]:
                if key in data:
                    local = extractor(data[key], {x: dicts[x][1:] if len(dicts[x][1:]) != 1 else dicts[x][1:][0]})
                    return_data.update(local if local else {})
        elif x in dicts:  # 如果key的值不是列表且在data的键中，就直接键值对应
            return_data.update({x: data[dicts[x]]} if dicts[x] in data else {x: None})
    return return_data


def get_null_data(mode_dict: dict) -> dict:
    for x in mode_dict:
        mode_dict[x] = ''
    return mode_dict


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


def console(prefix: str = 'Console:', exit_key: str = 'EXIT_CONSOLE', print_traceback: bool = True,
            catch_error: bool = True) -> None:
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
    :param print_traceback: 指定是否打印完整的报错内容(默认:True)
    :param catch_error: 指定是否抓取错误(默认True)
    """
    from traceback import print_exc
    for init_scripts in init_script:
        exec(init_scripts)
    while True:
        command = input(prefix)
        if command:
            if command == exit_key:
                return
            elif catch_error:
                try:
                    command = compile(command, 'command', 'single')
                    exec(command)
                except BaseException as Error:
                    if print_traceback:
                        print_exc()
                    else:
                        print(Error)
                    continue
            else:
                command = compile(command, 'command', 'single')
                exec(command)


# dev-functions
def replace_for_NTFS(string: str):
    ReplaceDict = {'/': '-', '\\': '-', ':': '-', '*': '-', '<': '-', '>': '-', '?': '-'}
    ReplaceByDict(string, ReplaceDict)
    return string


def requests_debug():
    from functools import wraps
    import requests

    def decorator(func, method):
        @wraps(func)
        def func_(url, params = None, data = None, json = None, **kwargs):
            from time import time
            start_time = time()
            print(log_str(f'Requests[{method.upper()}] starts at {format_time(start_time)}. Url:{url}'))
            print(log_str('kwargs:' + str(kwargs))) if kwargs else None
            response = func(url = url, params = params, data = data, json = json, **kwargs)
            print(log_str(f'Response at {format_time(time())}. Time:{"{:.3f}".format(time() - start_time)}sec '
                          f'Code:{response.status_code}'))
            return response

        return func_

    requests.get_ = requests.get
    requests.options_ = requests.options
    requests.head_ = requests.head
    requests.post_ = requests.post
    requests.put_ = requests.put
    requests.patch_ = requests.patch
    requests.delete_ = requests.delete

    def get(url, params = None, **kwargs):
        response = requests.get_(url = url, params = params, **kwargs)
        return response

    def options(url, **kwargs):
        response = requests.options_(url = url, **kwargs)
        return response

    def head(url, **kwargs):
        response = requests.head_(url = url, **kwargs)
        return response

    def post(url, data = None, json = None, **kwargs):
        response = requests.post_(url = url, data = data, json = json, **kwargs)
        return response

    def put(url, data = None, **kwargs):
        response = requests.put_(url = url, data = data, **kwargs)
        return response

    def patch(url, data = None, **kwargs):
        response = requests.patch_(url = url, data = data, **kwargs)
        return response

    def delete(url, **kwargs):
        response = requests.delete_(url = url, **kwargs)
        return response

    requests.get = decorator(get, 'get')
    requests.options = decorator(options, 'options')
    requests.head = decorator(head, 'head')
    requests.post = decorator(post, 'post')
    requests.put = decorator(put, 'put')
    requests.patch = decorator(patch, 'patch')
    requests.delete = decorator(delete, 'delete')
    return requests


def urllib_get(url: str, headers: dict = None, decode: bool = False) -> dict:
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


def get_request(*args, **kwargs):
    from requests import models
    return models.Request(*args, **kwargs).prepare()


def simple_request(url: str, session = None, method: str = 'get', **kwargs):
    from requests import Session
    from json import loads
    if not isinstance(session, Session) or session is None:
        session = Session()
    Data = session.request(url = url, method = method, **kwargs)
    if Data.status_code != 200:
        return {'status': 'fail', 'req': Data.content}
    else:
        try:
            JsonData = loads(Data.text)
        except json.JSONDecodeError:
            return {'status': 'json_fail', 'req': Data.content}
        else:
            return {'status': 'success' if JsonData['code'] == 0 else 'fail', 'req': JsonData}


def log_str(string: str, label: str = 'info') -> str:
    def merge_color_string(print_type: str = None, fore_color: str = None, background_color: str = None):
        color_dict = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
                      'purple': 35, 'cyan': 36, 'white': 37}
        type_dict = {'default': 0, 'bold': 1, 'underline': 4, 'shining': 5, 'reverse': 7}
        type_code = '' if print_type not in type_dict else type_dict[print_type]
        fore_code = '' if fore_color not in color_dict else ';' + str(color_dict[fore_color])
        background_code = '' if background_color not in color_dict else ';' + str(color_dict[background_color] + 10)
        return [f'\033[{type_code}{fore_code}{background_code}m', '\033[m']

    label_dict = {'info': {'fore_color': 'white'}, 'warning': {'fore_color': 'yellow'}, 'error': {'fore_color': 'red'}}
    return string.join(merge_color_string(**label_dict[label])) if string is not None else ''


def break_point_mnt():
    """Mount your debugger point at here!"""
    print('BREAK!')
    raise BaseException
    
    
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

init_script = ['from WebApi.video import video',
               'from WebApi.user import user',
               'from WebApi.search import new_search',
               'from WebApi.bangumi import bangumi',
               'from FileApi.download import download',
               'from WebApi.background import *',
               'from WebApi.tool import *',
               'import requests, re']

parseable = Union[int, str]
