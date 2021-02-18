# Bilibili_viewer
### 项目简介
**Bilibili_Viewer**是在python爬虫的基础上对B站功能进行模拟，尽量还原网页端和手机客户端的优点，后续准备接入GUI，打造成一个Bilibili微客户端，实现登录,自动签到等功能。

### 作者简介
一个初一学生，有意向一起开发的小伙伴可以私信B站[**@la博**](https://space.bilibili.com/436067826).

### 运行要求
    Python 3.6 or above
    库: regex，time，requests，json，os

### 已知BUG/改进点：
	不支持获取直播间
	不支持获取文章详细信息
	不支持GUI
	不支持下载图片
	不支持访问，纪录片

### 版本更新进度

| 版本号 | 更新信息 | 更新种类 | 更新难度 | 发布日期 |
|  :----:  | :----: | :----: | :---: | :----: |
| 1.0 | [Update Detail...](https://github.com/labo-China/Bilibili_viewer/releases/tag/v1.4) | —— | 2 | 2020/3/16 | 
| 1.3 | [Update Detail...](https://github.com/labo-China/Bilibili_viewer/releases/tag/v1.4) | Feature | 2 | 2020/3/17 |
| 1.4 | [Update Detail...](https://github.com/labo-China/Bilibili_viewer/releases/tag/v1.4)| Feature | 3 |2020/3/23|
| 1.5-Beta-1 | [Update Detail...](https://github.com/labo-China/Bilibili_viewer/releases/tag/v1.5-beta.1) | Feature | 5 |2020/4/15|
| 1.5-Beta-2 | [Update Detail...](https://github.com/labo-China/Bilibili_viewer/releases/tag/v1.5-beta.2) | Fix | 2 | 2020/4/25 |
| 1.5-Beta-3 | [Update Detail...](https://github.com/labo-China/Bilibili_viewer/releases/tag/v1.5-beta.3) | Fix | 1 | 2020/5/15 |
| 1.5 | [Update Detail...](https://github.com/labo-China/Bilibili_viewer/releases/tag/v1.5) | Fix | 3 | 2020/7/8 |
| **1.6.1** | 添加对番剧、文章的完整支持 补全搜索类型 | Feature | 2 | 制作中 |

#### 特性与漏洞的列表
说明：优先级为1-5之间的整数，数字最小最优先
#### api拓展

#### 客户端功能

#### 外部程序调用

### 程序文档

#### 一个标准的请求函数的模板

```python
import requests
import json
from scripts.tool import extractor


def func(*params):
    # func init
    Url = f'**requests url**?**{params}**'
    Data = requests.get(Url)
    JsonData = json.loads(Data.text)
    ReturnData = {}
    # data collect
    ExtractorDict = {'**something keys**': '**something values**'}
    for Targets in JsonData['data']['**something keys**']:
        ReturnData.update(extractor(data = Targets, dicts = ExtractorDict))
    # return
    return {'response_code': Data.status_code, 'return_code': JsonData['code'], **ReturnData}
``` 

    
