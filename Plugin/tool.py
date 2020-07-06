import time
from urllib.request import *
from urllib.error import *


# functions
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


def ReplaceByDict(string: str, replace_list: dict) -> str:
    for replace_str in replace_list:
        string = string.replace(replace_str, replace_list[replace_str])
    return string


def replace_for_NTFS(string: str):
    ReplaceDict = {'/': '-', '\\': '-', ':': '-', '*': '-', '<': '-', '>': '-', '?': ''}
    ReplaceByDict(string, ReplaceDict)
    return string


def replace_for_web(string: str):
    ReplaceDict = {'&quot;': '"', '&amp;': '&', '&lt;': '<', '&gt': '>', '&nbsp;': ' '}
    return ReplaceByDict(string = string, replace_list = ReplaceDict)


def replace_for_highlight(string: str):
    return string. \
        replace('<em class="keyword">', '<'). \
        replace('</em>', '>')


def format_time(time_tick: int) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_tick))


def TickToMinute(tick: int, minute_time: int = 60) -> str:
    return f'{str((int(tick / minute_time))).zfill(2)}:{str(tick % minute_time).zfill(2)}'


def extractor(data: dict, dicts: dict):
    return_data = {}
    try:
        iter(data)  # 检测一个对象是否为可迭代对象，不是就返回
    except TypeError:
        return
    for x in dicts:  # 遍历dicts的项，获得key
        if type(dicts[x]) is list:  # 如果key的值是一个列表，那么就递归处理
            for key in dicts[x]:
                if key in data:
                    local = extractor(data[key], {x: dicts[x][1:] if len(dicts[x][1:]) != 1 else dicts[x][1:][0]})
                    return_data.update(local if local else dict())
        elif x in dicts.keys():  # 如果key的值不是列表且在data的键中，就直接键值对应
            return_data.update({x: data[dicts[x]]})
    return return_data


def fill(target: dict, fill_list: list, fill_object: any = None) -> dict:
    dictionary = target
    for fill_index in set(fill_list):
        dictionary.setdefault(fill_index, fill_object)
    return dictionary


def get(url: str, headers: dict = None, decode: bool = True):
    request = Request(url = url, headers = headers if headers else {})
    try:
        req = urlopen(request)
    except HTTPError:
        return {'data': b'', 'complete': False}
    else:
        return {'data': req.read().decode() if decode else req.read(), 'complete': True}


def console(prefix: str = 'Console:', exit_key: str = 'EXIT_CONSOLE') -> None:
    """
    创建一个调试环境\n
    例：\n
    >>> console()\n
    Console: print('hello world!')\n
    hello world!\n
    Console: EXIT_CONSOLE\n
    >>>\n
    :param prefix: 调试环境的前缀(默认'Console: ')
    :param exit_key: 用于退出调试环境的命令（默认'EXIT_CONSOLE'）
    """
    while True:
        command = input(prefix)
        if command == exit_key:
            return
        try:
            command = compile(command, 'command', 'single')
            exec(command)
        except Exception as Error:
            print('Error:', Error)
            continue


# modules
video_module = [
    'aid', 'bvid', 'owner', 'length', 'upload_time', 'tname', 'copyrights', 'introduction',
    'title', 'view', 'danmaku', 'like', 'reply', 'coin', 'collect', 'share']

user_module = [
    'name', 'level', 'uid', 'sex', 'vip', 'official', 'fans_badge',
    'birthday', 'sign', 'video_count', 'fans'
]

reply_module = [
    'user_name', 'user_level', 'user_sex', 'user_official', 'upload_time',
    'content', 'like', 'reply', 'up_like', 'up_reply', 'replies'
]
