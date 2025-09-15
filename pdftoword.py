import os,shutil,tempfile
from pdf2docx import Converter
from docx import Document
from docx.shared import Inches
from zipfile import ZipFile
from xml.etree import ElementTree as ET

def extract_images(docx_path, output_dir):
    """从Word文件中提取所有图片"""
    images = []
    with ZipFile(docx_path, 'r') as zip_ref:
        # 解析文档关系
        rels_path = 'word/_rels/document.xml.rels'
        if rels_path in zip_ref.namelist():
            rels_data = zip_ref.read(rels_path)
            rels_tree = ET.fromstring(rels_data)
            
            # 命名空间处理
            ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}
            
            # 提取所有图片
            for rel in rels_tree.findall('r:Relationship', namespaces=ns):
                if rel.attrib['Type'].endswith('image'):
                    img_path = rel.attrib['Target']
                    img_name = os.path.basename(img_path)
                    img_data = zip_ref.read(f'word/{img_path}')
                    
                    # 保存图片到临时目录
                    img_save_path = os.path.join(output_dir, img_name)
                    with open(img_save_path, 'wb') as f:
                        f.write(img_data)
                    
                    images.append((rel.attrib['Id'], img_save_path))
    
    return images
def merge_word_files(input_files, output_file):
    merged_doc = Document()
    
    for file_num, file_path in enumerate(input_files, 1):
        try:
            # 创建临时目录存储提取的图片
            with tempfile.TemporaryDirectory() as temp_dir:
                # 提取当前文档中的图片
                images = extract_images(file_path, temp_dir)
                img_id_to_path = {img_id: path for img_id, path in images}
                
                # 打开当前Word文件
                doc = Document(file_path)
                
                # 为每个文件添加一个标题
                # if len(input_files) > 1:
                #     merged_doc.add_heading(f"文档 {file_num}: {os.path.basename(file_path)}", level=2)
                
                # 处理段落和图片
                for para in doc.paragraphs:
                    new_para = merged_doc.add_paragraph()
                    
                    # 检查段落中是否有图片
                    for run in para.runs:
                        # 复制文本和样式
                        new_run = new_para.add_run(run.text)
                        new_run.bold = run.bold
                        new_run.italic = run.italic
                        new_run.underline = run.underline
                        new_run.font.color.rgb = run.font.color.rgb
                        new_run.font.size = run.font.size
                        new_run.font.name = run.font.name
                    
                    # 处理段落中的图片
                    para_xml = para._p
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                          'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
                    
                    for drawing in para_xml.findall('.//w:drawing', namespaces=ns):
                        img_elem = drawing.find('.//r:embed', namespaces=ns)
                        if img_elem is not None and 'r:id' in img_elem.attrib:
                            img_id = img_elem.attrib['r:id']
                            if img_id in img_id_to_path:
                                # 插入图片
                                merged_doc.add_picture(img_id_to_path[img_id], width=Inches(6))
                                # 添加一个空段落分隔图片和文本
                                merged_doc.add_paragraph()
            
            # 复制表格
            for table in doc.tables:
                # 添加表格
                new_table = merged_doc.add_table(rows=len(table.rows), cols=len(table.columns))
                
                # 复制表格内容和样式
                for i, row in enumerate(table.rows):
                    for j, cell in enumerate(row.cells):
                        new_cell = new_table.cell(i, j)
                        new_cell.text = cell.text
                        # 简单复制单元格样式（实际应用中可能需要更复杂的样式处理）
                        new_cell.paragraphs[0].style = cell.paragraphs[0].style
            
            # 在文档之间添加分页符
            if file_num != len(input_files):
                merged_doc.add_page_break()
                
            print(f"已合并: {file_path}")
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")
    
    merged_doc.save(output_file)
    print(f"所有文档已成功合并到: {output_file}")
def get_word_files_from_directory(directory):
    word_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.docx') and not filename.startswith('~$'):  # 排除临时文件
            word_files.append(os.path.join(directory, filename))
    # 按文件名排序
    word_files.sort()
    return word_files
def do_convert(output_folder):
    print("正在转换为Word...")
    num = 0
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith(".pdf"):
                print(name)
                try:
                    base_name = os.path.splitext(os.path.basename(name))[0]
                    output_path = os.path.join(output_folder, f"{base_name}.docx")
                    cv = Converter(name)
                    cv.convert(output_path)
                    cv.close()
                    num += 1
                except Exception as e:
                    if not os.path.exists('failed'):
                        os.mkdir('failed')
                    shutil.copy(name, 'failed')
                    print('转换失败',e,name)
    print(f"转换完成: {num} 个文件")

def do_merge(input_directory):
	input_files = get_word_files_from_directory(input_directory)
	merge_word_files(input_files, 'word文档合集.docx')
do_convert('word')
# do_merge('word')