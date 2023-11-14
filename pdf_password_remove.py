import os
from PyPDF2 import PdfWriter, PdfReader
#pip install PyPDF2 pip install pikepdf
def get_reader(filename, password):
    try:
        old_file = open(filename, 'rb')
    except Exception as err:
        print('文件打开失败！' + str(err))
        return None
 
    # 创建读实例
    pdf_reader = PdfReader(old_file, strict=False)
 
    # 解密操作
    if pdf_reader.is_encrypted:
        if password is None:
            print('%s文件被加密，需要密码！' % filename)
            return None
        else:
            if pdf_reader.decrypt(password) != 1:
                print('%s密码不正确！' % filename)
                return None
 
    if old_file in locals():
        old_file.close()
 
    return pdf_reader
 
def decrypt_pdf(filename, password, decrypted_folder):
    """
    将加密的文件进行解密，并生成一个无需密码的pdf文件
    :param filename: 原先加密的pdf文件
    :param password: 对应的密码
    :param decrypted_folder: 解密后放置文件的文件夹路径
    :return:
    """
    # 生成一个Reader和Writer
    pdf_reader = get_reader(filename, password)
    if pdf_reader is None:
        return
 
    pdf_writer = PdfWriter()
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
 
    # 获取解密后的文件名
    file_name, _ = os.path.splitext(filename)
 
    if decrypted_folder is not None:
        decrypted_filepath = os.path.join(decrypted_folder, os.path.basename(file_name) + ".pdf")
    else:
        print('生成文件失败，请给出解密后放置文件夹')
        return
 
    # 写入新文件
    with open(decrypted_filepath, 'wb') as decrypted_file:
        pdf_writer.write(decrypted_file)
        print('解密成功' + decrypted_filepath)
 
# 获取文件夹中的pdf文件路径
def get_pdf_paths(folder_path):
    pdf_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                pdf_paths.append(pdf_path)
    return pdf_paths
 
 
pdf_path = input('请输入要解密的pdf或含pdf文件夹路径：')
# pdf_path = '文件夹或文件路径'
password = input('请输入密码：')
# password = '密码'
decrypted_folder = input('请输入解密文件夹：')
# decrypted_folder = '解密文件夹'
 
if os.path.isdir(pdf_path):
    pdf_paths = get_pdf_paths(pdf_path)
    for path in pdf_paths:
        decrypt_pdf(path, password, decrypted_folder)  # 修改此处，传递解密后文件存放的文件夹路径
else:
    _, extension = os.path.splitext(pdf_path)
    if extension.lower() == '.pdf':
        decrypt_pdf(pdf_path, password, decrypted_folder)
    else:
        print('文件非pdf')