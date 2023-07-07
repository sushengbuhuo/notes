import sys,json,csv,time
import hashlib
import random
import requests
import os
import re,html
from enum import Enum
from typing import NamedTuple
import binascii
import ctypes
import string
import binascii
import ctypes
import hashlib
import json
import random
import re
import string
import time
import urllib.parse
from playwright.sync_api import sync_playwright
from time import sleep
import requests
import urllib.parse
from enum import Enum
from typing import NamedTuple
from requests import RequestException
from tqdm import tqdm

class ErrorTuple(NamedTuple):
    code: int
    msg: str


class ErrorEnum(Enum):
    IP_BLOCK = ErrorTuple(300012, "网络连接异常，请检查网络设置或重启试试")
    NOTE_ABNORMAL = ErrorTuple(-510001, "笔记状态异常，请稍后查看")
    SIGN_FAULT = ErrorTuple(300015, "浏览器异常，请尝试关闭/卸载风险插件或重启试试！")


class DataFetchError(RequestException):
    """something error when fetch"""


class IPBlockError(RequestException):
    """fetch so fast that the server block us ip"""


class SignError(RequestException):
    """fetch error because x-s sign verror"""

def sign(uri, data=None, ctime=None, a1="", b1=""):
    """
    takes in a URI (uniform resource identifier), an optional data dictionary, and an optional ctime parameter. It returns a dictionary containing two keys: "x-s" and "x-t".
    """

    def h(n):
        m = ""
        d = "A4NjFqYu5wPHsO0XTdDgMa2r1ZQocVte9UJBvk6/7=yRnhISGKblCWi+LpfE8xzm3"
        for i in range(0, 32, 3):
            o = ord(n[i])
            g = ord(n[i + 1]) if i + 1 < 32 else 0
            h = ord(n[i + 2]) if i + 2 < 32 else 0
            x = ((o & 3) << 4) | (g >> 4)
            p = ((15 & g) << 2) | (h >> 6)
            v = o >> 2
            b = h & 63 if h else 64
            if not g:
                p = b = 64
            m += d[v] + d[x] + d[p] + d[b]
        return m

    v = int(round(time.time() * 1000) if not ctime else ctime)
    raw_str = f"{v}test{uri}{json.dumps(data, separators=(',', ':'), ensure_ascii=False) if isinstance(data, dict) else ''}"
    md5_str = hashlib.md5(raw_str.encode('utf-8')).hexdigest()
    x_s = h(md5_str)
    x_t = str(v)

    common = {
        "s0": 5,  # getPlatformCode
        "s1": "",
        "x0": "1",  # localStorage.getItem("b1b1")
        "x1": "3.2.0",  # version
        "x2": "Windows",
        "x3": "xhs-pc-web",
        "x4": "2.3.1",
        "x5": a1,  # cookie of a1
        "x6": x_t,
        "x7": x_s,
        "x8": b1,  # localStorage.getItem("b1")
        "x9": mrc(x_t + x_s),
        "x10": 1,  # getSigCount
    }
    encodeStr = encodeUtf8(json.dumps(common, separators=(',', ':')))
    x_s_common = b64Encode(encodeStr)
    return {
        "x-s": x_s,
        "x-t": x_t,
        "x-s-common": x_s_common,
    }


def get_a1_and_web_id():
    """generate a1 and webid cookie str, the first return value is a1, second is webId

    for example: a1, web_id = get_a1_and_web_id()
    """

    def random_str(length):
        alphabet = string.ascii_letters + string.digits
        return ''.join(random.choice(alphabet) for _ in range(length))

    d = hex(int(time.time() * 1000))[2:] + random_str(30) + "5" + "0" + "000"
    g = (d + str(binascii.crc32(str(d).encode('utf-8'))))[:52]
    return g, hashlib.md5(g.encode('utf-8')).hexdigest()


img_cdns = [
    "https://sns-img-qc.xhscdn.com",
    "https://sns-img-hw.xhscdn.com",
    "https://sns-img-bd.xhscdn.com",
    "https://sns-img-qn.xhscdn.com",
]


def get_img_url_by_trace_id(trace_id: str, format: str = "png"):
    return f"{random.choice(img_cdns)}/{trace_id}?imageView2/format/{format}"


def get_img_urls_by_trace_id(trace_id: str, format: str = "png"):
    return [f"{cdn}/{trace_id}?imageView2/format/{format}" for cdn in img_cdns]


def get_imgs_url_from_note(note) -> list:
    """the return type is [img1_url, img2_url, ...]"""
    imgs = note["image_list"]
    if not len(imgs):
        return []
    return [get_img_url_by_trace_id(img["trace_id"]) for img in imgs]


def get_imgs_urls_from_note(note) -> list:
    """the return type is [[img1_url1, img1_url2, img1_url3], [img2_url, img2_url2, img2_url3], ...]"""
    imgs = note["image_list"]
    if not len(imgs):
        return []
    return [get_img_urls_by_trace_id(img["trace_id"]) for img in imgs]


video_cdns = [
    "https://sns-video-qc.xhscdn.com",
    "https://sns-video-hw.xhscdn.com",
    "https://sns-video-bd.xhscdn.com",
    "https://sns-video-qn.xhscdn.com",
]


def get_video_url_from_note(note) -> str:
    if not note.get("video"):
        return ""
    origin_video_key = note['video']['consumer']['origin_video_key']
    return f"{random.choice(video_cdns)}/{origin_video_key}"


def get_video_urls_from_note(note) -> list:
    if not note.get("video"):
        return []
    origin_video_key = note['video']['consumer']['origin_video_key']
    return [f"{cdn}/{origin_video_key}" for cdn in video_cdns]


def download_file(url: str, filename: str):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def get_valid_path_name(text):
    invalid_chars = '<>:"/\\|?*'
    return re.sub('[{}]'.format(re.escape(invalid_chars)), '_', text)


def mrc(e):
    ie = [
        0, 1996959894, 3993919788, 2567524794, 124634137, 1886057615, 3915621685,
        2657392035, 249268274, 2044508324, 3772115230, 2547177864, 162941995,
        2125561021, 3887607047, 2428444049, 498536548, 1789927666, 4089016648,
        2227061214, 450548861, 1843258603, 4107580753, 2211677639, 325883990,
        1684777152, 4251122042, 2321926636, 335633487, 1661365465, 4195302755,
        2366115317, 997073096, 1281953886, 3579855332, 2724688242, 1006888145,
        1258607687, 3524101629, 2768942443, 901097722, 1119000684, 3686517206,
        2898065728, 853044451, 1172266101, 3705015759, 2882616665, 651767980,
        1373503546, 3369554304, 3218104598, 565507253, 1454621731, 3485111705,
        3099436303, 671266974, 1594198024, 3322730930, 2970347812, 795835527,
        1483230225, 3244367275, 3060149565, 1994146192, 31158534, 2563907772,
        4023717930, 1907459465, 112637215, 2680153253, 3904427059, 2013776290,
        251722036, 2517215374, 3775830040, 2137656763, 141376813, 2439277719,
        3865271297, 1802195444, 476864866, 2238001368, 4066508878, 1812370925,
        453092731, 2181625025, 4111451223, 1706088902, 314042704, 2344532202,
        4240017532, 1658658271, 366619977, 2362670323, 4224994405, 1303535960,
        984961486, 2747007092, 3569037538, 1256170817, 1037604311, 2765210733,
        3554079995, 1131014506, 879679996, 2909243462, 3663771856, 1141124467,
        855842277, 2852801631, 3708648649, 1342533948, 654459306, 3188396048,
        3373015174, 1466479909, 544179635, 3110523913, 3462522015, 1591671054,
        702138776, 2966460450, 3352799412, 1504918807, 783551873, 3082640443,
        3233442989, 3988292384, 2596254646, 62317068, 1957810842, 3939845945,
        2647816111, 81470997, 1943803523, 3814918930, 2489596804, 225274430,
        2053790376, 3826175755, 2466906013, 167816743, 2097651377, 4027552580,
        2265490386, 503444072, 1762050814, 4150417245, 2154129355, 426522225,
        1852507879, 4275313526, 2312317920, 282753626, 1742555852, 4189708143,
        2394877945, 397917763, 1622183637, 3604390888, 2714866558, 953729732,
        1340076626, 3518719985, 2797360999, 1068828381, 1219638859, 3624741850,
        2936675148, 906185462, 1090812512, 3747672003, 2825379669, 829329135,
        1181335161, 3412177804, 3160834842, 628085408, 1382605366, 3423369109,
        3138078467, 570562233, 1426400815, 3317316542, 2998733608, 733239954,
        1555261956, 3268935591, 3050360625, 752459403, 1541320221, 2607071920,
        3965973030, 1969922972, 40735498, 2617837225, 3943577151, 1913087877,
        83908371, 2512341634, 3803740692, 2075208622, 213261112, 2463272603,
        3855990285, 2094854071, 198958881, 2262029012, 4057260610, 1759359992,
        534414190, 2176718541, 4139329115, 1873836001, 414664567, 2282248934,
        4279200368, 1711684554, 285281116, 2405801727, 4167216745, 1634467795,
        376229701, 2685067896, 3608007406, 1308918612, 956543938, 2808555105,
        3495958263, 1231636301, 1047427035, 2932959818, 3654703836, 1088359270,
        936918000, 2847714899, 3736837829, 1202900863, 817233897, 3183342108,
        3401237130, 1404277552, 615818150, 3134207493, 3453421203, 1423857449,
        601450431, 3009837614, 3294710456, 1567103746, 711928724, 3020668471,
        3272380065, 1510334235, 755167117,
    ]
    o = -1

    def right_without_sign(num, bit=0) -> int:
        val = ctypes.c_uint32(num).value >> bit
        MAX32INT = 4294967295
        return (val + (MAX32INT + 1)) % (2 * (MAX32INT + 1)) - MAX32INT - 1

    for n in range(57):
        o = ie[(o & 255) ^ ord(e[n])] ^ right_without_sign(o, 8)
    return o ^ -1 ^ 3988292384


lookup = [
    "Z",
    "m",
    "s",
    "e",
    "r",
    "b",
    "B",
    "o",
    "H",
    "Q",
    "t",
    "N",
    "P",
    "+",
    "w",
    "O",
    "c",
    "z",
    "a",
    "/",
    "L",
    "p",
    "n",
    "g",
    "G",
    "8",
    "y",
    "J",
    "q",
    "4",
    "2",
    "K",
    "W",
    "Y",
    "j",
    "0",
    "D",
    "S",
    "f",
    "d",
    "i",
    "k",
    "x",
    "3",
    "V",
    "T",
    "1",
    "6",
    "I",
    "l",
    "U",
    "A",
    "F",
    "M",
    "9",
    "7",
    "h",
    "E",
    "C",
    "v",
    "u",
    "R",
    "X",
    "5",
]


def tripletToBase64(e):
    return (
            lookup[63 & (e >> 18)] +
            lookup[63 & (e >> 12)] +
            lookup[(e >> 6) & 63] +
            lookup[e & 63]
    )


def encodeChunk(e, t, r):
    m = []
    for b in range(t, r, 3):
        n = (16711680 & (e[b] << 16)) + \
            ((e[b + 1] << 8) & 65280) + (e[b + 2] & 255)
        m.append(tripletToBase64(n))
    return ''.join(m)


def b64Encode(e):
    P = len(e)
    W = P % 3
    U = []
    z = 16383
    H = 0
    Z = P - W
    while H < Z:
        U.append(encodeChunk(e, H, Z if H + z > Z else H + z))
        H += z
    if 1 == W:
        F = e[P - 1]
        U.append(lookup[F >> 2] + lookup[(F << 4) & 63] + "==")
    elif 2 == W:
        F = (e[P - 2] << 8) + e[P - 1]
        U.append(lookup[F >> 10] + lookup[63 & (F >> 4)] +
                 lookup[(F << 2) & 63] + "=")
    return "".join(U)


def encodeUtf8(e):
    b = []
    m = urllib.parse.quote(e, safe='~()*!.\'')
    w = 0
    while w < len(m):
        T = m[w]
        if T == "%":
            E = m[w + 1] + m[w + 2]
            S = int(E, 16)
            b.append(S)
            w += 2
        else:
            b.append(ord(T[0]))
        w += 1
    return b


def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def base36decode(number):
    return int(number, 36)


def get_search_id():
    e = int(time.time() * 1000) << 64
    t = int(random.uniform(0, 2147483646))
    return base36encode((e + t))


def cookie_str_to_cookie_dict(cookie_str: str):
    cookie_blocks = [cookie_block.split("=")
                     for cookie_block in cookie_str.split(";") if cookie_block]
    return {cookie[0].strip(): cookie[1].strip() for cookie in cookie_blocks}


def cookie_jar_to_cookie_str(cookie_jar):
    cookie_dict = requests.utils.dict_from_cookiejar(cookie_jar)
    return ";".join([f"{key}={value}" for key, value in cookie_dict.items()])


def update_session_cookies_from_cookie(session: requests.Session, cookie: str):
    cookie_dict = cookie_str_to_cookie_dict(cookie) if cookie else {}
    if "a1" not in cookie_dict or "webId" not in cookie_dict:
        # a1, web_id = get_a1_and_web_id()
        cookie_dict |= {"a1": "187d2defea8dz1fgwydnci40kw265ikh9fsxn66qs50000726043",
                        "webId": "ba57f42593b9e55840a289fa0b755374"}
    if "gid" not in cookie_dict:
        cookie_dict |= {
            "gid.sign": "PSF1M3U6EBC/Jv6eGddPbmsWzLI=",
            "gid": "yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy"
        }
    new_cookies = requests.utils.cookiejar_from_dict(cookie_dict)
    session.cookies = new_cookies
class FeedType(Enum):
    # 推荐
    RECOMMEND = "homefeed_recommend"
    # 穿搭
    FASION = "homefeed.fashion_v3"
    # 美食
    FOOD = "homefeed.food_v3"
    # 彩妆
    COSMETICS = "homefeed.cosmetics_v3"
    # 影视
    MOVIE = "homefeed.movie_and_tv_v3"
    # 职场
    CAREER = "homefeed.career_v3"
    # 情感
    EMOTION = "homefeed.love_v3"
    # 家居
    HOURSE = "homefeed.household_product_v3"
    # 游戏
    GAME = "homefeed.gaming_v3"
    # 旅行
    TRAVEL = "homefeed.travel_v3"
    # 健身
    FITNESS = "homefeed.fitness_v3"


class NoteType(Enum):
    NOMAL = "nomal"
    VIDEO = "video"


class SearchSortType(Enum):
    """serach sort type
    """
    # default
    GENERAL = "general"
    # most popular
    MOST_POPULAR = "popularity_descending"
    # Latest
    LATEST = "time_descending"


class SearchNoteType(Enum):
    """search note type
    """
    # default
    ALL = 0
    # only video
    VIDEO = 1
    # only image
    IMAGE = 2


class Note(NamedTuple):
    """note typle"""
    note_id: str
    title: str
    desc: str
    type: str
    user: dict
    img_urls: list
    video_url: str
    tag_list: list
    at_user_list: list
    collected_count: str
    comment_count: str
    liked_count: str
    share_count: str
    time: int
    last_update_time: int


class XhsClient:
    def __init__(self,
                 cookie=None,
                 user_agent=None,
                 timeout=10,
                 proxies=None,
                 sign=None):
        """constructor"""
        self.proxies = proxies
        self.__session: requests.Session = requests.session()
        self.timeout = timeout
        self.sign = sign
        self._host = "https://edith.xiaohongshu.com"
        self.home = "https://www.xiaohongshu.com"
        user_agent = user_agent or ("Mozilla/5.0 "
                                    "(Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) "
                                    "Chrome/111.0.0.0 Safari/537.36")
        self.__session.headers = {
            "user-agent": user_agent,
            "Content-Type": "application/json"
        }
        self.cookie = cookie

    @property
    def cookie(self):
        return cookie_jar_to_cookie_str(self.__session.cookies)

    @cookie.setter
    def cookie(self, cookie: str):
        update_session_cookies_from_cookie(self.__session, cookie)
        if "web_session" not in self.cookie_dict:
            self.activate()

    @property
    def cookie_dict(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    @property
    def session(self):
        return self.__session

    @property
    def user_agent(self):
        return self.__session.headers.get("user-agent")

    @user_agent.setter
    def user_agent(self, user_agent: str):
        self.__session.headers.update({"user-agent": user_agent})

    def _pre_headers(self, url: str, data=None, is_creator: bool = False):
        if is_creator:
            signs = sign(url, data, a1=self.cookie_dict.get("a1"))
            self.__session.headers.update({"x-s": signs["x-s"]})
            self.__session.headers.update({"x-t": signs["x-t"]})
            self.__session.headers.update({"x-s-common": signs["x-s-common"]})
        else:
            self.__session.headers.update(
                self.sign(url, data, a1=self.cookie_dict.get("a1"),
                          web_session=self.cookie_dict.get("web_session")))

    def request(self, method, url, **kwargs):
        response = self.__session.request(
            method, url, timeout=self.timeout,
            proxies=self.proxies, **kwargs)
        if not len(response.text):
            return response
        data = response.json()
        if data.get("success"):
            return data.get("data", data.get("success"))
        elif data["code"] == ErrorEnum.IP_BLOCK.value.code:
            raise IPBlockError(ErrorEnum.IP_BLOCK.value.msg)
        elif data["code"] == ErrorEnum.SIGN_FAULT.value.code:
            raise SignError(ErrorEnum.SIGN_FAULT.value.msg)
        else:
            raise DataFetchError(data.get("msg", None))

    def get(self, uri: str, params=None, is_creator: bool = False):
        final_uri = uri
        if isinstance(params, dict):
            final_uri = (f"{uri}?"
                         f"{'&'.join([f'{k}={v}' for k, v in params.items()])}")
        self._pre_headers(final_uri, is_creator=is_creator)
        return self.request(method="GET", url=f"{self._host}{final_uri}")

    def post(self, uri: str, data: dict, is_creator: bool = False):
        self._pre_headers(uri, data, is_creator=is_creator)
        json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        return self.request(method="POST", url=f"{self._host}{uri}",
                            data=json_str.encode("utf-8"))

    def get_note_by_id(self, note_id: str):
        """
        :param note_id: note_id you want to fetch
        :type note_id: str
        :return: {"time":1679019883000,"user":{"nickname":"nickname","avatar":"avatar","user_id":"user_id"},"image_list":[{"url":"https://sns-img-qc.xhscdn.com/c8e505ca-4e5f-44be-fe1c-ca0205a38bad","trace_id":"1000g00826s57r6cfu0005ossb1e9gk8c65d0c80","file_id":"c8e505ca-4e5f-44be-fe1c-ca0205a38bad","height":1920,"width":1440}],"tag_list":[{"id":"5be78cdfdb601f000100d0bc","name":"jk","type":"topic"}],"desc":"裙裙","interact_info":{"followed":false,"liked":false,"liked_count":"1732","collected":false,"collected_count":"453","comment_count":"30","share_count":"41"},"at_user_list":[],"last_update_time":1679019884000,"note_id":"6413cf6b00000000270115b5","type":"normal","title":"title"}
        :rtype: dict
        """
        data = {"source_note_id": note_id}
        uri = "/api/sns/web/v1/feed"
        res = self.post(uri, data)
        return res["items"][0]["note_card"]

    def get_note_by_id_from_html(self, note_id: str):
        """get note info from "https://www.xiaohongshu.com/explore/" + note_id, and the return obj is equal to get_note_by_id

        :param note_id: note_id you want to fetch
        :type note_id: str
        """

        def camel_to_underscore(key):
            return re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()

        def transform_json_keys(json_data):
            data_dict = json.loads(json_data)
            new_dict = {}
            for key, value in data_dict.items():
                new_key = camel_to_underscore(key)
                if not value:
                    new_dict[new_key] = value
                elif isinstance(value, dict):
                    new_dict[new_key] = transform_json_keys(json.dumps(value))
                elif isinstance(value, list):
                    new_dict[new_key] = [transform_json_keys(json.dumps(
                        item)) if (item and isinstance(item, dict)) else item for item in value]
                else:
                    new_dict[new_key] = value
            return new_dict

        url = "https://www.xiaohongshu.com/explore/" + note_id
        res = self.session.get(url, headers={"user-agent": self.user_agent})
        html = res.text
        state = re.findall(
            r'window.__INITIAL_STATE__=({.*})</script>', html)[0].replace("undefined", '""')
        if state != "{}":
            new_dict = transform_json_keys(state)
            return new_dict["note"]["note"]
        elif self.IP_ERROR_STR in html:
            raise IPBlockError(self.IP_ERROR_STR)
        raise DataFetchError()

    def report_note_metrics(self, note_id: str, note_type: int, note_user_id: str, viewer_user_id: str,
                            followed_author=0, report_type=1, stay_seconds=0):
        """report note stay seconds and other interaction info

        :param note_id: note_id which you want to report
        :type note_id: str
        :param note_type: input value -> 1: note is images, 2: note is video
        :type note_type: int
        :param note_user_id: note author id
        :type note_user_id: str
        :param viewer_user_id: report user id
        :type viewer_user_id: str
        :param followed_author: 1: the viewer user follow note's author, 0: the viewer user don't follow note's author
        :type followed_author: int
        :param report_type: 1: the first report, 2: the second report, so you must report twice, defaults to 1
        :type report_type: int, optional
        :param stay_seconds: report metric -> note you stay seconds, defaults to 0
        :type stay_seconds: int, optional
        :return: same as api
        :rtype: dict
        """
        uri = "/api/sns/web/v1/note/metrics_report"
        data = {
            "note_id": note_id,
            "note_type": note_type,
            "report_type": report_type,
            "stress_test": False,
            "viewer": {"user_id": viewer_user_id, "followed_author": followed_author},
            "author": {"user_id": note_user_id},
            "interaction": {"like": 0, "collect": 0, "comment": 0, "comment_read": 0},
            "note": {"stay_seconds": stay_seconds},
            "other": {"platform": "web"}
        }
        return self.post(uri, data)

    def save_files_from_note_id(self, note_id: str, dir_path: str):
        """this function will fetch note and save file in dir_path/note_title

        :param note_id: note_id that you want to fetch
        :type note_id: str
        :param dir_path: in fact, files will be stored in your dir_path/note_title directory
        :type dir_path: str
        """
        note = self.get_note_by_id(note_id)

        title = get_valid_path_name(note["title"])

        if not title:
            title = note_id

        new_dir_path = os.path.join(dir_path, title)
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)

        if note["type"] == NoteType.VIDEO.value:
            video_url = get_video_url_from_note(note)
            video_filename = os.path.join(new_dir_path, f"{title}.mp4")
            download_file(video_url, video_filename)
        else:
            img_urls = get_imgs_url_from_note(note)
            for index, img_url in enumerate(img_urls):
                img_file_name = os.path.join(
                    new_dir_path, f"{title}{index}.png")
                download_file(img_url, img_file_name)

    def get_self_info(self):
        uri = "/api/sns/web/v1/user/selfinfo"
        return self.get(uri)

    def get_self_info2(self):
        uri = "/api/sns/web/v2/user/me"
        return self.get(uri)

    def get_user_info(self, user_id: str):
        """
        :param user_id: user_id you want fetch
        :type user_id: str
        :return: {"basic_info":{"imageb":"imageb","nickname":"nickname","images":"images","red_id":"red_id","gender":1,"ip_location":"ip_location","desc":"desc"},"interactions":[{"count":"5","type":"follows","name":"关注"},{"type":"fans","name":"粉丝","count":"16736"},{"type":"interaction","name":"获赞与收藏","count":"293043"}],"tags":[{"icon":"icon","tagType":"info"}],"tab_public":{"collection":false},"extra_info":{"fstatus":"none"},"result":{"success":true,"code":0,"message":"success"}}
        :rtype: dict
        """
        uri = "/api/sns/web/v1/user/otherinfo"
        params = {
            "target_user_id": user_id
        }
        return self.get(uri, params)

    def get_home_feed_category(self):
        uri = "/api/sns/web/v1/homefeed/category"
        return self.get(uri)["categories"]

    def get_home_feed(self, feed_type: FeedType):
        uri = "/api/sns/web/v1/homefeed"
        data = {
            "cursor_score": "",
            "num": 40,
            "refresh_type": 1,
            "note_index": 0,
            "unread_begin_note_id": "",
            "unread_end_note_id": "",
            "unread_note_count": 0,
            "category": feed_type.value
        }
        return self.post(uri, data)

    def get_search_suggestion(self, keyword: str):
        uri = "/api/sns/web/v1/sug/recommend"
        params = {
            "keyword": keyword
        }
        return [sug["text"] for sug in self.get(uri, params)["sug_items"]]

    def get_note_by_keyword(self, keyword: str,
                            page: int = 1, page_size: int = 20,
                            sort: SearchSortType = SearchSortType.GENERAL,
                            note_type: SearchNoteType = SearchNoteType.ALL):
        """search note by keyword

        :param keyword: what notes you want to search
        :type keyword: str
        :param page: page number, defaults to 1
        :type page: int, optional
        :param page_size: page size, defaults to 20
        :type page_size: int, optional
        :param sort: sort ordering, defaults to SearchSortType.GENERAL
        :type sort: SearchSortType, optional
        :param note_type: note type, defaults to SearchNoteType.ALL
        :type note_type: SearchNoteType, optional
        :return: {has_more: true, items: []}
        :rtype: dict
        """
        uri = "/api/sns/web/v1/search/notes"
        data = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
            "search_id": get_search_id(),
            "sort": sort.value,
            "note_type": note_type.value
        }
        return self.post(uri, data)

    def get_user_notes(self, user_id: str, cursor: str = ""):
        """get user notes just have simple info

        :param user_id: user_id you want to fetch
        :type user_id: str
        :param cursor: return info has this argument, defaults to ""
        :type cursor: str, optional
        :return: {cursor:"", has_more:true,notes:[{cover:{},display_title:"",interact_info:{},note_id:"",type:"video"}]}
        :rtype: dict
        """
        uri = "/api/sns/web/v1/user_posted"
        params = {
            "num": 30,
            "cursor": cursor,
            "user_id": user_id
        }
        return self.get(uri, params)

    def get_user_all_notes(self, user_id: str, crawl_interval: int = 1):
        """get user all notes with more info, abnormal notes will be ignored

        :param user_id: user_id you want to fetch
        :type user_id: str
        :param crawl_interval: sleep seconds, defaults to 1
        :type crawl_interval: int, optional
        :return: note info list
        :rtype: list[Note]
        """
        has_more = True
        cursor = ""
        result = []
        while has_more:
            res = self.get_user_notes(user_id, cursor)
            has_more = res["has_more"]
            cursor = res["cursor"]
            note_ids = map(lambda note: note["note_id"], res["notes"])
            if len(result) > 500:
                break
            for note_id in note_ids:
                try:
                    note = self.get_note_by_id(note_id)
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(note["time"]/1000)),note["title"],time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                except DataFetchError as e:
                    if ErrorEnum.NOTE_ABNORMAL.value.msg in str(e):
                        continue
                    else:
                        raise
                interact_info = note["interact_info"]
                note_info = Note(
                    note_id=note["note_id"],
                    title=note["title"],
                    desc=note["desc"],
                    type=note["type"],
                    user=note["user"],
                    img_urls=get_imgs_url_from_note(note),
                    video_url=get_video_url_from_note(note),
                    tag_list=note["tag_list"],
                    at_user_list=note["at_user_list"],
                    collected_count=interact_info["collected_count"],
                    comment_count=interact_info["comment_count"],
                    liked_count=interact_info["liked_count"],
                    share_count=interact_info["share_count"],
                    time=note["time"],
                    last_update_time=note["last_update_time"],
                )
                result.append(note_info)
                time.sleep(crawl_interval)
        return result

    def get_note_comments(self, note_id: str, cursor: str = ""):
        """get note comments

        :param note_id: note id you want to fetch
        :type note_id: str
        :param cursor: last you get cursor, defaults to ""
        :type cursor: str, optional
        :return: {"has_more": true,"cursor": "6422442d000000000700dcdb",comments: [],"user_id": "63273a77000000002303cc9b","time": 1681566542930}
        :rtype: dict
        """
        uri = "/api/sns/web/v2/comment/page"
        params = {
            "note_id": note_id,
            "cursor": cursor
        }
        return self.get(uri, params)

    def get_note_sub_comments(self, note_id: str,
                              root_comment_id: str,
                              num: int = 30, cursor: str = ""):
        """get note sub comments

        :param note_id: note id you want to fetch
        :type note_id: str
        :param root_comment_id: parent comment id
        :type root_comment_id: str
        :param num: recommend 30, if num greater 30, it only return 30 comments
        :type num: int
        :param cursor: last you get cursor, defaults to ""
        :type cursor: str optional
        :return: {"has_more": true,"cursor": "6422442d000000000700dcdb",comments: [],"user_id": "63273a77000000002303cc9b","time": 1681566542930}
        :rtype: dict
        """
        uri = "/api/sns/web/v2/comment/sub/page"
        params = {
            "note_id": note_id,
            "root_comment_id": root_comment_id,
            "num": num,
            "cursor": cursor,
        }
        return self.get(uri, params)

    def get_note_all_comments(self, note_id: str, crawl_interval: int = 1):
        """get note all comments include sub comments

        :param note_id: note id you want to fetch
        :type note_id: str
        """
        result = []
        comments_has_more = True
        comments_cursor = ""
        while comments_has_more:
            comments_res = self.get_note_comments(note_id, comments_cursor)
            comments_has_more = comments_res.get("has_more", False)
            comments_cursor = comments_res.get("cursor", "")
            comments = comments_res["comments"]
            for comment in comments:
                result.append(comment)
                cur_sub_comment_count = int(comment["sub_comment_count"])
                cur_sub_comments = comment["sub_comments"]
                result.extend(cur_sub_comments)
                sub_comments_has_more = comment["sub_comment_has_more"] and len(
                    cur_sub_comments) < cur_sub_comment_count
                sub_comment_cursor = comment["sub_comment_cursor"]
                while sub_comments_has_more:
                    page_num = 30
                    sub_comments_res = self.get_note_sub_comments(
                        note_id, comment["id"], num=page_num, cursor=sub_comment_cursor)
                    sub_comments = sub_comments_res["comments"]
                    sub_comments_has_more = sub_comments_res["has_more"] and len(
                        sub_comments) == page_num
                    sub_comment_cursor = sub_comments_res["cursor"]
                    result.extend(sub_comments)
                    time.sleep(crawl_interval)
            time.sleep(crawl_interval)
        return result

    def comment_note(self, note_id: str, content: str):
        """comment a note

        :return: {"time":1680834576180,"toast":"评论已发布","comment":{"id":"id","note_id":"note_id","status":2,"liked":false,"show_tags":["is_author"],"ip_location":"ip_location","content":"content","at_users":[],"like_count":"0","user_info":{"image":"**","user_id":"user_id","nickname":"nickname"},"create_time":create_time}}
        :rtype: dict
        """
        uri = "/api/sns/web/v1/comment/post"
        data = {
            "note_id": note_id,
            "content": content,
            "at_users": []
        }
        return self.post(uri, data)

    def delete_note_comment(self, note_id: str, comment_id: str):
        uri = "/api/sns/web/v1/comment/delete"
        data = {
            "note_id": note_id,
            "comment_id": comment_id
        }
        return self.post(uri, data)

    def comment_user(self, note_id: str, comment_id: str, content: str):
        """
        :return: {"comment":{"like_count":"0","user_info":{"user_id":user_id"user_id":"user_id","image":"image"},"show_tags":["is_author"],"ip_location":"ip_location","id":"id","content":"content","at_users":[],"create_time":1680847204059,"target_comment":{"id":"id","user_info":{"user_id":"user_id","nickname":"nickname","image":"image"}},"note_id":"note_id","status":2,"liked":false},"time":1680847204089,"toast":"你的回复已发布"}
        :rtype: dict
        """
        uri = "/api/sns/web/v1/comment/post"
        data = {
            "note_id": note_id,
            "content": content,
            "target_comment_id": comment_id,
            "at_users": []
        }
        return self.post(uri, data)

    def follow_user(self, user_id: str):
        uri = "/api/sns/web/v1/user/follow"
        data = {
            "target_user_id": user_id
        }
        return self.post(uri, data)

    def unfollow_user(self, user_id: str):
        uri = "/api/sns/web/v1/user/unfollow"
        data = {
            "target_user_id": user_id
        }
        return self.post(uri, data)

    def collect_note(self, note_id: str):
        uri = "/api/sns/web/v1/note/collect"
        data = {
            "note_id": note_id
        }
        return self.post(uri, data)

    def uncollect_note(self, note_id: str):
        uri = "/api/sns/web/v1/note/uncollect"
        data = {
            "note_ids": note_id
        }
        return self.post(uri, data)

    def like_note(self, note_id: str):
        uri = "/api/sns/web/v1/note/like"
        data = {
            "note_oid": note_id
        }
        return self.post(uri, data)

    def like_comment(self, note_id: str, comment_id: str):
        uri = "/api/sns/web/v1/comment/like"
        data = {
            "note_id": note_id,
            "comment_id": comment_id
        }
        return self.post(uri, data)

    def dislike_note(self, note_id: str):
        uri = "/api/sns/web/v1/note/dislike"
        data = {
            "note_oid": note_id
        }
        return self.post(uri, data)

    def dislike_comment(self, comment_id: str):
        uri = "/api/sns/web/v1/comment/dislike"
        data = {
            "note_oid": comment_id
        }
        return self.post(uri, data)

    def get_qrcode(self):
        """create qrcode, you can trasform response url to qrcode

        :return: {"qr_id":"87323168**","code":"280148","url":"xhsdiscover://**","multi_flag":0}
        :rtype: dict
        """
        uri = "/api/sns/web/v1/login/qrcode/create"
        data = {}
        return self.post(uri, data)

    def check_qrcode(self, qr_id: str, code: str):
        uri = "/api/sns/web/v1/login/qrcode/status"
        params = {
            "qr_id": qr_id,
            "code": code
        }
        return self.get(uri, params)

    def activate(self):
        uri = "/api/sns/web/v1/login/activate"
        return self.post(uri, data={})

    def get_user_collect_notes(self, user_id: str, num: int = 30, cursor: str = ""):
        uri = "/api/sns/web/v2/note/collect/page"
        params = {
            "user_id": user_id,
            "num": num,
            "cursor": cursor
        }
        return self.get(uri, params)

    def get_user_like_notes(self, user_id: str, num: int = 30, cursor: str = ""):
        uri = "/api/sns/web/v1/note/like/page"
        params = {
            "user_id": user_id,
            "num": num,
            "cursor": cursor
        }
        return self.get(uri, params)

    def get_emojis(self):
        uri = "/api/im/redmoji/detail"
        return self.get(uri)["emoji"]["tabs"][0]["collection"]

    def get_upload_image_ids(self, count):
        uri = "/api/media/v1/upload/web/permit"
        params = {
            "biz_name": "spectrum",
            "scene": "image",
            "file_count": count,
            "version": "1",
            "source": "web",
        }
        return self.get(uri, params)["uploadTempPermits"]

    def upload_image(self, image_id: str, token: str, file_path: str):
        url = "https://ros-upload.xiaohongshu.com/spectrum/" + image_id
        headers = {
            "X-Cos-Security-Token": token
        }
        with open(file_path, "rb") as f:
            return self.request("PUT", url, data=f, headers=headers)

    def get_suggest_topic(self, keyword=""):
        uri = "/web_api/sns/v1/search/topic"
        data = {"keyword": keyword,
                "suggest_topic_request": {"title": "", "desc": ""},
                "page": {"page_size": 20, "page": 1}
                }
        return self.post(uri, data)["topic_info_dtos"]

    def get_suggest_ats(self, keyword=""):
        uri = "/web_api/sns/v1/search/user_info"
        data = {"keyword": keyword, "search_id": str(time.time() * 1000), "page": {"page_size": 20, "page": 1}}
        return self.post(uri, data)["user_info_dtos"]
# sys.path.insert(0,r"D:\code\xhs")
# sys.path.append(r"D:\code\xhs")
# for i in sys.path:
#     print(i)
# sys.exit()
#导入顺序 当前目录，python目录，安装目录 python -m pip install git+https://github.com/ReaJason/xhs pip install playwright  playwright install chrome
#playwright pdf  file://"file_path" filename.pdf https://playwright.dev/
# from xhs import FeedType, XhsClient
url = input("公众号苏生不惑提示你，请输入小红书主页链接：")#https://www.xiaohongshu.com/user/profile/5badf469dcf6180001b2588d
cookie = input("公众号苏生不惑提示你，请输入小红书cookie：")
url='https://www.xiaohongshu.com/user/profile/5badf469dcf6180001b2588d'
if not url or not cookie:
    sys.exit('输入为空')
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def get_context_page(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=True)
    browser_context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    browser_context.add_init_script(path=r"xiaohongshu_encrypt.js")
    context_page = browser_context.new_page()
    return browser_context, context_page

def get_history():
    history = []
    with open('xiaohongshu_list.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('xiaohongshu_list.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def signParam(uri, data, a1="", web_session=""):
    playwright = sync_playwright().start()
    browser_context, context_page = get_context_page(playwright)
    context_page.goto("https://www.xiaohongshu.com")
    cookie_list = browser_context.cookies()
    web_session_cookie = list(filter(lambda cookie: cookie["name"] == "web_session", cookie_list))
    if not web_session_cookie:
        browser_context.add_cookies([
            {'name': 'web_session', 'value': web_session, 'domain': ".xiaohongshu.com", 'path': "/"},
            {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
        )
        sleep(2)
    encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
    return {
        "x-s": encrypt_params["X-s"],
        "x-t": str(encrypt_params["X-t"])
    }
def data(url,cookie):
    user=re.search(r'https?://www.xiaohongshu.com/user/profile/(.*)',url)
    if not user:
        sys.exit('链接不正确')
    user_id = user.group(1)
    xhs_client = XhsClient(cookie, sign=signParam)
    notes = xhs_client.get_user_all_notes(user_id,3)
    fname = '小红书笔记数据'
    encoding = 'utf-8-sig'
    data=[]
    with open(f'{fname}.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['发布时间','链接','标题','简介','图片地址','视频地址','标签','@用户','收藏数','评论数','点赞数','分享数','更新时间'])
    for i in notes:
        try:
            tags = []
            for j in i.tag_list:
               tags.append(j['name'])
            tags = '，'.join(tags)   
            at = []
            for jj in i.at_user_list:
               at.append(jj['nickname'])
            at = '，'.join(at)
            data.append([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.time/1000)),f'https://www.xiaohongshu.com/explore/{i.note_id}', i.title,i.desc ,'，'.join(i.img_urls),i.video_url, tags, '，'.join(at), i.collected_count, i.comment_count,i.liked_count, i.share_count,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.last_update_time/1000))])
        except Exception as err:
            print(err,i)
    with open(f'{fname}.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
# data(url,cookie)
def download(filename):
    f = open(filename, encoding='UTF8')
    csv_reader = csv.reader(f)
    for line in csv_reader:
        if line[1] == "链接":
            continue
        try:
            urls_history = get_history()
            if html.unescape(line[1]) in urls_history:
                print('已经下载过:'+html.unescape(line[1]))
                continue
            if not os.path.exists('images'):
                os.mkdir('images')
            if not os.path.exists('video'):
                os.mkdir('video')
            images = line[4].split('，')
            num = 0
            save_history(html.unescape(line[1]))
            for i in images:
                print('开始下载图片',i,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                num+=1
                image_data = requests.get(i, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"})
                with open('images/'+line[0][:10]+'_'+trimName(line[2])+'_'+str(num)+'.jpg','wb') as f:
                    f.write(image_data.content)
            if line[5]:
                print('开始下载视频',line[5],time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                video_data = requests.get(line[5], headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"})
                with open('video/'+line[0][:10]+'_'+trimName(line[2])+'.mp4','wb') as f:
                    f.write(video_data.content)
        except Exception as e:
            print('错误信息',line[1],line[2],e)
download('小红书笔记数据.csv')
def user_all_notes(xhs_client: XhsClient):
    user_id = "5f6189040000000001003415"
    notes = xhs_client.get_user_all_notes(user_id,3)
    return notes
