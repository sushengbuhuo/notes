不用写代码抓取数据 https://www.cnblogs.com/web-scraper/

# 哔哩哔哩个人主页视频

```js
{"_id":"bilibili_videos","startUrl":["https://space.bilibili.com/927587/video?tid=0&pn=[1-42:1]&keyword=&order=pubdate"],"selectors":[{"id":"row","parentSelectors":["_root"],"type":"SelectorElement","selector":"li.small-item","multiple":true},{"id":"视频标题","parentSelectors":["row"],"type":"SelectorText","selector":"a.title","multiple":false,"regex":""},{"id":"视频链接","parentSelectors":["row"],"type":"SelectorElementAttribute","selector":"a.cover","multiple":false,"extractAttribute":"href"},{"id":"视频封面","parentSelectors":["row"],"type":"SelectorElementAttribute","selector":"a.cover div.b-img picture img","multiple":false,"extractAttribute":"src"},{"id":"视频播放量","parentSelectors":["row"],"type":"SelectorText","selector":".play span","multiple":false,"regex":""},{"id":"视频长度","parentSelectors":["row"],"type":"SelectorText","selector":" a.cover  span.length","multiple":false,"regex":""},{"id":"发布时间","parentSelectors":["row"],"type":"SelectorText","selector":"span.time","multiple":false,"regex":""}]}
```
### 知乎话题
```js
{"_id":"zhihu_top","startUrl":["https://www.zhihu.com/topic/19559424/top-answers"],"selectors":[{"delay":2000,"elementLimit":500,"id":"row","multiple":true,"parentSelectors":["_root"],"selector":"div.List-item:nth-of-type(-n+100)","type":"SelectorElementScroll"},{"id":"知乎标题","multiple":false,"parentSelectors":["row"],"regex":"","selector":"h2 a","type":"SelectorText"},{"id":"点赞数","multiple":false,"parentSelectors":["row"],"regex":"","selector":"span.AuthorInfo-name a","type":"SelectorText"}]}
```
### 知乎文章
```js
{"_id":"zhihu_zhuanlan","startUrl":["https://www.zhihu.com/people/zhi-shi-ku-21-42/posts?page=[1-4]"],"selectors":[{"id":"row","type":"SelectorElement","parentSelectors":["_root"],"selector":"div.List-item","multiple":true,"delay":0},{"id":"知乎标题","type":"SelectorText","parentSelectors":["row"],"selector":"h2.ContentItem-title","multiple":false,"regex":"","delay":0},{"id":"知乎链接","type":"SelectorElementAttribute","parentSelectors":["row"],"selector":"h2.ContentItem-title span a ","multiple":false,"extractAttribute":"href","delay":0}]}

```
### 知乎回答
```js
{"_id":"zhihu_answer","startUrl":["https://www.zhihu.com/people/mysusheng/answers?page=[1-15]"],"selectors":[{"id":"row","parentSelectors":["_root"],"type":"SelectorElement","selector":"div.List-item","multiple":true},{"id":"知乎问题标题","parentSelectors":["row"],"type":"SelectorText","selector":"div[itemprop='zhihu:question'] a","multiple":false,"regex":""},{"id":"知乎问题链接","parentSelectors":["row"],"type":"SelectorElementAttribute","selector":"[itemprop='zhihu:question'] a","multiple":false,"extractAttribute":"href"}]}
```


