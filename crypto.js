<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>测试加密</title>
    <script src="https://cdn.bootcss.com/crypto-js/3.1.9-1/crypto-js.min.js"></script>
 
  </head>
  <body>
    <p>在控制台查看结果</p>
  </body>
 <script>
const timestamp = Date.parse(new Date());//时间戳
const videoId="108548";
const md5=CryptoJS.MD5(videoId+"-"+timestamp).toString().slice(0,16);
//64 转hex https://www.52pojie.cn/thread-1719094-1-1.html  https://www.bdys01.com/play/16268-1.htm
function base64toHEX(base64) {
var raw = atob(base64);
var HEX = '';
for ( i = 0; i < raw.length; i++ ) {
  var _hex = raw.charCodeAt(i).toString(16)
  HEX += (_hex.length==2?_hex:'0'+_hex);
}
return HEX.toUpperCase();
}
const key = CryptoJS.enc.Utf8.parse(md5);
// AES加密
function encryptByAES (data) {
        let encryptData = CryptoJS.AES.encrypt(data, key, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        return encryptData.toString();
    }
     
console.log("时间戳:"+timestamp);
console.log("签名:"+base64toHEX(encryptByAES(videoId+"-"+timestamp)));
 
  </script>
</html>