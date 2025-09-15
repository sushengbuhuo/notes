import os
import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.font as tkfont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
 
 
class WatermarkThread(threading.Thread):
    """加水印线程，避免界面冻结"""
 
    def __init__(self, pdf_folder, output_folder, watermark_text, font_size, angle, spacing, alpha, column,progress_queue):
        super().__init__()
        self.pdf_folder = pdf_folder
        self.output_folder = output_folder
        self.watermark_text = watermark_text
        self.font_size = font_size
        self.angle = angle
        self.spacing = spacing
        self.alpha = alpha
        self.column = column
        self.progress_queue = progress_queue
        self.is_running = True
        self.daemon = True
 
    def run(self):
        total_files = 0
        processed_files = 0
 
        # 计算 PDF 文件总数
        if self.pdf_folder:
            for filename in os.listdir(self.pdf_folder):
                if filename.lower().endswith(".pdf"):
                    total_files += 1
 
        # 遍历文件并处理
        if self.pdf_folder:
            for filename in os.listdir(self.pdf_folder):
                if not self.is_running:
                    break
 
                if filename.lower().endswith(".pdf"):
                    pdf_path = os.path.join(self.pdf_folder, filename)
 
                    processed_files += 1
                    progress = int((processed_files / total_files) * 100) if total_files > 0 else 0
                    self.progress_queue.put((progress, f"处理中: {filename}"))
 
                    watermarked_pdf = self.add_watermark(pdf_path)
                    if watermarked_pdf:
                        self.progress_queue.put((progress, f"已添加水印: {watermarked_pdf}"))
                    else:
                        self.progress_queue.put((progress, f"处理失败: {filename}"))
 
        self.progress_queue.put((100, "全部完成！"))
 
    def stop_process(self):
        """点击停止按钮时调用"""
        self.is_running = False
 
 
 
    def add_watermark(self, pdf_path):
        """在 PDF 中添加水印"""
        try:
             
            # 注册中文字体（只需注册一次，可以放外面，但放这里也没问题）
            pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttc'))
            # 创建临时水印 PDF
            watermark_pdf = os.path.join(self.output_folder, "watermark_temp.pdf")
            c = canvas.Canvas(watermark_pdf, pagesize=letter)
            width, height = letter
 
            c.setFont("SimSun", self.font_size)  # 用宋体支持中文
            c.setFillColor(colors.grey, alpha=self.alpha)  # 淡灰色 + 透明度
            c.saveState()
            c.rotate(self.angle)
 
            # 行列循环打印水印
 
            row_spacing = self.spacing       # 行间距（上下）
            col_spacing = self.column                # 列间距（左右），可以做成参数
 
            for y in range(-500, int(height * 2), row_spacing):
                for x in range(-500, int(width * 2), col_spacing):
                    c.drawString(x, y, self.watermark_text)
             
            c.restoreState()
            c.save()
 
            # 合并水印和原 PDF
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            wm_reader = PdfReader(watermark_pdf)
 
            for page in reader.pages:
                page.merge_page(wm_reader.pages[0])
                writer.add_page(page)
 
            out_pdf = os.path.join(
                self.output_folder,
                os.path.splitext(os.path.basename(pdf_path))[0] + "_watermarked.pdf"
            )
             
            out_pdf = os.path.normpath(out_pdf)
             
            with open(out_pdf, "wb") as f:
                writer.write(f)
 
            os.remove(watermark_pdf)  # 删除临时文件
            return out_pdf
 
        except Exception as e:
            self.progress_queue.put((0, f"加水印失败: {e}"))
            return None
 
 
class PDFWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.watermark_thread = None
        self.progress_queue = queue.Queue()
        self.initUI()
        self.check_queue()
 
    def initUI(self):
        self.root.title('PDF加水印工具')
        self.root.geometry('600x520')
        # 修改全局默认字体为 宋体 11号
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="宋体", size=11)
 
        # 让 ttk 里的控件也跟随默认字体
        root.option_add("*Font", default_font)
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
 
        # 文件夹选择
        folder_group = ttk.LabelFrame(main_frame, text="文件夹选择")
        folder_group.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        folder_group.columnconfigure(1, weight=1)
 
        ttk.Label(folder_group, text="PDF文件夹:").grid(row=0, column=0, sticky=tk.W)
        self.pdf_folder_var = tk.StringVar()
        pdf_entry = ttk.Entry(folder_group, textvariable=self.pdf_folder_var, width=50)
        pdf_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(folder_group, text="选择", command=self.browse_pdf_folder).grid(row=0, column=2, padx=5)
 
        ttk.Label(folder_group, text="输出文件夹:").grid(row=1, column=0, sticky=tk.W)
        self.output_folder_var = tk.StringVar()
        output_entry = ttk.Entry(folder_group, textvariable=self.output_folder_var, width=50)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(folder_group, text="选择", command=self.browse_output_folder).grid(row=1, column=2, padx=5)
 
        # 水印设置
        watermark_group = ttk.LabelFrame(main_frame, text="水印设置", padding="5")
        watermark_group.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
 
        # 第1行：水印文字
        ttk.Label(watermark_group, text="水印文字:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.watermark_var = tk.StringVar(value="xx出品")
        ttk.Entry(watermark_group, textvariable=self.watermark_var, width=40).grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)
 
        # 第2行：字体大小 + 角度
        ttk.Label(watermark_group, text="字体大小:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.font_size_var = tk.IntVar(value=42)
        ttk.Spinbox(watermark_group, from_=10, to=100, textvariable=self.font_size_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
 
        ttk.Label(watermark_group, text="角度:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.angle_var = tk.IntVar(value=45)
        ttk.Spinbox(watermark_group, from_=0, to=90, textvariable=self.angle_var, width=10).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
 
        # 第3行：行间距 + 列间距
        ttk.Label(watermark_group, text="行间距:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.spacing_var = tk.IntVar(value=80)
        ttk.Spinbox(watermark_group, from_=20, to=200, textvariable=self.spacing_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
 
        ttk.Label(watermark_group, text="列间距:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.column_var = tk.IntVar(value=500)
        ttk.Spinbox(watermark_group, from_=300, to=800, increment=50, textvariable=self.column_var, width=10).grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)
 
        # 第4行：透明度
        ttk.Label(watermark_group, text="透明度:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.alpha_var = tk.DoubleVar(value=0.2)
        ttk.Spinbox(watermark_group, from_=0.1, to=0.9, increment=0.1, textvariable=self.alpha_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
                 
        # 进度条
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        #self.progress_bar.grid_remove()
 
        # 日志
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="5")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, width=70, height=8)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_text.config(state=tk.DISABLED)
 
        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        self.start_btn = ttk.Button(button_frame, text="开始加水印", command=self.start_watermark)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(button_frame, text="重置服务", command=self.stop_watermark, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
 
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
 
    def browse_pdf_folder(self):
        path = filedialog.askdirectory(title="选择PDF文件夹", initialdir=".")
        if path:
            self.pdf_folder_var.set(path)
 
    def browse_output_folder(self):
        path = filedialog.askdirectory(title="选择输出文件夹", initialdir=".")
        if path:
            self.output_folder_var.set(path)
 
    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status_var.set(message)
 
    def start_watermark(self):
        if not self.pdf_folder_var.get() or not self.output_folder_var.get():
            messagebox.showwarning("警告", "请选择文件夹")
            return
 
        if not os.path.exists(self.output_folder_var.get()):
            os.makedirs(self.output_folder_var.get())
 
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_bar.grid()
        self.progress_var.set(0)
 
        self.watermark_thread = WatermarkThread(
            self.pdf_folder_var.get(),
            self.output_folder_var.get(),
            self.watermark_var.get(),
            self.font_size_var.get(),
            self.angle_var.get(),
            self.spacing_var.get(),
            self.alpha_var.get(),
            self.column_var.get(),
            self.progress_queue
        )
        self.watermark_thread.start()
 
    def stop_watermark(self):
        if self.watermark_thread and self.watermark_thread.is_alive():
            self.watermark_thread.stop_process()   # 调用线程的停止方法
            self.watermark_thread.join()
            self.log_message("已停止")
 
        # 重置 UI
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("准备就绪")
 
 
    def check_queue(self):
        try:
            while True:
                progress, message = self.progress_queue.get_nowait()
                self.progress_var.set(progress)
                self.log_message(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
 
 
if __name__ == '__main__':
    root = tk.Tk()
    app = PDFWatermarkApp(root)
    root.mainloop()