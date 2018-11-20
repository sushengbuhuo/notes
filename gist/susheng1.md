[if(true)是个什么习惯](https://www.v2ex.com/t/382089#reply82)
```js
是为了防止以后又要改回去 
boolean flag = check(model); //检查模型部分参数及功能合法性 

flag = true; //由于 XXX 需求修改 

if(flag == true){ 
//do something 
}else{ 
//do other 
}这叫防御性开发，防止需求的多次更改
我喜欢用注释 

//* this block is for test 
console.log('this line would be output'); 
//*/ 

不用的时候删除掉第一个 / 

/* 
console.log('this line would not'); 
//*/ 

另外还有两个代码块切换的用法 

//* 
console.log('run this'); 
/*/ 
console.log('or this'); 
//*/
```
[MySQL 时间存储类型的问题](https://www.v2ex.com/t/381257#reply27)
```js
int

优点： 存储基本类型，精度高，范围查找快

缺点： 使用 cursor 分页时很容易出问题；需要转化；

timestamp

优点： 方便时间函数操作

缺点： 会随时区变化

datetime

优点：方便时间函数操作
```

[单表三千万数据分页优化方案](https://www.v2ex.com/t/381671)
```js
直接用变通的查询方式，查询时间高的吓人，因为有些数据查询是不连贯的，不能用大于多少或等于多少来查询； 
[sql] => SELECT * FROM `article_comments` ORDER BY id DESC LIMIT 199980, 20; 
[time] => 0.438656 
[sql] => SELECT * FROM `article_comments` ORDER BY id DESC LIMIT 1999980, 20; 
[time] => 26.835051 
[sql] => SELECT * FROM `article_comments` ORDER BY id DESC LIMIT 19999980, 20; 
[time] => 31.343988 
[sql] => SELECT * FROM `article_comments` ORDER BY id DESC LIMIT 29999980, 20; 
[time] => 32.138655 

现在的做法是通过先查询取出 id 
SELECT id FROM `article_comments` LIMIT 19999980, 20; 

然后用 id 去取数据 
SELECT * FROM `article_comments` WHERE id IN('1','2'....); 
虽然这样优化了很多，但是也不是很理想，如果取的 ID 间隔大，也会进行全表扫描
数据库查询规范第一条 : 绝对不允许使用 select *
改分页查询条件吧, limit offset 几十万,能不慢. 
用当前页最大评价 id ,下一页查询大于此 id 即可. 
select * from user where id>(select id from user where id>=100000 limit 1) limit 20;  //time 0.003s
这方法不适用有些场景的，如，需要查询用户回复的留言，这个留言 ID 非顺序的，很乱的，在几千万条数据中断断的出现几千条；
https://juejin.im/entry/5865c81fac502e006d5e72de
分两次查询 select id from mytable order by id limit 13456901,1; 先查出分页的首页的 ID

得到 ID x 

然后 select * from mytable order by id where id > x limit 10; 
得到数据.
[].slice.call( document.querySelectorAll('.content p') ).forEach(function(e){ 
if( e.textContent.trim() == '' ) 
e.parentNode.removeChild(e); 
});
for(var i=1 ; i<7 ; i++ ) 
{ 
(function(i){ 
var x = document.getElementById("clean"+i); 
if(x) 
x.parentNode.removeChild(x); 
})(i); 
}
传递实参 
(function(i){ 
// doSomething 
})(i); 

从作用域链中查找 
var i; 
(function(){ 
// doSomething with i	
})();
```

[模拟登录一些常见的网站](https://github.com/xchaoinfo/fuck-login)
深处移动互联网时代，每天产生数以亿计的数据，浩瀚如烟，想找到我们需要的信息，这就需要搜索了，今天就说说那些你可能每天用但还不会的搜索技能。
搜索很方便，但使用不同的关键字往往得到不同的结果，先推荐你看看这篇《提问的智慧》https://github.com/ruby-china/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md 

可参考搜索网站
```js
通过代理访问谷歌，默认会跳转到代理地的谷歌，比如香港http://www.google.com.hk 如果想使用不跳转的谷歌使用http://www.google.com/ncr
天眼查 tianyancha.com  
快搜http://magnet.chongbuluo.com/
三百搜http://www.3bsou.com
```

[运算符优先级](https://www.v2ex.com/t/379912)
```js
print(1<(2==2)) #False print(1<2 ==2) #True
 0 == False, 1 == True. Python 中，除了‘’、""、0、()、[]、{}、None 转 bool 类型为 False 
其他转换基本都为 True
第一个 ,首先 2==2 结果是 1，所以 1<1 是 False 
第二个，你先理解(1<2<3) is True, (4>2<3) is True 
可以理解成先比较 1<2，再比较 2==2，所以结果是 True 第二个类似于 1<2 and 2==2
 (b > a and b < c) ， 可以直接写做 （ a < b < c)； 所以题目的 1 < 2 == 2 其实就是 (1 < 2 and 2 == 2) 
```
[站长之家反查地址： ](http://whois.chinaz.com/reverse?host=%E6%9E%97%E8%BF%9B%E6%A0%87&ddlSearchMode=2&page=4)
[钓鱼网站](https://www.v2ex.com/t/379768)
```js
压测命令：ab -n 10000 -c 100 http://www.appeiphone.cn/
ab -n 1000 -c 1000 -p post.txt -T 'application/x-www-form-urlencoded' http://www.app-im.cn/save.asp 

post.txt 内容是 u=123456&p=12345&x=4&y=10
ab -n 1000 -c 1000 -p <(echo 'u=123456&p=12345&x=4&y=10') -T 'application/x-www-form-urlencoded' http://www.app-im.cn/save.asp
先 F12 进 Network，填好信息提交的时候按 esc，看到有一条 cancel 的记录，右键复制 copy->copy as cURL 
curl 可以直接干，脚本最简单就是 

for((i=0;i<20;++i));do while :;do 

{{Curl command goes here}} 

done;  QQ 群社工库 林进标 http://whois.chinaz.com/?DomainName=www.app-im.cn&ws= https://www.v2ex.com/t/379768 https://12321.cn/ 天眼查的信息 https://www.tianyancha.com/company/2317597321 https://try.github.io/levels/1/challenges/1
```
[postman 右侧的 Code, 窗口 GENERATE CODE SNIPPETS, 左侧可以转换成各种语言 /类型的请求](http://t.cn/R99hEzt)
```js

<?php
	//请输入你的php代码
$curl = curl_init(); 

curl_setopt_array($curl, array( 
CURLOPT_URL => "http://ups.youku.com/ups/get.json?vid=XMTQ4ODM5Mjk2MA%3D%3D&ct=10&ccode=0502&client_ip=0.0.0.0&utid=Ga3jEdWulXoCAXZwOs6IYOEY&client_ts=1501211617", 
CURLOPT_RETURNTRANSFER => true, 
CURLOPT_ENCODING => "", 
CURLOPT_MAXREDIRS => 10, 
CURLOPT_TIMEOUT => 30, 
CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1, 
CURLOPT_CUSTOMREQUEST => "GET", 
CURLOPT_HTTPHEADER => array( 
"cache-control: no-cache", 
"postman-token: 88976d57-03fd-7950-6c65-9d0f191010dc", 
"referer: http://static.youku.com/" 
), 
)); 

$response = curl_exec($curl); 
$err = curl_error($curl); 

curl_close($curl); 

if ($err) { 
echo "cURL Error #:" . $err; 
} else { 
echo $response; 
}
```
