import csv
from datetime import datetime


def sort_csv_by_time(input_file, output_file, time_column):
    try:
        with open(input_file, 'r', newline='', encoding='UTF8') as infile:
            reader = csv.DictReader(infile)
            data = list(reader)

        def get_time(row):
            try:
                return datetime.strptime(row[time_column], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None

        data.sort(key=get_time, reverse=True)

        with open(output_file, 'w', newline='', encoding='UTF8') as outfile:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"数据已根据 {time_column} 倒序排序并保存到 {output_file}")
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_file}")
    except KeyError:
        print(f"错误：文件中不存在 {time_column} 列")
    except Exception as e:
        print(f"发生未知错误：{e}")


if __name__ == "__main__":
    input_file = '冀时微博.csv'
    output_file = '冀时微博数据.csv'
    time_column = '发布时间'
    sort_csv_by_time(input_file, output_file, time_column)
    