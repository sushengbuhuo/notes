# !/usr/bin/env python
# coding=utf-8`
#https://www.52pojie.cn/thread-2071308-1-1.html
import asyncio
import os
import random
import time
import warnings
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlencode
 
import kaleido
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import requests
from plotly.subplots import make_subplots
 
warnings.filterwarnings("ignore")
 
BASE_DIR = Path("D:/")
CSV_DIR  = BASE_DIR / "StockBaseData"
if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)
 
 
def BOLL(CLOSE, N=20, P=2):  # BOLL指标，布林带
    MID = MA(CLOSE, N)
    UPPER = MID + STD(CLOSE, N) * P
    LOWER = MID - STD(CLOSE, N) * P
    return RD(UPPER), RD(MID), RD(LOWER)
 
 
def EMA(S, N):  # 指数移动平均,为了精度 S>4*N  EMA至少需要120周期
    df = pd.Series(S).ewm(span=N, adjust=False).mean().values
    return df
 
 
def MA(S, N):  # 求序列的N日简单移动平均值，返回序列
    return pd.Series(S).rolling(N).mean().values
 
 
def MACD(CLOSE, SHORT=12, LONG=26, M=9): # MACD指标
    DIF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIF, M)
    MACD = (DIF - DEA) * 2
    return RD(DIF), RD(DEA), RD(MACD)
 
 
# 资金流量与比率指标
def MFI(df):
    df['PP'] = (df['high'] + df['low'] + df['close']) / 3
    LP = df['PP'].shift(1).fillna(df['PP'].iloc[0])  # 使用第一个有效的典型价格填充NaN值
    MF = df['PP'] * df['volume'] * 100
 
    # 计算正向和负向资金流量
    PosMF = MF.where(df['PP'] > LP, 0.0).rolling(window=14).sum()
    NegMF = MF.where(df['PP'] <= LP, 0.0).rolling(window=14).sum()
 
    # 避免除以0的情况
    MFR = PosMF / NegMF.replace(0, 1)  # 如果NegMF是0，则用1替代以避免除零错误
    MFI = 100 - (100 / (1 + MFR))
 
    df['MFI'] = MFI.round(4)
    df['MAMFI'] = EMA(df['MFI'], 6).round(4)
 
    return df
 
def KDJ(CLOSE, HIGH, LOW, N=9, M1=3, M2=3):  # KDJ指标
    RSV = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    K = EMA(RSV, (M1 * 2 - 1))
    D = EMA(K, (M2 * 2 - 1))
    J = K * 3 - D * 2
    return K, D, J
 
 
def HHV(S, N):  # HHV,支持N为序列版本
    # type: (np.ndarray, Optional[int,float, np.ndarray]) -> np.ndarray
    """
    HHV(C, 5)  # 最近5天收盘最高价
    """
    if isinstance(N, (int, float)):
        return pd.Series(S).rolling(N).max().values
    else:
        res = np.repeat(np.nan, len(S))
        for i in range(len(S)):
            if (not np.isnan(N[i])) and N[i] <= i + 1:
                res[i] = S[i + 1 - N[i]:i + 1].max()
        return res
 
 
def LLV(S, N):  # LLV,支持N为序列版本
    # type: (np.ndarray, Optional[int,float, np.ndarray]) -> np.ndarray
    """
    LLV(C, 5)  # 最近5天收盘最低价
    """
    if isinstance(N, (int, float)):
        return pd.Series(S).rolling(N).min().values
    else:
        res = np.repeat(np.nan, len(S))
        for i in range(len(S)):
            if (not np.isnan(N[i])) and N[i] <= i + 1:
                res[i] = S[i + 1 - N[i]:i + 1].min()
        return res
 
 
def RD(N, D=3):   return np.round(N, D)  # 四舍五入取3位小数
 
 
def REF(S, N=1):  # 对序列整体下移动N,返回序列(shift后会产生NAN)
    return pd.Series(S).shift(N).values
 
 
def STD(S, N):  # 求序列的N日标准差，返回序列
    return pd.Series(S).rolling(N).std(ddof=0).values
 
 
def SUM(S, N):  # 对序列求N天累计和，返回序列    N=0对序列所有依次求和
    return pd.Series(S).rolling(N).sum().values if N > 0 else pd.Series(S).cumsum().values
 
 
def TDX_SAR(High, Low, iAFStep=2, iAFLimit=20):    # type: (np.ndarray, np.ndarray, int, int) -> np.ndarray
    """  通达信SAR算法,和通达信SAR对比完全一致   by: jqz1226, 2021-12-18
    :param High: 最高价序列
    :param Low: 最低价序列
    :param iAFStep: AF步长
    :param iAFLimit: AF极限值
    :return: SAR序列
    """
    af_step = iAFStep / 100;     af_limit = iAFLimit / 100
    SarX = np.zeros(len(High))   # 初始化返回数组
 
    # 第一个bar
    bull = True
    af = af_step
    ep = High[0]
    SarX[0] = Low[0]
    # 第2个bar及其以后
    for i in range(1, len(High)):
        # 1.更新：hv, lv, af, ep
        if bull:  # 多
            if High[i] > ep:  # 创新高
                ep = High[i]
                af = min(af + af_step, af_limit)
        else:  # 空
            if Low[i] < ep:  # 创新低
                ep = Low[i]
                af = min(af + af_step, af_limit)
        # 2.计算SarX
        SarX[i] = SarX[i - 1] + af * (ep - SarX[i - 1])
 
        # 3.修正SarX
        if bull:
            SarX[i] = max(SarX[i - 1], min(SarX[i], Low[i], Low[i - 1]))
        else:
            SarX[i] = min(SarX[i - 1], max(SarX[i], High[i], High[i - 1]))
 
        # 4. 判断是否：向下跌破，向上突破
        if bull:  # 多
            if Low[i] < SarX[i]:  # 向下跌破，转空
                bull = False
                tmp_SarX = ep  # 上阶段的最高点
                ep = Low[i]
                af = af_step
                if High[i - 1] == tmp_SarX:  # 紧邻即最高点
                    SarX[i] = tmp_SarX
                else:
                    SarX[i] = tmp_SarX + af * (ep - tmp_SarX)
        else:  # 空
            if High[i] > SarX[i]:  # 向上突破, 转多
                bull = True
                ep = High[i]
                af = af_step
                SarX[i] = min(Low[i], Low[i - 1])
    # end for
    return SarX
 
 
def get_k_history(stock_code):
    """
    功能获取k线数据（Akshare函数）
    Parameters
    ----------
    code : 6 位股票代码
    beg: 开始日期 例如 20200101
    end: 结束日期 例如 20200201
    klt: k线间距 默认为 101 即日k
        klt:1 1 分钟
        klt:5 5 分钟
        klt:101 日
        klt:102 周
    fqt: 复权方式
        不复权 : 0
        前复权 : 1
        后复权 : 2
    Return
    ------
    DateFrame : 包含股票k线数据
    """
 
    beg = '19700101'
    end = "22240101"
    klt = 101  # 日线数据
    fqt = 1  # 前复权
    EastmoneyKlines = {'f51': 'date', 'f52': 'open', 'f53': 'close', 'f54': 'high', 'f55': 'low', 'f56': 'volume',
                       'f57': 'amount', 'f58': 'AMP', 'f59': 'pctChg', 'f60': 'prcChg', 'f61': 'turn', }
    EastmoneyHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
                        'Accept': '*/*',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Referer': 'http://quote.eastmoney.com/center/gridlist.html', }
    fields = list(EastmoneyKlines.keys())
    columns = list(EastmoneyKlines.values())
    fields2 = ",".join(fields)
    market_code = 1 if stock_code.startswith("6") else 0
    params = (
        ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'), ('fields2', fields2), ('beg', beg), ('end', end),
        ('rtntype', '6'), ('secid', f"{market_code}.{stock_code}"), ('klt', f'{klt}'), ('fqt', f'{fqt}'),)
    base_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
    url = base_url + '?' + urlencode(params)
    while True:
        try:
            response = requests.get(url, headers=EastmoneyHeaders, timeout=50)
            if response.status_code == 200:
                print("Stock Base Data Requested successfully.")
                break
            else:
                print(f"Unexpected status code: {response.status_code}")
                time.sleep(random.randint(1, 3))
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            print("Error:", e)
            time.sleep(random.randint(1, 3))
 
    json_response = response.json()
    if json_response is None:
        print("JSON响应为空")
        return
    else:
        data = json_response.get('data')
        if data is None:
            print("未找到 'data' 键")
            return
        else:
            name = data.get('name')
            if name is None:
                print("未找到 'name' 键")
                return
 
    klines = data['klines']
    rows = [kline.split(',') for kline in klines]
 
    df_dk = pd.DataFrame(rows, columns=columns)
    if len(df_dk) < 1:
        print(stock_code, name, "没有数据。。。。。。")
        return
 
    df_dk.insert(1, 'code', stock_code)
    df_dk.insert(2, 'name', name)
 
    csv_path = CSV_DIR / f"{stock_code}.csv"
    df_dk.to_csv(csv_path, mode="w", header=True, encoding="gbk", index=False)
 
    return
 
 
def plot_stock_k_line(stock_code, name):
    csv_path = CSV_DIR / f"{stock_code}.csv"
    df_dk = pd.read_csv(csv_path, encoding="gbk", dtype={'code': str, 'name': str})
    df_dk['MA5'] = df_dk['close'].rolling(5).mean().round(4)
    df_dk['MA10'] = df_dk['close'].rolling(10).mean().round(4)
    df_dk['MA20'] = df_dk['close'].rolling(20).mean().round(4)
    df_dk['Vol5'] = df_dk['turn'].rolling(5).mean().round(4)
    df_dk['Vol21'] = df_dk['turn'].rolling(21).mean().round(4)
    df_dk['sar'] = TDX_SAR(df_dk.high.to_numpy(), df_dk.low.to_numpy(), iAFStep=2, iAFLimit=20).round(4)
    df_dk[['DIF', 'DEA', 'MACD']] = pd.DataFrame(MACD(df_dk.close)).T
    df_dk[['UPPER', 'MID', 'LOWER']] = pd.DataFrame(BOLL(df_dk.close)).T
    df_dk[['K', 'D', 'J']] = pd.DataFrame(KDJ(df_dk.close, df_dk.high, df_dk.low)).T
    MFI(df_dk)
    # 计算狄马克指标之TD序列
    prices = df_dk['close'].values
    indices = [0] * len(prices)
    for i in range(4, len(prices)):
        if prices[i] > prices[i - 4]:
            if indices[i - 1] > 0:
                indices[i] = indices[i - 1] + 1
            else:
                indices[i] = 1
        elif prices[i] < prices[i - 4]:
            if indices[i - 1] < 0:
                indices[i] = indices[i - 1] - 1
            else:
                indices[i] = -1
    df_dk['TDS'] = indices    #取两年的数据。画图
    df_dk = df_dk.tail(504).reset_index(drop=True)
    fig = make_subplots(rows=5, cols=1, vertical_spacing=0.004, shared_xaxes=False,
                             horizontal_spacing=0.00, print_grid=False, subplot_titles=(""),
                             row_heights=[0.60, 0.10, 0.10, 0.10, 0.10],
                             specs=[[{"secondary_y": True},],
                                    [{"secondary_y": True},],
                                    [{"secondary_y": True},],
                                    [{"secondary_y": True},],
                                    [{"secondary_y": True},]
                                    ])
 
    df_dk['used'] = False
    close_shift = df_dk["close"].shift()
    high_thr = (close_shift * 1.1).round(2)
    low_thr = (close_shift * 0.9).round(2)
    # 绘制跌停K线, 黑色柱, 标注向下的黑色箭头
    df_dk_filtered = df_dk[df_dk['close'] <= low_thr].dropna(subset=['date', 'open', 'high', 'low', 'close'])
    df_dk.loc[df_dk_filtered.index, 'used'] = True
    if len(df_dk_filtered) > 0:
        fig.add_trace(
            go.Candlestick(x=df_dk_filtered["date"], open=df_dk_filtered["open"], high=df_dk_filtered["high"],
                           low=df_dk_filtered["low"], close=df_dk_filtered["close"],
                           increasing={'line': {'color': 'black'}, 'fillcolor': 'black'},
                           decreasing={'line': {'color': 'black'}, 'fillcolor': 'black'}, name='跌停日K线',
                           line=dict(width=.5), opacity=1, zorder=1, hoverinfo='skip', showlegend=False),
                           row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_dk_filtered["date"], y=df_dk_filtered["low"] * 0.98, mode='markers', showlegend=False,
                   hoverinfo='skip', marker=dict(color='black', opacity=0.75, size=8, symbol='triangle-down')),
                   row=1, col=1)
    # 绘制涨停K线, 紫色柱, 标注向上的紫色箭头
    df_dk_filtered = df_dk[(df_dk['close'] >= high_thr) & (~df_dk['used'])].dropna(
        subset=['date', 'open', 'high', 'low', 'close'])
    df_dk.loc[df_dk_filtered.index, 'used'] = True
    if len(df_dk_filtered) > 0:
        fig.add_trace(
            go.Candlestick(x=df_dk_filtered["date"], open=df_dk_filtered["open"], high=df_dk_filtered["high"],
                           low=df_dk_filtered["low"], close=df_dk_filtered["close"],
                           increasing={'line': {'color': 'rgba(255,0,255,0.8)'}, 'fillcolor': 'rgba(255,0,255,0.8)'},
                           decreasing={'line': {'color': 'red'}, 'fillcolor': 'red'}, name='涨停日K线',
                           line=dict(width=.5), opacity=1, zorder=1, hoverinfo='skip', showlegend=False),
                           row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_dk_filtered["date"], y=df_dk_filtered["high"] * 1.02, mode='markers', showlegend=False,
                   hoverinfo='skip', marker=dict(color='rgba(255,0,255,0.8)', opacity=0.75, size=8,
                   symbol='triangle-up')), row=1, col=1)
    # 绘制涨停炸板K线, 橘色柱, 标注向上的橘色箭头
    df_dk_filtered = df_dk[
        (df_dk['high'] != df_dk['close']) & (df_dk['high'] >= high_thr) & (~df_dk['used'])].dropna(
        subset=['date', 'open', 'high', 'low', 'close'])
    df_dk.loc[df_dk_filtered.index, 'used'] = True
    if len(df_dk_filtered) > 0:
        fig.add_trace(
            go.Candlestick(x=df_dk_filtered["date"], open=df_dk_filtered["open"], high=df_dk_filtered["high"],
                           low=df_dk_filtered["low"], close=df_dk_filtered["close"],
                           increasing={'line': {'color': 'rgba(255,140,0,1)'}, 'fillcolor': 'rgba(255,140,0,1)'},
                           decreasing={'line': {'color': 'olive'}, 'fillcolor': 'olive'}, name='涨停炸板日K线',
                           line=dict(width=.5), opacity=1, zorder=1, hoverinfo='skip', showlegend=False),
                           row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_dk_filtered["date"], y=df_dk_filtered["high"] * 1.02, mode='markers', showlegend=False,
                   hoverinfo='skip', marker=dict(color='rgba(255,140,0,1)', opacity=0.75, size=8,
                   symbol='triangle-up')), row=1, col=1)
    # 绘制跌停开板K线, 蓝色柱, 标注向下的蓝色箭头
    df_dk_filtered = df_dk[
        (df_dk['low'] != df_dk['close']) & (df_dk['low'] <= low_thr) & (~df_dk['used'])].dropna(
        subset=['date', 'open', 'high', 'low', 'close'])
    df_dk.loc[df_dk_filtered.index, 'used'] = True
    if len(df_dk_filtered) > 0:
        fig.add_trace(
            go.Candlestick(x=df_dk_filtered["date"], open=df_dk_filtered["open"], high=df_dk_filtered["high"],
                           low=df_dk_filtered["low"], close=df_dk_filtered["close"],
                           increasing={'line': {'color': 'blue'}, 'fillcolor': 'rgba(255,99,71,0.3)'},
                           decreasing={'line': {'color': 'rgba(65,105,255,1)'}, 'fillcolor': 'rgba(65,105,255,1)'},
                           name='跌停开板日K线', line=dict(width=.5), opacity=1, zorder=1, hoverinfo='skip',
                           showlegend=False), row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df_dk_filtered["date"], y=df_dk_filtered["low"] * 0.98, mode='markers', showlegend=False,
                   hoverinfo='skip', marker=dict(color='rgba(65,105,255,1)', opacity=0.75, size=8,
                   symbol='triangle-down')), row=1, col=1)
    # 其余K线
    df_dk_filtered = df_dk[~df_dk['used']]
    fig.add_trace(
        go.Candlestick(x=df_dk_filtered["date"], open=df_dk_filtered["open"], high=df_dk_filtered["high"],
                       low=df_dk_filtered["low"], close=df_dk_filtered["close"],
                       increasing={'line': {'color': 'red'}, 'fillcolor': 'rgba(255,99,71,0.3)'},
                       decreasing={'line': {'color': 'green'}, 'fillcolor': 'green'}, name='个股日K线',
                       line=dict(width=.5), opacity=1, zorder=1, hoverinfo='skip', showlegend=False),
                       row=1, col=1)
    # 绘制5日、10日、20日移动平均线
    fig.add_trace(go.Scatter(x=df_dk['date'], y=df_dk['MA5'], mode='lines', name='MA5',
                             line=dict(width=.75, color='red'), opacity=0.75,
                             hoverinfo='skip', showlegend=False, zorder=1), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_dk['date'], y=df_dk['MA10'], mode='lines', name='MA10',
                             line=dict(width=.75, color='blue'), opacity=0.75,
                             hoverinfo='skip', showlegend=False, zorder=1), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_dk['date'], y=df_dk['MA20'], mode='lines', name='MA20',
                             line=dict(width=.75, color='teal'), opacity=0.75,
                             hoverinfo='skip', showlegend=False, zorder=1), row=1, col=1)
    # 绘制SAR散点图
    df_dk['color'] = np.empty(len(df_dk))
    df_dk.color[df_dk.close >= abs(df_dk.sar)] = 'red'
    df_dk.color[df_dk.close < abs(df_dk.sar)] = 'green'
    fig.add_trace(go.Scatter(x=df_dk["date"], y=abs(df_dk["sar"]), mode='markers', showlegend=False, hoverinfo='skip',
                             marker=dict(color=df_dk.color, opacity=0.75, size=4, symbol='circle')), row=1, col=1)
    # 布林带
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['UPPER'], mode='lines', name='up', line=dict(width=.75, color='royalblue'),
                   hoverinfo='skip', showlegend=False, fill=None), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['MID'], mode='lines', name='mid',
                   line=dict(width=.75, color='limegreen'), hoverinfo='skip',
                   showlegend=False, fill='tonextx', fillcolor='rgba(191,0,255,0.1)'), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['LOWER'], mode='lines', name='lower', line=dict(width=.75, color='magenta'),
                   hoverinfo='skip', showlegend=False, fill='tonextx', fillcolor='rgba(0,191,255,0.1)'), row=1, col=1)
    # 绘制昨日倍量, 橙色五星
    pattern = df_dk[(df_dk['turn'] >= 2 * df_dk['turn'].shift()) & (df_dk['turn'] < 3 * df_dk['turn'].shift())]
    fig.add_trace(
        go.Scatter(x=pattern["date"], y=pattern["high"] * 1.03, mode='markers', showlegend=False, hoverinfo='skip',
                   marker=dict(color='orange', opacity=1, size=10, symbol='star')), row=1, col=1)
    # 绘制昨日三倍量及以上, 紫色五星
    pattern = df_dk[(df_dk['turn'] >= 3 * df_dk['turn'].shift())]
    fig.add_trace(
        go.Scatter(x=pattern["date"], y=pattern["high"] * 1.03, mode='markers', showlegend=False, hoverinfo='skip',
                   marker=dict(color='magenta', opacity=1, size=10, symbol='star')), row=1, col=1)
    # 标注狄马克指标之TD序列
    df_dk_filtered = df_dk[df_dk['TDS'] < 0]
    fig.add_trace(go.Scatter(
        x=df_dk_filtered['date'],  # X 轴数据
        y=df_dk_filtered['low'] * 0.99,  # 文字标注的位置（在最低价下方）
        text=df_dk_filtered['TDS'],  # 文字内容
        mode='text',  # 仅显示文字
        textposition='bottom center',  # 文字位置
        textfont=dict(size=6, color='black', family='SimHei'),  # 文字样式
        name='Text Labels',
        zorder=2,
        hoverinfo='skip'
    ), row=1, col=1)
    df_dk_filtered = df_dk[df_dk['TDS'] > 0]
    fig.add_trace(go.Scatter(
        x=df_dk_filtered['date'],  # X 轴数据
        y=df_dk_filtered['high'] * 1.01,  # 文字标注的位置（在最高价上方）
        text=df_dk_filtered['TDS'],  # 文字内容
        mode='text',  # 仅显示文字
        textposition='bottom center',  # 文字位置
        textfont=dict(size=6, color='red', family='SimHei'),  # 文字样式
        name='Text Labels',
        zorder=2,
        hoverinfo='skip'
    ), row=1, col=1)    # X轴
    dt_all = pd.date_range(start=df_dk['date'].min(), end=df_dk['date'].max(), freq='D')
    dt_all = pd.to_datetime(dt_all).strftime("%Y-%m-%d")
    trade_date = pd.to_datetime(df_dk['date']).dt.strftime("%Y-%m-%d")
    dt_breaks = dt_all[~dt_all.isin(trade_date)].tolist()
    start_date = pd.to_datetime(df_dk['date'].iloc[0]) - timedelta(days=2)
    end_date = pd.to_datetime(df_dk['date'].iloc[-1]) + timedelta(days=2)
    for row_count in range(1, 6):
        fig.update_xaxes(range=[start_date, end_date],
                         rangebreaks=[dict(values=dt_breaks)], nticks=len(df_dk['date']),
                         showticklabels=(row_count in [1, 5]), domain=[0, 1],
                         showline=(row_count in [1, 5]), linecolor='black', linewidth=1, ticks="inside", showgrid=False,
                         rangeslider_visible=False, dtick="M1", tickformat="%b %y", ticklabelmode="period",
                         row=row_count, col=1)
    fig.update_layout(title="",
                      margin=dict(l=0, r=0, b=0, t=0, pad=0),
                      font=dict(family='SimHei', size=10, color="black"),
                      plot_bgcolor='aliceblue',
                      paper_bgcolor='aliceblue',
                      showlegend=False, dragmode=False, hovermode=False, width=3840, height=2160)
    # 第二个子图， 换手率
    conditions = [
        df_dk["close"] >= high_thr,
        df_dk["close"] <= low_thr,
        (df_dk["high"] > df_dk["close"]) & (df_dk["high"] >= high_thr),
        (df_dk["low"] < df_dk["close"]) & (df_dk["low"] <= low_thr),
        df_dk["pctChg"] > 0,
        df_dk["pctChg"] <= 0,
    ]
    colors = [
        "rgba(255, 0, 255, 0.75)",  # magenta（涨停）
        "rgba(0, 0, 0, 0.75)",  # black（跌停）
        "gold",  # 涨停炸板
        "royalblue",  # 跌停开板
        "rgba(255, 0, 0, 0.75)",  # red
        "rgba(34, 139, 34, 0.75)",  # green
    ]
    diag = np.select(conditions, colors, default="")
    df_dk["diag"] = diag
    fig.add_trace(go.Bar(x=df_dk['date'], y=df_dk['turn'],
                         marker=dict(color=df_dk.diag, line=dict(color=df_dk.diag, width=.75)),
                         hoverinfo='skip', showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_dk['date'], y=df_dk['Vol5'], mode='lines', name='Vol5',
                             line=dict(width=.75, color='red'), opacity=0.75,
                             hoverinfo='skip', showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_dk['date'], y=df_dk['Vol21'], mode='lines', name='Vol21',
                             line=dict(width=.75, color='blue'), opacity=0.75,
                             hoverinfo='skip', showlegend=False), row=2, col=1)
    # 第三个子图， 资金流量MFI
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['MFI'], mode='lines+markers', name='MFI',
                   line=dict(width=1, color='red'), marker=dict(color='red', size=2),
                   opacity=1, hoverinfo='skip', showlegend=False), row=3, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['MAMFI'], mode='lines+markers', name='MAMFI',
                   line=dict(width=1, color='blue'), marker=dict(color='blue', size=2), opacity=1,
                   hoverinfo='skip', showlegend=False), row=3, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=[20 for i in range(len(df_dk))], mode='lines', name='基准线20',
                   line=dict(width=1, color='black'), opacity=0.75, hoverinfo='skip', showlegend=False),
        row=3, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=[80 for i in range(len(df_dk))], mode='lines', name='基准线80',
                   line=dict(width=1, color='black'), opacity=0.75, hoverinfo='skip', showlegend=False),
                   row=3, col=1)
    fig.update_yaxes(dtick=10, showgrid=False, ticklabelposition="outside", range=[0, 100], row=3, col=1)
    # 第四个子图， MACD
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['DIF'], mode='lines', name='DIF', line=dict(width=.75, color='blue'),
                   hoverinfo='skip', showlegend=False), row=4, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['DEA'], mode='lines', name='DEA', line=dict(width=.75, color='red'),
                   showlegend=False), row=4, col=1)
    df_dk['color'] = np.empty(len(df_dk))
    df_dk.color[df_dk.MACD >= 0] = 'rgba(255, 0, 0, 0.75)'
    df_dk.color[df_dk.MACD < 0] = 'rgba(34, 139, 34, 0.75)'
    fig.add_trace(go.Bar(x=df_dk['date'], y=df_dk['MACD'],
                         marker=dict(color=df_dk.color, line=dict(color=df_dk.color, width=.75)),
                         opacity=0.75, hoverinfo='skip', showlegend=False), row=4, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=[0 for i in range(len(df_dk))], mode='lines', name='基准线0',
                   line=dict(width=1, color='black'), opacity=1, hoverinfo='skip', showlegend=False),
                   row=4, col=1)
    # 第五个子图， KDJ
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['K'], mode='lines', name='', line=dict(width=1, color='red'),
                   opacity=1, hoverinfo='skip', showlegend=False), row=5, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['D'], mode='lines', name='D', line=dict(width=1, color='blue'),
                   opacity=1, hoverinfo='skip', showlegend=False), row=5, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=df_dk['J'], mode='lines', name='D', line=dict(width=1, color='purple'),
                   opacity=1, hoverinfo='skip', showlegend=False), row=5, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=[20 for i in range(len(df_dk))], mode='lines', name='基准线20',
                   line=dict(width=1, color='green'), opacity=0.75, hoverinfo='skip', showlegend=False),
                   row=5, col=1)
    fig.add_trace(
        go.Scatter(x=df_dk['date'], y=[80 for i in range(len(df_dk))], mode='lines', name='基准线80',
                   line=dict(width=1, color='red'), opacity=0.75, hoverinfo='skip', showlegend=False),
                   row=5, col=1)
    fig.update_yaxes(dtick=10, showgrid=False, ticklabelposition="outside", range=[0, 100], row=5, col=1)
    fig.add_annotation(
        text=f"{stock_code} {name} 日K线图",
        xref="x domain",
        yref="y domain",
        x=0.022,
        y=0.98,
        showarrow=False,
        font=dict(
            family="SimHei",
            size=22,
            color="black"),
        row=1, col=1)
 
    latest_dk = df_dk.iloc[-1]
    fig.add_annotation(
        text=f"资金流量指标 MFI：{latest_dk['MFI']:.3f}, MAMFI：{latest_dk['MAMFI']:.3f}",
        xref="x domain",
        yref="y domain",
        x=0.99,
        y=1.05,
        showarrow=False,
        font=dict(
            family="SimHei",
            size=12,
            color="black"
        ),
        row=3, col=1
    )
    fig.add_annotation(
        text=f"MACD指标 DIF：{latest_dk['DIF']:.3f}, DEA：{latest_dk['DEA']:.3f}, MACD：{latest_dk['MACD']:.3f}",
        xref="x domain",
        yref="y domain",
        x=0.99,
        y=1.05,
        showarrow=False,
        font=dict(
            family="SimHei",
            size=12,
            color="black"
        ),
        row=4, col=1
    )
    fig.add_annotation(
        text=f"KDJ指标 K：{latest_dk['K']:.3f}, D：{latest_dk['D']:.3f}, J：{latest_dk['J']:.3f}",
        xref="x domain",
        yref="y domain",
        x=0.99,
        y=1.05,
        showarrow=False,
        font=dict(
            family="SimHei",
            size=12,
            color="black"
        ),
        row=5, col=1
    )
    # fig.show()
    output_path = os.path.join(CSV_DIR, f"{stock_code}{name}.png")
 
    #  pio.write_image(fig, output_path, validate=False, engine="kaleido")
 
    async def export_figures():
        async with kaleido.Kaleido(timeout=180) as k:
            fig_object = {
                "fig": fig,
                "path": output_path,
                "opts": {"format": "png", "width": 3840, "height": 2160, "scale": 3}
            }
            await k.write_fig_from_object([fig_object])
 
    asyncio.run(export_figures())
 
    return
 
 
if __name__ == '__main__':
    get_k_history("002976")
    plot_stock_k_line("002976", "瑞玛精密")