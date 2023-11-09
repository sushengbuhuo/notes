import csv
from openpyxl import Workbook

# 读取 CSV 文件
csv_file = '公众号历史文章数据.csv'

# 创建一个新的工作簿
wb = Workbook()
ws = wb.active

# 打开 CSV 文件并将数据写入 XLSX 工作表
with open(csv_file, 'r', encoding='utf-8') as f:
    for row in csv.reader(f):
        ws.append(row)

# 保存 XLSX 文件
xlsx_file = 'output.xlsx'
wb.save(xlsx_file)

print(f'CSV 文件 "{csv_file}" 已成功转换为 XLSX 文件 "{xlsx_file}"')
import pandas as pd

# 读取 CSV 文件
df = pd.read_csv(csv_file)

# 将数据保存为 XLSX 文件
xlsx_file = 'output2.xlsx'
df.to_excel(xlsx_file, index=False)

print(f'CSV 文件 "{csv_file}" 已成功转换为 XLSX 文件 "{xlsx_file}"')
