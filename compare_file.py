import os
import argparse
# python .\compare_file.py html pdf
def get_file_names(directory):
    """获取指定目录下的所有文件名列表"""
    if not os.path.isdir(directory):
        raise ValueError(f"目录不存在: {directory}")
    
    # 获取目录中所有文件和子目录的名称
    entries = os.listdir(directory)
    # 只保留文件（排除子目录）
    files = [os.path.splitext(os.path.basename(entry))[0] for entry in entries if os.path.isfile(os.path.join(directory, entry))]
    return set(files)

def compare_directories(dir1, dir2):
    """对比两个目录中的文件名差异"""
    # 获取两个目录中的文件名集合
    files1 = get_file_names(dir1)
    files2 = get_file_names(dir2)
    
    # 计算差异
    only_in_dir1 = files1 - files2  # 只在第一个目录中存在的文件
    only_in_dir2 = files2 - files1  # 只在第二个目录中存在的文件
    in_both = files1 & files2       # 两个目录中都存在的文件
    
    return only_in_dir1, only_in_dir2, in_both

def print_results(dir1, dir2, only1, only2, both):
    """打印对比结果"""
    print(f"对比目录: {dir1} 和 {dir2}\n")
    
    print(f"只存在于 {dir1} 中的文件 ({len(only1)} 个):")
    # for file in sorted(only1):
    #     print(f"  - {file}")
    
    print(f"\n只存在于 {dir2} 中的文件 ({len(only2)} 个):")
    for file in sorted(only2):
        print(f"  - {file}")
    
    print(f"\n两个目录中都存在的文件 ({len(both)} 个):")
    # for file in sorted(both):
    #     print(f"  - {file}")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='对比两个目录中的文件名差异')
    parser.add_argument('dir1', help='第一个目录的路径')
    parser.add_argument('dir2', help='第二个目录的路径')
    args = parser.parse_args()
    
    try:
        # 比较目录
        only_in_dir1, only_in_dir2, in_both = compare_directories(args.dir1, args.dir2)
        # 打印结果
        print_results(args.dir1, args.dir2, only_in_dir1, only_in_dir2, in_both)
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
