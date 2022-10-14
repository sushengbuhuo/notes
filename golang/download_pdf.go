package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
)

// 通过Content-Length分成3部分并发执行
var spPart = 3

// 任务编排控制https://learnku.com/articles/71651
var wg sync.WaitGroup

func main() {
	url := "https://agritrop.cirad.fr/584726/1/Rapport.pdf"

	err := DownloadFile(url, "rapport.pdf")
	if err != nil {
		panic(err)
	}
}

func DownloadFile(url string, filename string) error {
	if strings.TrimSpace(url) == "" {
		return nil
	}

	// head请求获取url的header
	head, err := http.Head(url)
	if err != nil {
		return err
	}

	// 判断url是否支持指定范围请求及哪种类型的分段请求
	if head.Header.Get("Accept-Ranges") != "bytes" {
		return errors.New("not support range download")
	}

	contentLen, err := strconv.Atoi(head.Header.Get("Content-Length"))
	if err != nil {
		return err
	}

	offset := contentLen / spPart

	for i := 0; i < spPart; i++ {
		wg.Add(1)
		start := offset * i
		end := offset * (i + 1)
		name := fmt.Sprintf("part%d", i)

		go rangeDownload(url, name, start, end)
	}

	wg.Wait()

	out, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer out.Close()

	for i := 0; i < spPart; i++ {
		name := fmt.Sprintf("part%d", i)
		file, err := ioutil.ReadFile(name)
		if err != nil {
			return err
		}
		out.WriteAt(file, int64(i*offset))

		if err := os.Remove(name); err != nil {
			return err
		}
	}

	return nil

}

func rangeDownload(url string, name string, start int, end int) {
	defer wg.Done()

	client := http.Client{}
	file, err := os.Create(name)
	if err != nil {
		fmt.Println("创建文件失败：", err)
		return
	}

	defer file.Close()

	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		fmt.Println("初始化request失败：", err)
		return
	}

	rangeL := fmt.Sprintf("bytes=%d-%d", start, end)
	fmt.Println("字符范围：", rangeL)
	// 获取制定范围的数据
	req.Header.Add("Range", rangeL)
	res, err := client.Do(req)

	if err != nil {
		fmt.Println("发起http请求失败：", err)
		return
	}

	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println("读取返回体失败：", err)
		return
	}

	_, err = file.Write(body)
	if err != nil {
		fmt.Println("写入文件失败：", err)
		return
	}
}
