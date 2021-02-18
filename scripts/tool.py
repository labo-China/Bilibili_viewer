# coding: UTF-8
from typing import Union


# using-functions
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


def bp_mnt():
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
               'from scripts.tool import *',
               'from scripts.data_process import *',
               'import requests, re, json']

parseable = Union[int, str]
