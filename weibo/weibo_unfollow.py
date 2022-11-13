import requests
from jsonpath import jsonpath
import os
 
 
def get_first_followContent(headers):
    """
    这个方法里面 会先获取 总共的关注数量 一页大概50个 如果第二页也超过50个 则进行下一页 以此类推
    :return: https://www.52pojie.cn/thread-1676538-1-1.html
    """
 
    r = requests.get('https://weibo.com/ajax/profile/followContent?sortType=all?sortType=all', headers=headers)
 
    # print(r.json())
    follow_list = jsonpath(r.json(), "$.data.follows.users.id")
    print(len(follow_list))
    total_number = int(jsonpath(r.json(), "$.data.follows.total_number")[0])  # 总共关注的数量
    page = int(total_number / 50)
 
    if page * 50 < total_number:
        page = page + 1
    if total_number < 50:
        return follow_list  # 如果关注的人低于50个 一般是只有一页直接返回关注ID列表
 
    for i in range(1, page):
        if i + 1 * 50 > total_number:
            break
 
        url = f'https://weibo.com/ajax/profile/followContent?page={i + 1}&next_cursor=50'
        print(url)
 
        req = requests.get(url, headers=headers).json()
 
        result = jsonpath(req, "$.data.follows.users.id")
 
        follow_list = follow_list + result
 
    return follow_list
 
 
def get_white_list():
    if not os.path.exists('不取消关注列表.txt'):
        with open('不取消关注列表.txt', 'w') as f:
            f.write('请将不取消关注列表 通过ID 换行的方式写入')
            f.close()
        return None
    return open('不取消关注列表.txt', 'r', encoding='utf-8').read().split('\n')
 
 
def destroyBatch(headers, destroylist):
    for i in destroylist:
        result = requests.post('https://weibo.com/ajax/friendships/destory', json={"uid": "%s" % i}, headers=headers)
 
        print(result.json())
 
 
if __name__ == '__main__':
    headers = {
 
    }
    # 请求头请自行复制
    result = [str(x) for x in get_first_followContent(headers)]
 
    white_lists = get_white_list()  # 获取白名单
 
    if white_lists is not None:
        for j in white_lists:
            if j not in result:
                continue
            result.remove(j)
 
    destroyBatch(headers, result)
    # get_first_followContent()