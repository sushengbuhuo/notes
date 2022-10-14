package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gin-contrib/pprof"
	"github.com/gin-gonic/gin"
)

// StatCost 是一个统计耗时请求耗时的中间件
func StatCost() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		c.Set("name", "小王子") // 可以通过c.Set在请求上下文中设置值，后续的处理函数能够取到该值
		// 调用该请求的剩余处理程序
		c.Next()
		// 不调用该请求的剩余处理程序
		// c.Abort()
		// 计算耗时
		cost := time.Since(start)
		log.Println(cost)
	}
}
func main() {
	r := gin.Default()
	// 注册一个全局中间件
	r.Use(StatCost())
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Hello World!",
		})
	})
	// ShouldBind 可用于 GET 的绑定参数，ShouldBindJSON 和 ShouldBind 一样，只是增加了一个格式参数，ShouldBindWith 同 json。后发现 ShouldBind 类型的函数只能使用一次，第二次再绑定的时候就无法使用了

	r.GET("/long_async", func(c *gin.Context) {
		// 创建要在goroutine中使用的副本 gin 使用 sync.Pool 重用 context，请求结束会将 context 放回对象池，供其他请求复用。异步任务不 copy context 的话，其他请求可能从对象池中拿到同一个 context，会有问题
		// cCp := c.Copy()
		// go func() {
		// 	// simulate a long task with time.Sleep(). 5 seconds
		// 	// time.Sleep(5 * time.Second)

		// 	// 这里使用你创建的副本
		// 	log.Println("Done! in path " + cCp.Request.URL.Path)
		// }()
	})
	r.LoadHTMLGlob("templates/**/*")
	//r.LoadHTMLFiles("templates/posts/index.html", "templates/users/index.html")
	r.GET("/posts/index", func(c *gin.Context) {
		c.HTML(http.StatusOK, "posts/index.html", gin.H{
			"title": "posts/index",
		})
	})
	// gin.H 是map[string]interface{}的缩写
	r.GET("/someJSON", StatCost(), func(c *gin.Context) {
		name := c.MustGet("name").(string) // 从上下文取值
		// 方式一：自己拼接JSON
		c.JSON(http.StatusOK, gin.H{"message": "Hello world!", "name": name})
		// c.XML(http.StatusOK, gin.H{"message": "Hello world!"})
	})
	r.GET("/user/search", func(c *gin.Context) {
		//defaultQuery 如果不传参数username，那将使用默认值
		username := c.DefaultQuery("username", "小王子")
		//username := c.Query("username")
		address := c.Query("address")
		//输出json结果给调用方
		c.JSON(http.StatusOK, gin.H{
			"message":  "ok",
			"username": username,
			"address":  address,
		})
	})
	{
		var id = 2
		id += 1
	}
	// 绑定JSON的示例 ({"user": "q1mi", "password": "123456"})
	r.POST("/loginJSON", func(c *gin.Context) {
		type Login struct {
			User     string `form:"user" json:"user" binding:"required"`
			Password string `form:"password" json:"password" binding:"required"`
		}

		var login Login

		if err := c.ShouldBind(&login); err == nil {
			fmt.Printf("login info:%#v\n", login)
			c.JSON(http.StatusOK, gin.H{
				"user":     login.User,
				"password": login.Password,
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		}
	})

	r.POST("/json", func(c *gin.Context) {
		// 注意：下面为了举例子方便，暂时忽略了错误处理
		b, _ := c.GetRawData() // 从c.Request.Body读取请求数据
		// 定义map或结构体
		var m map[string]interface{}
		// 反序列化
		_ = json.Unmarshal(b, &m)

		c.JSON(http.StatusOK, m)
	})

	r.GET("/moreJSON", func(c *gin.Context) {
		// 方法二：使用结构体
		var msg struct {
			Name    string `json:"user"`
			Message string
			Age     int
		}
		msg.Name = "小王子"
		msg.Message = "Hello world!"
		msg.Age = 18
		c.JSON(http.StatusOK, msg)
	})

	r.GET("users/index", func(c *gin.Context) {
		c.HTML(http.StatusOK, "users/index.html", gin.H{
			"title": "users/index",
		})
	})

	pprof.Register(r)
	r.GET("/long_sync", func(c *gin.Context) {
		// simulate a long task with time.Sleep(). 5 seconds
		// time.Sleep(5 * time.Second)

		// 这里没有使用goroutine，所以不用使用副本
		log.Println("Done! in path " + c.Request.URL.Path)
	})
	// 使用9000端口开启http服务
	debugHttp := &http.Server{
		Addr:    ":9001",
		Handler: r,
	}
	debugHttp.ListenAndServe()

	// r.Run(":8890")
}
