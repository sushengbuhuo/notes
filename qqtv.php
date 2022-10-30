<?php
/*
    qq视频 m3u8解析
 https://www.52pojie.cn/thread-1699907-1-1.html
    首先你需要一个有vip权限的Cookies账号
    获取Cookies方法不多赘述
    $VIPCookies 为Cookie必填参数
    如果无法播放 仅需给m3u8文件进行保存 且补齐协议头即可
    */ 
 
    $VIPCookies = [
        '',
        '',
    ];// 必填VIP Cookies
    $getUrl = isset($_GET['url'])?$_GET['url']:'';
    $getUrl='https://v.qq.com/x/cover/aqp1qrk3w1atuki/c00315kl35t.html';
    if($getUrl == ''){
        $data = [
            'code'=>400,
            'msg'=>'NO Url?'
        ];
        echo json_encode($data);
    }else{
        preg_match("/https:\/\/v.qq.com\/x\/cover\/(.*?)\/(.*?).html/", $getUrl, $vid);
        $curl ='https://vv.video.qq.com/getinfo?encver=2&defn=shd&platform=10801&otype=ojson&sdtfrom=v4138&appVer=7&dtype=3&vid='.$vid[2].'&newnettype=1';
        $JsonInfo = vip_curl($curl,$VIPCookies[mt_rand(0,count($VIPCookies))]);
        $JsonData = json_decode($JsonInfo,true);
        $vurl = $JsonData["vl"]["vi"][0]['ul']['ui'][0]['url'].$JsonData["vl"]["vi"][0]['ul']['ui'][0]['hls']['pt'];
        $data = [
            'code'=>200,
            'msg'=>'OK',
            'url'=>$vurl,
            'm3u8_to'=>$JsonData["vl"]["vi"][0]['ul']['ui'][0]['url']
        ];echo $data['m3u8_to'];
        echo json_encode($data);
 
    }
    function getC($str, $leftStr, $rightStr)
    {
        $left = strpos($str, $leftStr);
        $right = strpos($str, $rightStr,$left);
        if($left < 0 or $right < $left) return '';
        return substr($str, $left + strlen($leftStr), $right-$left-strlen($leftStr));
    }
    function vip_curl($url,$cookie='')
    {
        $header = array (
            0 => 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            1 => 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7',
            2 => 'Cache-Control: max-age=0',
            3 => 'Connection: keep-alive',
            4 => 'Sec-Fetch-Dest: document',
            5 => 'Sec-Fetch-Mode: navigate',
            6 => 'Sec-Fetch-Site: none',
            7 => 'Sec-Fetch-User: ?1',
            8 => 'Upgrade-Insecure-Requests: 1',
            9 => 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            10 => 'sec-ch-ua: ^\\^',
            11 => 'sec-ch-ua-mobile: ?0',
            12 => 'sec-ch-ua-platform: ^\\^',
            13 =>'Cookie:'.$cookie
          );
        $timeout = 10;
        $ch  = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_ENCODING, "gzip");
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        if(substr($url, 0, 8) === 'https://') {
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
            curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        }
        if(!empty($postData)) {
            curl_setopt($ch, CURLOPT_POST, 1);               
            curl_setopt($ch, CURLOPT_POSTFIELDS, $postData); 
        }
        if(!empty($cookie)) {
            $header[] = $cookie;
        }
        if(!empty($header)) {
            curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
        }
        curl_setopt($ch, CURLOPT_TIMEOUT, (int)$timeout);
        $content = curl_exec($ch);
        if($error = curl_error($ch)) {
            error_log($error);
        }
        curl_close($ch);
        return $content;
    }
    function rand_ip(){
        $ip_long = array(
        array('607649792', '608174079'), //36.56.0.0-36.63.255.255
        array('975044608', '977272831'), //58.30.0.0-58.63.255.255
        array('999751680', '999784447'), //59.151.0.0-59.151.127.255
        array('1019346944', '1019478015'), //60.194.0.0-60.195.255.255
        array('1038614528', '1039007743'), //61.232.0.0-61.237.255.255
        array('1783627776', '1784676351'), //106.80.0.0-106.95.255.255
        array('1947009024', '1947074559'), //116.13.0.0-116.13.255.255
        array('1987051520', '1988034559'), //118.112.0.0-118.126.255.255
        array('2035023872', '2035154943'), //121.76.0.0-121.77.255.255
        array('2078801920', '2079064063'), //123.232.0.0-123.235.255.255
        array('-1950089216', '-1948778497'), //139.196.0.0-139.215.255.255
        array('-1425539072', '-1425014785'), //171.8.0.0-171.15.255.255
        array('-1236271104', '-1235419137'), //182.80.0.0-182.92.255.255
        array('-770113536', '-768606209'), //210.25.0.0-210.47.255.255
        array('-569376768', '-564133889'), //222.16.0.0-222.95.255.255
        );
        $rand_key = mt_rand(0, 14);
        $huoduan_ip= long2ip(mt_rand($ip_long[$rand_key][0], $ip_long[$rand_key][1]));
        return $huoduan_ip;
        }