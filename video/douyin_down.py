# -*- coding: utf-8 -*-
import requests
import time
import json,html
import random,re,os,csv
requests.packages.urllib3.disable_warnings()
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
fname=input("请输入文件名：")
# 油猴脚本抓取视频地址 https://greasyfork.org/scripts/471880
# https://v.douyin.com/rWa6bh8/
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xea in position 0: invalid continuation byte gb18030 ISO-8859-1
"""

function downloadData(encoding) {
        let text = userKey.join(",") + "\n" + userData.join(",") + "\n\n";
        text += "作品描述,作品链接,点赞数,评论数,收藏数,分享数,发布时间,封面,时长,标签,话题,下载链接\n";//item.collectCount, item.shareCount, item.date, item.url].join(",") + "\n"
        aweme_list.forEach(item => {
            let tag=item.tag.map(obj => obj.tag_name)
        let topic=item.topic.map(obj => obj.hashtag_name)
            text += ['"' + item.desc + '"', "https://www.douyin.com/video/"+item.awemeId, item.diggCount, item.commentCount,item.collectCount, item.shareCount, item.date, item.image,item.duration,tag.join("#"),topic.join("#"),item.url].join(",") + "\n"
        });
        if (encoding === "gbk")
            text = str2gbk(text);
        txt2file(text, userData[0] + ".csv");
    }
   if (self._url.indexOf("/aweme/v1/web/aweme/post") > -1) {
                        var json = JSON.parse(self.response);
                        let post_data = json.aweme_list.map(item => Object.assign(
                            {"awemeId": item.aweme_id, "desc": item.desc},
                            {
                                "diggCount": item.statistics.digg_count,
                                "commentCount": item.statistics.comment_count,
                                "collectCount": item.statistics.collect_count,
                                "shareCount": item.statistics.share_count
                            },
                            {
                                "date": new Date(item.create_time * 1000).toLocaleString(),
                                "url": item.video.play_addr.url_list[0],
                                "image": item.video.cover.url_list[0].replace(/\\u([\d\w]{4})/gi, function (match, grp) {return String.fromCharCode(parseInt(grp, 16));}),
                                "duration":item.duration,
                                "tag":item.video_tag,
                                "topic":item.text_extra,
                            }));
                        aweme_list = aweme_list.concat(post_data);
                        if (timer !== undefined)
                            clearTimeout(timer);
                        timer = setTimeout(() => createDownloadButton(), 1000);
                    } 
"""
f = open(f'{fname}', encoding='gbk')
csv_reader = csv.reader(f)
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def down(title,date,url):
	try:
		if not os.path.exists('douyin'):
			os.mkdir('douyin')
		print('开始下载视频：',date,title)
		video_data = requests.get(url,headers=headers)
		with open('douyin/'+date.replace('/','-').replace(' ','')+'_'+trimName(title)+'.mp4','wb') as f:
			f.write(video_data.content)
	except Exception as e:
		print('出错了',e)
for line in csv_reader:
    # print(line)
    if len(line) == 0:
       continue
    if line[6] == "年龄" or line[6] == "" or line[6] == "下载链接":
        continue
    res = down(line[0],line[5][0:10],line[6])
    if not res:
       continue
    if res == "error":
       break
