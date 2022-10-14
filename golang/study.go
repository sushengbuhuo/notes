package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"reflect"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/golang-module/carbon/v2"
	"github.com/shockerli/cvt"
	// cryptobin_sm2 "github.com/deatil/go-cryptobin/cryptobin/sm2"
)

type User struct {
	Name string
	Age  int
}

func (_ User) Say() {
	fmt.Println("user 说话")
}
func (_ User) SayContent(content string, a int) {
	fmt.Println("user", content, a)
}
func Hello() {
	fmt.Println("hello")
	var fs [4]func()
	{
	}
	for i := 0; i < 4; i++ {
		// fs[i] = func() {
		// 	fmt.Println("打印i = ", i)
		// }
		fs[i] = (func(i int) func() {
			return func() {
				fmt.Println("打印i = ", i)
			}
		})(i)
	}
	//打破 for/switch 或 for/select 的，一种方案是直接 return 结束整个函数不是break，下面如果还有代码不会被执行。
	for _, f := range fs {
		f() //闭包捕获的是你外部 for 里面的局部变量 i，i 迭代 4 次之后值为 4，然后执行闭包就输出 i，也就是 4
	}

}
func test() {
	var s string = "中文测试长度"
	fmt.Println(len(s), len([]rune(s)))
	str := "hello word"
	reflect.ValueOf(&str).Elem().SetString("张三")
	user := User{Name: "张三", Age: 10}
	//Elem() 获取user原始的值
	elem := reflect.ValueOf(&user).Elem()
	//FieldByName() 通过Name返回具有给定名称的结构字段 通过SetString 修改原始的值
	elem.FieldByName("Name").SetString("李四")
	elem.FieldByName("Age").SetInt(18)
	fmt.Println(reflect.TypeOf(struct{ age int }{10}))       //struct { age int }
	fmt.Println(reflect.TypeOf(map[string]string{"a": "a"})) //map[string]string
	fmt.Println(reflect.TypeOf(map[string]string{"a": "a"}).Kind())
	fmt.Println(reflect.ValueOf("hello word"))          //hello word
	fmt.Println(reflect.ValueOf(struct{ age int }{10})) //{10}
	reflect.ValueOf(&user).MethodByName("Say").Call([]reflect.Value{})
	reflect.ValueOf(user).MethodByName("Say").Call(make([]reflect.Value, 0))
	reflect.ValueOf(user).MethodByName("SayContent").Call([]reflect.Value{reflect.ValueOf("该说话了"), reflect.ValueOf(1)})
	//调用本地的方法
	reflect.ValueOf(Hello).Call([]reflect.Value{})
	reflect.ValueOf(Hello).Call(nil)

	//类型判断
	if t := reflect.TypeOf(struct{ age int }{10}).Kind(); t == reflect.Struct {
		fmt.Println("是结构体")
	} else {
		fmt.Println("不是结构体")
	}

	fmt.Println(str, user)
}
func CurrentTimeByTimeZone(timeZone string) time.Time {
	loc, _ := time.LoadLocation(timeZone)
	return time.Now().In(loc)
}
func Shuffle(array []string) []string {
	// New 返回一个使用来自 src 的随机值的新 Rand 生成其他随机值
	random := rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := len(array) - 1; i > 0; i-- {
		// Intn 以 int 形式返回半开区间 [0,n) 中的非负伪随机数。
		j := random.Intn(i + 1)
		array[i], array[j] = array[j], array[i]
	}
	return array
}

func SliceUnique(intSlice []string) []string {
	keys := make(map[string]bool)
	list := make([]string, 0)
	for _, entry := range intSlice {
		if _, value := keys[entry]; !value {
			keys[entry] = true
			list = append(list, entry)
		}
	}
	return list
}

var LOC, _ = time.LoadLocation("Asia/Shanghai")

type T struct {
	x int
}

func Sec2TimeStr(sec int64, fmtStr string) string {
	if fmtStr == "" {
		fmtStr = "2006-01-02 15:04:05"
	}
	return time.Unix(sec, 0).Format(fmtStr)
}
func TimeStr2Time(fmtStr, valueStr, locStr string) int64 {
	loc := time.Local
	if locStr != "" {
		loc, _ = time.LoadLocation(locStr) // 设置时区
	}
	if fmtStr == "" {
		fmtStr = "2006-01-02 15:04:05"
	}
	t, _ := time.ParseInLocation(fmtStr, valueStr, loc)
	return t.Unix()
}
func mytime() {
	// 1小时之后
	now := time.Now()
	layout := "2006-01-02 15:04:05"
	t1, _ := time.ParseDuration("1h")
	m1 := now.Add(t1)
	fmt.Println(m1)
	m1 = now.AddDate(0, 0, -2)
	t := time.Unix(now.Unix(), 0) // 参数分别是：秒数,纳秒数
	fmt.Println(t.Format(layout))
	//分别指定年，月，日，时，分，秒，纳秒，时区
	t = time.Date(2011, time.Month(3), 12, 15, 30, 20, 0, now.Location())
	fmt.Println(t.Format(layout))
	t2, _ := time.ParseInLocation("2006-01-02 15:04:05", time.Now().Format("2006-01-02 15:04:05"), time.Local)
	//time.Now() 使用的 CST(中国标准时间)，而 time.Parse() 默认的是 UTC(零时区)，它们相差 8 小时。所以解析时常用 time.ParseInLocation()，可以指定时区。
	t3, _ := time.Parse("2006-01-02 15:04:05", "2021-01-10 15:01:02")
	t4, _ := time.ParseDuration("-1h")
	m2 := now.Add(t4)
	m11 := now.AddDate(0, 0, -2)
	fmt.Println(m11)
	fmt.Println(m2)
	fmt.Println(time.Since(m2))
	fmt.Println(time.Until(m2))
	fmt.Println(t2, t3)
	timeZone := "Asia/Kolkata"
	currentTime := CurrentTimeByTimeZone(timeZone)
	fmt.Println("currentTime : ", currentTime.Format("2006-01-02 15:04:05"), time.Now().Unix())
	// timeZone = "Asia/ShangHai"
	// currentTime = CurrentTimeByTimeZone(timeZone)
	// fmt.Println("currentTime : ", currentTime)
	st := "2019-11-21 11:59:01"
	fmt.Printf("%s\n", st)

	t, _ := time.ParseInLocation("2006-01-02 15:04:05", st, LOC)
	fmt.Println(t.Unix())

	tt := time.Unix(t.Unix(), 0)
	fmt.Println(tt.Format("2006-01-02 15:04:05"))
	te := T{123}
	fmt.Printf("%v\n", te)
	fmt.Printf("%+v\n", te) //额外输出字段名{x:123}
	fmt.Printf("%#v\n", te) //额外输出类型名main.T{x:123}
	tt2 := struct {
		time.Time
		N int
	}{
		time.Date(2020, 12, 20, 0, 0, 0, 0, time.UTC),
		5,
	}

	m, _ := json.Marshal(tt2)
	fmt.Printf("stru%s", m)

}

type Json2 struct {
	Data struct {
		Content string `json:"content"`
	} `json:""`
}
type Data struct {
	Content string `json:"content"`
}
type Json struct {
	Data
}

func writeToFile(wg *sync.WaitGroup) {
	defer wg.Done()

	file, _ := os.OpenFile("file.txt", os.O_RDWR|os.O_CREATE, 0755)           // 系统调用阻塞
	resp, _ := http.Get("https://blog.waterflow.link/articles/1662706601117") // 网络IO阻塞
	body, _ := ioutil.ReadAll(resp.Body)                                      // 系统调用阻塞

	// file.WriteString(string(body))
	file.Write(body)
}

// Go 避免 go func(){} 如果方法中抛出 panic 无法被捕获到
// 或者是每在每个 go 前面都 recover() 一次，造成的代码混乱不可维护
func Go(f func()) {
	defer func() {
		if err := recover(); err != nil {
			// 记录日志
			log.Println(err)
		}
	}()

	go f()
	// Go(func() {
	// 	// code
	//   })
}
func SetupLogger() {
	logFileLocation, _ := os.OpenFile("/tmp/test.log", os.O_CREATE|os.O_APPEND|os.O_RDWR, 0644)
	log.SetOutput(logFileLocation)
}
func bank() {
	//  sm2  签名【招商银行】go 国密招商银行对接https://learnku.com/go/t/70314 go  get  -u  github.com/deatil/go-cryptobin https://learnku.com/php/t/68126
	// sm2key := "NBtl7WnuUtA2v5FaebEkU0/Jj1IodLGT6lQqwkzmd2E="
	// sm2keyBytes, _ := base64.StdEncoding.DecodeString(sm2key)
	// sm2data := `{"request":{"body":{"TEST":"中文","TEST2":"!@#$%^&*()","TEST3":12345,"TEST4":[{"arrItem1":"qaz","arrItem2":123,"arrItem3":true,"arrItem4":"中文"}],"buscod":"N02030"},"head":{"funcode":"DCLISMOD","userid":"N003261207"}},"signature":{"sigdat":"__signature_sigdat__"}}`
	// sm2userid := "N0033511370000000000000000"
	// sm2userid = sm2userid[0:16]

	// sm2Sign := cryptobin_sm2.NewSM2().
	// 	FromPrivateKeyBytes(sm2keyBytes).
	// 	FromString(sm2data).
	// 	SignHex([]byte(sm2userid)).
	// 	ToBase64String()

	// //  sm2  验证【招商银行】 https://github.com/lpilp/phpsm2sm3sm4 https://github.com/lat751608899/sm2
	// sm2signdata := "CDAYcxm3jM+65XKtFNii0tKrTmEbfNdR/Q/BtuQFzm5+luEf2nAhkjYTS2ygPjodpuAkarsNqjIhCZ6+xD4WKA=="
	// sm2Very := cryptobin_sm2.NewSM2().
	// 	FromBase64String(sm2signdata).
	// 	FromPrivateKeyBytes(sm2keyBytes).
	// 	MakePublicKey().
	// 	VerifyHex([]byte(sm2data), []byte(sm2userid)).
	// 	ToVeryed()

	// fmt.Println("签名结果：", sm2Sign)
	// fmt.Println("验证结果：", sm2Very)

}
func wait(wg *sync.WaitGroup, ch chan string) {
	who := "你："
	fmt.Println(who, "等待外卖……")
	// time.Sleep(time.Second * 3)
	fmt.Println(who, "磨磨唧唧开门中……3s")
	food := <-ch
	fmt.Println(who, "拿到", food, "开吃！")
	wg.Done()
}
func BubbleSort(arr *[5]int) {
	//定义一个临时变量
	temp := 0
	//最外层循环轮数
	for j := 0; j < len(*arr)-1; j++ {
		//循环每一轮排序
		for i := 0; i < len(*arr)-1-j; i++ {

			if (*arr)[i] < (*arr)[i+1] {
				temp = (*arr)[i]
				(*arr)[i] = (*arr)[i+1]
				(*arr)[i+1] = temp
			}
		}
	}
}

type integer int

func (i integer) String() string {
	return "hello"
}
func addElem(a []int, i int) {
	// a[0] = 6
	a = append(a, 5) //传入的是该 slice 的拷贝，故 addElem 中是一个新的 slice

	fmt.Println("addElem", a) // [5]
}
func TestURL() {
	URL, err := url.Parse("https://www.baidu.com/s?wd=golang")
	fmt.Println("Url before modification is", URL)
	if err != nil {
		log.Fatal("An error occurs while handling url", err)
	}
	URL.Scheme = "https"
	URL.Host = "bing.com"
	query := URL.Query()
	query.Set("q", "go")
	URL.RawQuery = query.Encode()
	fmt.Println("The url after modification is", URL, URL.String())

	fmt.Println(url.QueryEscape("Hello World"))
	params := url.Values{}
	params.Add("name", "@Wade")
	params.Add("phone", "+111111111111")
	fmt.Println(params.Encode()) // name=%40Wade&phone=%2B111111111111
	var stu Stu
	var a AInterface = stu
	var b BInterface = stu
	a.Say()
	b.Hello() //一个自定义类型将某个接口的方法都实现了，说这个自定义变量实现了该接口  一个自定义类型可以实现多个接口
	fmt.Println(xTime{time.Now()}, time.Now().Format("2006-01-02 15:04:05"))
	// (p Person) , 则是值拷贝, 如果和指针类型,比如是 (p *Person) 则是地址拷贝
	ste := "hello@aaaa"
	slice := ste[3:]
	// slice[0] = 'a'
	fmt.Println(slice)
	// string 是不可变的,也就说不能通过 str[0] = 'z' 方式来修改字符串
	str := "我问问"
	arr := []rune(str)
	arr[0] = '被'
	str1 := string(arr)
	fmt.Println(str1)
}

type xTime struct {
	time.Time
}

func (t xTime) String() string {
	return t.Format("2006-01-02 15:04:05")
}
func cloForFib(num int) int {
	var g int
	go func(num int) {
		if num <= 2 {
			g = 1
		} else {
			for m, n, j := 0, 1, 1; j < num; j++ {
				g = m + n
				m = n
				n = g
			}
		}
	}(num)
	return g
}

//定义接口
type AInterface interface {
	Say()
}
type BInterface interface {
	Hello()
}
type Stu struct {
}

func (stu Stu) Say() {
	fmt.Println("stu say()")
}
func (stu Stu) Hello() {
	fmt.Println("stu Hello()")
}
func httpPostJson(url string, jsonStr string) (string, error) {
	var json = []byte(jsonStr)
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(json)) //bytes.buffer是一个缓冲byte类型的缓冲器存放着都是byte,Buffer 就像一个集装箱容器，可以存东西，取东西（存取数据）
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}    //创建一个客户端
	resp, err := client.Do(req) //构造并发送请求
	if err != nil {
		log.Println("post err")
	}

	defer resp.Body.Close()
	body, err2 := ioutil.ReadAll(resp.Body)
	if err2 != nil {
		log.Println("ioutil reas err")
	}

	return string(body), err
}

// PrivateKeyDecrypt  Rsa私钥解密
func PrivateKeyDecrypt(cipherData string) (error, []byte) {

	// b, err := base64.StdEncoding.DecodeString(cipherData)
	// if err != nil {
	// 	fmt.Println(err.Error())
	// 	return
	// }

	// //1、通过私钥文件获取私钥信息
	// _, err = ioutil.ReadFile("./private.pem")

	// if err != nil {
	// 	fmt.Println("ReadFile err:", err)
	// 	return err, nil
	// }

	// text, err := goencryption.PrvKeyDecrypt(privateKey, b)

	// if err != nil {
	// 	fmt.Println("PrvKeyDecrypt err:", err)
	// 	return err, nil
	// }

	return nil, []byte{}

}

//通过反射调用方法
type Info struct {
	Name string
	Desc string
}

func (i Info) Detail() {
	fmt.Println("detail info")
}

func input() {
	var num int
	for {
		fmt.Println("输入一个数字")
		line, err := bufio.NewReader(os.Stdin).ReadString('\n')
		if err != nil {
			continue
		}
		line = strings.Trim(line, "\r\n")
		num, err = strconv.Atoi(line)
		if err == nil {
			break
		}
	}
	fmt.Println("结束", num)
	// var num int
	// fmt.Println("请输入一个数字")
	// input := bufio.NewScanner(os.Stdin)
	// for input.Scan() {
	//     indata := input.Text()
	//     if n, err := strconv.Atoi(indata); err == nil {
	//         num = n
	//         break
	//     }
	// }
	// fmt.Println("结束", num)
}
func ch2() {
	ii := Info{Name: "抢手", Desc: "php"}
	v := reflect.ValueOf(ii)
	t1 := reflect.TypeOf(ii)
	// 获取方法控制权
	mv := v.MethodByName("Detail")
	mv.Call([]reflect.Value{}) // 这里是无调用参数 []reflect.Value{}
	// 修改值必须是指针类型
	if v.Kind() != reflect.Ptr {
		fmt.Println("不是指针类型", t1.Kind() == reflect.Struct)
		return
	}

	bMap := []map[string]string{{
		"customerCode": "str12345",
		"deliveryId":   "str67890",
	}}
	bBODY, _ := json.Marshal(bMap)
	fmt.Println("map", string(bBODY))
	// fmt.Println(1 % 2.0) 两个操作数都是字面量常量，都是无类型的，这时会以 2.0 的 untype float constant 为准，1 隐式转为 untype float constant，所以编译错误
	fmt.Println(int(1) % 2.0) // int (1) 是 int，因此 2.0 会转为 int，因此能正常编译。
	r, _ := httpPostJson("http://httpbin.org", `{"field1": "hello", "field2": [1,2,3]}`)
	log.Println(r)
	c := make(chan int, 5)
	c <- 5
	c <- 6
	close(c)
	fmt.Println(<-c)        //5 通道关闭后，仍然能获取值 使用内置函数 close 可以关闭 channel, 当 channel 关闭后，就不能再向 channel 写数据了，但是仍然可以从该 channel 读取数据
	fmt.Println(integer(5)) // hello 调用的是 interger 的 String 方法，所以是 hello。不要被 integer 是整型所迷惑
	var i float64 = 3 / 2
	fmt.Print(i) //关键在于 3/2 计算的结果，3、2 这是整型字面值常量。根据 Go 的规则，3/2 结果也是整型，因此是 1，最后会隐式转换为 float64。
	a := make([]int, 0, 5)
	addElem(a, 5)
	fmt.Println(a) //5 参数传递只是结构体复制传递。切片在大多数情况下，只能修改元素，不能删除或者新增元素。
	arr := [3]int{11, 22, 33}
	arr2 := &arr
	(*arr2)[0] = 88
	var bytes = []byte("hello go")
	str1 := string([]byte{97, 98, 99})
	fmt.Printf("str=%v\n%v", str1, bytes)
	// 在 Go 中，字符的本质是一个整数，直接输出时，是该字符对应的 UTF-8 编码的码值
	// 直接给某个变量赋一个数字，然后按格式化输出时 % c, 会输出该数字对应的 unicode 字符
	var c3 int = '北'
	fmt.Printf("c3=%c c3=%d\n", c3, c3)

	var c4 int = 22269
	fmt.Printf("c4=%c", c4)
	var age int
	var hobby string
	fmt.Println("请输入年龄，爱好")
	fmt.Scanf("%d %s", &age, &hobby)
	fmt.Println("年龄%v 名字%v", age, hobby)
	ints := make([]int, 1)
	ints = append(ints, 2)
	fmt.Println(ints[0]) //0  注意 ints := make ([] int, 1) 创建的是一个长度为 1 的 slice，第一个元素是 int 的默认值
}

//接口与接口间可以通过嵌套创造出新的接口。
type Sayer interface {
	say()
}

type Mover interface {
	move()
}

//接口嵌套
type animal interface {
	Sayer
	Mover
}

type cat struct {
	name string
}

func (c cat) say() {
	fmt.Println("sss")
}

func (c cat) move() {
	fmt.Println("mmm")
}

type Retriever interface {
	Get(cur string) string
}

//接口由使用者定义,接口的实现其实就是对象函数(方法)的实现
//golang中duck type
func download(r Retriever) string {
	//下载https://www.imooc.com网页
	return r.Get("https://www.imooc.com")
}

type Retrievers struct {
	Context string
}

//实现接口
func (r Retrievers) Get(cur string) string {
	return r.Context
}

func main() {
	mytime()
	ints := []int{1, 2, 3}
	for _, i := range ints {
		go func(i int) {
			fmt.Printf("%v\n", i)
		}(i)
	}
	startT := time.Now()
	// time.Sleep(time.Second)
	m := make(map[string]Data) //interface 也是一种类型，其组成为 type+value，只有当 type 和 value 都为空时才是 nil 值

	jsonStr := "{\"\":{\"content\":\"....cxc.\"}}"

	var extend Json
	err := json.Unmarshal([]byte(jsonStr), &m)
	if err != nil {
		panic(err)
	}
	extend.Data = m[""]
	fmt.Println(extend.Content)
	var value1 map[string]interface{}
	mm := map[string]interface{}{
		"key1": value1,
	}
	println(value1)
	println(mm["key1"])
	println(mm["key1"] == nil)
	println(mm["key2"] == nil)
	today := time.Date(2022, 10, 31, 0, 0, 0, 0, time.Local)
	nextDay := today.AddDate(0, 1, 0)
	fmt.Println(nextDay.Format("20060102")) //20221201

	today = time.Date(2022, 10, 31, 0, 0, 0, 0, time.Local)
	d := today.Day()

	// 上个月最后一天 Date () 输入 2022-11-31 和输入 2022-12-01，将得到同样的 d（天数）。两者底层存储的时候都是一样的数据，Format () 时将 2022-11-31 的 Time 格式化成 2022-12-01 也就不例外了

	// 10-00 日 等于 9-30 日
	day1 := today.AddDate(0, 0, -d)
	fmt.Println(day1.Format("20060102"))

	// 下个月最后一天
	// 12-00 日 等于 11-30 日
	day2 := today.AddDate(0, 2, -d)
	fmt.Println(day2.Format("20060102"))

	// 20220930
	// 20221130
	fmt.Println('a' + 1)
	fmt.Println()
	// ch := make(chan string)
	wg := sync.WaitGroup{}
	ch := make(chan string, 2)
	// 无缓冲 channel 就是需要我把鸡腿亲手交到你的手上，缓冲 channel 就是我可以把鸡腿挂到门把手上，等待你需要时来取。
	wg.Add(1)
	go func() {
		who := "外卖小哥我："
		food := "鸡腿"
		fmt.Println(who, "送餐中……2s")
		// time.Sleep(time.Second * 2)
		fmt.Println(who, "已送餐到门口，等待顾客开门取餐")
		ch <- food
		fmt.Println(who, "订单已送达，开始送其他单")
		wg.Done()
	}()

	wg.Add(1)
	go wait(&wg, ch)
	// go func() {
	// 	who := "你："
	// 	fmt.Println(who, "等待外卖……")
	// 	// time.Sleep(time.Second * 3)
	// 	fmt.Println(who, "磨磨唧唧开门中……3s")
	// 	food := <-ch
	// 	fmt.Println(who, "拿到", food, "开吃！")
	// 	wg.Done()
	// }()
	wg.Wait()
	// time.Sleep(time.Second * 1)
	tc := time.Since(startT) //time.Now().Sub(start)
	//map 中元素顺序是随机的
	i := 1
	j := 1
	no1 := &i
	no2 := &j
	if reflect.DeepEqual(no1, no2) {
		// fmt.Println("equal")
		// return
	}
	fmt.Println("not equal")
	num := 65
	str := string(num) //A
	fmt.Printf("%v, %T\n", str, str)
	slice := []int{0, 1, 2, 3}
	mq := make(map[int]*int)

	for key, val := range slice {
		mq[key] = &val //val 只会定义一次
	}

	fmt.Println(*mq[1], *mq[2], *mq[3])  //3,3,3
	n := fmt.Sprintf("%s", carbon.Now()) // 2020-08-05 13:14:15
	carbon.Now().ToString()              // 2020-08-05 13:14:15 +0800 CST
	carbon.Now().ToDateTimeString()      // 2020-08-05 13:14:15
	fmt.Printf("同步执行时间 = %v\n %v", tc, n)
	fmt.Println(carbon.Now().ToString(), carbon.Now().ToDateTimeString())
	// ch2()
	// TestURL()
	// bao()
	api()
}
func api() {
	var q = Retrievers{"my name"} // 实现了接口可以直接当做Retriever
	fmt.Println(download(q))      //此时输出的是my name
	arr := [...]int{0, 1, 2, 3, 4, 5, 6, 7}
	fmt.Println("Extneding Slice:")
	fmt.Println(arr)
	s1 := arr[2:6] //Slice 的扩展
	s2 := s1[3:5]  //此时已经超出 s1 的范围了，但是 Slice 是对底层 arr 的操作，并且可以往后扩展的，所以往底层走就应该是 [5 6]，s2 = s1 [3:5] = [5 6] *
	fmt.Println(s1)
	fmt.Println(s2)
	fmt.Println(arr)
	a := adder()      //函数 + 引用环境 = 闭包
	fmt.Println(a(1)) //第一次调用时sum = 0 ， sum = 0 + 1，返回值为1
	fmt.Println(a(2)) //第二次调用时sum = 1 ，sum = 1 +2，返回值为3
	fmt.Println(a(9))
	for i := 0; i <= 5; i++ {
		fmt.Println(a(i))
	}
	//输出结果为：0、1、3、6、10、15
	f := fibonacci()

	fmt.Println(f()) //1
	fmt.Println(f()) //1
	fmt.Println(f()) //2
	fmt.Println(f()) //3
	fmt.Println(f()) //5
	fmt.Println(f()) //8
	t := time.Now()
	fmt.Println(t)

	//年月日
	fmt.Println(t.Year(), t.Month(), t.Day())

	//时分秒
	fmt.Println(t.Hour(), t.Minute(), t.Second())
	//将字符串转换为time类型
	layout := "2006-01-02 15:04:05"
	ts := "2022-07-28 23:28:40"
	_, _ = time.Parse(layout, ts)

}
func getCurrentPath() string {
	if ex, err := os.Executable(); err == nil {
		return filepath.Dir(ex)
	}
	return "./"
}

type Queue []int

//加入元素
func (q *Queue) Push(v int) {
	*q = append(*q, v)
}

//移出首元素
func (q *Queue) Pop() int {
	head := (*q)[0]
	*q = (*q)[1:]
	return head
}

//判断队列是否为空
func (q *Queue) IsImpty() bool {
	return len((*q)) == 0
}
func adder() func(v int) int {
	sum := 0
	return func(v int) int {
		sum += v
		return sum
	}
}
func fibonacci() func() int {
	a := 0
	b := 1
	return func() int {
		a, b = b, a+b
		return a
	}
}

//ReadDir 获取目录
func ReadDir(name string) {
	file, err := os.Open(name)
	if err != nil {
		fmt.Printf("err:%v\n", err)
	}
	dir, err := file.ReadDir(-1)
	if err != nil {
		fmt.Printf("err:%v\n", err)
	}
	for key, value := range dir {
		fmt.Printf("dir:  key:%v, value: %v\n", key, value)
	}
}

//ReadFile 读取文件
func ReadFile(name string) {
	//打开文件
	file, err := os.Open(name)
	if err != nil {
		fmt.Printf("err:%v\n", err)
		return
	}
	for {
		//将文件读取到缓冲区
		buf := make([]byte, 5) //设置一个缓冲区,一次读取5个字节
		n, err := file.Read(buf)
		fmt.Printf("buf:%v\n", string(buf))
		fmt.Printf("数字:%d\n", n)
		if err == io.EOF { //表示文件读取完毕
			break
		}
	}
	file.Close()
}

//WriteFile 使用缓冲区
func WriteFile3(name string) {
	file, err := os.OpenFile(name, syscall.O_RDWR, 0775) // 以读写模式打开文件，并且打开时清空文件
	if err != nil {
		fmt.Printf("err:%v\n")
	}
	defer file.Close()

	//写入文件时，使用带缓存的 *Writer
	writefile := bufio.NewWriter(file)
	for i := 0; i < 50; i++ {
		writefile.WriteString(fmt.Sprintf("您好，我是第%d个帅哥  \n", i))
	}
	//Flush将缓存的文件真正写入到文件中
	writefile.Flush()
}

//ReadLine 逐行读
func ReadLine(fileName string) error {
	f, err := os.Open(fileName)
	if err != nil {
		return err
	}
	//将文件读到缓冲区
	buf := bufio.NewReader(f)

	for {
		line, err := buf.ReadString('\n')
		line = strings.TrimSpace(line)
		fmt.Printf("行数据:%v\n", line)
		if err != nil {
			if err == io.EOF {
				return nil
			}
			return err
		}
	}
	return nil
}

//WritFile 写入数据
func WritFile2(name string) {
	file, err := os.OpenFile(name, syscall.O_RDWR, 0775) // 以读写模式打开文件，并且打开时清空文件
	if err != nil {
		fmt.Printf("err:%v\n", err)
	}
	for i := 0; i < 10; i++ {
		file.Write([]byte(fmt.Sprintf("hello golang 我是%d\n  ", i)))
	}
	file.WriteString("您好 golang")
	file.Close()
}
func writeFile(filename string) {
	file, err := os.Create(filename) //os.Create()建立文件
	if err != nil {                  //err不为空，则文件建立失败，panic输出err信息
		panic(err)
	}

	defer file.Close() //最后将文件关闭

	writer := bufio.NewWriter(file)
	defer writer.Flush()

	f := fibonacci()
	for i := 0; i < 20; i++ {
		fmt.Fprintln(writer, f())
	}
}

func bao() {
	d, _ := cvt.StringE(12.34)
	fmt.Println(d, cvt.Time("2018-10-21T23:21:29+0200").Format("2006"), []map[string]string{{"a": "1"}, {"a": "2"}})

}
