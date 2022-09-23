package main

import (
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"regexp"
	"strings"
	"sync"
	"time"

	"github.com/bitly/go-simplejson"
	carbon "github.com/golang-module/carbon/v2"
)

const URL = "https://learnku.com/go?filter=created_at_1_month&order=score&l=y"

var wg sync.WaitGroup
var tmp *int

type Person struct {
	Name string `json:"name,omitempty"` //先查找与key一样的json标签 没有json标签的，就从上往下依次查找变量名与key一样的变量 或者变量名忽略大小写后与key一样的变量 字段为空时( 空指针, 空接口, 空数组, slice, map, or string.)，json encode时不返回该字段
	Age  int
}

func GetKey(params ...interface{}) (string, error) {
	data, err := json.Marshal(params)
	fmt.Println(params...)
	if err != nil {
		return "", err
	}
	h := md5.New()
	h.Write(data)
	return hex.EncodeToString(h.Sum(nil)), nil
}

type Response struct {
	Result `json:"result"`
}
type Result struct {
	// Status    `json:"status"`
	Timestamp string `json:"timestamp"`
	Data      struct {
		Feed LiveFeed `json:"feed"`
	} `json:"data"`
}
type LiveApi struct {
	Id         int    `json:"id"`
	RichText   string `json:"rich_text"`
	CreateTime string `json:"create_time"`
	UpdateTime string `json:"update_time"`
	DocUrl     string `json:"docurl"`
	// Tag        []LiveTag   `json:"tag"`
	Multimedia interface{} `json:"multimedia"`
}
type LiveFeed struct {
	List []LiveApi `json:"list"`
	// PageInfo PageInfo  `json:"page_info"`
}

func live() {
	resp, _ := http.Get("http://")
	bResp, _ := io.ReadAll(resp.Body)
	// res := &Response{}
	// _ = json.Unmarshal([]byte(bResp), &res)
	// fmt.Println(res.Result.Data)
	// for _, v := range res.Data.Feed.List {
	// fmt.Println(v.RichText)
	// }
	json, _ := simplejson.NewJson(bResp)
	j_article_list := json.Get("result").Get("data").Get("feed").Get("list").GetIndex(0)
	fmt.Println(j_article_list)
}

func main() {
	list := []map[string]interface{}{
		{
			"id":   1,
			"name": "张三",
			"age":  20,
		},
		{
			"id":   2,
			"name": "李翠花",
			"age":  18,
		},
		{
			"id":   3,
			"name": "王老五",
			"age":  25,
		},
	}
	live()
	url := fmt.Sprintf("http://i.zhibo.sina.com.cn/api/zhibo/feed?zhibo_id=152&id=%v", 100)
	arr := []interface{}{1, "fd"}
	params := map[string]interface{}{"docId": "x"}
	bb, _ := params["docId"].(string)
	fmt.Println(bb, []interface{}{}, url, params)
	// var p Person
	p := Person{}
	// p:=new(Person)
	jsonString := `{"name": "ziji",
          "age" : 18}`
	fmt.Println(arr)
	err := json.Unmarshal([]byte(jsonString), &p)
	p2 := &Person{Age: 16}
	res3, err3 := json.Marshal(p2)
	if err3 == nil {
		fmt.Println(string(res3)) //结构体转字符串
	}
	fmt.Println(666, p2, time.Now().Format(time.RubyDate))
	if err == nil {
		// fmt.Println(p)
		fmt.Printf("%+v\n", p)
	}
	res, err := json.Marshal(list)
	if err == nil {
		fmt.Println(string(res))
	}
	fmt.Println(GetKey(1, "xxxx"))
	// fmt.Print([]byte("Hi asong\n"))
	fmt.Print([]byte{72, 105})
	setTmp() //修改tmp
	params2 := map[string]interface{}{"docId": 6666}
	fmt.Println(*tmp, time.Now().Format("2006-01-02 15:04:05"), struct{}{}, carbon.Now(), params2, []interface{}{})

	// wg.Add(1)
	// go fetchArticles()
	// wg.Wait()
	fmt.Println("完成抓取....")
}
func setTmp() {
	s := 10
	tmp = &s
}
func fetchArticles() {
	defer wg.Done()
	req, _ := http.NewRequest("GET", URL, nil)
	resp, _ := http.DefaultClient.Do(req)
	// 读取网页内容
	content, _ := ioutil.ReadAll(resp.Body)
	// 二进制文件转成网页内容
	respBody := string(content)
	// 正则表达式匹配
	reg := regexp.MustCompile(`<span class="topic-title">(?s:(.*?))</span>`)
	if reg == nil {
		fmt.Println("regex err")
		return
	}
	result := reg.FindAllStringSubmatch(respBody, -1)
	for _, values := range result {
		// 这里可以去除html元素和空格
		title := trimHtml(values[1])
		fmt.Println(title)
	}
}

// 去除html元素标签
func trimHtml(src string) string {
	//将HTML标签全转换成小写
	re, _ := regexp.Compile("\\<[\\S\\s]+?\\>")
	src = re.ReplaceAllStringFunc(src, strings.ToLower)
	//去除STYLE
	re, _ = regexp.Compile("\\<style[\\S\\s]+?\\</style\\>")
	src = re.ReplaceAllString(src, "")
	//去除SCRIPT
	re, _ = regexp.Compile("\\<script[\\S\\s]+?\\</script\\>")
	src = re.ReplaceAllString(src, "")
	//去除所有尖括号内的HTML代码，并换成换行符
	re, _ = regexp.Compile("\\<[\\S\\s]+?\\>")
	src = re.ReplaceAllString(src, "\n")
	//去除连续的换行符
	re, _ = regexp.Compile("\\s{2,}")
	src = re.ReplaceAllString(src, "\n")
	return strings.TrimSpace(src)
}
