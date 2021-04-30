import requests,hashlib,time
def get_page(url, data):
    try:
        response = requests.post(url=url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)
def sign_md5(text, timestamp):
    string = 'fanyideskweb' + text + f'{timestamp}1' + 'mmbP%A-r6U3Nw(n]BjuEU'
    return hashlib.md5(string.encode('utf-8')).hexdigest()
#https://zhuanlan.zhihu.com/p/159912197 断点调试
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
                  'Referer':'http://fanyi.youdao.com',
                  'Cookie':'OUTFOX_SEARCH_USER_ID_NCOO=1816517197.5239441; OUTFOX_SEARCH_USER_ID="1388622947@10.108.160.19"; _ga=GA1.2.1432186159.1613716053; JSESSIONID=aaamcAfnqXGwm9V0Ic6Gx; ___rl__test__cookies=1615881510295'
}
def main():
    need_translate_text = input('输入需要翻译的文本：')
    timestamp = int(time.time() * 1000)
    sign = sign_md5(text=need_translate_text, timestamp=timestamp)
    data = {
        'i': need_translate_text,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': f'{timestamp}1',
        'sign': sign,
        'ts': f'{timestamp}',
        'bv': '07f15609aa4583527f9a1c22f48db662',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    result = get_page(url=url, data=data)
    print(result)
    print(f"需要翻译的文本：{need_translate_text} \n结果为：{result.get('translateResult')[0][0].get('tgt')}")
main()    