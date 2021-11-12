# -*- coding: utf-8 -*-

from functools import reduce
import sys, locale, platform
import time, os, json, re, datetime, math, operator
import concurrent.futures
import requests
import argparse
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass

is_python2 = sys.version[0] == '2'
system_encoding = sys.stdin.encoding or locale.getpreferredencoding(True)

if platform.system() == 'Windows':
    if operator.ge(*map(lambda version: list(map(int, version.split('.'))), [platform.version(), '10.0.14393'])):
        os.system('')
    else:
        import colorama
        colorama.init()

try:
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
except:
    pass



def nargs_fit(parser, args):
    flags = parser._option_string_actions
    short_flags = [flag for flag in flags.keys() if len(flag) == 2]
    long_flags = [flag for flag in flags.keys() if len(flag) > 2]
    short_flags_with_nargs = set([flag[1] for flag in short_flags if flags[flag].nargs])
    short_flags_without_args = set([flag[1] for flag in short_flags if flags[flag].nargs == 0])
    validate = lambda part : (re.match(r'-[^-]', part) and (set(part[1:-1]).issubset(short_flags_without_args) and '-' + part[-1] in short_flags)) or (part.startswith('--') and part in long_flags)

    greedy = False
    for index, arg in enumerate(args):
        if arg.startswith('-'):
            valid = validate(arg)
            if valid and arg[-1] in short_flags_with_nargs:
                greedy = True
            elif valid:
                greedy = False
            elif greedy:
                args[index] = ' ' + args[index]
    return args

def print_fit(string, pin = False):
    if is_python2:
        string = string.encode(system_encoding)
    if pin == True:
        sys.stdout.write('\r\033[K')
        sys.stdout.write(string)
        sys.stdout.flush()
    else:
        sys.stdout.write(string + '\n')

def input_fit(string = ''):
    if is_python2:
        return raw_input(string.encode(system_encoding)).decode(system_encoding)
    else:
        return input(string)

def merge(*dicts):
    result = {}
    for dictionary in dicts: result.update(dictionary)
    return result

def quit(string = ''):
    print_fit(string)
    # exit()

def make_dir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        quit(str(e))

def confirm(message):
    while True:
        answer = input_fit('{} [Y/n] '.format(message)).strip()
        if answer == 'y' or answer == 'Y':
            return True
        elif answer == 'n' or answer == 'N':
            return False
        print_fit('unexpected answer')

def progress(part, whole, percent = False):
    if percent:
        return '{}/{}({}%)'.format(part, whole, int(float(part) / whole * 100))
    else:
        return '{}/{}'.format(part, whole)

def request_fit(method, url, max_retry = 0, cookie = None, stream = False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36',
        'Cookie': cookie
    }
    return requests.request(method, url, headers = headers, timeout = 5, stream = stream, verify = False)

def read_from_file(path):
    try:
        with open(path, 'r') as f:
            return [line.strip().decode(system_encoding) if is_python2 else line.strip() for line in f]
    except Exception as e:
        quit(str(e))

def nickname_to_uid(nickname):
    url = 'https://m.weibo.cn/n/{}'.format(nickname)
    response = request_fit('GET', url, cookie = token)
    if re.search(r'/u/\d{10}$', response.url):
        return response.url[-10:]
    else:
        return

def uid_to_nickname(uid):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(uid)
    response = request_fit('GET', url, cookie = token)
    try:
        return json.loads(response.text)['data']['userInfo']['screen_name']
    except:
        return

def bid_to_mid(string):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = {x: n for n, x in enumerate(alphabet)}

    splited = [string[(g + 1) * -4 : g * -4 if g * -4 else None] for g in reversed(range(math.ceil(len(string) / 4.0)))]
    convert = lambda s : str(sum([alphabet[c] * (len(alphabet) ** k) for k, c in enumerate(reversed(s))])).zfill(7)
    return int(''.join(map(convert, splited)))

def parse_date(text):
    now = datetime.datetime.now()
    if u'前' in text:
        if u'小时' in text:
            return (now - datetime.timedelta(hours = int(re.search(r'\d+', text).group()))).date()
        else:
            return now.date()
    elif u'昨天' in text:
        return now.date() - datetime.timedelta(days = 1)
    elif re.search(r'^[\d|-]+$', text):
        return datetime.datetime.strptime(((str(now.year) + '-') if not re.search(r'^\d{4}', text) else '') + text, '%Y-%m-%d').date()

def compare(standard, operation, candidate):
    for target in candidate:
        try:
            result = '>=<'
            if standard > target: result = '>'
            elif standard == target: result = '='
            else: result = '<'
            return result in operation
        except TypeError:
            pass

def get_resources(uid, video, interval, limit):
    page = 1
    size = 25
    amount = 0
    total = 0
    empty = 0
    aware = 1
    exceed = False
    resources = []
    while empty < aware and not exceed:
        try:
            url = 'https://m.weibo.cn/api/container/getIndex?count={}&page={}&containerid=107603{}'.format(size, page, uid)
            response = request_fit('GET', url, cookie = token)
            assert response.status_code != 418
            json_data = json.loads(response.text)
        except AssertionError:
            print_fit('punished by anti-scraping mechanism (#{})'.format(page), pin = True)
            empty = aware
        except Exception:
            pass
        else:
            empty = empty + 1 if json_data['ok'] == 0 else 0
            if total == 0 and 'cardlistInfo' in json_data['data']: total = json_data['data']['cardlistInfo']['total']
            cards = json_data['data']['cards']
            for card in cards:
                if 'mblog' in card:
                    mblog = card['mblog']
                    if 'isTop' in mblog and mblog['isTop']: continue
                    mid = int(mblog['mid'])
                    date = parse_date(mblog['created_at'])
                    mark = {'mid': mid, 'bid': mblog['bid'], 'date': date, 'text': mblog['text']}
                    amount += 1
                    # if compare(limit[0], '>', [mid, date]): exceed = True
                    # if compare(limit[0], '>', [mid, date]) or compare(limit[1], '<', [mid, date]): continue
                    if 'pics' in mblog:
                        for index, pic in enumerate(mblog['pics'], 1):
                            if 'large' in pic:
                                resources.append(merge({'url': pic['large']['url'], 'index': index, 'type': 'photo'}, mark))
                                # print(pic)
                    elif 'page_info' in mblog and video:
                        if 'media_info' in mblog['page_info']:
                            media_info = mblog['page_info']['media_info']
                            streams = [media_info[key] for key in ['mp4_720p_mp4', 'mp4_hd_url', 'mp4_sd_url', 'stream_url'] if key in media_info and media_info[key]]
                            if streams:
                                resources.append(merge({'url': streams.pop(0), 'type': 'video'}, mark))
                                # print(streams)
            print_fit('{} {}(#{})'.format('analysing weibos...' if empty < aware and not exceed else 'finish analysis', progress(amount, total), page), pin = True)
            page += 1
        finally:
            time.sleep(interval)

    print_fit('\npractically scan {} weibos, get {} {}'.format(amount, len(resources), 'resources' if video else 'pictures'))
    return resources

def format_name(item):
    item['name'] = re.sub(r'\?\S+$', '', re.sub(r'^\S+/', '', item['url']))

    def safeify(name):
        template = {u'\\': u'＼', u'/': u'／', u':': u'：', u'*': u'＊', u'?': u'？', u'"': u'＂', u'<': u'＜', u'>': u'＞', u'|': u'｜'}
        for illegal in template:
            name = name.replace(illegal, template[illegal])
        return name

    def substitute(matched):
        key = matched.group(1).split(':')
        if key[0] not in item:
            return ':'.join(key)
        elif key[0] == 'date':
            return item[key[0]].strftime(key[1]) if len(key) > 1 else str(item[key[0]])
        elif key[0] == 'index':
            return str(item[key[0]]).zfill(int(key[1] if len(key) > 1 else '0'))
        elif key[0] == 'text':
            return re.sub(r'<.*?>', '', item[key[0]]).strip()
        else:
            return str(item[key[0]])

    return safeify(re.sub(r'{(.*?)}', substitute, '{name}'))

def download(url, path, overwrite):
    # print(url, path, overwrite)
    if os.path.exists(path) and not overwrite: return True
    try:
        response = request_fit('GET', url, stream = True)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size = 512):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(e)
        if os.path.exists(path): os.remove(path)
        return False
    else:
        return True



user_input = input('苏生不惑提示你请输入微博uid:')#1744395855
users = [user_input]

base = os.path.join(os.getcwd(), 'weibo')

if not os.path.exists(base): make_dir(base)

cookie_input = input('请输入微博cookie:')

token = 'SUB={}'.format(cookie_input) if cookie_input else None
pool = concurrent.futures.ThreadPoolExecutor(max_workers = 3)

for number, user in enumerate(users, 1):
    
    print_fit('{}/{} {}'.format(number, len(users), time.ctime()))
    
    if re.search(r'^\d{10}$', user):
        nickname = uid_to_nickname(user)
        uid = user
    else:
        nickname = user
        uid = nickname_to_uid(user)

    if not nickname or not uid:
        print_fit('invalid account {}'.format(user))
        print_fit('-' * 30)
        continue

    print_fit('{} {}'.format(nickname, uid))
    
    try:
        resources = get_resources(uid, 1, 1, [0, int(time.time())])
    except KeyboardInterrupt:
        quit()

    album = os.path.join(base, nickname)
    if resources and not os.path.exists(album): make_dir(album)

    retry = 0
    while resources and retry <= 3:
        
        if retry > 0: print_fit('automatic retry {}'.format(retry))

        total = len(resources)
        tasks = []
        done = 0
        failed = {}
        cancel = False

        for resource in resources:
            path = os.path.join(album, format_name(resource))
            tasks.append(pool.submit(download, resource['url'], path, False))

        while done != total:
            try:
                done = 0
                for index, task in enumerate(tasks):
                    if task.done() == True:
                        done += 1
                        if task.cancelled(): continue
                        elif task.result() == False: failed[index] = ''
                    elif cancel:
                        if not task.cancelled(): task.cancel()
                time.sleep(0.5)
            except KeyboardInterrupt:
                cancel = True
            finally:
                if not cancel:
                    print_fit('{} {}'.format(
                        'downloading...' if done != total else 'all tasks done',
                        progress(done, total, True)
                    ), pin = True)
                else:
                    print_fit('waiting for cancellation... ({})'.format(total - done), pin = True) 

        if cancel: quit()
        print_fit('\nsuccess {}, failure {}, total {}'.format(total - len(failed), len(failed), total))

        resources = [resources[index] for index in failed]
        retry += 1

    for resource in resources: print_fit('{} failed'.format(resource['url']))
    print_fit('-' * 30)

quit('下载完成')
