# Bilibili_viewer
## 项目简介
**Bilibili_Viewer**python爬虫的基础上对B站其他客户端的功能进行模拟，尽量还原网页端和手机客户端的优点，后续准备接入GUI，打造成一个Bilibili微客户端，实现登录,自动签到等功能。

## 作者简介
一个六年级小学生，有意向一起开发的小伙伴可以私信B站[**@la博**](https://space.bilibili.com/436067826).

## 运行要求
    python3.4+
    库: re，time，requests，json，os

## 已知BUG/改进点：
	不支持获取直播间
	不支持获取文章详细信息
	不支持GUI
	不支持下载图片
	不支持访问番剧，纪录片

## 文件说明：

| 文件名 | 是否必需 | 作用 | 文件大小 |
|  :----:  | :---: | :---: | :----: |
| DanmakuFactory | 否 | 弹幕转换工具 | 416KB |
| Plugin  | 是 | Bilibili_viewer插件| 72KB |
| bilibili_viewer.py | 是 | Bilibili_viewer主程序 | 16KB |
| FFmpeg.7z | 否 | 视频合并&弹幕混流(需解压) | 15.6MB |
| README.md | 是 | 项目说明文件 | 3KB |

    更新打印模块
    移动一些函数至tool.py
    更新数据获取方式，减小代码体积
    使用aria2多线程下载视频(默认8线程)
    补全了一些文档
    修正了一些不规范的返回数据
    现在遇到空弹幕文件会直接跳过
    移除了ass文件嵌入视频的功能(由于效果不佳)
    使用老版本的FFmpeg,减小体积
    正在测试番剧api
    添加了调试功能,在初始界面输入console即可进入，输入EXIT_CONSOLE可退出
    
    
    
