import requests
import pandas as pd
import multitasking
import os
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77',
    'Accept': '*/*',
    'Referer': 'http://fundf10.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}
@multitasking.task
def download_file(fund_code: str, url: str, filename: str, file_type='.pdf'):
    '''
    根据文件名、文件直链等参数下载文件
    '''
    fund_code = str(fund_code)
    if not os.path.exists(fund_code):
        os.mkdir(fund_code)
    response = requests.get(url, headers=headers)
    path = f'{fund_code}/{filename}{file_type}'
    with open(path, 'wb') as f:
        f.write(response.content)
    if os.path.getsize(path) == 0:
        os.remove(path)
        return
    print(filename+file_type, '下载完毕')


def get_pdf_by_fund_code(fund_code: str):
    '''
    根据基金代码获取其全部 pdf 报告

    Parameters
    ----------
    fund_code :6 位基金代码

    '''

    params = (
        ('fundcode', fund_code),
        ('pageIndex', '1'),
        ('pageSize', '20000'),
        ('type', '3'),
    )

    response = requests.get(
        'http://api.fund.eastmoney.com/f10/JJGG', headers=headers, params=params)

    base_link = 'http://pdf.dfcfw.com/pdf/H2_{}_1.pdf'
    for item in response.json()['Data']:
        title = item['TITLE']
        download_url = base_link.format(item['ID'])
        download_file(fund_code, download_url, title)
    multitasking.wait_for_tasks()
    print(f'{fund_code} 的 pdf 全部下载完毕并存储在文件夹 {fund_code} 里面')
def get_public_dates(code: str) -> list:
    '''
    获取基金持仓的公开日期
    -
    参数
    -
        code 基金代码
    返回
        公开持仓的日期列表
    '''
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Accept': '*/*',
        'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }
    params = (
        ('FCODE', code),
        ('MobileKey', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
        ('OSVersion', '14.3'),
        ('appVersion', '6.3.8'),
        ('cToken', 'a6hdhrfejje88ruaeduau1rdufna1e--.6'),
        ('deviceid', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
        ('passportid', '3061335960830820'),
        ('plat', 'Iphone'),
        ('product', 'EFund'),
        ('serverVersion', '6.3.6'),
        ('version', '6.3.8'),
    )

    json_response = requests.get(
        'https://fundmobapi.eastmoney.com/FundMNewApi/FundMNIVInfoMultiple', headers=headers, params=params).json()
    if json_response['Datas'] is None:
        return []
    return json_response['Datas']


def get_inverst_postion(code: str, date=None) -> pd.DataFrame:
    '''
    根据基金代码跟日期获取基金持仓信息https://zhuanlan.zhihu.com/p/350600670
    -
    参数

        code 基金代码
        date 公布日期 形如 '2020-09-31' 默认为 None，得到最新公布的数据
    返回

        持仓信息表格

    '''
    EastmoneyFundHeaders = {
        'User-Agent': 'EMProjJijin/6.2.8 (iPhone; iOS 13.6; Scale/2.00)',
        'GTOKEN': '98B423068C1F4DEF9842F82ADF08C5db',
        'clientInfo': 'ttjj-iPhone10,1-iOS-iOS13.6',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'fundmobapi.eastmoney.com',
        'Referer': 'https://mpservice.com/516939c37bdb4ba2b1138c50cf69a2e1/release/pages/FundHistoryNetWorth',
    }
    params = [
        ('FCODE', code),
        ('MobileKey', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
        ('OSVersion', '14.3'),
        ('appType', 'ttjj'),
        ('appVersion', '6.2.8'),
        ('deviceid', '3EA024C2-7F22-408B-95E4-383D38160FB3'),
        ('plat', 'Iphone'),
        ('product', 'EFund'),
        ('serverVersion', '6.2.8'),
        ('version', '6.2.8'),
    ]
    if date is not None:
        params.append(('DATE', date))
    params = tuple(params)

    response = requests.get('https://fundmobapi.eastmoney.com/FundMNewApi/FundMNInverstPosition',
                            headers=EastmoneyFundHeaders, params=params)
    rows = []
    stocks = response.json()['Datas']['fundStocks']

    columns = {
        'GPDM': '股票代码',
        'GPJC': '股票简称',
        'JZBL': '持仓占比(%)',
        'PCTNVCHG': '较上期变化(%)',
    }
    if stocks is None:
        return pd.DataFrame(rows, columns=columns.values())

    df = pd.DataFrame(stocks)
    df = df[list(columns.keys())].rename(columns=columns)
    return df


if __name__ == "__main__":
    # 6 位基金代码
    code = '161725'
    # 创建 excel 文件
    writer = pd.ExcelWriter(f'{code}.xlsx')
    # 获取基金公开持仓日期
    # public_dates = get_public_dates(code)
    # # 遍历全部公开日期，获取该日期公开的持仓信息
    # for date in public_dates:
    #     print(f'正在获取 {date} 的持仓信息......')
    #     df = get_inverst_postion(code, date=date)
    #     # 添加到 excel 表格中
    #     df.to_excel(writer, index=None, sheet_name=date)
    #     print(f'{date} 的持仓信息获取成功')
    # # 保存 excel 文件
    # writer.save()
    # print(f'{code} 的历史持仓信息已保存到文件 {code}.xlsx 中')
    fund_code = '110011'
    get_pdf_by_fund_code(fund_code)