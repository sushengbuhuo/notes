package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
)

func Exists(path string) bool {
	_, err := os.Stat(path) //os.Stat获取文件信息
	if err != nil {
		if os.IsExist(err) {
			return true
		}
		return false
	}
	return true
}
func InArray(items []string, item string) bool {
	for _, eachItem := range items {
		if eachItem == item {
			return true
		}
	}
	return false
}
func main() {
	defer func() {
      if err := recover(); err != nil {
      	fmt.Print("错误信息：")
         fmt.Println(err) // panic传入的内容
      }
   }()
	var url string
	fmt.Print("苏生不惑提示你请输入话题地址:")
	fmt.Scanln(&url)
	if len(url) == 0 {
		panic("话题地址为空")
	}
	client := &http.Client{}
	reqest, err := http.NewRequest("GET", url, nil)
	reqest.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat")
	if err != nil {
		panic(err)
	}
	response, _ := client.Do(reqest)
	defer response.Body.Close()
	bResp, _ := io.ReadAll(response.Body)
	// json, _ := simplejson.NewJson(bResp)
	content := string(bResp)
	var voiceids = regexp.MustCompile(`data-voiceid="(.*)"`).FindAllStringSubmatch(content, -1)
	var titles = regexp.MustCompile(`data-title="(.*)" data-voiceid`).FindAllStringSubmatch(content, -1)
	fileName := "wechat_topic_audio_list.txt"
	// fmt.Print(voiceids, titles)
	fileContent, _ := ioutil.ReadFile(fileName)
	var voice_urls = regexp.MustCompile(`\n`).Split(string(fileContent), -1)
	// fmt.Print(voice_urls)
	var f2 *os.File
	for k, v := range voiceids {
		if InArray(voice_urls, "https://res.wx.qq.com/voice/getvoice?mediaid="+v[1]) {
			fmt.Println("已经下载过音频：" + titles[k][1])
			continue
		}
		res, _ := http.Get("https://res.wx.qq.com/voice/getvoice?mediaid=" + v[1])
		f, _ := os.Create(titles[k][1] + ".mp3")
		io.Copy(f, res.Body)
		if Exists(fileName) {
			f2, _ = os.OpenFile(fileName, os.O_APPEND, 0666)
		} else {
			f2, _ = os.Create(fileName)
		}
		defer f2.Close()
		fmt.Println("正在下载音频：" + titles[k][1])
		// _, _ = io.WriteString(f2, "https://res.wx.qq.com/voice/getvoice?mediaid="+v[1]+"\n")
		// _, _ =f2.Write([]byte("https://res.wx.qq.com/voice/getvoice?mediaid="+v[1]+"\n"))
		_, _ = f2.WriteString("https://res.wx.qq.com/voice/getvoice?mediaid=" + v[1] + "\n")
		// _, _ = ioutil.WriteFile(fileName, []byte("https://res.wx.qq.com/voice/getvoice?mediaid="+v[1]+"\n"), 0666)

	}
	fmt.Print("下载完成")
}