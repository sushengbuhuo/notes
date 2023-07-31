package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

// 目前支持 皮皮虾/抖音/微视/6间房/哔哩哔哩/微博/绿洲/度小视/开眼/陌陌/皮皮搞笑/全民k歌/逗拍/虎牙/新片场/哔哩哔哩/Acfun/美拍/西瓜视频/火山小视频/网易云Mlog/好看视频哔哩哔哩/6间房/微博仅支持下载无法去除水印
func main() {
	url := "https://tenapi.cn/v2/video"
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("公众号苏生不惑请输入视频链接: ")
	urlInput, _ := reader.ReadString('\n')
	urlInput = strings.TrimSpace(urlInput)
	payload := strings.NewReader("url=" + urlInput)
	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	decoder := json.NewDecoder(res.Body)

	var data map[string]interface{}
	err := decoder.Decode(&data)
	if err != nil {
		panic(err)
	}
	// fmt.Println(data)
	video_title := data["data"].(map[string]interface{})["title"].(string)
	// video_cover := data["data"].(map[string]interface{})["cover"].(string)
	video_url := data["data"].(map[string]interface{})["url"].(string)

	file, err := os.Create(video_title + ".mp4")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	resp, err := http.Get(video_url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		panic(err)
	}

	fmt.Println("开始下载视频：", video_title, video_url)
	body, _ := ioutil.ReadAll(res.Body)
	fmt.Println(string(body))
}
