import os
from PIL import Image
import pillow_heif  # 轻量级HEIC处理库 pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow pillow-heif

def convert_heic_to_jpg(input_folder, output_folder):
    """将HEIC文件转换为JPG，保存到指定文件夹"""
    # 初始化pillow-heif
    pillow_heif.register_heif_opener()  # 注册HEIC格式支持

    # 处理路径
    input_folder = input_folder.strip()
    output_folder = output_folder.strip()

    # 检查输入文件夹
    if not os.path.exists(input_folder):
        print(f"错误：输入文件夹 '{input_folder}' 不存在")
        return

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    converted_count = 0
    skipped_count = 0

    # 遍历文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.heic', '.heif')):
            heic_path = os.path.join(input_folder, filename)
            jpg_filename = os.path.splitext(filename)[0] + '.jpg'
            jpg_path = os.path.join(output_folder, jpg_filename)

            # 跳过已存在的JPG
            if os.path.exists(jpg_path):
                print(f"已跳过：{filename}（JPG已存在）")
                skipped_count += 1
                continue

            try:
                # 用Pillow直接打开HEIC（因为注册了opener）
                with Image.open(heic_path) as img:
                    # 保存为JPG（质量95）
                    img.save(jpg_path, "JPEG", quality=95)
                print(f"已转换：{filename} -> 保存至 {output_folder}")
                converted_count += 1
            except Exception as e:
                print(f"转换失败：{filename} - 错误：{str(e)}")

    print("\n转换完成！")
    print(f"成功转换：{converted_count} 个文件")
    print(f"已跳过：{skipped_count} 个文件")

if __name__ == "__main__":
    # 输入文件夹（HEIC所在路径）
    input_folder = r"D:\hec"  # 直接粘贴路径

    # 输出文件夹（JPG保存路径）
    output_folder = r"D:\jpg_output"  # 自定义路径

    convert_heic_to_jpg(input_folder, output_folder)