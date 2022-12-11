微博pc版url：https://weibo.com/xxx/Hd1N2qpta h5 版url：https://m.weibo.cn/detail/xxx

转换代码：

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#http://jermic.cc/2019/02/13/weibo-url-mid-convert/
#https://gist.github.com/Jermic/16f8a129b0b30311ab4584b610351613
def base62_encode(num, alphabet=ALPHABET):
    num = int(num)
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string, alphabet=ALPHABET):
    string = str(string)
    num = 0
    idx = 0
    for char in string:
        power = (len(string) - (idx + 1))
        num += alphabet.index(char) * (len(alphabet) ** power)
        idx += 1

    return num


def reverse_cut_to_length(content, code_func, cut_num=4, fill_num=7):
    content = str(content)
    cut_list = [content[i - cut_num if i >= cut_num else 0:i] for i in range(len(content), 0, (-1 * cut_num))]
    cut_list.reverse()
    result = []
    for i, item in enumerate(cut_list):
        s = str(code_func(item))
        if i > 0 and len(s) < fill_num:
            s = (fill_num - len(s)) * '0' + s
        result.append(s)
    return ''.join(result)


def url_to_mid(url: str):
    """
    >>> url_to_mid('z0JH2lOMb')
    3501756485200075
    >>> url_to_mid('z0IgABdSn')
    3501701648871479
    >>> url_to_mid('z08AUBmUe')
    3500330408906190
    >>> url_to_mid('z06qL6b28')
    3500247231472384
    >>> url_to_mid('yAt1n2xRa')
    3486913690606804
    """
    result = reverse_cut_to_length(url, base62_decode, 4, 7)
    return int(result)


def mid_to_url(mid_int: int):
    """
    >>> mid_to_url(3501756485200075)
    'z0JH2lOMb'
    >>> mid_to_url(3501701648871479)
    'z0IgABdSn'
    >>> mid_to_url(3500330408906190)
    'z08AUBmUe'
    >>> mid_to_url(3500247231472384)
    'z06qL6b28'
    >>> mid_to_url(3486913690606804)
    'yAt1n2xRa'
    """
    result = reverse_cut_to_length(mid_int, base62_encode, 7, 4)
    return result


if __name__ == "__main__":
    print(url_to_mid('Hd1N2qpta'))
    print(mid_to_url(4331051486294436))
js转换

str62keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
/**
* 10进制值转换为62进制
* @param {String} int10 10进制值
* @return {String} 62进制值
*/
function int10to62(int10) {
    var s62 = '';
    var r = 0;
    while (int10 != 0) {
            r = int10 % 62;
            s62 = this.str62keys.charAt(r) + s62;
            int10 = Math.floor(int10 / 62);
    }
    return s62;
}
/**
* 62进制值转换为10进制
* @param {String} str62 62进制值
* @return {String} 10进制值
*/
function str62to10(str62) {
    var i10 = 0;
    for (var i = 0; i < str62.length; i++) {
            var n = str62.length - i - 1;
            var s = str62.substr(i, 1);  // str62[i]; 字符串用数组方式获取，IE下不支持为“undefined”
            i10 += parseInt(str62keys.indexOf(s)) * Math.pow(62, n);
    }
    return i10;
}
/**
* id转换为mid
* @param {String} id 微博id，如 "201110410216293360"
* @return {String} 微博mid，如 "wr4mOFqpbO"
*/
function id2mid(id) {
    if (typeof (id) != 'string') {
            return false; // id数值较大，必须为字符串！
    }
    var mid = '';
    for (var i = id.length - 7; i > -7; i = i - 7) //从最后往前以7字节为一组读取mid
    {
            var offset1 = i < 0 ? 0 : i;
            var offset2 = i + 7;
            var num = id.substring(offset1, offset2);
            num = int10to62(num);
            mid = num + mid;
    }
    return mid;
}
/**
* mid转换为id
* @param {String} mid 微博mid，如 "wr4mOFqpbO"
* @return {String} 微博id，如 "201110410216293360"
*/
function mid2id(mid) {
    var id = '';
    for (var i = mid.length - 4; i > -4; i = i - 4) //从最后往前以4字节为一组读取mid字符
    {
            var offset1 = i < 0 ? 0 : i;
            var len = i < 0 ? parseInt(mid.length % 4) : 4;
            var str = mid.substr(offset1, len);
            str = str62to10(str).toString();
            if (offset1 > 0) //若不是第一组，则不足7位补0
            {
                    while (str.length < 7) {
                            str = '0' + str;
                    }
            }
            id = str + id;
    }
    return id;
}