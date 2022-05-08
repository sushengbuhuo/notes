import random
import sys
import requests
import re
import jsonpath
 
 
class Dy:
    def __init__(self, url_str):
        self.headers = {
            'User-Agent': 'com.ss.android.ugc.live/110400 (Linux; U; Android 7.0; zh_CN_'
        }
 
        self.url_str = url_str
 
    def get_item_id(self):
        """从分享链接中提取url"""
        url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.url_str)[
            0]
        res = requests.get(url)
        item_id = re.findall(r'\d+', res.url)[0]
        if item_id == '404':
            print('分享链接错误!')
            sys.exit()
        else:
            return item_id
 
    def play_count(self, item_id):
        """
        获取播放量
        :param item_id:
        :return:{"data":{"digg_count":,"play_count":,"share_count":,"user_bury":,"user_digg":},"extra":{"now":13位时间戳},"status_code":0}
        """
        url = 'https://api3-normal-c-lq.huoshan.com/hotsoon/item/reaction/_play/'
 
        params = {
            'iid': 756942400129936,
            'device_id': 69336530495,
            'channel': 'dc_samsung_1112_64',
            'aid': '1112',
            'app_name': 'live_stream',
            'version_code': '110600',
            'device_platform': 'android',
            'os_version': '7.0',
            'manifest_version_code': '110600',
            'hs_location_permission': 0,
        }
 
        data = {
            'item_id': item_id,
        }
 
        res = requests.post(url, headers=self.headers, data=data, params=params)
        json_obj = res.json()
        print('播放量:', json_obj['data']['play_count'])
 
    def info(self, item_id):
        """
        :param item_id:
        :return:
        """
        try:
            # 如果在火山和抖音都能查询到
            url = 'https://api3-normal-c-lq.huoshan.com/hotsoon/item/video/_get/'
 
            params = {
                'item_id': item_id,
                'language': 'zh',
            }
 
            res = requests.get(url=url, headers=self.headers, params=params)
            json_obj = res.json()
 
            digg_count = jsonpath.jsonpath(json_obj, "$..digg_count")[0]
            comment_count = jsonpath.jsonpath(json_obj, "$..comment_count")[0]
            share_count = jsonpath.jsonpath(json_obj, "$..share_count")[0]
            url_list = jsonpath.jsonpath(json_obj, "$..video.url_list")[0]
            nickname = jsonpath.jsonpath(json_obj, "$..nickname")[0]
            short_id_str = jsonpath.jsonpath(json_obj, "$..short_id_str")[0]
            title = jsonpath.jsonpath(json_obj, "$..description")[0]
            signature = jsonpath.jsonpath(json_obj, "$..signature")[0].replace('\n', '')
            print('点赞量: {}\n评论量: {}\n分享量: {}\n视频url: {}\n标题: {}\n作者: {}\n抖音号: {}\n个人简介: {}'.format(digg_count,
                                                                                                   comment_count,
                                                                                                   share_count,
                                                                                                   url_list[0], title,
                                                                                                   nickname,
                                                                                                   short_id_str,
                                                                                                   signature))
        except:
            # 只能在抖音查询到
            url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_id}'
            res = requests.get(url=url, headers=self.headers)
            json_obj = res.json()
 
            digg_count = jsonpath.jsonpath(json_obj, "$..digg_count")[0]
            comment_count = jsonpath.jsonpath(json_obj, "$..comment_count")[0]
            share_count = jsonpath.jsonpath(json_obj, "$..share_count")[0]
            url_list = jsonpath.jsonpath(json_obj, "$..play_addr.url_list")[0][0]
            nickname = jsonpath.jsonpath(json_obj, "$..nickname")[0]
            short_id = jsonpath.jsonpath(json_obj, "$..short_id")[0]
            title = jsonpath.jsonpath(json_obj, "$..desc")[0]
            signature = jsonpath.jsonpath(json_obj, "$..signature")[0].replace('\n', '')
            print('点赞量: {}\n评论量: {}\n分享量: {}\n视频url: {}\n标题: {}\n作者: {}\n抖音号: {}\n个人简介: {}'.format(digg_count,
                                                                                                   comment_count,
                                                                                                   share_count,
                                                                                                   url_list.replace('playwm', 'play'), title,
                                                                                                   nickname,
                                                                                                   short_id, signature))
 
 
if __name__ == '__main__':
    url = input('输入分享链接:')
    s = Dy(url)
    ids = s.get_item_id()
    s.info(ids)