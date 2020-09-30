import requests
import time
import pandas as pd

#https://github.com/zhangzhe532/icodebugs/blob/master/DataAnalysis/%E6%8B%89%E5%8B%BE%E7%BD%91%E5%88%86%E6%9E%90/lagou_get_data.py
#https://github.com/JustDoPython/python-examples/blob/master/doudou/2020-07-13-lagou/app.py
#https://github.com/JustDoPython/python-examples/blob/master/doudou/2020-07-13-lagou/analysis.py
#http://www.justdopython.com/2020/07/13/lagou/
def get_page(num):
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    # 构造请求头
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Referer': "https://www.lagou.com/jobs/list_%E7%AE%97%E6%B3%95%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput="
    }
    form_data = {
        'first': 'true',
        'pn': num,
        'kd': '算法工程师'
    }
    # %E7%AE%97%E6%B3%95%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E5%85%A8%E5%9B%BD 指算法工程师五个汉字，可以自定义构造其他搜索关键字
    url_start = 'https://www.lagou.com/jobs/list_%E7%AE%97%E6%B3%95%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
    s = requests.Session()  # 创建一个session对象
    s.get(url_start, headers=headers, timeout=3)
    cookie = s.cookies#为了获取网站cookie
    response = s.post(url, data=form_data, headers=headers,
                      cookies=cookie, timeout=3)
    response.raise_for_status()##如果状态不是200抛出异常
    response.encoding = response.apparent_encoding#encoding:从HTTP header中猜测的响应内容编码方式 apparent_encoding:从内容分析出的响应内容编码方式（备选编码方式）
    return response.json()


def parse_page(job_json):
    job_list = job_json['content']['positionResult']['result']
    company_info = []
    # for job in job_list:
    #     job_info = []
    #     job_info.append(job['companyFullName'])  # 公司全称
    #     job_info.append(job['companySize'])  # 规模
    #     job_info.append(job['financeStage'])  # 融资情况
    #     job_info.append(job['district'])  # 位置
    #     job_info.append(job['positionName'])  # 职位
    #     job_info.append(job['workYear'])  # 工作经验要求
    #     job_info.append(job['education'])  # 学历
    #     job_info.append(job['salary'])  # 工资
    #     job_info.append(job['positionAdvantage'])  # 福利待遇
    #     company_info.append(job_info)  # 把所有职位情况添加到网页信息page_info
    for item in job_list:
        dict = {
            'city': item['city'],
            'industryField': item['industryField'],
            'education': item['education'],
            'workYear': item['workYear'],
            'salary': item['salary'],
            'firstType': item['firstType'],
            'secondType': item['secondType'],
            'thirdType': item['thirdType'],
            # list
            'skillLables': ','.join(item['skillLables']),
            'companyLabelList': ','.join(item['companyLabelList'])
        }
        company_info.append(dict)
    return company_info


if __name__ == '__main__':
    all_company = []
    # for page_num in range(1, 3):
    #     job_json = get_page(page_num)
    #     result = parse_page(job_json)
    #     all_company += result
    #     print('已抓取{}页, 总职位数:{}'.format(page_num, len(all_company)))
    #     time.sleep(10)  # 如果速度太快可能被网站识别出爬虫
    # print(all_company)
    # df = pd.DataFrame(all_company)
    df = pd.read_csv('拉钩.csv')
    print(df.head(5))
    citys_value_counts = df['city'].value_counts()
    top = 15
    citys = list(citys_value_counts.head(top).index)#索引
    city_counts = list(citys_value_counts.head(top))#值

    bar = (
        Bar()
            .add_xaxis(citys)
            .add_yaxis("", city_counts)
    )
    bar.render('lagou.html')
    pie = (
        Pie()
        .add("", [list(z) for z in zip(citys, city_counts)])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    )
    # bar.render_notebook()
    # df = pd.DataFrame(data=all_company, columns=['公司', '规模', '融资', '位置', '职位', '经验', '学历', '工资', '福利'])
    # 指定csv数据存储路径
    # df.to_csv('拉钩.csv', index=False,encoding="utf_8_sig")
