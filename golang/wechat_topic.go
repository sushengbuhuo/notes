package main

import (
	"fmt"
	"io"
	"net/http"
	"regexp"

	"github.com/bitly/go-simplejson"
)

// var REG_MSG_ID = regexp.MustCompile("data-msgid=\"(.*)\"")
var REG_MSG_ID = regexp.MustCompile(`data-msgid="(.*)"`) // https://learnku.com/articles/35121
var REG_DATA_LINK = regexp.MustCompile("data-link=\"(.*)\"")
var REG_DATA_TITLE = regexp.MustCompile("data-title=\"(.*)\"")
var FMT_ALBUM_DATA_URL = "https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=MzUyMzUyNzM4Ng==&album_id=2091728990028824579&count=10&begin_msgid=%s&begin_itemidx=1&uin=777&key=777&pass_ticket=&wxtoken=&devicetype=Windows10x64&clientversion=62090529&__biz=MzUyMzUyNzM4Ng%3D%3D&appmsg_token=&x5=0&f=json"

func main() {

	resp, _ := http.Get("https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzUyMzUyNzM4Ng==&action=getalbum&album_id=2091728990028824579&scene=173&from_msgid=2247507484&from_itemidx=1&count=3&nolastread=1#wechat_redirect")
	bResp, _ := io.ReadAll(resp.Body)
	sResp := string(bResp)
	msgid := REG_MSG_ID.FindAllStringSubmatch(sResp, 1)[0][1]
	data_link := REG_DATA_LINK.FindAllStringSubmatch(sResp, 1)[0][1]
	data_title := REG_DATA_TITLE.FindAllStringSubmatch(sResp, 1)[0][1]

	fmt.Println(REG_MSG_ID.FindString(sResp), msgid, data_link, data_title)
	//这里传入了第一篇文章的msgid，用于拼接请求连接，实际使用的时候__biz，album_id都必须从第一个链接获取，不能写死
	for {
		break
		resp, _ = http.Get(fmt.Sprintf(FMT_ALBUM_DATA_URL, msgid))
		bResp, _ = io.ReadAll(resp.Body)
		json, _ := simplejson.NewJson(bResp)
		j_article_list := json.Get("getalbum_resp").Get("article_list")
		length := len(j_article_list.MustArray())
		//长度不在正确范围内，退出
		if length == 0 || length > 20 {
			return
		}
		i := 0
		for {
			article := j_article_list.GetIndex(i)
			create_time := article.Get("create_time").MustString()
			title := article.Get("title").MustString()
			_url := article.Get("url").MustString()
			fmt.Println(create_time, title, _url)
			i++
			if i == length {
				msgid = article.Get("msgid").MustString()
				resp, _ = http.Get(fmt.Sprintf(FMT_ALBUM_DATA_URL, msgid))
				bResp, _ = io.ReadAll(resp.Body)
				//如果数据中不包含文章信息，就使用上一篇文章的 msgid
				for len(string(bResp)) < 4096 {
					i -= 1
					if i < 0 {
						break
					}
					msgid = j_article_list.GetIndex(i).Get("msgid").MustString()
					resp, _ = http.Get(fmt.Sprintf(FMT_ALBUM_DATA_URL, msgid))
					bResp, _ = io.ReadAll(resp.Body)
				}
				break
			}
		}
		if json.Get("getalbum_resp").Get("continue_flag").MustString() == "0" {
			break
		}
	}

}
