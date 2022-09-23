package main

import (
	"encoding/json"
	"fmt"
	"reflect"
	"time"

	"gitee.com/xuesongtao/spellsql"
	"github.com/golang-module/carbon/v2"
	"github.com/gookit/color"
	// "github.com/gookit/goutil/dump"
)

type response struct {
	PageNumber int      `json:"page"`
	Fruits     []string `json:"fruits"`
}

func main() { // main函数，是程序执行的入口
	a := 'a'
	kdata := make(map[interface{}]interface{})
	kdata["vvv"] = 1
	kdata["vv"] = []string{"qwqwq"}
	aa := map[interface{}]interface{}{"x": 1, "p[": "xxx"}
	fmt.Println(a, kdata, aa)
	fmt.Println("Hello World!") // 在终端打印 Hello World!
	mapA := map[string]int{"apple": 5, "lettuce": 7}
	mapB, _ := json.Marshal(mapA)
	fmt.Println(string(mapB))
	str := `{"page": 1, "fruits": ["apple", "peach"]}`
	// res := response{}
	var res response
	json.Unmarshal([]byte(str), &res)
	fmt.Println(res, 66)
	n := make([]int, 0)
	n = append(n, 1, 2, 3, 4)        // 添加多个元素
	n = append(n, []int{5, 6, 7}...) // 添加一个切片
	fmt.Println(n)                   // [1 2 3 4 5 6 7]
	// s := "xxx"
	fmt.Println(reflect.TypeOf(mapB), reflect.TypeOf(kdata)) // string
	str2 := color.Red.Sprint("an colored message string")
	color.Println(str2)
	fmt.Print(spellsql.NewCacheSql("SELECT username, password FROM sys_user WHERE username = ? AND password = ?", "test", 123).GetSqlStr())
	fmt.Print(StructToMapJson(res))
	fmt.Print([]byte("我是xxx"), "x", 'x')
	// b := []byte("hello world")
	// fmt.Printf("%x%s\n", md5.Sum(b), md5.Sum(b))
	// m := fmt.Sprintf("%x", md5.Sum(b))
	// fmt.Print(m, []byte{1, 2, 'x', })
	fmt.Printf("%s", carbon.Now())
	var test *string
	test = new(string)
	*test = "测试"
	fmt.Println(*test)
	//遍历含有中文的字符串，需要用切片 r := []rune(str)
	str1 := "hello北京"
	str22 := []rune(str1)
	for i := 0; i < len(str22); i++ {
		fmt.Printf("%d字符=%c%v\n", i, str22[i], str22[i])
	}
	fmt.Println(len(str22), []rune(str1), []byte(str1), str1[5], string([]byte{97, 98, 99}))
	now := time.Now()
	fmt.Printf("now %v \n type %t\n", now, now)

	// dump.P(
	// 	nil, true,
	// 	12, int8(12), int16(12), int32(12), int64(12),
	// 	uint(22), uint8(22), uint16(22), uint32(22), uint64(22),
	// 	float32(23.78), float64(56.45),
	// 	'c', byte('d'),
	// 	"string",
	// )

	// resp, err := http.Get("http://httpbin.org")
	// if err != nil {
	// 	fmt.Println(err)
	// 	return
	// }
	// bResp, _ := io.ReadAll(resp.Body)
	// sResp := string(bResp)
	// fmt.Println(sResp)
}

// @title struct转map 返回的map键为struct的成员名
func StructToMap(obj interface{}) map[string]interface{} {
	t := reflect.TypeOf(obj)
	v := reflect.ValueOf(obj)

	var data = make(map[string]interface{})
	for i := 0; i < t.NumField(); i++ {
		data[t.Field(i).Name] = v.Field(i).Interface()
	}
	return data
}

// @title struct转map 返回的map键为struct的json键名
func StructToMapJson(obj interface{}) map[string]interface{} {
	t := reflect.TypeOf(obj)
	v := reflect.ValueOf(obj)

	var data = make(map[string]interface{})
	for i := 0; i < t.NumField(); i++ {
		jsonKey := t.Field(i).Tag.Get("json")
		if jsonKey != "-" {
			data[jsonKey] = v.Field(i).Interface()
		}
	}
	return data
}
