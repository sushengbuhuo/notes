###[Image()对象实例化获取图片宽高](https://segmentfault.com/q/1010000008138930)
```php
imgitem.forEach(function(item){
    var img = new Image();
    img.src = item.url;
    img.onload = function(){
        var w = img.width, 
            h = img.height;

        console.log(item, img, w, h);

        if(h/w >= 1.5){
                //...
        }
    }
});
```
###[js递归遍历](https://segmentfault.com/q/1010000008139179)
```php
var tree = {
    name: 'root',
    children: [{
        name: 'child1',
        children: [{
            name: 'child1_1',
            children: [{
                name: 'child1_1_1'
            }]
        }]
    }, {
        name: 'child2',
        children: [{
            name: 'child2_1'
        }]
    }, {
        name: 'child3'
    }]
};
function traverseTree(node){
  var child = node.children,
      arr = [];

  arr.push({ name: node.name });
  if(child){
    child.forEach(function(node){
      arr = arr.concat(traverseTree(node));
    });
  }
  return arr;
}
JSON.stringify(traverseTree(tree))
"[{"name":"root"},{"name":"child1"},{"name":"child1_1"},{"name":"child1_1_1"},{"name":"child2"},{"name":"child2_1"},{"name":"child3"}]"
```
###[js字典排序](https://segmentfault.com/q/1010000008141620)
```php
var myObject = {
    code: 'jonyqin_1434008071',
    timestamp: '1404896688',
    card_id: 'pjZ8Yt1XGILfi-FUsewpnnolGgZk',
    api_ticket: 'ojZ8YtyVyr30HheH3CM73y7h4jJE',
    nonce_str: 'jonyqin'
}

var arr=[];

for(var a in myObject){
    arr.push(myObject[a])
}
arr.sort();
console.log(arr);
```
###[配置机器之间免密码登录](https://segmentfault.com/q/1010000008143786)
```php
先在登录机上安装一个sshpass软件，然后执行脚本
cd /etc/yum.repos.d/ 
wget http://download.opensuse.org/repositories/home:Strahlex/CentOS_CentOS-6/home:Strahlex.repo
yum install sshpass
#!/bin/bash
#设置SSHPASS环境变量
export SSHPASS='对端密码'
#ip.txt中每行为一台机器的IP地址
for IP in `cat ip.txt`
do
    sshpass -e ssh-copy-id -o StrictHostKeyChecking=no $IP
done
```
###[分别是取变量的 个位、十位、百位、千位](https://www.v2ex.com/t/47288)
```php
Math.floor(1234 % 10) 个
Math.floor(1234 / 10 %10) 十
Math.floor(1234 / 100 %10) 百
Math.floor(1234 / 1000 % 10) 千 
str_split(""+228)
```
###[处理未定义变量](https://www.v2ex.com/t/196697)
```php
$params = array_merge(['id' => ''], $_GET);

if ($params['id']) 
$_GET += [
'id' => 0,
'page' => 1,
]; array_get($arr, 'foo.bar') 
	function array_get($array, $key, $default = null)
	{
		return Arr::get($array, $key, $default);
	}
```
###[浮点数计算比较](http://www.5idev.com/p-php_float_bcadd_ceil_floor.shtml)
```php
$a = 0.2+0.7;
$b = 0.9;
var_dump($a == $b);
printf("%0.20f", $a);0.89999999999999991118
printf("%0.20f", $b);0.90000000000000002220
var_dump(bcadd(0.2,0.7,1) == 0.9);	// 输出：bool(true) 
echo ceil( round((2.1/0.7),1) );
$a = 0.1;
$b = 0.9;
$c = 1;

printf("%.20f", $a+$b); // 1.00000000000000000000
printf("%.20f", $c-$b); // 0.09999999999999997780
$f = 0.07;
var_dump($f * 100 == 7);//输出false
$f = 0.07;
//输出7.00000000000000088818
echo number_format($f * 100, 20);
$f = 0.07;
var_dump($f * 100 == 7);
//输出0，表示两个数字精度为小数点后3位的时候相等
var_dump(bccomp($f * 100, 7, 3));
```
###[foreach循环后,无法用while+list+each循环输出](https://segmentfault.com/q/1010000008146643)
```php
$prices = array('Tom' => 100, 'len' => 20, 'youuu' => 38);
foreach ($prices as $key => $value) {
    echo "$key - $value <br/> ";
}
while (list($name, $price) = each($prices)) {
    echo "$name - $price <br/>";
} 
使用过一次while (list($name, $price) = each($prices))之后，因为使用了each函数会将数组内部的指针移动到最后，再次遍历的时候没有重置指针位置，就会出现不管怎么遍历都没有结果。

而使用foreach则会在每次遍历的时候自动设置指针到数组顶部，因此可以遍历出结果。

题主可以在使用while (list($name, $price) = each($prices))遍历一次之后，使用reset函数重置数组指针之后就可以了

reset($prices);
while (list($name, $price) = each($prices)) {
    echo "$name - $price \n";
}

```
###[不重启mysql情况修改参数变量](http://www.hdj.me/evil-replication-management)
```php
mysql> show variables like 'log_slave_updates';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| log_slave_updates | OFF   |
+-------------------+-------+
1 row in set (0.00 sec)
 
mysql> set global log_slave_updates=1;
ERROR 1238 (HY000): Variable 'log_slave_updates' is a read only variable
mysql> system gdb -p $(pidof mysqld) -ex "set opt_log_slave_updates=1" -batch
mysql> show variables like 'log_slave_updates';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| log_slave_updates | ON    |
+-------------------+-------+
1 row in set (0.00 sec)
mysql> show slave status \G
...
     Replicate_Do_DB: test
...
mysql> system gdb -p $(pidof mysqld)
          -ex 'call rpl_filter->add_do_db(strdup("hehehe"))' -batch
mysql> show slave status \G
```
###[查找表中的主键](http://www.hdj.me/category/mysql/page/2)
```php
查看你的数库有多大
SELECT
  table_schema AS 'Db Name',
  Round( Sum( data_length + index_length ) / 1024 / 1024, 3 ) AS 'Db Size (MB)',
  Round( Sum( data_free ) / 1024 / 1024, 3 ) AS 'Free Space (MB)'
FROM information_schema.tables
GROUP BY table_schema ;
SELECT k.column_name
FROM information_schema.table_constraints t
JOIN information_schema.key_column_usage k
USING (constraint_name,table_schema,table_name)
WHERE t.constraint_type='PRIMARY KEY'
  AND t.table_schema='db'
  AND t.table_name=tbl'

```
###[MySql中如何用LIKE来查找带反斜线“\”的记录](http://www.hdj.me/mysql-like-with-backlash)
```php
$sql = ‘SELECT * FROM table WHERE col LIKE \’%a\\%\’ ‘;
SELECT * FROM table WHERE col LIKE ‘%a\\%’;
    $sql = “SELECT * FROM table WHERE col LIKE ‘%a\\\\%’ “;

这样实际上经过转义发给 MySQL 的是

    SELECT * FROM table WHERE col LIKE ‘%a\\%’;
```
###[重置MySQL密码](http://www.hdj.me/how-to-reset-the-root-password)
```php
mysqld_safe --skip-grant-tables --skip-networking &
/etc/init.d/mysqld restart
把用到的SQL语句保存到一个文本文件里（/path/to/init/file）
UPDATE `mysql`.`user` SET `Password`=PASSWORD('yourpassword') WHERE `User`='root' AND `Host`= '127.0.0.1';
FLUSH PRIVILEGES;
shell> /etc/init.d/mysql stop
shell> mysqld_safe --init-file=/path/to/init/file &
```
###[COUNT(DISTINCT `field`)](http://www.hdj.me/mysql-count-distinct-duplicate-entry)
```php
SELECT COUNT(*) FROM (SELECT `field` FROM `table` GROUP BY `field`) a LIMIT 1;
```
###[ucs-2实体编码反转](http://www.hdj.me/php-ucs-2-decode)
```php
echo iconv('ucs-2','utf-8',pack('n','40670'));
echo mb_convert_encoding('&#40670;','utf-8','HTML-ENTITIES');
```
###[若非去空格，请慎用trim](http://www.hdj.me/php-trim-charlist-usage)
```php
trim('www.example.com.tw', 'www.')    期望的结果是example.com.tw，可实际的结果却是example.com.t，tw中的w没了。

问题出现在第二个参数$charlist，它代表的是一个字符列表，而不是一个单纯的字符串，所以tw的w属于www.这个列表中的一员，被一起去掉了
$domain = preg_replace(‘/^www\.|www\.$/’, ”, ‘www.example.com.tw’);
```
###[基于crc32的短网址算法](http://www.hdj.me/php-crc32-shorturl)
```php
function khash($data){
    $map        = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    $hash       = bcadd(sprintf('%u',crc32($data)) , 0x100000000);
    $str        = "";
    do {
        $str    = $map[bcmod($hash, 62)] . $str;
        $hash   = bcdiv($hash, 62);
    } while ($hash >= 1);
    return $str;
}
10000个循环内未出现碰撞；
100000个循环仅出现1个碰撞；
$sids       = array();
$repeats    = array();
$result     = array();
for($i=1; $i<=100000; $i++){
    $url    = "http://www.hdj.me/?id=".md5($i);
    $sid    = shorurl($url);
    // echo $sid."\n";
    if(in_array($sid, $sids)){
        $repeats[]  = $sid;
    }
    $sids[]         = $sid;
    $result[$sid][] = $url;
}
foreach((array)$repeats as $sid){
    var_dump($result[$sid]);
}
```
###[微信红包算法](http://www.hdj.me/bonus-algorithm-of-wechat)
```php
// $bonus_total 红包总金额
// $bonus_count 红包个数
// $bonus_type 红包类型 1=拼手气红包 0=普通红包
function randBonus($bonus_total=0, $bonus_count=3, $bonus_type=1){
    $bonus_items    = array(); // 将要瓜分的结果
    $bonus_balance  = $bonus_total; // 每次分完之后的余额
    $bonus_avg      = number_format($bonus_total/$bonus_count, 2); // 平均每个红包多少钱
 
    $i              = 0;
    while($i<$bonus_count){
        if($i<$bonus_count-1){
            $rand           = $bonus_type?(rand(1, $bonus_balance*100-1)/100):$bonus_avg; // 根据红包类型计算当前红包的金额
            $bonus_items[]  = $rand;
            $bonus_balance  -= $rand;
        }else{
            $bonus_items[]  = $bonus_balance; // 最后一个红包直接承包最后所有的金额，保证发出的总金额正确
        }
        $i++;
    }
    return $bonus_items;
}
// 发3个拼手气红包，总金额是100元
$bonus_items    = randBonus(100, 3, 1);
// 查看生成的红包
var_dump($bonus_items);
// 校验总金额是不是正确，看看微信有没有坑我们的钱
var_dump(array_sum($bonus_items));
function sendRandBonus($total=0, $count=3, $type=1){
    if($type==1){
        $input          = range(0.01, $total, 0.01);
        if($count>1){
            $rand_keys  = (array) array_rand($input,  $count-1);
            $last       = 0;
            foreach($rand_keys as $i=>$key){
                $current    = $input[$key]-$last;
                $items[]    = $current;
                $last       = $input[$key];
            }
        }
        $items[]        = $total-array_sum($items);
    }else{
        $avg            = number_format($total/$count, 2);
        $i              = 0;
        while($i<$count){
            $items[]    = $i<$count-1?$avg:($total-array_sum($items));
            $i++;
        }
    }
    return $items;
}
```
###[自定义apk安装包](http://www.hdj.me/custom-apk-by-php-ziparchive)
```php
// 源文件
$apk    = "gb.apk";
// 生成临时文件
$file   = tempnam("tmp", "zip");
// 复制文件
if(false===file_put_contents($file, file_get_contents($apk))){
    exit('copy faild!');
}
// 打开临时文件
$zip    = new ZipArchive();
$zip->open($file); 
// 添加文件
// 由于apk限定只能修改此目录内的文件，否则会报无效apk包
$zip->addFromString('META-INF/extends.json', json_encode(array('author'=>'deeka')));
// 关闭zip
$zip->close();
// 下载文件
header("Content-Type: application/zip"); 
header("Content-Length: " . filesize($file)); 
header("Content-Disposition: attachment; filename=\"{$apk}\""); 
// 输出二进制流
readfile($file);
// 删除临时文件
unlink($file); 
```
###[php对象数组转型的BUG](http://www.hdj.me/a-php-object-to-array-bug)
```php
$o = new stdClass();
$o->{'123'} = 1;
$a = (array) $o;
var_dump($a);
var_dump(isset($a['123']));
var_dump(isset($a[123]));
 
$a = array(1,2,3);
$o = (object) $a;
var_dump($o);
var_dump(isset($o->{1}));
var_dump(isset($o->{'1'}));
class Test {
    private $a = 1;
    protected $b = 2;
    public $c = 3;
}
$o = new Test();
$a = (array) $o;
var_dump($a);
var_dump($a["\0Test\0a"]);
var_dump($a["\0*\0b"]);
```
###[php/js获取客户端mac地址](http://www.hdj.me/php-js-get-client-mac-addr)
```php
class MacAddr
{  
    public $returnArray = array();   
    public $macAddr;  
 
    function __contruct($os_type=null){
        if(is_null($os_type)) $os_type = PHP_OS;  
        switch (strtolower($os_type)){  
        case "linux":  
            $this->forLinux();  
            break;  
        case "solaris":  
            break;  
        case "unix":  
            break;  
        case "aix":  
            break;  
        default:  
            $this->forWindows();  
            break;  
        }  
        $temp_array = array();  
        foreach($this->returnArray as $value ){  
            if(preg_match("/[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f][:-]"."[0-9a-f][0-9a-f]/i", $value, $temp_array)){  
                $this->macAddr = $temp_array[0];  
                break;  
            }  
        }  
        unset($temp_array);  
        return $this->macAddr;  
    }
 
    function forWindows(){  
        @exec("ipconfig /all", $this->returnArray);  
        if($this->returnArray)  
            return $this->returnArray;  
        else{  
            $ipconfig = $_SERVER["WINDIR"]."system32ipconfig.exe";  
            if (is_file($ipconfig))  
                @exec($ipconfig." /all", $this->returnArray);  
            else 
                @exec($_SERVER["WINDIR"]."systemipconfig.exe /all", $this->returnArray);  
            return $this->returnArray;  
        }  
    }
 
    function forLinux(){  
        @exec("ifconfig -a", $this->returnArray);  
        return $this->returnArray;  
    }  
}  
 
$mac = new MacAddr(PHP_OS);  
echo $mac->macAddr;  
echo "<br />";
 
// 获取客户端
// linux
$command = "arp -a {$_SERVER['REMOTE_ADDR']}";
echo $command;
echo "<br />";
$result=`{$command}`; 
 
// windows
$command = "nbtstat -a {$_SERVER['REMOTE_ADDR']}";
echo $command;
echo "<br />";
$result=`{$command}`; 
print_r($result);  
```
###[print不是一个函数](http://www.hdj.me/language-construct-of-php)
```php
// 初始化一个字符串变量
$func = 'foo';
 
// 找到名字和这个字符串一样的函数，并且执行它
$func();
$func = 'print';
 
// 这样做会产生异常，因为print不是一个函数，而是语言的构成部分
$func('hello world');

```
###[PHP程序里的敏感信息](http://www.hdj.me/hidden-php-configs)
```php
nginx 
fastcgi_param DATABASE_HOST 192.168.0.1;
fastcgi_param DATABASE_USER administrator;
fastcgi_param DATABASE_PASSWORD e1bfd762321e409cee4ac0b6e84
return array(
    'database' => array(
        'host'     => $_SERVER['DATABASE_HOST'],
        'user'     => $_SERVER['DATABASE_USERNAME'],
        'password' => $_SERVER['DATABASE_PASSWORD'],
    ),
);
通过php-fpm的env指令来设置：

env[DATABASE_HOST] = 192.168.0.1
env[DATABASE_USERNAME] = administrator
env[DATABASE_PASSWORD] = e1bfd762321e409cee4ac0b6e841963c
```
###[php在CLI模式下传入值的几种方法](http://www.hdj.me/php-cli-getoptions)
```php
$opt= getopt('m:n:');
// $value_m= $opt&#91;'m'&#93;;
// $value_n= $opt&#91;'n'&#93;;
print_r($opt);
php test.php -mvaluem -n value n

```
###[内网机器的获取公网IP](http://www.hdj.me/intranet-computer-get-internet-ip-by-php)
```php
function getClientIp(){  
    $socket = socket_create(AF_INET, SOCK_STREAM, 6);  
    $ret = socket_connect($socket,'ns1.dnspod.net',6666);  
    $buf = socket_read($socket, 16);  
    socket_close($socket);  
    return $buf;      
} 
```
###[微博开发之@替换](http://www.hdj.me/weiboapi-dev-replace-at)
```php
$users['pony']      = '马化腾';
$users['ponyma']    = '坡泥马';
$users['ponyli']    = '坡泥李';
$text = "@pony:特别声明,@ponyli@ponyma@ponywong@ponylao什么的都不是我";
preg_match_all('/@\w+/', $text, $matches);
if(is_array($matches[0]) && !empty($matches[0])){
    $replaces       = array_combine($matches[0], $matches[0]);
}
foreach($users as $userid=>$username){
    $replaces['@'.$userid]  = "<a href='http://t.qq.com/{$userid}'>{$username}</a>";
}
$html               = strtr($text, $replaces);
echo $html;
<a href=’http://t.qq.com/pony’>马化腾</a>:特别声明,<a href=’http://t.qq.com/ponyli’>坡泥李</a><a href=’http://t.qq.com/ponyma’>坡泥马</a>@ponywong@ponylao什么的都不是我 
```
###[preg_match正则匹配的字符串长度问题](http://www.hdj.me/strlen-of-preg-match)
“pcre.backtrack_limit ”的值默认只设了100000。
解决办法：ini_set(‘pcre.backtrack_limit’, 999999999);
###[代码压缩](http://www.hdj.me/when-php-strip-whitespace-meet-heredoc)
`php_strip_whitespace压缩`
###[匹配图片地址](http://www.hdj.me/php-regular-match-image-src)
$p = "/src=\"([^\"]+)/isu";
//$p = "/<&#91;^>]+>/isu";
//$p = "/<a&#91;^>]+>/isu";
preg_match_all($p, $html, $m);
var_dump($m);
###[PHP断点续传下载](http://www.hdj.me/php-reget-download-support)
```php
$fname = './MMLDZG.mp3';
$fp = fopen($fname,'rb');
$fsize = filesize($fname);
if (isset($_SERVER['HTTP_RANGE']) && ($_SERVER['HTTP_RANGE'] != "") && preg_match("/^bytes=([0-9]+)-$/i", $_SERVER['HTTP_RANGE'], $match) && ($match[1] < $fsize)) {     $start = $match&#91;1&#93;; } else {     $start = 0; } @header("Cache-control: public"); @header("Pragma: public"); if ($star--> 0) {
    fseek($fp, $start);
    Header("HTTP/1.1 206 Partial Content");
    Header("Content-Length: " . ($fsize - $start));
    Header("Content-Ranges: bytes" . $start . "-" . ($fsize - 1) . "/" . $fsize);
} else {
    header("Content-Length: $fsize");
    Header("Accept-Ranges: bytes");
}
@header("Content-Type: application/octet-stream");
@header("Content-Disposition: attachment;filename=mmdld.mp3");
fpassthru($fp);
fpassthru();//函数输出文件指针处的所有剩余数据。http://www.hdj.me/omb-download-in-php-code
```
###[CURL不依赖COOKIEJAR获取COOKIE](http://www.hdj.me/get-cookie-without-cookiejar-by-curl)
```php
// 初始化CURL
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
// 获取头部信息
curl_setopt($ch, CURLOPT_HEADER, 1);
// 返回原生的（Raw）输出
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
// 执行并获取返回结果
$content = curl_exec($ch);
// 关闭CURL
curl_close($ch);
// 解析HTTP数据流
list($header, $body) = explode("\r\n\r\n", $content);
// 解析COOKIE
preg_match("/set\-cookie:([^\r\n]*)/i", $header, $matches);
// 后面用CURL提交的时候可以直接使用
// curl_setopt($ch, CURLOPT_COOKIE, $cookie);
$cookie = $matches[1];
```
###[汉诺塔算法](http://www.hdj.me/some-php-algorithm)
```php
function hanoi($n,$x,$y,$z){
    if($n==1){
        echo 'move disk 1 from '.$x.' to '.$z."\n";
    }else{
        hanoi($n-1,$x,$z,$y);
        echo 'move disk '.$n.' from '.$x.' to '.$z."\n";
        hanoi($n-1,$y,$x,$z);
    }     
}
hanoi(3,'A','B','C');
```
###[过滤emoji](https://segmentfault.com/q/1010000007329875)
```php
var param = "";
var regRule = /\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]/g;
if(param.match(regRule)) {
    param = param.replace(/\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDE4F]/g, "");
    alert("不支持表情");
} 
```
###[MySQL关联比较](https://segmentfault.com/q/1010000008146270)
```php
姓名 分数
小红 97
小白 86
小黑 44

另外有一张rank表
low up rank
90 100 A 
80 90 B
70 80 C
60 70 D
0 60 E
 
我最后想得出结果为
姓名 分数 rank 
小红 97 A
小白 86 B
小黑 44 E
SELECT grade.name,grade.score,rank.rank from grade JOIN rank ON grade.score > rank.low and grade.score < rank.up
```
###一次匹配
```php
function str_replace_once($needle, $replace, $haystack)
    {
        $pos = strpos($haystack, $needle);
        if ($pos === false) {
            return $haystack;
        }
        return substr_replace($haystack, $replace, $pos, strlen($needle));
    }
```
###[微博短链接算法php版本](http://www.hdj.me/php-shorturl-function)
```php
function shorturl($url='', $prefix='', $suffix='') {
    $base = array(
            "a","b","c","d","e","f","g","h",
            "i","j","k","l","m","n","o","p",
            "q","r","s","t","u","v","w","x",
            "y","z","0","1","2","3","4","5",
            "6","7","8","9","A","B","C","D",
            "E","F","G","H","I","J","K","L",
            "M","N","O","P","Q","R","S","T",
            "U","V","W","X","Y","Z");
  
    $hex = md5($prefix.$url.$suffix);
    $hexLen = strlen($hex);
    $subHexLen = $hexLen / 8;
    $output = array();
  
    for ($i = 0; $i < $subHexLen; $i++) {
        $subHex = substr ($hex, $i * 8, 8);
        $int = 0x3FFFFFFF & (1 * ('0x'.$subHex));
        $out = '';
        for ($j = 0; $j < 6; $j++) {
            $val = 0x0000003D & $int;
            $out .= $base&#91;$val&#93;;
            $int = $int >> 5;
        }
        $output[] = $out;
    }
    return $output;
}
```
###[mysql表删除重复记录方法总结及效率对比](http://www.hdj.me/mysql-remove-repeat-records)
```php
CREATE TABLE `test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(20) DEFAULT NULL COMMENT '姓名',
  `age` tinyint(4) DEFAULT NULL COMMENT '年龄',
  `mate` tinyint(4) DEFAULT '1' COMMENT '有无配偶(1-有 0-无)',
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`),
  KEY `idx_age` (`age`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
insert  into `test`(`id`,`name`,`age`,`mate`) values (2,'aaaaa',28,0),
(3,'bbbb',23,0),
(4,'cccc',25,1),
(5,'dddd',26,0),
(6,'eeee',24,0),
(7,'fffff',18,0),
(8,'eeee',40,1),
(9,'eeee',60,1);
alter ignore table test add unique idx_name (name); 去掉name重名的记录

DELETE  a  FROM test AS a,
(
SELECT * 
FROM  test
GROUP BY name 
HAVING count(1) >1
order by null
) AS b
WHERE a.name = b.name AND a.id > b.id;

```
###[监控MySQL你还应该收集表信息](http://seanlook.com/2016/12/04/mysql-schema-gather-statistics/)
```js
SELECT
    IFNULL(@@hostname, @@server_id) SERVER_NAME,
    %s as HOST,
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    t.TABLE_ROWS,
    t.DATA_LENGTH,
    t.INDEX_LENGTH,
    t.AUTO_INCREMENT,
  c.COLUMN_NAME,
  c.DATA_TYPE,
  LOCATE('unsigned', c.COLUMN_TYPE) COL_UNSIGNED
  # CONCAT(c.DATA_TYPE, IF(LOCATE('unsigned', c.COLUMN_TYPE)=0, '', '_unsigned'))
FROM
    information_schema.`TABLES` t
LEFT JOIN information_schema.`COLUMNS` c ON t.TABLE_SCHEMA = c.TABLE_SCHEMA
AND t.TABLE_NAME = c.TABLE_NAME
AND c.EXTRA = 'auto_increment'
WHERE
    t.TABLE_SCHEMA NOT IN (
        'mysql',
        'information_schema',
        'performance_schema',
        'sys'
    )
AND t.TABLE_TYPE = 'BASE TABLE'
sudo pip install mysql-python influxdb

 
CREATE DATABASE "mysql_info"
CREATE RETENTION POLICY "mysql_info_schema" ON "mysql_info" DURATION 730d REPLICATION 1 DEFAULT
40 23,5,12,18 * * * /opt/DBschema_info/mysql_schema_info.py >> /tmp/collect_DBschema_info.log 2>&1
利用 mydumper 导出表时会把各表（结构）单独导成一个文件的特性

```
###[实时抓取MySQL慢查询现场的程序](http://seanlook.com/2016/09/27/python-mysql-querykill/)
```php
https://github.com/seanlook/myquerykill
```
###[utf8 与 utf8mb4 异同](http://seanlook.com/2016/10/23/mysql-utf8mb4/)
```php
ALTER TABLE tbl_name CONVERT TO CHARACTER SET utf8mb4;
连接的时候需要使用set names utf8mb4便可以插入四字节字符。（如果依然使用 utf8 连接，只要不出现四字节字符则完全没问题）。
修改服务端 character-set-server=utf8mb4
CREATE TABLE t1 (
  f_id varchar(20) NOT NULL,
  f_action char(25) NOT NULL DEFAULT '' COMMENT '',
  PRIMARY KEY (`f_id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
CREATE TABLE t1_copy_mb4 (
  f_id varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  f_action char(25) NOT NULL DEFAULT '' COMMENT '',
  PRIMARY KEY (`f_id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
1.
EXPLAIN extended select * from t1 INNER JOIN t1_copy_mb4 t2 on t1.f_id=t2.f_id where t1.f_id='421036';
2.
EXPLAIN extended select * from t1 INNER JOIN t1_copy_mb4 t2 on t1.f_id=t2.f_id where t2.f_id='421036';

索引失效发生在utf8mb4列 在条件左边
mysql> show warnings;
+---------+------+-------------------------------------------------------+
| Level   | Code | Message                                               |
+---------+------+-------------------------------------------------------+
| Warning | 1366 | Incorrect integer value: 'f' for column 'pv' at row 1 |
+---------+------+-------------------------------------------------------+
1 row in set (0.00 sec)
```
###[MySQL避免索引列使用 OR 条件](http://seanlook.com/2016/04/05/mysql-avoid-or-query/)
```php
select f_crm_id from d_dbname1.t_tbname1 where  f_xxx_id = 926067  
and (f_mobile ='1234567891' or f_phone ='1234567891' ) limit 1
mysql的每条查询，每个表上只能选择一个索引。如果使用了 idx_id_mobile 索引，恰好有一条数据，因为有 limit 1 ，那么恭喜很快得到结果；但如果 f_mobile 没有数据，那 f_phone 字段只能在f_id条件下挨个查找，扫描12w行
(select f_crm_id from d_dbname1.t_tbname1 where  f_xxx_id = 900000  and f_mobile ='1234567891' limit 1 )
UNION ALL 
(select f_crm_id from d_dbname1.t_tbname1 where  f_xxx_id = 900000  and f_phone ='1234567891' limit 1 )

sql1 = (select a.f_crm_id from d_dbname1.t_tbname1 as a where a.f_create_time > from_unixtime('1464397527') limit 0,200 );
sql1.execute();
sql1_count = sql1.result.count
if sql1_count < 200 :
  sql2 = (select a.f_crm_id from d_dbname1.t_tbname1 as a where a.f_modify_time > from_unixtime('1464397527') and a.f_create_time <= from_unixtime('1464397527') limit 0, (200 - sql1_count) );
  sql2.execute();
final_result = paste(sql1,sql2);
```
###[MySQL的隐式类型转换陷阱](http://seanlook.com/2016/05/05/mysql-type-conversion/)
```php
SELECT f_col3_id,f_qq1_id FROM d_dbname.t_tb1 WHERE f_col1_id=1226391 and f_col2_id=1244378 and 
f_qq1_id in (12345,23456,34567,45678,56789,67890,78901,89012,90123,901231,901232,901233)

mysql>explain extended SELECT f_col3_id,f_qq1_id FROM d_dbname.t_tb1  use index(idx_corpid_qq1id) WHERE f_col1_id=1226391 and f_col2_id=1244378 and f_qq1_id in (12345,23456,34567,45678,56789,67890,78901,89012,90123,901231,901232,901233);
+------+---------------+--------+--------+---------------------+------------------+------------+----------+-------------+------------------------------------+
| id   | select_type   | table  | type   | possible_keys       | key              | key_len    | ref      | rows        | Extra                              |
+------+---------------+--------+--------+---------------------+------------------+------------+----------+-------------+------------------------------------+
| 1    | SIMPLE        | t_tb1  | ref    | idx_corpid_qq1id    | idx_corpid_qq1id | 8          | const    | 2375752     | Using index condition; Using where |
+---- -+---------------+--------+--------+---------------------+------------------+------------+----------+-------------+------------------------------------+
共返回 1 行记录,花费 17.48 ms.
mysql>show warnings;
+-----------------+----------------+-----------------------------------------------------------------------------------------------------------------------+
| Level           | Code           | Message                                                                                                               |
+-----------------+----------------+-----------------------------------------------------------------------------------------------------------------------+
| Warning         |           1739 | Cannot use range access on index 'idx_corpid_qq1id' due to type or collation conversion on field 'f_qq1_id'           |
| Note            |           1003 | /* select#1 */ select `d_dbname`.`t_tb1`.`f_col3_id` AS `f_col3_id`,`d_dbname`.`t_tb1`.`f_qq1_id` AS `f_qq1_id` from `d_dbname`.`t_tb1` USE INDEX (`idx_corpid_qq1id`) where |
|                 |                |  ((`d_dbname`.`t_tb1`.`f_col2_id` = 1244378) and (`d_dbname`.`t_tb1`.`f_col1_id` = 1226391) and (`d_dbname`.`t_tb1`.`f_qq1_id` in |
|                 |                | (12345,23456,34567,45678,56789,67890,78901,89012,90123,901231,901232,901233)))                                        |
+-----------------+----------------+-----------------------------------------------------------------------------------------------------------------------+
共返回 2 行记录,花费 10.81 ms.
mysql> select 11 + '11', 11 + 'aa', 'a1' + 'bb', 11 + '0.01a';  
+-----------+-----------+-------------+--------------+
| 11 + '11' | 11 + 'aa' | 'a1' + 'bb' | 11 + '0.01a' |
+-----------+-----------+-------------+--------------+
|        22 |        11 |           0 |        11.01 |
+-----------+-----------+-------------+--------------+
1 row in set, 4 warnings (0.00 sec)
mysql> show warnings;
+---------+------+-------------------------------------------+
| Level   | Code | Message                                   |
+---------+------+-------------------------------------------+
| Warning | 1292 | Truncated incorrect DOUBLE value: 'aa'    |
| Warning | 1292 | Truncated incorrect DOUBLE value: 'a1'    |
| Warning | 1292 | Truncated incorrect DOUBLE value: 'bb'    |
| Warning | 1292 | Truncated incorrect DOUBLE value: '0.01a' |
+---------+------+-------------------------------------------+
4 rows in set (0.00 sec)
mysql> select '11a' = 11, '11.0' = 11, '11.0' = '11', NULL = 1;
+------------+-------------+---------------+----------+
| '11a' = 11 | '11.0' = 11 | '11.0' = '11' | NULL = 1 |
+------------+-------------+---------------+----------+
|          1 |           1 |             0 |     NULL |
+------------+-------------+---------------+----------+
1 row in set, 1 warning (0.01 sec)
'11a'和'11.0'转换后都等于 11，这也正是文章开头实例为什么没走索引的原因： varchar型的f_qq1_id，转换成浮点型比较时，等于 12345 的情况有无数种如12345a、12345.b等待，MySQL优化器无法确定索引是否更有效，所以选择了其它方案。
假如应用前端没有WAF防护，那么下面的sql很容易注入：
mysql> select * from t_account where fname='A' ;
fname传入  A' OR 1='1  
mysql> select * from t_account where fname='A' OR 1='1';
fname传入 A'+'B ，fpassword传入 ccc'+0 ：
mysql> select * from t_account where fname='A'+'B' and fpassword='ccc'+0;
+-----+-----------+-------------+
| fid | fname     | fpassword   |
+-----+-----------+-------------+
|   1 | xiaoming  | p_xiaoming  |
|   2 | xiaoming1 | p_xiaoming1 |
+-----+-----------+-------------+
2 rows in set, 7 warnings (0.00 sec)
```
###[常用linux alias](http://seanlook.com/2014/03/09/linux-bash/)
```php
alias wl='ll | wc -l'
alias l='ls -l'
alias lh='ls -lh'
alias grep='grep -i --color' #用颜色标识，更醒目；忽略大小写
alias vi=vim
alias c='clear'  # 快速清屏
alias p='pwd'
# 进入目录并列出文件，如 cdl ../conf.d/
cdl() { cd "$@" && pwd ; ls -alF; }
alias ..="cdl .."
alias ...="cd ../.."   # 快速进入上上层目录
alias .3="cd ../../.." 
alias cd..='cdl ..'
# alias cp="cp -iv"      # interactive, verbose
alias rm="rm -i"      # interactive
# alias mv="mv -iv"       # interactive, verbose
alias psg='\ps aux | grep -v grep | grep --color' # 查看进程信息
alias hg='history|grep'
alias netp='netstat -tulanp'  # 查看服务器端口连接信息
alias lvim="vim -c \"normal '0\""  # 编辑vim最近打开的文件
alias tf='tail -f '  # 快速查看文件末尾输出
# 自动在文件末尾加上 .bak-日期 来备份文件，如 bu nginx.conf
bak() { cp "$@" "$@.bak"-`date +%y%m%d`; echo "`date +%Y-%m-%d` backed up $PWD/$@"; }
# 级联创建目录并进入，如 mcd a/b/c
mcd() { mkdir -p $1 && cd $1 && pwd ; }
# 查看去掉#注释和空行的配置文件，如 nocomm /etc/squid/squid.conf
alias nocomm='grep -Ev '\''^(#|$)'\'''
# 快速根据进程号pid杀死进程，如 psid tomcat， 然后 kill9 两个tab键提示要kill的进程号
alias kill9='kill -9';
psid() {
  [[ ! -n ${1} ]] && return;   # bail if no argument
  pro="[${1:0:1}]${1:1}";      # process-name –> [p]rocess-name (makes grep better)
  ps axo pid,user,command | grep -v grep |grep -i --color ${pro};   # show matching processes
  pids="$(ps axo pid,user,command | grep -v grep | grep -i ${pro} | awk '{print $1}')";   # get pids
  complete -W "${pids}" kill9     # make a completion list for kk
}
# 解压所有归档文件工具
function extract {
 if [ -z "$1" ]; then
    # display usage if no parameters given
    echo "Usage: extract <path/file_name>.<zip|rar|bz2|gz|tar|tbz2|tgz|Z|7z|xz|ex|tar.bz2|tar.gz|tar.xz>"
 else
    if [ -f $1 ] ; then
        # NAME=${1%.*}
        # mkdir $NAME && cd $NAME
        case $1 in
          *.tar.bz2)   tar xvjf $1    ;;
          *.tar.gz)    tar xvzf $1    ;;
          *.tar.xz)    tar xvJf $1    ;;
          *.lzma)      unlzma $1      ;;
          *.bz2)       bunzip2 $1     ;;
          *.rar)       unrar x -ad $1 ;;
          *.gz)        gunzip $1      ;;
          *.tar)       tar xvf $1     ;;
          *.tbz2)      tar xvjf $1    ;;
          *.tgz)       tar xvzf $1    ;;
          *.zip)       unzip $1       ;;
          *.Z)         uncompress $1  ;;
          *.7z)        7z x $1        ;;
          *.xz)        unxz $1        ;;
          *.exe)       cabextract $1  ;;
          *)           echo "extract: '$1' - unknown archive method" ;;
        esac
    else
        echo "$1 - file does not exist"
    fi
fi
}
# 其它你自己的命令
alias nginxreload='sudo /usr/local/nginx/sbin/nginx -s reload'
要去掉别名，请用unalias aliasname，或者临时执行不用别名，执行原始命令\alias 。
```
###[仿豆丁网文件在线浏览word,pdf解决方案搭建 ](http://seanlook.com/2015/05/13/pdf2swf-preview/)
```php
# tar -zxf Apache_OpenOffice_4.0.1_Linux_x86-64_install-rpm_zh-CN.tar.gz
# cd zh-CN/RPMS
# rpm –ivh *.rpm
$ /opt/openoffice4/program/soffice -headless -accept="socket,host=127.0.0.1,port=8100;urp;" -nofirststartwizard &
	

java -jar /opt/jodconverter-2.2.2/lib/jodconverter-cli-2.2.2.jar /home/oa/docker.docx /home/oa/docker.pdf
# yum install gcc* automake zlib-devel libjpeg-devel giflib-devel freetype-devel
# tar vxzf swftools-0.9.1.tar.gz
# cd swftools-0.9.1
# ./configure --prefix=/usr/local/swftools
# make && make install
	

/usr/local/bin/pdf2swf -t docker4.pdf -o docker4.swf -T 9 -f -z
# vi /usr/local/xpdf-chinese-simplified/add-to-xpdfrc
```

###后台用户权限
```php

用户表 users: id name
角色表 roles: id role_name
用户角色表 user_roles: user_id role_id
角色权限表 permissions : menu_id role_id
权限菜单表 admin_menus : id menu_name url parent_id 
$router->group(
    ['middleware' => ['auth', 'menu'], 'prefix' => 'admin', 'namespace' => 'Admin'],
    function () use ($router) {
        $router->controller('user', 'UserController');
});
class MenuMiddleware {
public function handle($request, Closure $next)
	{   
        $user_id = Auth::id();
        //判断是否有后台权限
        $user_pro = UserRelationRole::where("user_id","=",$user_id)->first();
        if(!empty($user_pro)){
            $user_pro = $user_pro->toArray();
        }else{
            $user_pro = [];
        }
        if(empty($user_pro)){
            return redirect('/');
        }
        $url = Route::current()->uri();
        
	    $menu = $this->getMenuPermission();dump($url,$user_pro,$menu);die();
        $menu_str = implode(",",$menu);
        if($url != 'admin'){
            //验证
            $url_arr = explode("/",$url);
            if(count($url_arr)==2){
                if(strpos($menu_str,$url)===false){
                    return response("没有权限1",403);
                }
            }else if(count($url_arr)>2){
                $arr[] = $url_arr[0];
                $arr[] = $url_arr[1];
                $arr_str = implode("/",$arr);
                if(strpos($menu_str,$arr_str)===false){
                    return response("没有权限2",403);
                }
            }
        }
		return $next($request);
	}
	}
mysql> select *from user_relation_roles where user_id=13\G
*************************** 1. row ***************************
        id: 3
   user_id: 13
   role_id: 3
created_at: 2015-05-20 00:16:38
updated_at: 2015-05-20 00:33:53
1 row in set (0.00 sec)

mysql> select *from roles where id=3\G
*************************** 1. row ***************************
        id: 3
 role_name: 研发部
created_at: 2015-05-14 23:22:02
updated_at: 2015-05-14 23:22:05
1 row in set (0.01 sec)
mysql> select *from permissions where role_id=3 and type='admin';
+------+---------+---------+-------+---------------------+---------------------+

| id   | menu_id | role_id | type  | created_at          | updated_at          |

+------+---------+---------+-------+---------------------+---------------------+

| 1135 |       1 |       3 | admin | 2015-06-27 21:41:38 | 2015-06-27 21:41:38 |

| 1136 |       3 |       3 | admin | 2015-06-27 21:41:38 | 2015-06-27 21:41:38 |

| 1137 |      16 |       3 | admin | 2015-06-27 21:41:38 | 2015-06-27 21:41:38 |

| 1138 |      57 |       3 | admin | 2015-06-27 21:41:38 | 2015-06-27 21:41:38 |
mysql> select *from admin_menus where id=3;
+----+----------+-----+-----------+---------------------+---------------------+
| id | name     | url | parent_id | created_at          | updated_at          |
+----+----------+-----+-----------+---------------------+---------------------+
|  3 | 用户管理 | 0   |         0 | 2015-05-15 18:13:30 | 2015-05-15 18:13:33 |
+----+----------+-----+-----------+---------------------+---------------------+
1 row in set (0.00 sec)


/**
     * 根据用户ID，返回菜单列表
     */
    public function getMenus($user_id = 0,$type = 'admin'){
        if(empty($user_id)){
            return false;
        }
        
            //先获取角色
            $role = UserRelationRole::where('user_id',$user_id)->first();
            if(empty($role)){
                return false;
            }
            $roles = Roles::find($role->role_id)->toArray();
            /*
            public function menu(){

        		return $this->belongsTo(AdminMenu::class,'menu_id');
    		}
             */
            //通过角色获取权限
        	$permissions = Permissions::with('menu')->whereRaw("`role_id` =".$role->role_id." and `type`='".$type."'")->get();
            $data[$type] = array();
            dump($permissions->toarray());
            /*
            array:114 [▼
			  0 => array:7 [▼
			    "id" => 4583
			    "menu_id" => 1
			    "role_id" => 1
			    "type" => "admin"
			    "created_at" => "-0001-11-30 00:00:00"
			    "updated_at" => "-0001-11-30 00:00:00"
			    "menu" => array:6 [▼
			      "id" => 1
			      "name" => "后台首页"
			      "url" => "0"
			      "parent_id" => 0
			      "created_at" => "2015-05-15 18:13:12"
			      "updated_at" => "2015-08-25 15:12:20"
			    ]
			  ]
			  1 => array:7 [▼
			    "id" => 4584
			    "menu_id" => 3
			    "role_id" => 1
			    "type" => "admin"
			    "created_at" => "-0001-11-30 00:00:00"
			    "updated_at" => "-0001-11-30 00:00:00"
			    "menu" => array:6 [▼
			      "id" => 3
			      "name" => "用户管理"
			      "url" => "0"
			      "parent_id" => 0
			      "created_at" => "2015-05-15 18:13:30"
			      "updated_at" => "2015-05-15 18:13:33"
			    ]
			  ]
			  2 => array:7 [▶]
             */
            $data['role'] = $roles;
            if(!empty($permissions)){
                foreach($permissions as $key=>$val){
                    $temp=$val->menu;

                    if(empty($temp)){
                        continue;
                    }
                    $temp = $temp->toArray();

                    if(!empty($temp['url']) && !empty($temp['parent_id'])){
                        $data[$type][$temp['parent_id']]['children'][$temp['id']] = $temp;
                    }else{
                        $data[$type][$temp['id']]['parent'] = $temp;
                    }
                }
            }
            /*
            array:2 [▼
		  "admin" => array:20 [▼
		    1 => array:2 [▼
		      "parent" => array:6 [▼
		        "id" => 1
		        "name" => "后台首页"
		        "url" => "0"
		        "parent_id" => 0
		        "created_at" => "2015-05-15 18:13:12"
		        "updated_at" => "2015-08-25 15:12:20"
		      ]
		      "children" => array:1 [▼
		        2 => array:6 [▼
		          "id" => 2
		          "name" => "默认首页"
		          "url" => "admin/index"
		          "parent_id" => 1
		          "created_at" => "2015-05-15 18:13:07"
		          "updated_at" => "2015-06-06 02:09:29"
		        ]
		      ]
		    ]
		    3 => array:2 [▶]
		    "role" => array:4 [▼
		    "id" => 1
		    "role_name" => "管理员"
		    "created_at" => "2015-05-14 23:20:06"
		    "updated_at" => "2015-05-22 01:26:38"
		  ]
             */
        return $data;
    }
    /**
     * 返回用后台权限地址
     * array:94 [▼
	*	  0 => "admin/index"
	*	  1 => "admin/user"
	*	  2 => "admin/user/vip"
	*	  3 => "admin/menu"
     */
    public function getMenuPermission(){
        $menu = $this->getMenus(\Auth::id());dump($menu);
        $menu_url = [];
        if(!empty($menu)){
            foreach($menu['admin'] as $key=>$values){
                if(!empty($values['children'])){
                    foreach($values['children'] as $val){
                        $menu_url[] = $val['url'];
                    }
                }
            }
        }
        return $menu_url;
    }

```
