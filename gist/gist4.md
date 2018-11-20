###[文字倒过来](https://www.zhihu.com/question/29676030)
`console.log(String.fromCharCode(0x202E) + '一段文字') `
###[Javascript 中的 UTF-8](https://www.v2ex.com/t/331142#reply4)
```php
function encode_utf8(s) {
  return unescape(endcodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}
> btoa(encode_utf8('\u0227'));
"yKc=="
```
###[python 字符串形式的列表转列表](https://www.v2ex.com/t/330389)
```php
>>> a = [1, 2, 3, 4]
>>> str(a)
'[1, 2, 3, 4]'
>>> import json 
>>> a = '[1,2,2]' 
>>> b = json.loads(a) 
>>> b 
[1, 2, 2] 
>>> a = '[1,2,2]' 
>>> b = list(a)[1::2] 
>>> b 
['1', '2', '2']
>>> b
'[1, 2, 3, 4]'
>>> ast.literal_eval(b)
[1, 2, 3, 4]
a = '[1, 2, 3, 4]'.strip('[').strip(']').split(',')
```
###[同一台电脑下如何进行 Python 2 与 3 的切换](https://www.zhihu.com/question/22846291)
```php
Windows 上的 Python 自带启动器 py.exe，默认安装到系统盘的 system32 文件夹里。如果你同时安装了 Python 2 和 Python 3，用的时候直接在终端里输入：
py -3
就是打开 Python 3 的 REPL，或者
py -3 example.py
就可以运行 Python 3 的脚本了。
同理，直接输入
py example.py
使用 Python 2 来运行脚本。
py -2.7，出来2.7
py -3,出来3
py -3 -m pip install 也是可以的 可以直接pip3 install
手動把 python27下面的python.exe改成python2.exe
python35下面的python.exe改成python3.exe
你的腳本第一行就加上類似
#! D:\python27\python2.exe
這樣的一行就是調用python2
若是你想通过双击py文件运行程序，那么首先确保py文件关联执行的程序是py.exe。其次在你的源文件头部添加
#! python
或
#! python3
或
#! /usr/bin/env python3
```
###[mysql_real_escape_string() sql注入](http://stackoverflow.com/questions/5741187/sql-injection-that-gets-around-mysql-real-escape-string/12118602#12118602)
```php
$iId = mysql_real_escape_string("1 OR 1=1");    
$sSql = "SELECT * FROM table WHERE id = $iId";

$iId = (int)"1 OR 1=1";
$sSql = "SELECT * FROM table WHERE id = $iId";
mysql_query('SET NAMES gbk');
$var = mysql_real_escape_string("\xbf\x27 OR 1=1 /*");//縗' OR 1=1 /* SELECT * FROM test WHERE name = '縗' OR 1=1 /*' LIMIT 1
mysql_query("SELECT * FROM test WHERE name = '$var' LIMIT 1");

$pdo->query('SET NAMES gbk');
$stmt = $pdo->prepare('SELECT * FROM test WHERE name = ? LIMIT 1');
$stmt->execute(array("\xbf\x27 OR 1=1 /*"));
$pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
//Safe Examples
mysql_query('SET NAMES utf8');
$var = mysql_real_escape_string("\xbf\x27 OR 1=1 /*");
mysql_query("SELECT * FROM test WHERE name = '$var' LIMIT 1");

```
###[javascript抓取v2ex头像代码](https://www.v2ex.com/t/331524)
```php
var htmlURL = window.location.href;
var baselink = htmlURL.match(/.*=/g);
var toplink = "https://www.v2ex.com/recent?p=";
var toplinkNaN  = "https://www.v2ex.com/recent?p=NaN";
if ( baselink != toplink || htmlURL==toplinkNaN )
{
window.open("https://www.v2ex.com/recent?p=1");
localStorage.setItem("message",'');
}
function getLastNumberStr(str)
{
 var strs = str.replace(/.*=/g,'');
 return strs;
}
var i = getLastNumberStr(htmlURL);
i++;
self.location=toplink+i.toString();
var singlereg= /(\/\/cdn\.v2ex\.co\/avatar).*(png)/g;
var html = document.documentElement.innerHTML;
var htmlele = html.match(singlereg).toString().replace(/normal/g,"large").replace(/\,/g," ").replace(/\/\//g,"https://").replace(/png/g,"png\n");
var localdata=localStorage.getItem("message");
htmlele += localdata;
localStorage.setItem("message",htmlele);
console.log(htmlele);
```
###[sql注入必备知识](http://blog.spoock.com/2016/06/28/sql-injection-1/)
```php
mysql常用注释

#
--[空格]或者是--+
/*…*/
在注意过程中，这些注释可能都需要进行urlencode
```
###[0e开头MD5值小结](http://www.219.me/posts/2884.html)
```php
<?php
echo "-------------------------------------------\r\n";

while(1){
$s=rand();
$s.="a";
$s="s".$s;
if(md5($s)=="0") {
echo $s;
echo "\r\n";
echo md5($s)."\r\n";
}
}
```
###[无需编译的文档撰写工具](https://github.com/egoist/docute)
```php
npm i -g docute-cli

docute init ./docs
docute
```
###[Laravel 中的 model 里面能对某个属性进行过滤操作](https://laravel-china.org/topics/3526)

```php
public function getImagesAttribute($value)
{
    return json_decode($value);
}
$data         = Template::latest()->forPage($current_page, $page_size)->get();
```
###[引入第三方类](https://laravel-china.org/topics/3525)
```php
function model($name)
{
       $class = 'App\\'.$name;
       return new $class;
}
```
###[终端显示 Git 当前所在分支](https://pigjian.com/article/linux-git)
```php
编辑.bashrc文件
function git_branch {
  branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
  if [ "${branch}" != "" ];then
      if [ "${branch}" = "(no branch)" ];then
          branch="(`git rev-parse --short HEAD`...)"
      fi
      echo "->$branch"
  fi
}

export PS1='\[\e[37;40m\][\[\033[01;36m\]\u\[\e[37;40m\]@\[\e[0m\]\h \[\033[01;36m\]\W\[\033[01;32m\]$(git_branch)\[\033[00m\]\[\e[37;40m\]]\[\e[0m\]\$ '
source ./.bashrc
```
###[开启mysql远程连接](https://pigjian.com/article/centos-mysql)
```php
grant all privileges on *.* to 'root'@'%' identified by '123456' with grant option;
# root是用户名，%代表任意主机，'123456'指定的登录密码（这个和本地的root密码可以设置不同的，互不影响）
flush privileges; # 重载系统权限
exit;
允许3306端口

iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 3306 -j ACCEPT
# 查看规则是否生效
iptables -L -n # 或者: service iptables status

# 此时生产环境是不安全的，远程管理之后应该关闭端口，删除之前添加的规则
iptables -D INPUT -p tcp -m state --state NEW -m tcp --dport 3306 -j ACCEPT
service iptables save # 或者: /etc/init.d/iptables save
```
###[VarDumper高亮提示](https://pigjian.com/article/vardumper)
```php
composer require symfony/var-dumper
require 'vendor/autoload.php';

$var = array(
  'a simple string'=>'in an array of 5 elements',
  'a float' => 1.0,
  'an integer' => 1,
  'a boolean' => true,
  'an empty array' => array(),
);

dump($var);

composer global require symfony/var-dumper;
配置php.ini auto_prepend_file = ${HOME}/.composer/vendor/autoload.php
composer global update
```
###斐波那契数列
```php
function fib($n)
{
$cur = 1;
$prev = 0;
for ($i = 0; $i < $n; $i++) {
yield $prev;

    $temp = $cur;
    $cur = $prev + $cur;
    $prev = $temp;
}
}

$fibs = fib(9);
foreach ($fibs as $fib) {
echo $fib.PHP_EOL;
}
```
###[Eloquent ORM 模型中添加自定义值](https://laravel-china.org/topics/3521)
```php
class Post extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = ['title', 'text'];

    /**
     * 文章对应多条评论
     * @return \Illuminate\Database\Eloquent\Relations\HasMany
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
public function getCountCommentsAttribute()
{
    return $this->comments()->count();
}
protected $appends = ['count_comments'];
```
###[Laravel collect 的 PHP Extension](https://laravel-china.org/topics/3528)
```php
git clone https://github.com/VikinDev/v-collect.git
phpize
./configure
make && make install
$vcollect = vcollect([
    ['developer' => ['name' => 'Taylor', 'option' => ['test' => 'one'] ] ],
    ['developer' => ['name' => 'Abigail', 'option' => ['test' => 'two'] ] ]
]);

$vcollect->where('developer.option.test', 'one')->toArray();

// ['developer' => ['name' => 'Taylor', 'option' => ['test' => 'one'] ] ]
```
###[项目所依赖的组件的require-dev是不会安装到你的项目](https://segmentfault.com/q/1010000007967298)
```php
"require-dev": {
        "phpunit/phpunit": "~4.0",
    },
    "require": {
        "phpunit/phpunit": "5.7.*",
    },
```
###[读取/dev/urandom生成指定长度的随机数](https://segmentfault.com/q/1010000007959046)
```php
$pr_bits = '';
// Unix/Linux platform?
$fp = @fopen('/dev/urandom','rb');
if ($fp !== FALSE) {
    $pr_bits .= @fread($fp, 16);
    @fclose($fp);
}

echo $pr_bits;
```
###[php数组重组](https://segmentfault.com/q/1010000007943712)
```php

$array = [
     1 => [ 'k' => 0 ],
     2 => [ 'k' => 1 ],
     3 => [ 'k' => 1 ],
     4 => [ 'k' => 2 ],
     5 => [ 'k' => 4 ],
     6 => [ 'k' => 3 ],
     7 => [ 'k' => 0 ],
     8 => [ 'k' => 6 ]
];


$tree  = [];
$refer = $array;

foreach($array as $key => $val) {
    if (isset($refer[$val['k']])) {
        $refer[$val['k']]['children'][$key] = &$refer[$key];
    } else {
        $tree[$key] = &$refer[$key];
    }
}

print_r($tree);
[
    1 => [
      'k' => 0,
      'children' => [
          2 => [
            'k' => 1,
            'children' => [
                4 => [
                    'k' => 2
                    'children' => [
                        5 => ['k' => 4]
                    ]
                ]
            ]
          ],
          3 => [
              'k' => 1,
              'children' => [
                  6 => [
                  'k' => 3,
                  'children' => [
                      8 => ['k' => 6]
                  ]
              ]
          ]
      ]
    ],
    7 => [ 'k' => 0 ]
]

```
###[实现无限级分类](https://segmentfault.com/q/1010000007933292)
```php
$categories = [
  ['id'=>1,'cat_id'=>1,'cat_name'=>'a','pid'=>0],
  ['id'=>2,'cat_id'=>2,'cat_name'=>'b','pid'=>1],
  ['id'=>3,'cat_id'=>3,'cat_name'=>'c','pid'=>1],
  ['id'=>4,'cat_id'=>4,'cat_name'=>'d','pid'=>2],
  ['id'=>5,'cat_id'=>5,'cat_name'=>'e','pid'=>3],
];
    
    
$tree = [];

foreach($categories as $v){
    $tree[$v['id']] = $v;
    $tree[$v['id']]['children'] = array();
}

foreach ($tree as $k=>$v) {
    if ($v['pid'] > 0) {
        $tree[$v['pid']]['children'][] = &$tree[$k];
    }
}    
print_r($tree);
function _data_to_tree(&$items, $topid = 0, $with_id = TRUE)
{
    $result = [];
    foreach($items as $v)
        if ($topid == $v['parent'])  {
            $r = $v + ['children' => _data_to_tree($items, $v['id'], $with_id)];
            if ($with_id)
                $result[$v['id']] = $r;
            else
                $result[] = $r;
        }
            
    return $result;
}
//使用PHP的指针特性
function _data_to_tree($items, $topid = 0, $with_id = TRUE)
{
    if ($with_id)
        foreach ($items as $item)
            $items[ $item['parent'] ]['children'][ $item['id'] ] = &$items[ $item['id'] ];
    else
        foreach ($items as $item)
                $items[ $item['parent'] ]['children'][] = &$items[ $item['id'] ];

         return isset($items[ $topid ]['children']) ? $items[ $topid ][ 'children' ] : [];
}
//注意本算法 不会输出 0 的根节点
//并且数据必须有KEY，并且需要与id相等，也就是如下格式：
// 1 => ['id' => 1]
// 2 => ['id' => 2] 
$data = [
  4 => ['id' => 4, 'parent' => 1 , 'text' => 'Parent1'], 
  1 => ['id' => 1, 'parent' => 0 , 'text' => 'Root'],
  2 => ['id' => 2, 'parent' => 1 , 'text' => 'Parent2'], 
  3 => ['id' => 3, 'parent' => 2 , 'text' => 'Sub1'], 
];
print_r ( _data_to_tree($data, 0) );


```
###[联合查询如何无缝使用limit翻页](https://segmentfault.com/q/1010000007957291)
```php
SELECT id,title,time,flag FROM (
select id,title,time,'zhuan' flag from zhuan 
UNION ALL
select id,title,time,'post' from post) a GROUP BY time DESC LIMIT 0,10;

select id,title,cdn,time FROM (
(select id,title,111 as cdn,time from set_gif where zhuanid = 0) 
UNION ALL
(select id,name as title,222 as cdn,time from set_zhuan) order by time desc) a LIMIT 0,100
```
###[php全局变量](https://segmentfault.com/q/1010000007920887)
```php
function global_references($flag)
{
    $var1 = &$GLOBALS['var1'];
    $var2 = &$GLOBALS['var2'];
    if ($flag) {
        $var2 = &$var1; //1
    } else {
        $var2 = '1'; //2
    }
}
```
###[数组转换](https://segmentfault.com/q/1010000007913647)
```php
<?php
// +----------------------------------------------------------------------
// | lmxdawn [ WE CAN DO IT JUST THINK IT ]
// +----------------------------------------------------------------------
// | Copyright (c) 2016 .
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: Byron Sampson <lmxdawn@gmail.com>
// +----------------------------------------------------------------------

/*
//设，有数组：
    $arr = [3, 1, 2, 4, 8, 7, 9, 10, 13, 15];
//写一个函数，使其输出格式为:
    $arr = array(
        0 => '1~4',
        1 => '7~10',
        2 => '13',
        3 => '15'
    );
 //*/

class Test {

    private $test_array;//需要操作的数组

    private $ico = '~';//分隔符

    private static $_instance;//

    private function __construct($test_array = array()) {
        $this->test_array = $test_array;
    }

    private function __clone() {
        // TODO: Implement __clone() method.
    }

    public static function getInstance($test_array = array()){
        if (is_null(self::$_instance) || !isset(self::$_instance)){
            self::$_instance = new self($test_array);
        }
        return self::$_instance;
    }

    /**
     * 数组分组
     * @return array 返回分好的数组
     */
    public function array_group(){

        //首先 升序对数组排序
        sort($this->test_array);
        // 去重数组
        $test_array = array_unique($this->test_array);
        //定义临时数组
        $tmp_array = array();
        $one = $test_array[0];//记录第一次的值
        $tmp_array_key = -1;//临时数组的下标 （初始值为 -1）不然临时数组的下标会从 1 开始
        foreach ($test_array as $key => $val){
            // 取出临时数组的最后一个元素
            $last_val = end($tmp_array);
            // 用分隔符把字符串转换为数组
            $last_array = explode($this->ico,$last_val);
            //如果最后一个元素为数组 就去最后一个元素的最后一个元素，否则就是取第一个
            $tmp_last_val = (is_array($last_array)) ? end($last_array) : $last_array[0];
            //判断是否是连续值
            if (!empty($tmp_last_val) && ($tmp_last_val + 1) == $val){
                $val = $one.$this->ico.$val;
            }else{
                // 如果不连续，更改第一次记录的值
                $one = $val;
                // 临时数组的值加一
                $tmp_array_key++;
            }
            //存入临数组
            $tmp_array[$tmp_array_key] = $val;
        }

        return $tmp_array;//返回临时数组

    }


    /**
     * 格式化输出数组
     * @param      $var
     * @param bool $echo
     * @param null $label
     * @param bool $strict
     * @return mixed|null|string
     */
    public static function dump($var, $echo=true, $label=null, $strict=true) {
        header("Content-type: text/html; charset=utf-8");
        $label = ($label === null) ? '' : rtrim($label) . ' ';
        if (!$strict) {
            if (ini_get('html_errors')) {
                $output = print_r($var, true);
                $output = '<pre>' . $label . htmlspecialchars($output, ENT_QUOTES) . '</pre>';
            } else {
                $output = $label . print_r($var, true);
            }
        } else {
            ob_start();
            var_dump($var);
            $output = ob_get_clean();
            if (!extension_loaded('xdebug')) {
                $output = preg_replace('/\]\=\>\n(\s+)/m', '] => ', $output);
                $output = '<pre>' . $label . htmlspecialchars($output, ENT_QUOTES) . '</pre>';
            }
        }
        if ($echo) {
            echo($output);
            return null;
        }else
            return $output;
    }

}

$test_array = array(3, 1, 2, 4, 8, 7, 9, 10, 13, 15,3,1,2,4,23,56,85,24);
$test = Test::getInstance($test_array);

// 打印数组
Test::dump($test->array_group());
$arr = array(
        0 => '1~4',
        1 => '7~10',
        2 => '13',
        3 => '15'
);
```
###[根据一个字段查找另一个字段重复的数据](https://segmentfault.com/q/1010000007931297)
```php
delete a from product_code_relate_titletext a,product_code_relate_titletext b where a.id>b.id and a.product_code=b.product_code and a.raw_title=b.raw_title;
delete from product_code_relate_titletext where id not in (select * from (select min(id) from product_code_relate_titletext group by product_code,raw_title having count(*) > 1) as b);
```
###[同一个表查询更新](https://segmentfault.com/q/1010000007945346)
`update guideline_news set content =(select content from (select * from guideline_news) a where a.id = 16) where id>16;`
###[mysql in指定查询](https://segmentfault.com/q/1010000007965209)
```php
(select * from table_name where column_name = value1 limit 5)
union all
(select * from table_name where column_name = value2 limit 5);
```
###获取ip
```php
curl ifcfg.cn/echo |python -m json.tool
{
    "url": "http://ifcfg.cn/echo",
    "user_agent": "curl/7.30.0",
    "protocol": "http",
    "query_string": "",
    "ip": "223.20.168.245",
    "headers": {
        "CONNECTION": "close",
        "HOST": "ifcfg.cn",
        "ACCEPT": "*/*",
        "USER-AGENT": "curl/7.30.0"
    },
    "location": "\u4e2d\u56fd \u5317\u4eac",
    "method": "GET",
    "path": "/echo",
    "host": "ifcfg.cn"
}

```
###[附近地点搜索](http://mp.weixin.qq.com/s?__biz=MjM5NDM4MDIwNw==&mid=2448834749&idx=1&sn=48aacf951928cb5241beda4c88453051&chksm=b28a407d85fdc96b2fd0c7e9bbde0c19dc0d8b580cd681d6887ad5f97c2659ef2836fbb83174#rd)
```php
$longitude = ''; //经度

$latitude = '';  //纬度

$objGeoHash = new Geohash();  //文末有该类的下载方式

$strGeoHashCode = $objGeoHash->encode($latitude, $longitude);

//在采集数据的时候，这个值保存到数据库中即可。
/**
 * [PHP Code] 根据经纬度计算两点之间的记录
 * @param $lat1 纬度1
 * @param $lng1 经度1
 * @param $lat2 纬度2
 * @param $lng2 经度2
 * @return float 单位(米)
 */
function getDistance($lat1, $lng1, $lat2, $lng2)
{
    //地球半径
    $R = 6378137;

    //将角度转为弧度
    $radLat1 = deg2rad($lat1);
    $radLat2 = deg2rad($lat2);
    $radLng1 = deg2rad($lng1);
    $radLng2 = deg2rad($lng2);

    //结果
    $s = acos(cos($radLat1) * cos($radLat2) * cos($radLng1 - $radLng2)
            + sin($radLat1) * sin($radLat2)) * $R;

    //精度
    $s = round($s * 10000)/10000;

    return  round($s);
}
```
###[ ].concat[1,2,3]
```php
//https://zhuanlan.zhihu.com/p/24596013
Array.prototype.concat[3]
Array.prototype.concat[3] = [1,2,3];
```
###github文件地址
```php
github上打开文件， 然后点 raw
https://raw.githubusercontent.com/mingyun/mingyun.github.io/master/gists4.md
sudo wget http://github.com/username/yourproject/raw/master/shellfile -O /etc/
```
###[curl 或 file_get_contents 获取需要授权页面的方法](http://blog.csdn.net/fdipzone/article/details/44475801)
```php
$url = 'http://localhost/server.php';  
$param = array('content'=>'fdipzone blog');  
  
$auth = sprintf('Authorization: Basic %s', base64_encode('fdipzone:654321')); // 加入这句  
  
$opt = array(  
    'http' => array(  
        'method' => 'POST',  
        'header' => "content-type:application/x-www-form-urlencoded\r\n".$auth."\r\n", // 把$auth加入到header  
        'content' => http_build_query($param)  
    )  
);  
  
$context = stream_context_create($opt);  
  
$ret = file_get_contents($url, false, $context);  
  
if($ret){  
    $data = json_decode($ret, true);  
    print_r($data);  
}else{  
    echo 'POST Fail';  
}  

$url = 'http://localhost/server.php';  
$param = array('content'=>'fdipzone blog');  
  
$ch = curl_init();  
curl_setopt($ch, CURLOPT_URL, $url);  
curl_setopt($ch, CURLOPT_POST, true);  
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($param));  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  
curl_setopt($ch, CURLOPT_USERPWD, 'fdipzone:654321'); // 加入这句  
$ret = curl_exec($ch);  
$retinfo = curl_getinfo($ch);  
curl_close($ch);  
  
if($retinfo['http_code']==200){  
    $data = json_decode($ret, true);  
    print_r($data);  
}else{  
    echo 'POST Fail';  
}  

if(!isset($_SERVER['PHP_AUTH_USER']))   
{   
    header('WWW-Authenticate: Basic realm="localhost"');   
    header("HTTP/1.0 401 Unauthorized");   
    exit;   
}else{   
    if (($_SERVER['PHP_AUTH_USER']!= "fdipzone" || $_SERVER['PHP_AUTH_PW']!="654321")) {  
        header('WWW-Authenticate: Basic realm="localhost"');  
        header("HTTP/1.0 401 Unauthorized");  
        exit;  
    }  
}  
  
$content = isset($_POST['content'])? $_POST['content'] : '';  
header('content-type:application/json');  
echo json_encode(array('content'=>$content));
```
###mysql导出查询结果到csv方法
```php
http://blog.csdn.net/fdipzone/article/details/48399831
mysql -u root
use test;
select * from table into outfile '/tmp/table.csv' fields terminated by ',' optionally enclosed by '"' lines terminated by '\r\n';
```
###from_unixtime
```php
mysql> select from_unixtime(1459338786, '%Y-%m-%d %H:%i:%s');
+------------------------------------------------+
| from_unixtime(1459338786, '%Y-%m-%d %H:%i:%s') |
+------------------------------------------------+
| 2016-03-30 19:53:06                            |
+------------------------------------------------+
1 row in set (0.00 sec)
按小时统计数量
mysql> select from_unixtime(addtime,'%Y-%m-%d %H') as date,count(*) from `table` group by from_unixtime(addtime,'%Y-%m-%d %H');
+---------------+----------+
| date          | count(*) |
+---------------+----------+
| 2016-03-30 19 |      409 |
| 2016-03-30 20 |      161 |
+---------------+----------+
```
###判斷字段是否存在方法
```php
desc `table` `mid`
desc `table` '%abc%'
show columns from `table` like 'mid'
show columns from `table` like '%abc%'
```
###优化 insert 性能
```php
一条sql语句插入多条数据INSERT INTO `insert_table` (`uid`, `content`, `type`) VALUES ('userid_0', 'content_0', 0), ('userid_1', 'content_1', 1);  
使用事务
START TRANSACTION;  
INSERT INTO `insert_table` (`uid`, `content`, `type`) VALUES ('userid_0', 'content_0', 0);  
INSERT INTO `insert_table` (`uid`, `content`, `type`) VALUES ('userid_1', 'content_1', 1);  
...  
COMMIT; 
1.sql语句长度有限制，合并sql语句时要注意。长度限制可以通过max_allowed_packet配置项修改，默认为1M。
2.事务太大会影响执行效率，mysql有innodb_log_buffer_size配置项，超过这个值会使用磁盘数据，影响执行效率
```
###[You can't specify target table for update in FROM clause错误的解决方法](http://blog.csdn.net/fdipzone/article/details/52695371)
```php
mysql> update message set content='Hello World' where id in(select min(id) from message group by uid);
ERROR 1093 (HY000): You can't specify target table 'message' for update in FROM clause
update message set content='Hello World' where id in( select min_id from ( select min(id) as min_id from message group by uid) as a );

```
###导入大批量数据出现MySQL server has gone away的解决方法
set global max_allowed_packet=268435456;
show global variables like 'max_allowed_packet';

使用set global命令修改 max_allowed_packet 的值，重启mysql后会失效，还原为默认值。

如果想重启后不还原，可以打开 my.cnf 文件，添加 max_allowed_packet = 256M 即可
###[使用inet_aton和inet_ntoa处理ip地址数据](http://blog.csdn.net/fdipzone/article/details/49532127)
```php
CREATE TABLE `user` (
 `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
 `name` varchar(100) NOT NULL,
 `ip` int(10) unsigned NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB;
INSERT INTO `user` (`id`, `name`, `ip`) VALUES
(2, 'Abby', inet_aton('192.168.1.1')),
(3, 'Daisy', inet_aton('172.16.11.66')),
(4, 'Christine', inet_aton('220.117.131.12'));
mysql> select * from `user`;
+----+-----------+------------+
| id | name      | ip         |
+----+-----------+------------+
|  2 | Abby      | 3232235777 |
|  3 | Daisy     | 2886732610 |
|  4 | Christine | 3698688780 |
+----+-----------+------------+
$ip_start = '172.16.11.1';
$ip_end = '172.16.11.100';

echo 'ip2long(ip_start):'.sprintf('%u',ip2long($ip_start)); // 2886732545
echo 'ip2long(ip_end):'.sprintf('%u',ip2long($ip_end));     // 2886732644
mysql> select ip,name,inet_ntoa(ip) as ip from `user` where ip>=2886732545 and ip<=2886732644;
+------------+-------+---------------+
| ip         | name  | ip            |
+------------+-------+---------------+
| 2886732610 | Daisy | 172.16.11.66  |
+------------+-------+---------------+
```
###查看与修改auto_increment方法
```php
mysql> select auto_increment from information_schema.tables where table_schema='test_user' and table_name='user';
+----------------+
| auto_increment |
+----------------+
|           1002 |
+----------------+
1 row in set (0.04 sec)
alter table tablename auto_increment=10000;
mysql> select auto_increment from information_schema.tables where table_schema='test_user' and table_name='user';
+----------------+
| auto_increment |
+----------------+
|          10000 |
+----------------+
1 row in set (0.04 sec)
```
###[mysql order by rand() 效率优化方法](http://blog.csdn.net/fdipzone/article/details/51541729)
```php
select * from user order by rand() limit 1;

$sqlstr = 'select count(*) as recount from user';
$query = mysql_query($sqlstr) or die(mysql_error());
$stat = mysql_fetch_assoc($query);
$total = $stat['recount'];

// 随机偏移
$offset = mt_rand(0, $total-1);

// 偏移后查询
$sqlstr = 'select * from user limit '.$offset.',1';
$query = mysql_query($sqlstr) or die(mysql_error());
$result = mysql_fetch_assoc($query);

print_r($result);
select * from user limit 23541,1;
```
###[PDO查询mysql避免SQL注入](http://blog.csdn.net/fdipzone/article/details/22330345)
```php
$dbh = new PDO("mysql:host=localhost; dbname=mydb", "root", "pass");  
$dbh->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); //禁用prepared statements的仿真效果  
//当调用 prepare() 时，查询语句已经发送给了数据库服务器，此时只有占位符 ? 发送过去，没有用户提交的数据；当调用到 execute()时，用户提交过来的值才会传送给数据库，它们是分开传送的，两者独立的，SQL攻击者没有一点机会。
setAttribute()这一行是强制性的，它会告诉 PDO 禁用模拟预处理语句，并使用 real parepared statements 。这可以确保SQL语句和相应的值在传递到mysql服务器之前是不会被PHP解析的（禁止了所有可能的恶意SQL注入攻击）。
$dbh->exec("set names 'utf8'");   
$sql="select * from table where username = ? and password = ?";  
$query = $dbh->prepare($sql);   
$exeres = $query->execute(array($username, $pass));   
if ($exeres) {   
    while ($row = $query->fetch(PDO::FETCH_ASSOC)) {  
        print_r($row);  
    }  
}  
$dbh = null; 
不能让占位符 ? 代替一组值，这样只会获取到这组数据的第一个值
select * from table where userid in ( ? );  
如果要用in來查找，可以改用find_in_set()实现
$ids = '1,2,3,4,5,6';  
select * from table where find_in_set(userid, ?);  

```
###[互换表中两列数据方法](http://blog.csdn.net/fdipzone/article/details/50864196)
```php
mysql> select * from product;
+----+--------+----------------+--------+
| id | name   | original_price | price  |
+----+--------+----------------+--------+
|  1 | 雪糕   |           5.00 |   3.50 |
|  2 | 鲜花   |          18.00 |  15.00 |
|  3 | 甜点   |          25.00 |  12.50 |
|  4 | 玩具   |          55.00 |  45.00 |
|  5 | 钱包   |         285.00 | 195.00 |
+----+--------+----------------+--------+
5 rows in set (0.00 sec)

mysql> update product as a, product as b set a.original_price=b.price, a.price=b.original_price where a.id=b.id;
Query OK, 5 rows affected (0.01 sec)
Rows matched: 5  Changed: 5  Warnings: 0

mysql> select * from product;
+----+--------+----------------+--------+
| id | name   | original_price | price  |
+----+--------+----------------+--------+
|  1 | 雪糕   |           3.50 |   5.00 |
|  2 | 鲜花   |          15.00 |  18.00 |
|  3 | 甜点   |          12.50 |  25.00 |
|  4 | 玩具   |          45.00 |  55.00 |
|  5 | 钱包   |         195.00 | 285.00 |
+----+--------+----------------+--------+
5 rows in set (0.00 sec)
```
###JS将unicode码转中文方法
var str = "\u7434\u5fc3\u5251\u9b44\u4eca\u4f55\u5728\uff0c\u6c38\u591c\u521d\u6657\u51dd\u78a7\u5929\u3002";  
document.write(unescape(str.replace(/\\u/g, '%u')));

###[HTML实体编号与非ASCII字符串相互转换类](http://blog.csdn.net/fdipzone/article/details/52464068)
```php
    /**
 *  HTML实体编号与非ASCII字符串相互转换类
 *  Date:   2016-09-07
 *  Author: fdipzone
 *  Ver:    1.0
 *
 *  Func:
 *  public  encode 字符串转为HTML实体编号
 *  public  decode HTML实体编号转为字符串
 *  private _convertToHtmlEntities 转换为HTML实体编号处理
 */
class HtmlEntitie{ // class start

    public static $_encoding = 'UTF-8';

    /**
     * 字符串转为HTML实体编号
     * @param  String $str      字符串
     * @param  String $encoding 编码
     * @return String
     */
    public static function encode($str, $encoding='UTF-8'){
        self::$_encoding = $encoding;
        return preg_replace_callback('|[^\x00-\x7F]+|', array(__CLASS__, '_convertToHtmlEntities'), $str);
    }

    /**
     * HTML实体编号转为字符串
     * @param  String $str      HTML实体编号字符串
     * @param  String $encoding 编码
     * @return String
     */
    public static function decode($str, $encoding='UTF-8'){
        return html_entity_decode($str, null, $encoding);
    }

    /**
     * 转换为HTML实体编号处理
     * @param Mixed  $data 待处理的数据
     * @param String
     */
    private static function _convertToHtmlEntities($data){
        if(is_array($data)){
            $chars = str_split(iconv(self::$_encoding, 'UCS-2BE', $data[0]), 2);
            $chars = array_map(array(__CLASS__, __FUNCTION__), $chars);
            return implode("", $chars);
        }else{
            $code = hexdec(sprintf("%02s%02s;", dechex(ord($data {0})), dechex(ord($data {1})) ));
            return sprintf("&#%s;", $code);
        }
    }

} // class end
$str = '<p>更多资讯可关注本人微信号：fdipzone-idea</p><p><img border="0" src="http://img.blog.csdn.net/20141224160911852" width="180" height="180" title="破晓领域"></p><p>您的支持是我最大的动力，谢谢！</p>';

// 字符串转为HTML实体编号
$cstr = HtmlEntitie::encode($str);
echo '字符串转为HTML实体编号'.PHP_EOL;
echo $cstr.PHP_EOL.PHP_EOL;

// HTML实体编号转为字符串
echo 'HTML实体编号转为字符串'.PHP_EOL;
echo HtmlEntitie::decode($cstr);
字符串转为HTML实体编号
<p>&#26356;&#22810;&#36164;&#35759;&#21487;&#20851;&#27880;&#26412;&#20154;&#24494;&#20449;&#21495;&#65306;fdipzone-idea</p><p><img border="0" src="http://img.blog.csdn.net/20141224160911852" width="180" height="180" title="&#30772;&#26195;&#39046;&#22495;"></p><p>&#24744;&#30340;&#25903;&#25345;&#26159;&#25105;&#26368;&#22823;&#30340;&#21160;&#21147;&#65292;&#35874;&#35874;&#65281;</p>

HTML实体编号转为字符串
<p>更多资讯可关注本人微信号：fdipzone-idea</p><p><img border="0" src="http://img.blog.csdn.net/20141224160911852" width="180" height="180" title="破晓领域"></p><p>您的支持是我最大的动力，谢谢！</p>
```
###[版本处理类](http://blog.csdn.net/fdipzone/article/details/46702553)
```php
class Version{ // class start

    /**
     * 将版本转为数字
     * @param  String $version 版本
     * @return Int
     */
    public function version_to_integer($version){
        if($this->check($version)){
            list($major, $minor, $sub) = explode('.', $version);
            $integer_version = $major*10000 + $minor*100 + $sub;
            return intval($integer_version);
        }else{
            throw new ErrorException('version Validate Error');
        }
    }

    /**
     * 将数字转为版本
     * @param  Int     $version_code 版本的数字表示
     * @return String
     */
    public function integer_to_version($version_code){
        if(is_numeric($version_code) && $version_code>=10000){
            $version = array();
            $version[0] = (int)($version_code/10000);
            $version[1] = (int)($version_code%10000/100);
            $version[2] = $version_code%100;
            return implode('.', $version);
        }else{
            throw new ErrorException('version code Validate Error');
        }
    }

    /**
     * 检查版本格式是否正确
     * @param  String  $version 版本
     * @return Boolean
     */
    public function check($version){
        $ret = preg_match('/^[0-9]{1,3}\.[0-9]{1,2}\.[0-9]{1,2}$/', $version);
        return $ret? true : false;
    }

    /**
     * 比较两个版本的值
     * @param  String  $version1  版本1
     * @param  String  $version2  版本2
     * @return Int                -1:1<2, 0:相等, 1:1>2
     */
    public function compare($version1, $version2){
        if($this->check($version1) && $this->check($version2)){
            $version1_code = $this->version_to_integer($version1);
            $version2_code = $this->version_to_integer($version2);

            if($version1_code>$version2_code){
                return 1;
            }elseif($version1_code<$version2_code){
                return -1;
            }else{
                return 0;
            }
        }else{
            throw new ErrorException('version1 or version2 Validate Error');
        }
    }

} // class end
$version = '2.7.1';

$obj = new Version();

// 版本转数字
$version_code = $obj->version_to_integer($version);
echo $version_code.'<br>';  // 20701

// 数字转版本
$version = $obj->integer_to_version($version_code);
echo $version.'<br>'; // 2.7.1

// 检查版本
$version = '1.1.a';
var_dump($obj->check($version)); // false

// 比较两个版本
$version1 = '2.9.9';
$version2 = '10.0.1';

$result = $obj->compare($version1, $version2);
echo $result; // -1
>>> '3.0.1'>'10.0.1'
=> true
```
###[被@的用户名添加a标签](https://segmentfault.com/q/1010000007971440)
```php

$text = preg_replace_callback('(@[^\s]+)',function($matches){
    //这里直接把要替换的结果return出去就可以了
    return "<a href='javascript:;'>{$matches[0]}</a> ";
},'是否订购@刘一届 @测试 @zxldev');

print_r($text);//是否订购<a href="javascript:;">@刘一届</a> <a href="javascript:;">@测试</a> <a href="javascript:;">@zxldev</a>
```
###[ mysql left join 右表数据不唯一的情况解决方法](http://blog.csdn.net/fdipzone/article/details/45119551)
```php
如果B表符合条件的记录数大于1条，就会出现1:n的情况，这样left join后的结果，记录数会多于A表的记录数。
member 表
id	username
1	fdipzone
2	terry
 
member_login_log 表
id	uid	logindate
1	1	2015-01-01
2	2	2015-01-01
3	1	2015-01-02
4	2	2015-01-02
5	2	2015-01-03
 
查询member用户的资料及最后登入日期
select a.id, a.username, b.logindate  
from member as a   
left join member_login_log as b on a.id = b.uid; 
id	username	logindate
1	fdipzone	2015-01-01
1	fdipzone	2015-01-02
2	terry	2015-01-01
2	terry	2015-01-02
2	terry	2015-01-03
select a.id, a.username, b.logindate  
from member as a   
left join (select uid, max(logindate) as logindate from member_login_log group by uid) as b  
on a.id = b.uid;
id	username	logindate
1	fdipzone	2015-01-02
2	terry	2015-01-03
```
###[内存溢出](https://segmentfault.com/q/1010000007997441)
```php
register_shutdown_function方法观察并捕获程序最后的状态http://www.bo56.com/%E4%B8%80%E6%AC%A1php%E8%BF%9B%E7%A8%8B%E8%AF%A1%E5%BC%82%E9%80%80%E5%87%BA%E7%9A%84%E6%8E%92%E6%9F%A5%E8%BF%87%E7%A8%8B/ 
使用cli模式，如果有curl，没设置超时时间，就会一直存在于内存，如果多的话，就会内存溢出，服务器崩溃。
sdk里面加上curl_setopt($connection, CURLOPT_TIMEOUT, 30)，就不会有一直存在的php进程
```
###[Python解析PDF](https://github.com/euske/pdfminer/)
```php
git clone https://github.com/euske/pdfminer
$ python setup.py install
If you are using python 3 you will need to pip install pdfminer.six
 http://gohom.win/2015/12/18/pdfminer/

$ pdf2txt.py samples/simple1.pdf
#http://stackoverflow.com/questions/5725278/how-do-i-use-pdfminer-as-a-library
from bs4 import BeautifulSoup
import requests
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO  import StringIO
from io import open
from pdfminer.pdfpage import PDFPage
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
     fp = file(path, 'rb')
    #fp = requests.get("http://pythonscraping.com/pages/warandpeace/chapter1.pdf").content
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
print convert_pdf_to_txt('pdfminer-master/samples/simple1.pdf') 

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO  import StringIO
from io import open
from pdfminer.pdfpage import PDFPage
def pdf_txt(url):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    f = requests.get(url).content
    fp = StringIO(f)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp,
                                  pagenos,
                                  maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
print pdf_txt('http://pythonscraping.com/pages/warandpeace/chapter1.pdf')


```
