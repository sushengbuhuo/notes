from docx import Document
import os
def merge_documents(output_filename, *input_filenames):
    output = Document()
    for root, dirs, files in os.walk('.'):
        for filename in files:
            print(filename)
            if not filename.endswith(".docx"):
                continue
            sub_doc = Document(filename)
            for element in sub_doc.element.body:
                output.element.body.append(element)
 
    output.save(output_filename)
 
# 使用函数合并文档
merge_documents('微博内容.docx')