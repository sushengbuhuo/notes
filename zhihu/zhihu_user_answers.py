from __future__ import annotations
import multitasking
import requests
from tqdm import tqdm
import pandas as pd
from retry import retry
from bs4 import BeautifulSoup
import time
#pip install tqdm requests multitasking retry bs4 pandas https://www.zhihu.com/people/la-ge-lang-ri-96-69/posts
def get_uid_by_url_token(url_token: str) -> str:
    '''
    根据知乎用户 url_token 获取其 uid

    Parameters
    ----------
    url_token : 知乎用户 url_token
        例如主页为:https://www.zhihu.com/people/la-ge-lang-ri-96-69 的用户
        其 url_token 为: la-ge-lang-ri-96-69

        注意,此参数类型为字符串

    Return
    ------
    str : 用户 uid
    '''
    headers = {
        'authority': 'www.zhihu.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
        'x-requested-with': 'fetch',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarycwskcLmf85lBwPKR',
        'accept': '*/*',
        'origin': 'https://www.zhihu.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhihu.com/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    url = 'https://api.zhihu.com/people/'+url_token
    response = requests.get(url, headers=headers)
    uid = response.json()['id']
    return uid


@retry(tries=3)
def get_user_answers(url_token: str, max_count: int = 100000) -> pd.DataFrame:
    '''
    获取用户的回答脚本数据列表

    Parameters
    ----------
    url_token : 知乎用户 url_token
        例如主页为:https://www.zhihu.com/people/la-ge-lang-ri-96-69 的用户
        其 url_token 为: la-ge-lang-ri-96-69

        注意,此参数类型为字符串

    max_count : 限制获取的最大回答数(默认为 100000)

    Return
    ------
    DataFrame : 包含用户回答数据的 DataFrame


    '''
    headers = {

        'User-Agent': 'osee2unifiedRelease/4318 osee2unifiedReleaseVersion/7.7.0 Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'X-APP-BUILD-VERSION': '4318',
        'x-app-bundleid': 'com.zhihu.ios',
        'X-APP-ZA': 'OS=iOS&Release=14.5&Model=iPhone10,1&VersionName=7.7.0&VersionCode=4318&Width=750&Height=1334&DeviceType=Phone&Brand=Apple&OperatorType=46009',

    }

    operations = {
        '作者': ['author', lambda x: x['name']],
        '作者id': ['author', lambda x: x['id']],
        '作者token': ['author', lambda x:x['url_token']],
        '回答点赞数': ['voteup_count', lambda x: x],
        '回答时间': ['created_time', lambda x:time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x))],
        '更新时间': ['updated_time', lambda x:time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x))],
        '回答id': ['url', lambda x: x.split('/')[-1]],
        '问题id': ['question', lambda x: x['id']],
        '问题内容': ['question', lambda x:x['title']]
    }
    try:
        uid = get_uid_by_url_token(url_token)
    except:
        return pd.DataFrame(columns=operations.keys())
    bar: tqdm = None
    offset = 0
    limit = 20
    dfs: list[pd.DataFrame] = []
    url = f'https://api.zhihu.com/members/{uid}/answers'
    while 1:
        params = (
            ('limit', f'{limit}'),
            ('offset', f'{offset}'),
        )

        response = requests.get(
            url, headers=headers, params=params)

        if response.json().get('paging') is None:
            return pd.DataFrame(columns=operations.keys())
        total = response.json()['paging']['totals']
        if bar is None:
            bar = tqdm(total=total, desc='正在获取知乎回答')
        bar.update(limit)
        data = response.json().get('data')
        raw_df = pd.DataFrame(data)
        if len(raw_df) == 0\
                or offset >= total \
                or offset > max_count:
            break
        df = pd.DataFrame(columns=operations.keys())
        for new_column, (old_column, operation) in operations.items():
            df[new_column] = raw_df[old_column].apply(operation)
        dfs.append(df)
        offset += 20

    bar.close()
    df = pd.concat(dfs)
    return df


def get_answer_content(qid: str, aid) -> str:
    '''
    根据回答ID和问题ID获取回答内容

    Parameters
    ----------
    qid : 问题ID
    aid : 回答ID
    例如一个回答链接为: https://www.zhihu.com/question/438404653/answer/1794419766

    其 qid 为 438404653

    其 aid 为 1794419766

    注意,这两个参数均为字符串

    Return
    ------
    str : 回答内容
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1',
        'Host': 'www.zhihu.com',
    }
    url = f'https://www.zhihu.com/question/{qid}/answer/{aid}'
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    content = " ".join([p.text.strip() for p in soup.find_all('p')])
    return content


def save_answers_to_csv(url_token: str, csv_path: str, max_count: int = 10000) -> None:
    '''
    根据用户 url_token 获取用户回答数据,兵保存到 csv 文件中

    Parameters
    ----------
    url_token : 知乎用户 url_token
        例如主页为:https://www.zhihu.com/people/la-ge-lang-ri-96-69 的用户
        其 url_token 为: la-ge-lang-ri-96-69

        注意,此参数类型为字符串

    csv_path : 待保存的回答数据 csv 路径
        例如: '回答数据.csv'

    max_count : 限制获取的最大回答数(可选,默认为 100000)

    Return
    ------
    DataFrame:包含用户多个回答数据的 DataFrame
    '''
    df = get_user_answers(url_token, max_count=max_count)
    if len(df) == 0:
        print('请重试')
        return
    content_list = []

    @retry(tries=3)
    @multitasking.task
    def start(qid: str, aid: str):
        content = get_answer_content(qid, aid)
        content_list.append(content)
        bar.update()
    bar = tqdm(total=len(df), desc='获取知乎回答内容')
    for row in df.iloc:
        qid, aid = row['问题id'], row['回答id']
        start(qid, aid)
    multitasking.wait_for_tasks()
    df['回答内容'] = content_list
    df.to_csv(csv_path, encoding='utf-8-sig', index=None)
    bar.close()
    print(f'知乎用户 {url_token} 的回答数据已保存到文件:{csv_path}')


if __name__ == "__main__":
    # 知乎用户的 url_token
    # 例如主页为 : https://www.zhihu.com/people/la-ge-lang-ri-96-69 的用户
    # 其 url_token 为 la-ge-lang-ri-96-69
    url_token = input('请输入知乎用户id：')
    # 回答数据保存路径
    csv_path = '知乎回答数据.csv'
    # 调用函数获取数据
    save_answers_to_csv(url_token, csv_path)