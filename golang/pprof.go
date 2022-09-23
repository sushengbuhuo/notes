package main

import (
	"fmt"
	"reflect"
	"time"

	"github.com/gogf/gf/container/garray"
)

// "github.com/gin-contrib/pprof"
// "github.com/gin-gonic/gin"

func main() {
	// var debugHttp *http.Server

	// g := gin.New()
	// g.Use(gin.Recovery())
	// g.Use(gin.Logger())

	// pprof.Register(g)

	// // 使用9000端口开启http服务
	// debugHttp = &http.Server{
	// 	Addr:    ":9000",
	// 	Handler: g,
	// }
	// debugHttp.ListenAndServe()
	// fetchArticles()
	b := time.Now().Format("2006-01-02 15:04:05")
	// c := time.Now().Date()
	fmt.Println("格式化时间", b)
	fmt.Println(time.Now().Date())
	fmt.Println(time.Now().Clock())
	fmt.Println(time.Now().Year(), time.Now().Month(), time.Now().Day())
	fmt.Println(time.Now().String())
	a := 10
	fmt.Println("a的数值：", a)
	fmt.Printf("%T\n", a)
	fmt.Printf("变量的地址:p%x", &a) // 0xc0008a008
	// time.AfterFunc(2*time.Second, func() {
	// 	fmt.Println("hello 2s")
	// })
	fmt.Print(reflect.TypeOf(struct{ age int }{10}))
	fmt.Println("xxxxxx")
	fmt.Print(struct{ age int }{10})
	const json = `{"name":{"first":"Janet","last":"Prichard"},"age":47}`
	var SECRETKEYS = map[string]interface{}{
		"cgb": "xxx",
	}
	// value := gjson.Get(json, "#")
	println(time.Now().Format("2006-01-02 15:04"), SECRETKEYS["cgb"].(string))
	aa := garray.NewIntArray(true)
	//添加数组项
	for i := 0; i < 10; i++ {
		aa.Append(i)
	}
	// 打印结果：
	fmt.Println(aa) //"[0,1,2,3,4,5,6,7,8,9]"

	fmt.Println("数组长度：", aa.Len())
	fmt.Println("数组的值：", aa.Slice())

}
