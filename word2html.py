import mammoth,time
from markdownify import markdownify
# 转存Word文档内的图片https://zmister.com/archives/1601.html
def convert_img(image):
    with image.open() as image_bytes:
        file_suffix = image.content_type.split("/")[1]
        path_file = "./{}.{}".format(str(time.time()),file_suffix)
        with open(path_file, 'wb') as f:
            f.write(image_bytes.read())
    return {"src":path_file}
def word2html():
    # 读取Word文件 pip install mammoth markdownify
    with open(r"test.docx" ,"rb") as docx_file:
        # 转化Word文档为HTML
        result = mammoth.convert_to_html(docx_file,convert_image=mammoth.images.img_element(convert_img))
        # 获取HTML内容
        html = result.value
        # 转化HTML为Markdown
        md = markdownify(html,heading_style="ATX")
        print(md)
        with open("./test.html",'w',encoding='utf-8') as html_file,open("./test.md","w",encoding='utf-8') as md_file:
            html_file.write(html)
            md_file.write(md)
        messages = result.messages
        print(messages)
"""
　　pypandoc.convert_file(source_file, to, format=None, extra_args=(), encoding='utf-8',
                 outputfile=None, filters=None, verify_format=True)
    参数说明： 直接用 pandoc 就可以了，pypandoc 是隔着 python 用 pandoc
    source_file:源文件路径
    to：输入应转换为的格式；可以是'pypandoc.get_pandoc_formats（）[1]`之一
    format：输入的格式；将从具有已知文件扩展名的源_文件推断；可以是“pypandoc.get_pandoc_formats（）[1]”之一（默认值= None)
    extra_args：要传递给pandoc的额外参数（字符串列表）(Default value = ())
    encoding：文件或输入字节的编码 (Default value = 'utf-8')
    outputfile：转换后的内容输出路径+文件名，文件名的后缀要和to的一致，如果没有，则返回转换后的内容（默认值= None)
    filters – pandoc过滤器，例如过滤器=['pandoc-citeproc']
    verify_format：是否对给定的格式参数进行验证，（pypandoc根据文件名截取后缀格式，与用户输入的format进行比对）
     
    pypandoc.convert_text(source, to, format, extra_args=(), encoding='utf-8',
                     outputfile=None, filters=None, verify_format=True):
    参数说明：
    source：字符串       
    其余和canvert_file()相同      
 
"""
def html2word(name):
    import pypandoc #https://github.com/jgm/pandoc  convenr_text(string)
    # output = pypandoc.convert_file(f'{name}.html', 'docx', outputfile=f"{name}.docx")
    output = pypandoc.convert_file(f'.md', 'html','md', outputfile=f".html")
html2word('') 