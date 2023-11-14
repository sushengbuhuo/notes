import pandas as pd
from win32com import client as wc
import os
import os.path as osp
from glob import glob 
 
 
df_list=[]
 
file_list=glob('*.xls')
for file_name in file_list:
    for sheet in pd.read_excel(file_name,sheet_name=None).keys():#遍历子表名称
        df=pd.read_excel(file_name,sheet_name=sheet,header=4)#读取sheet页
        #删除空值列
        na_cols=df.columns[df.isna().all()].tolist()#先找出有空值的列
        df.drop(labels=na_cols,axis=1,inplace=True)#再删除列
        #删除空值行，保留至多有两个的空值行，其他行都删除
        df.dropna(thresh=2,inplace=True,axis=0)
        #if df.applymap(lambda x: '交维结果' in str(x)).any().any():#查询excel表里是否有交维结果字符串
            #print(file_name)
        df_list.append(df)
 
 
df_all=pd.concat(df_list)#拼接合并
df_grouped=df_all.groupby('')[['','']].sum()#分组求和
with pd.ExcelWriter('合并.xlsx',engine='openpyxl',mode='w') as writer:#新建1个xlsx工作表
        df_all.to_excel(writer,sheet_name='',index=None)#保存多个sheet子表在工作表
        df_grouped.to_excel(writer,sheet_name='')#保存多个sheet子表在工作表