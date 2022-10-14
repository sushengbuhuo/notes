import requests,re,json,time,pandas as pd
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = ''
headers={
	'referer':'http://mds.nmdis.org.cn/pages/tidalCurrent.html',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 FirePHP/0.7.4',
	'Content-Type':'application/json;charset=UTF-8'
}
writer = pd.ExcelWriter('数据.xlsx')
df = pd.DataFrame() 
dates = []
result =[]
df['days'] = pd.date_range(start='2021-01-01', end='2022-01-02')
dic = {}
def result(i,ids):
    print('开始',i)
    for index,value in df['days'].items():
        # time.sleep(1)
    # print(index,value.strftime('%Y-%m'))
    # dates.append(value.strftime('%Y-%m-%d'))
        try:
            res = requests.post(url, headers=headers, data=json.dumps({'serchdate':value.strftime('%Y-%m-%d'),'sitecode':i})).json()
            time.sleep(1)
            dic[value.strftime('%Y-%m-%d')] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            if res['data']:
               dic[value.strftime('%Y-%m-%d')] = [res['data'][0]['filedata']['a0'],res['data'][0]['filedata']['a1'],res['data'][0]['filedata']['a2'],res['data'][0]['filedata']['a3'],res['data'][0]['filedata']['a4'],res['data'][0]['filedata']['a5'],res['data'][0]['filedata']['a6'],res['data'][0]['filedata']['a7'],res['data'][0]['filedata']['a8'],res['data'][0]['filedata']['a9'],res['data'][0]['filedata']['a10'],res['data'][0]['filedata']['a11'],res['data'][0]['filedata']['a12'],res['data'][0]['filedata']['a13'],res['data'][0]['filedata']['a14'],res['data'][0]['filedata']['a15'],res['data'][0]['filedata']['a16'],res['data'][0]['filedata']['a17'],res['data'][0]['filedata']['a18'],res['data'][0]['filedata']['a19'],res['data'][0]['filedata']['a20'],res['data'][0]['filedata']['a21'],res['data'][0]['filedata']['a22'],res['data'][0]['filedata']['a23']]
        except Exception as e:
           print(e)
        df2 = pd.DataFrame(data=dic,index=['0:00','1:00','2:00','3:00','4.00','5:00','6:00','7:00','8:00','9:00','10.00','11:00','12:00','13:00','14:00','15:00','16.00','17:00','18:00','19:00','20:00','21:00','22.00','23:00'])
        print(dic)
        df2.to_excel(writer,f'{ids[i]}数据')

ids={'T147':'黄埔'}
print(ids.keys())
for i in ids.keys():
    result(i,ids)
writer.save()
writer.close()

# with pd.ExcelWriter(r'test.xls') as writer:
#     df1.to_excel(writer, sheet_name='df1')
#     df2.to_excel(writer, sheet_name='df2')