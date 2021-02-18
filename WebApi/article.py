# coding: UTF-8
from scripts.tool import extractor
import requests
import json


def get_article_info(article_id: int) -> dict:
    Data = requests.get(f'https://api.bilibili.com/x/article/viewinfo?id={article_id}')
    JsonData = json.loads(Data.text)
    
    return {}


def get_article_author(article_id: int) -> dict:
    Data = requests.get(f'https://api.bilibili.com/x/article/more?aid={article_id}')
    JsonData = json.loads(Data.text)
    UserDict = {'name': 'name', 'sex': 'sex', 'sign': 'sign', 'level': 'level', 'birthday': 'birthday',
                'fans_badge': 'fans_badge', 'official': ['official', 'title'], 'vip': ['vip', 'status']}
    AuthorDict = {'read_count': 'read_count', 'total': 'total', **UserDict}
    return {'response_code': Data.status_code, 'return_code': JsonData['code'],
            **extractor(data = {**JsonData, **JsonData['author']}, dicts = AuthorDict)}


# def
