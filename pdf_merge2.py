from PIL import Image, ImageFont, ImageDraw
import re
import os
from PyPDF2 import PdfReader, PdfWriter
 
 
class PDFMerge:
    @staticmethod
    def get_mark_img(text, size=30):
        width = len(text) * size
        mark = Image.new(mode='RGB', size=(
            width, size + 20), color=(255, 255, 255))
        ImageDraw.Draw(im=mark) \
            .text(xy=(0, 0),
                  text=text,
                  fill="black",
                  font=ImageFont.truetype('msyhbd.ttc', size=size))
        mark.save("watermark.pdf", "PDF", resolution=100.0, save_all=True)
        return mark
 
    @staticmethod
    def windows_files_sort(files):
        files.sort(key=lambda s: [(s, int(n))
                                  for s, n in re.findall('(\D+)(\d+)', f'a{s}0')])
 
    def __merge_pdf_in(self, path, parent=None):
        files = []
        dirs = []
        for file in os.listdir(path):
            file = os.path.join(path, file)
            if os.path.isfile(file):
                if file.endswith(".pdf"):
                    files.append(file)
            elif os.path.isdir(file):
                if os.path.basename(file) != "__MACOSX":
                    dirs.append(file)
        PDFMerge.windows_files_sort(files)
        PDFMerge.windows_files_sort(dirs)
 
        for pdf_file in files:
            pdf_reader = PdfReader(pdf_file)
            pdf_file = os.path.basename(pdf_file)
            pageCount = len(pdf_reader.pages)
            print(pdf_file, pageCount, self.pagenum_total)
            for page in pdf_reader.pages:
                page.compress_content_streams()
                self.pdf_writer.add_page(page)
            self.pdf_writer.add_outline_item(
                pdf_file[:pdf_file.rfind(".")], self.pagenum_total, parent=parent)
            self.pagenum_total += pageCount
        for path in dirs:
            title = os.path.basename(path)
            print(title, self.pagenum_total)
            PDFMerge.get_mark_img(title)
            watermark = PdfReader('watermark.pdf').pages[0]
            self.pdf_writer.add_page(watermark)
            os.remove('watermark.pdf')
            parent_id = self.pdf_writer.add_outline_item(
                title, self.pagenum_total, parent=parent)
            self.pagenum_total += 1
            self.__merge_pdf_in(path, parent=parent_id)
 
    def merge_pdf(self, path, out_name):
        self.pagenum_total = 0
        self.pdf_writer = PdfWriter()
        self.__merge_pdf_in(path)
        # os.remove('watermark.pdf')
        print("总页数：", self.pagenum_total)
        with open(out_name, "wb") as outputfile:
            self.pdf_writer.write(outputfile)
        print("PDF文件合并完成")
 
 
if __name__ == '__main__':
    pdfmerge = PDFMerge()
    pdfmerge.merge_pdf(r"pdf", "merge.pdf")