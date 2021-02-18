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


class pattern:
    def __init__(self, dict_pattern: dict = None, list_pattern: list = None):
        self.dict_pattern = dict_pattern or {}
        self.list_pattern = list_pattern or []

    @staticmethod
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

    def match(self, data: dict):
        return self.extractor(data = data, dicts = self.dict_pattern, copy_list = self.list_pattern)

    def __call__(self, *args, **kwargs):
        return self.match(*args, **kwargs)


extractor = pattern.extractor


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


def replace_for_NTFS(string: str):
    ReplaceDict = {'/': '-', '\\': '-', ':': '-', '*': '-', '<': '-', '>': '-', '?': '-'}
    ReplaceByDict(string, ReplaceDict)
    return string
