#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import sys
import json
import yaml
import time
from datetime import datetime
from apiproxy.douyin.douyin import Douyin
from apiproxy.douyin.download import Download
from apiproxy.douyin import douyin_headers
from apiproxy.common import utils

configModel = {
    "link": [],
    "path": os.getcwd(),
    "music": True,
    "cover": True,
    "avatar": True,
    "json": True,
    "folderstyle": True,
    "mode": ["post"],
    "number": {
        "post": 0,
        "like": 0,
        "allmix": 0,
        "mix": 0,
        "music": 0,
    },
    'database': True,
    "increase": {
        "post": False,
        "like": False,
        "allmix": False,
        "mix": False,
        "music": False,
    },
    "thread": 5,
    "cookie": None

}


def argument():
    parser = argparse.ArgumentParser(description='抖音批量下载工具 使用帮助')
    parser.add_argument("--cmd", "-C", help="使用命令行(True)或者配置文件(False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--link", "-l",
                        help="作品(视频或图集)、直播、合集、音乐集合、个人主页的分享链接或者电脑浏览器网址, 可以设置多个链接(删除文案, 保证只有URL, https://v.douyin.com/kcvMpuN/ 或者 https://www.douyin.com/开头的)",
                        type=str, required=False, default=[], action="append")
    parser.add_argument("--path", "-p", help="下载保存位置, 默认当前文件位置",
                        type=str, required=False, default=os.getcwd())
    parser.add_argument("--music", "-m", help="是否下载视频中的音乐(True/False), 默认为True",
                        type=utils.str2bool, required=False, default=True)
    parser.add_argument("--cover", "-c", help="是否下载视频的封面(True/False), 默认为True, 当下载视频时有效",
                        type=utils.str2bool, required=False, default=True)
    parser.add_argument("--avatar", "-a", help="是否下载作者的头像(True/False), 默认为True",
                        type=utils.str2bool, required=False, default=True)
    parser.add_argument("--json", "-j", help="是否保存获取到的数据(True/False), 默认为True",
                        type=utils.str2bool, required=False, default=True)
    parser.add_argument("--folderstyle", "-fs", help="文件保存风格, 默认为True",
                        type=utils.str2bool, required=False, default=True)
    parser.add_argument("--mode", "-M", help="link是个人主页时, 设置下载发布的作品(post)或喜欢的作品(like)或者用户所有合集(mix), 默认为post, 可以设置多种模式",
                        type=str, required=False, default=[], action="append")
    parser.add_argument("--postnumber", help="主页下作品下载个数设置, 默认为0 全部下载",
                        type=int, required=False, default=0)
    parser.add_argument("--likenumber", help="主页下喜欢下载个数设置, 默认为0 全部下载",
                        type=int, required=False, default=0)
    parser.add_argument("--allmixnumber", help="主页下合集下载个数设置, 默认为0 全部下载",
                        type=int, required=False, default=0)
    parser.add_argument("--mixnumber", help="单个合集下作品下载个数设置, 默认为0 全部下载",
                        type=int, required=False, default=0)
    parser.add_argument("--musicnumber", help="音乐(原声)下作品下载个数设置, 默认为0 全部下载",
                        type=int, required=False, default=0)
    parser.add_argument("--database", "-d", help="是否使用数据库, 默认为True 使用数据库; 如果不使用数据库, 增量更新不可用",
                        type=utils.str2bool, required=False, default=True)
    parser.add_argument("--postincrease", help="是否开启主页作品增量下载(True/False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--likeincrease", help="是否开启主页喜欢增量下载(True/False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--allmixincrease", help="是否开启主页合集增量下载(True/False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--mixincrease", help="是否开启单个合集下作品增量下载(True/False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--musicincrease", help="是否开启音乐(原声)下作品增量下载(True/False), 默认为False",
                        type=utils.str2bool, required=False, default=False)
    parser.add_argument("--thread", "-t",
                        help="设置线程数, 默认5个线程",
                        type=int, required=False, default=5)
    parser.add_argument("--cookie", help="设置cookie, 格式: \"name1=value1; name2=value2;\" 注意要加冒号",
                        type=str, required=False, default='')
    args = parser.parse_args()
    if args.thread <= 0:
        args.thread = 5

    return args


def yamlConfig():
    curPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    yamlPath = os.path.join(curPath, "config.yml")
    f = open(yamlPath, 'r', encoding='utf-8')
    cfg = f.read()
    configDict = yaml.load(stream=cfg, Loader=yaml.FullLoader)

    try:
        if configDict["link"] != None:
            configModel["link"] = configDict["link"]
    except Exception as e:
        print("[  警告  ]:link未设置, 程序退出...\r\n")
    try:
        if configDict["path"] != None:
            configModel["path"] = configDict["path"]
    except Exception as e:
        print("[  警告  ]:path未设置, 使用当前路径...\r\n")
    try:
        if configDict["music"] != None:
            configModel["music"] = configDict["music"]
    except Exception as e:
        print("[  警告  ]:music未设置, 使用默认值True...\r\n")
    try:
        if configDict["cover"] != None:
            configModel["cover"] = configDict["cover"]
    except Exception as e:
        print("[  警告  ]:cover未设置, 使用默认值True...\r\n")
    try:
        if configDict["avatar"] != None:
            configModel["avatar"] = configDict["avatar"]
    except Exception as e:
        print("[  警告  ]:avatar未设置, 使用默认值True...\r\n")
    try:
        if configDict["json"] != None:
            configModel["json"] = configDict["json"]
    except Exception as e:
        print("[  警告  ]:json未设置, 使用默认值True...\r\n")
    try:
        if configDict["folderstyle"] != None:
            configModel["folderstyle"] = configDict["folderstyle"]
    except Exception as e:
        print("[  警告  ]:folderstyle未设置, 使用默认值True...\r\n")
    try:
        if configDict["mode"] != None:
            configModel["mode"] = configDict["mode"]
    except Exception as e:
        print("[  警告  ]:mode未设置, 使用默认值post...\r\n")
    try:
        if configDict["number"]["post"] != None:
            configModel["number"]["post"] = configDict["number"]["post"]
    except Exception as e:
        print("[  警告  ]:post number未设置, 使用默认值0...\r\n")
    try:
        if configDict["number"]["like"] != None:
            configModel["number"]["like"] = configDict["number"]["like"]
    except Exception as e:
        print("[  警告  ]:like number未设置, 使用默认值0...\r\n")
    try:
        if configDict["number"]["allmix"] != None:
            configModel["number"]["allmix"] = configDict["number"]["allmix"]
    except Exception as e:
        print("[  警告  ]:allmix number未设置, 使用默认值0...\r\n")
    try:
        if configDict["number"]["mix"] != None:
            configModel["number"]["mix"] = configDict["number"]["mix"]
    except Exception as e:
        print("[  警告  ]:mix number未设置, 使用默认值0...\r\n")
    try:
        if configDict["number"]["music"] != None:
            configModel["number"]["music"] = configDict["number"]["music"]
    except Exception as e:
        print("[  警告  ]:music number未设置, 使用默认值0...\r\n")
    try:
        if configDict["database"] != None:
            configModel["database"] = configDict["database"]
    except Exception as e:
        print("[  警告  ]:database未设置, 使用默认值False...\r\n")
    try:
        if configDict["increase"]["post"] != None:
            configModel["increase"]["post"] = configDict["increase"]["post"]
    except Exception as e:
        print("[  警告  ]:post 增量更新未设置, 使用默认值False...\r\n")
    try:
        if configDict["increase"]["like"] != None:
            configModel["increase"]["like"] = configDict["increase"]["like"]
    except Exception as e:
        print("[  警告  ]:like 增量更新未设置, 使用默认值False...\r\n")
    try:
        if configDict["increase"]["allmix"] != None:
            configModel["increase"]["allmix"] = configDict["increase"]["allmix"]
    except Exception as e:
        print("[  警告  ]:allmix 增量更新未设置, 使用默认值False...\r\n")
    try:
        if configDict["increase"]["mix"] != None:
            configModel["increase"]["mix"] = configDict["increase"]["mix"]
    except Exception as e:
        print("[  警告  ]:mix 增量更新未设置, 使用默认值False...\r\n")
    try:
        if configDict["increase"]["music"] != None:
            configModel["increase"]["music"] = configDict["increase"]["music"]
    except Exception as e:
        print("[  警告  ]:music 增量更新未设置, 使用默认值False...\r\n")
    try:
        if configDict["thread"] != None:
            configModel["thread"] = configDict["thread"]
    except Exception as e:
        print("[  警告  ]:thread未设置, 使用默认值5...\r\n")
    try:
        if configDict["cookies"] != None:
            cookiekey = configDict["cookies"].keys()
            cookieStr = ""
            for i in cookiekey:
                cookieStr = cookieStr + i + "=" + configDict["cookies"][i] + "; "
            configModel["cookie"] = cookieStr
    except Exception as e:
        pass
    try:
        if configDict["cookie"] != None:
            configModel["cookie"] = configDict["cookie"]
    except Exception as e:
        pass

"""
[{'create_time': '2023-10-05 16.35.12', 'awemeType': 0, 'aweme_id': '7286390117046963497', 'author': {'avatar_thumb': {'height': 720, 'uri': '100x100/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1', 'url_list': ['https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1.jpeg?from=116350172'], 'width': 720}, 'avatar': {'height': 720, 'uri': '1080x1080/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1', 'url_list': ['https://p3-pc.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1.jpeg?from=116350172'], 'width': 720}, 'cover_url': {'height': 720, 'uri': 'c8510002be9a3a61aad2', 'url_list': ['https://p9-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1699106400&x-signature=T3Y%2FiuRUa%2BI6G8uX%2FNNuA1vo%2FSY%3D&from=116350172', 'https://p6-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1699106400&x-signature=Ge0Aaab%2BYpxQXHG393ZmqTSjF4A%3D&from=116350172', 'https://p3-pc-sign.douyinpic.com/obj/c8510002be9a3a61aad2?x-expires=1699106400&x-signature=kQRj%2BZm7ckNju%2Fr%2FHJqfdh5tw84%3D&from=116350172'], 'width': 720}, 'favoriting_count': 0, 'follower_count': 75152700, 'following_count': 0, 'nickname': '刘德华', 'prevent_download': False, 'sec_uid': 'MS4wLjABAAAAU7ibxriLF-GSBF5QKa1Op9hxcMAPVmzmXwXqqvMfrhs', 'secret': '', 'short_id': '', 'signature': '', 'total_favorited': 431702955, 'uid': '562575903556992', 'unique_id': '', 'user_age': ''}, 'desc': '越来越好！', 'images': [], 'music': {'cover_hd': {'height': 720, 'uri': '1080x1080/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1', 'url_list': ['https://p3-pc.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1.jpeg?from=116350172'], 'width': 720}, 'cover_large': {'height': 720, 'uri': '1080x1080/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1', 'url_list': ['https://p3-pc.douyinpic.com/aweme/1080x1080/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1.jpeg?from=116350172'], 'width': 720}, 'cover_medium': {'height': 720, 'uri': '720x720/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1', 'url_list': ['https://p3-pc.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1.jpeg?from=116350172'], 'width': 720}, 'cover_thumb': {'height': 720, 'uri': '100x100/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1', 'url_list': ['https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i-0813c001_b2de06d2daf34c02b28837aa729ea4d1.jpeg?from=116350172'], 'width': 720}, 'owner_handle': 'andylau.9.27', 'owner_id': '562575903556992', 'owner_nickname': '刘德华', 'play_url': {'height': 720, 'uri': 'https://sf86-cdn-tos.douyinstatic.com/obj/ies-music/7286390157220252473.mp3', 'url_key': '7286390176966789925', 'url_list': ['https://sf86-cdn-tos.douyinstatic.com/obj/ies-music/7286390157220252473.mp3', 'https://sf3-cdn-tos.douyinstatic.com/obj/ies-music/7286390157220252473.mp3'], 'width': 720}, 'title': '@刘德华创作的原声'}, 'mix_info': {'cover_url': {'height': '', 'uri': '', 'url_list': [], 'width': ''}, 'ids': '', 'is_serial_mix': '', 'mix_id': '', 'mix_name': '', 'mix_pic_type': '', 'mix_type': '', 'statis': {'current_episode': '', 'updated_to_episode': ''}}, 'video': {'play_addr': {'uri': 'v0300fg10000ckf793rc77u5ir86d0gg', 'url_list': ['http://v3-web.douyinvod.com/79f0054671635c42f1413b32501a8cd1/6533ecdf/video/tos/cn/tos-cn-ve-15c001-alinc2/o8LlHaSDJAcLg9ougQeCHuDnPbaBNenDAABhNI/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=925&bt=925&cs=0&ds=6&ft=GN7rKGVVywIiRZm8Zmo~ySqTeaApjP~NEvrKbWnimto0g3&mime_type=video_mp4&qs=0&rc=PDQ8OGU4NjY1NjdkOjY4NUBpajM5dTg6ZjY6bjMzNGkzM0BhMDZhMTVgNjYxNTZeL2ExYSNkYTVmcjRvNmNgLS1kLTBzcw%3D%3D&btag=e00018000&dy_q=1697898150&l=202310212222292EB11AB3EBDC6C8AF481', 'http://v26-web.douyinvod.com/7de657f8cdc97a7c474a094aa0cbfaf6/6533ecdf/video/tos/cn/tos-cn-ve-15c001-alinc2/o8LlHaSDJAcLg9ougQeCHuDnPbaBNenDAABhNI/?a=6383&ch=10010&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=925&bt=925&cs=0&ds=6&ft=GN7rKGVVywIiRZm8Zmo~ySqTeaApjP~NEvrKbWnimto0g3&mime_type=video_mp4&qs=0&rc=PDQ8OGU4NjY1NjdkOjY4NUBpajM5dTg6ZjY6bjMzNGkzM0BhMDZhMTVgNjYxNTZeL2ExYSNkYTVmcjRvNmNgLS1kLTBzcw%3D%3D&btag=e00018000&dy_q=1697898150&l=202310212222292EB11AB3EBDC6C8AF481', 'https://www.douyin.com/aweme/v1/play/?video_id=v0300fg10000ckf793rc77u5ir86d0gg&line=0&file_id=42d523a79a84439293c3854bd59931d9&sign=5b8c187207815d80c2fcf6b8d3ecd396&is_play_url=1&source=PackSourceEnum_PUBLISH']}, 'cover_original_scale': {'height': '', 'uri': '', 'url_list': [], 'width': ''}, 'dynamic_cover': {'height': 720, 'uri': 'tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q', 'url_list': ['https://p3-pc-sign.douyinpic.com/obj/tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q?x-expires=1699106400&x-signature=YaXc390tIgNzSi9Wua9JADDlINA%3D&from=3213915784_large&s=PackSourceEnum_PUBLISH&se=false&sc=dynamic_cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481', 'https://p9-pc-sign.douyinpic.com/obj/tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q?x-expires=1699106400&x-signature=G9t1RynXlOW2TyFeqlrWIpFzPDM%3D&from=3213915784_large&s=PackSourceEnum_PUBLISH&se=false&sc=dynamic_cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481', 'https://p6-pc-sign.douyinpic.com/obj/tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q?x-expires=1699106400&x-signature=28HkAJdYPEvfNOSg%2FHb%2FgQJHxs8%3D&from=3213915784_large&s=PackSourceEnum_PUBLISH&se=false&sc=dynamic_cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481'], 'width': 720}, 'origin_cover': {'height': 640, 'uri': 'tos-cn-p-0015/876cf7dc8ec34491a37da61a4639a8fe_1696494916', 'url_list': ['https://p9-pc-sign.douyinpic.com/tos-cn-p-0015/876cf7dc8ec34491a37da61a4639a8fe_1696494916~tplv-dy-360p.jpeg?x-expires=1699106400&x-signature=McyzABFeVdI7UflYcsizheC6Dcw%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=origin_cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481', 'https://p3-pc-sign.douyinpic.com/tos-cn-p-0015/876cf7dc8ec34491a37da61a4639a8fe_1696494916~tplv-dy-360p.jpeg?x-expires=1699106400&x-signature=SAXqpuOL17A%2FmrPRSw%2Bj7mjHD4U%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=origin_cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481', 'https://p6-pc-sign.douyinpic.com/tos-cn-p-0015/876cf7dc8ec34491a37da61a4639a8fe_1696494916~tplv-dy-360p.jpeg?x-expires=1699106400&x-signature=JXRty3IYomsvqlk9Z8O6lvBcL60%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=origin_cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481'], 'width': 360}, 'cover': {'height': 720, 'uri': 'tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q', 'url_list': ['https://p9-pc-sign.douyinpic.com/tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q~tplv-dy-cropcenter:323:430.jpeg?x-expires=2013256800&x-signature=7oJ81gJoBp8H%2FGv7dvHy%2B3p%2BVJ4%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=true&sh=323_430&sc=cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481', 'https://p9-pc-sign.douyinpic.com/obj/tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q?x-expires=2013256800&x-signature=2apEEChoU%2FvhLXsV6rn4NNOVQVo%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481', 'https://p6-pc-sign.douyinpic.com/obj/tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q?x-expires=2013256800&x-signature=AgIbpxzMZKZML7eU4ZIuJeHTmcw%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481', 'https://p3-pc-sign.douyinpic.com/obj/tos-cn-i-0813/oQNKzfpuAAAaA7tnAIesP6GnebU2DnODBBEA8Q?x-expires=2013256800&x-signature=u1cF%2BW%2FCpL6OsJnCSXdu%2F4SobgI%3D&from=3213915784&s=PackSourceEnum_PUBLISH&se=false&sc=cover&biz_tag=pcweb_cover&l=202310212222292EB11AB3EBDC6C8AF481'], 'width': 720}}, 'statistics': {'admire_count': 0, 'collect_count': 112239, 'comment_count': 212336, 'digg_count': 5374980, 'play_count': 0, 'share_count': 70094}}]

"""
def main():
    start = time.time()  # 开始时间
    fname='抖音视频数据'
    encoding='utf-8-sig'
    with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
        f.write('视频日期'+','+'视频标题' + ','+'视频链接'+ ','+'点赞数'+ ','+'评论数'+ ','+'收藏数'+','+'转发数'+ ','+'\n')
    args = argument()

    if args.cmd:
        configModel["link"] = args.link
        configModel["path"] = args.path
        configModel["music"] = args.music
        configModel["cover"] = args.cover
        configModel["avatar"] = args.avatar
        configModel["json"] = args.json
        configModel["folderstyle"] = args.folderstyle
        if args.mode == None or args.mode == []:
            args.mode = []
            args.mode.append("post")
        configModel["mode"] = list(set(args.mode))
        configModel["number"]["post"] = args.postnumber
        configModel["number"]["like"] = args.likenumber
        configModel["number"]["allmix"] = args.allmixnumber
        configModel["number"]["mix"] = args.mixnumber
        configModel["number"]["music"] = args.musicnumber
        configModel["database"] = args.database
        configModel["increase"]["post"] = args.postincrease
        configModel["increase"]["like"] = args.likeincrease
        configModel["increase"]["allmix"] = args.allmixincrease
        configModel["increase"]["mix"] = args.mixincrease
        configModel["increase"]["music"] = args.musicincrease
        configModel["thread"] = args.thread
        configModel["cookie"] = args.cookie
    else:
        yamlConfig()

    if configModel["link"] == []:
        return

    if configModel["cookie"] is not None and configModel["cookie"] != "":
        douyin_headers["Cookie"] = configModel["cookie"]

    configModel["path"] = os.path.abspath(configModel["path"])
    print("[  提示  ]:数据保存路径 " + configModel["path"])
    if not os.path.exists(configModel["path"]):
        os.mkdir(configModel["path"])

    dy = Douyin(database=configModel["database"])
    dl = Download(thread=configModel["thread"], music=configModel["music"], cover=configModel["cover"],
                  avatar=configModel["avatar"], resjson=configModel["json"],
                  folderstyle=configModel["folderstyle"])

    for link in configModel["link"]:
        print("--------------------------------------------------------------------------------")
        print("[  提示  ]:正在请求的链接: " + link + "\r\n")
        url = dy.getShareLink(link)
        key_type, key = dy.getKey(url)
        if key_type == "user":
            print("[  提示  ]:正在请求用户主页下作品\r\n")
            data = dy.getUserDetailInfo(sec_uid=key)
            nickname = ""
            if data is not None and data != {}:
                nickname = utils.replaceStr(data['user']['nickname'])

            userPath = os.path.join(configModel["path"], "user_" + nickname + "_" + key)
            if not os.path.exists(userPath):
                os.mkdir(userPath)

            for mode in configModel["mode"]:
                print("--------------------------------------------------------------------------------")
                print("[  提示  ]:正在请求用户主页模式: " + mode + "\r\n")
                if mode == 'post' or mode == 'like':
                    datalist = dy.getUserInfo(key, mode, 35, configModel["number"][mode], configModel["increase"][mode])
                    # print(datalist)
                    if datalist is not None and datalist != []:
                        modePath = os.path.join(userPath, mode)
                        if not os.path.exists(modePath):
                            os.mkdir(modePath)
                        for item in datalist:
                            print(item)
                            create_time = datetime.strptime(item['create_time'].replace('.',':'), "%Y-%m-%d %H:%M:%S")
                            if create_time < datetime.strptime('2021-01-01 00:00:00', "%Y-%m-%d %H:%M:%S"):
                                break
                            with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
                                f.write(item['create_time'].replace('.',':')+','+item['desc'] + ','+'https://www.douyin.com/video/'+item['aweme_id']+ ','+str(item['statistics']['digg_count'])+ ','+str(item['statistics']['comment_count'])+ ','+str(item['statistics']['collect_count'])+','+str(item['statistics']['share_count'])+ ','+'\n')
                        # dl.userDownload(awemeList=datalist, savePath=modePath)
                elif mode == 'mix':
                    mixIdNameDict = dy.getUserAllMixInfo(key, 35, configModel["number"]["allmix"])
                    if mixIdNameDict is not None and mixIdNameDict != {}:
                        for mix_id in mixIdNameDict:
                            print(f'[  提示  ]:正在下载合集 [{mixIdNameDict[mix_id]}] 中的作品\r\n')
                            mix_file_name = utils.replaceStr(mixIdNameDict[mix_id])
                            datalist = dy.getMixInfo(mix_id, 35, 0, configModel["increase"]["allmix"], key)
                            if datalist is not None and datalist != []:
                                modePath = os.path.join(userPath, mode)
                                if not os.path.exists(modePath):
                                    os.mkdir(modePath)
                                # dl.userDownload(awemeList=datalist, savePath=os.path.join(modePath, mix_file_name))
                                print(f'[  提示  ]:合集 [{mixIdNameDict[mix_id]}] 中的作品下载完成\r\n')
        elif key_type == "mix":
            print("[  提示  ]:正在请求单个合集下作品\r\n")
            datalist = dy.getMixInfo(key, 35, configModel["number"]["mix"], configModel["increase"]["mix"], "")
            if datalist is not None and datalist != []:
                mixname = utils.replaceStr(datalist[0]["mix_info"]["mix_name"])
                mixPath = os.path.join(configModel["path"], "mix_" + mixname + "_" + key)
                if not os.path.exists(mixPath):
                    os.mkdir(mixPath)
                # dl.userDownload(awemeList=datalist, savePath=mixPath)
        elif key_type == "music":
            print("[  提示  ]:正在请求音乐(原声)下作品\r\n")
            datalist = dy.getMusicInfo(key, 35, configModel["number"]["music"], configModel["increase"]["music"])

            if datalist is not None and datalist != []:
                musicname = utils.replaceStr(datalist[0]["music"]["title"])
                musicPath = os.path.join(configModel["path"], "music_" + musicname + "_" + key)
                if not os.path.exists(musicPath):
                    os.mkdir(musicPath)
                # dl.userDownload(awemeList=datalist, savePath=musicPath)
        elif key_type == "aweme":
            print("[  提示  ]:正在请求单个作品\r\n")
            datanew, dataraw = dy.getAwemeInfo(key)
            if datanew is not None and datanew != {}:
                datalist = []
                datalist.append(datanew)
                awemePath = os.path.join(configModel["path"], "aweme")
                if not os.path.exists(awemePath):
                    os.mkdir(awemePath)
                # dl.userDownload(awemeList=datalist, savePath=awemePath)
        elif key_type == "live":
            print("[  提示  ]:正在进行直播解析\r\n")
            live_json = dy.getLiveInfo(key)
            if configModel["json"]:
                livePath = os.path.join(configModel["path"], "live")
                if not os.path.exists(livePath):
                    os.mkdir(livePath)
                live_file_name = utils.replaceStr(key + live_json["nickname"])
                # 保存获取到json
                print("[  提示  ]:正在保存获取到的信息到result.json\r\n")
                with open(os.path.join(livePath, live_file_name + ".json"), "w", encoding='utf-8') as f:
                    f.write(json.dumps(live_json, ensure_ascii=False, indent=2))
                    f.close()

    end = time.time()  # 结束时间
    print('\n' + '[下载完成]:总耗时: %d分钟%d秒\n' % (int((end - start) / 60), ((end - start) % 60)))  # 输出下载用时时间


if __name__ == "__main__":
    main()
