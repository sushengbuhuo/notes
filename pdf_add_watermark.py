import os
import sys
import threading
import queue
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.font as tkfont
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter
 
# ---------- 过滤控制台无关输出 ----------
class FilterStderr:
    def __init__(self, stream):
        self.stream = stream
    def write(self, msg):
        if not any(x in msg for x in ('libpng warning', '生成链路关键节点上报')):
            self.stream.write(msg)
    def flush(self):
        self.stream.flush()
 
sys.stderr = FilterStderr(sys.stderr)
 
 
# ------------------ 字体扫描辅助函数 ------------------
def get_system_font_dirs():
    system = platform.system()
    dirs = []
    if system == 'Windows':
        dirs.append(r'C:\Windows\Fonts')
        username = os.environ.get('USERNAME') or os.environ.get('USER')
        if username:
            user_font_dir = fr'C:\Users\{username}\AppData\Local\Microsoft\Windows\Fonts'
            if os.path.exists(user_font_dir):
                dirs.append(user_font_dir)
        local_appdata = os.environ.get('LOCALAPPDATA')
        if local_appdata:
            dirs.append(os.path.join(local_appdata, 'Microsoft', 'Windows', 'Fonts'))
    elif system == 'Darwin':
        dirs.extend([
            '/System/Library/Fonts',
            '/Library/Fonts',
            os.path.expanduser('~/Library/Fonts')
        ])
    else:
        dirs.extend(['/usr/share/fonts', os.path.expanduser('~/.fonts')])
    return [d for d in dirs if d and os.path.exists(d)]
 
 
def get_installed_fonts_from_tk():
    root_tmp = tk.Tk()
    root_tmp.withdraw()
    families = list(tkfont.families(root_tmp))
    root_tmp.destroy()
    return families
 
 
def extract_font_family(font_path):
    try:
        if font_path.lower().endswith('.ttc'):
            font = TTFont(font_path, subfontIndex=0, validate=False)
        else:
            font = TTFont(font_path, validate=False)
        return font.face.family_name
    except:
        return None
 
 
def scan_available_fonts():
    font_map = {}
    font_dirs = get_system_font_dirs()
    installed_families = get_installed_fonts_from_tk()
    chinese_keywords = ['宋', '黑', '楷', '仿', '雅黑', '苹方', 'song', 'hei', 'kai', 'fang',
                        'microsoft yahei', 'pingfang', 'simsun', 'simhei', 'simkai', 'kaiti', 'songti']
 
    file_family_map = {}
    for font_dir in font_dirs:
        for root, _, files in os.walk(font_dir):
            for file in files:
                if file.lower().endswith(('.ttf', '.ttc')):
                    full_path = os.path.join(root, file)
                    family = extract_font_family(full_path)
                    if family:
                        file_family_map[full_path] = family
                    elif any(kw in file.lower() for kw in chinese_keywords):
                        file_family_map[full_path] = os.path.splitext(file)[0]
 
    for family in installed_families:
        family_lower = family.lower()
        if not any(kw in family_lower for kw in chinese_keywords):
            continue
        found_path = None
        for path, fam in file_family_map.items():
            if fam == family or family in fam or fam in family:
                found_path = path
                break
        if not found_path:
            for path in file_family_map:
                file_name = os.path.basename(path).lower()
                if family_lower.replace(' ', '') in file_name.replace(' ', ''):
                    found_path = path
                    break
        if found_path:
            font_map[family] = found_path
 
    if len(font_map) < 2:
        for path, family in file_family_map.items():
            if any(kw in family.lower() for kw in chinese_keywords) and family not in font_map:
                font_map[family] = path
 
    if not font_map:
        font_map["默认字体 (无法显示中文)"] = ""
    return font_map
 
 
# ------------------ 加水印线程 ------------------
class WatermarkThread(threading.Thread):
    def __init__(self, settings, progress_queue):
        super().__init__()
        self.settings = settings
        self.progress_queue = progress_queue
        self.is_running = True
        self.daemon = True
 
    def stop_process(self):
        self.is_running = False
 
    def run(self):
        input_mode = self.settings['input_mode']
        output_folder = self.settings['output_folder']
 
        if input_mode == 'folder':
            pdf_folder = self.settings['pdf_folder']
            if not pdf_folder or not output_folder:
                self.progress_queue.put((0, "错误：文件夹模式需要指定输出文件夹"))
                return
            pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
        else:
            pdf_path = self.settings['pdf_file']
            if not pdf_path:
                self.progress_queue.put((0, "错误：未选择 PDF 文件"))
                return
            pdf_files = [pdf_path]
            if not output_folder:
                output_folder = os.path.dirname(pdf_path)
                self.settings['output_folder'] = output_folder
 
        os.makedirs(output_folder, exist_ok=True)
        total = len(pdf_files)
        processed = 0
 
        for file_path in pdf_files:
            if not self.is_running:
                self.progress_queue.put((0, "用户中止"))
                return
            processed += 1
            progress = int((processed / total) * 100) if total > 0 else 0
            filename = os.path.basename(file_path)
            self.progress_queue.put((progress, f"正在处理 ({processed}/{total}): {filename}"))
            try:
                out_path = self.add_watermark(file_path)
                self.progress_queue.put((progress, f"完成: {os.path.basename(out_path)}"))
            except Exception as e:
                self.progress_queue.put((progress, f"失败 {filename}: {str(e)}"))
        self.progress_queue.put((100, "所有任务完成！"))
 
    def add_watermark(self, pdf_path):
        s = self.settings
        reader = PdfReader(pdf_path)
        if len(reader.pages) == 0:
            raise ValueError("PDF 无页面")
        first_page = reader.pages[0]
        mb = first_page.mediabox
        page_width = float(mb.width)
        page_height = float(mb.height)
 
        if s['use_relative_scale']:
            base_size = min(page_width, page_height) * (s['relative_scale_percent'] / 100.0)
        else:
            base_size = s['font_size']
 
        font_name = s['font_family']
        font_path = s['font_path']
        if font_path and font_name not in pdfmetrics.getRegisteredFontNames():
            subfont = 0 if font_path.lower().endswith('.ttc') else None
            pdfmetrics.registerFont(TTFont(font_name, font_path, subfontIndex=subfont))
 
        temp_wm = os.path.join(s['output_folder'], "__temp_watermark.pdf")
        c = canvas.Canvas(temp_wm, pagesize=(page_width, page_height))
 
        c.setFillColor(colors.black, alpha=s['alpha'])
        if font_name in pdfmetrics.getRegisteredFontNames():
            c.setFont(font_name, base_size)
        else:
            c.setFont("Helvetica", base_size)
 
        lines = s['watermark_text'].split('\n')
        line_height = base_size * 1.2
        mm_to_pt = 2.83465
        offset_x = s['offset_x_mm'] * mm_to_pt
        offset_y = s['offset_y_mm'] * mm_to_pt
 
        c.saveState()
        c.translate(page_width / 2 + offset_x, page_height / 2 + offset_y)
        c.rotate(s['angle'])
 
        row_spacing = s['row_spacing']
        col_spacing = s['col_spacing']
 
        extend = max(page_width, page_height) * 2
        start_x = -extend
        start_y = -extend
        end_x = extend
        end_y = extend
 
        x = start_x
        while x < end_x:
            y = start_y
            while y < end_y:
                for i, line in enumerate(lines):
                    total_height = (len(lines) - 1) * line_height
                    y_offset = total_height / 2 - i * line_height
                    c.drawString(x, y + y_offset, line)
                y += row_spacing
            x += col_spacing
 
        c.restoreState()
        c.save()
 
        wm_reader = PdfReader(temp_wm)
        writer = PdfWriter()
        page_range = self.parse_page_range(s['page_range'], len(reader.pages))
        for i, page in enumerate(reader.pages):
            if i in page_range:
                page.merge_page(wm_reader.pages[0])
            writer.add_page(page)
 
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        out_file = os.path.join(s['output_folder'], f"{base}_watermarked.pdf")
        with open(out_file, "wb") as f:
            writer.write(f)
        os.remove(temp_wm)
        return out_file
 
    def parse_page_range(self, range_str, total_pages):
        if range_str.strip() == "全部页面":
            return set(range(total_pages))
        pages = set()
        for p in range_str.split(','):
            p = p.strip()
            if '-' in p:
                start, end = p.split('-')
                start = int(start) - 1
                end = int(end) - 1
                if start < 0: start = 0
                if end >= total_pages: end = total_pages - 1
                pages.update(range(start, end + 1))
            else:
                idx = int(p) - 1
                if 0 <= idx < total_pages:
                    pages.add(idx)
        return pages
 
 
# ------------------ 主界面 ------------------
class PDFWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.watermark_thread = None
        self.progress_queue = queue.Queue()
        self.available_fonts = {}
        self.initUI()
        self.check_queue()
        self.scan_fonts()
 
    def initUI(self):
        self.root.title('PDF 水印工具 - 专业版')
        self.root.geometry('700x700')
        self.root.minsize(650, 600)
 
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="微软雅黑" if platform.system() == 'Windows' else "PingFang SC", size=10)
        self.root.option_add("*Font", default_font)
 
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
 
        # 输入模式
        mode_frame = ttk.LabelFrame(main_frame, text="输入模式", padding="5")
        mode_frame.pack(fill=tk.X, pady=5)
        self.input_mode = tk.StringVar(value="single")
        ttk.Radiobutton(mode_frame, text="处理文件夹", variable=self.input_mode, value="folder", command=self.on_mode_change).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="处理单个文件", variable=self.input_mode, value="single", command=self.on_mode_change).pack(side=tk.LEFT, padx=10)
 
        self.folder_frame = ttk.LabelFrame(main_frame, text="源文件设置", padding="5")
        self.folder_frame.pack(fill=tk.X, pady=5)
 
        # 文件夹模式控件
        self.folder_widgets = []
        self.single_widgets = []
 
        # 文件夹模式
        f1 = ttk.Frame(self.folder_frame)
        ttk.Label(f1, text="PDF 文件夹:", width=12).pack(side=tk.LEFT)
        self.pdf_folder_var = tk.StringVar()
        ttk.Entry(f1, textvariable=self.pdf_folder_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(f1, text="选择", command=self.browse_pdf_folder).pack(side=tk.RIGHT)
        self.folder_widgets.append(f1)
 
        # 单文件模式
        f2 = ttk.Frame(self.folder_frame)
        ttk.Label(f2, text="PDF 文件:", width=12).pack(side=tk.LEFT)
        self.pdf_file_var = tk.StringVar()
        ttk.Entry(f2, textvariable=self.pdf_file_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(f2, text="选择", command=self.browse_pdf_file).pack(side=tk.RIGHT)
        self.single_widgets.append(f2)
 
        # 输出文件夹
        f3 = ttk.Frame(self.folder_frame)
        ttk.Label(f3, text="输出文件夹:", width=12).pack(side=tk.LEFT)
        self.output_folder_var = tk.StringVar()
        self.output_entry = ttk.Entry(f3, textvariable=self.output_folder_var)  # 确保 output_entry 存在
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(f3, text="选择", command=self.browse_output_folder).pack(side=tk.RIGHT)
        ttk.Label(f3, text="(留空则与源文件同目录)", foreground="gray").pack(side=tk.LEFT, padx=5)
        f3.pack(fill=tk.X, pady=2)  # 提前 pack，确保在 on_mode_change 之前已布局
 
        # 现在可以安全调用 on_mode_change
        self.on_mode_change()
 
        # Notebook 设置
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
 
        # ---------- 标签页1：基本设置 ----------
        tab1 = ttk.Frame(notebook, padding="10")
        notebook.add(tab1, text="基本设置")
 
        row = 0
        ttk.Label(tab1, text="水印文字:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.watermark_var = tk.StringVar(value="安全组评审完了")
        text_frame = ttk.Frame(tab1)
        text_frame.grid(row=row, column=1, columnspan=3, sticky=tk.EW, pady=5)
        self.watermark_entry = tk.Text(text_frame, height=3, width=50, font=default_font)
        self.watermark_entry.insert("1.0", self.watermark_var.get())
        self.watermark_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(text_frame, command=self.watermark_entry.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.watermark_entry.config(yscrollcommand=scroll.set)
        tab1.columnconfigure(1, weight=1)
 
        row += 1
        ttk.Label(tab1, text="字体:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.font_var = tk.StringVar()
        self.font_combo = ttk.Combobox(tab1, textvariable=self.font_var, state="readonly", width=40)
        self.font_combo.grid(row=row, column=1, columnspan=3, sticky=tk.W, pady=5, padx=(0,5))
        ttk.Button(tab1, text="刷新字体", command=self.scan_fonts).grid(row=row, column=4, padx=5)
 
        row += 1
        ttk.Label(tab1, text="字号:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.IntVar(value=20)
        self.font_size_spinbox = ttk.Spinbox(tab1, from_=5, to=200, textvariable=self.font_size_var, width=8)
        self.font_size_spinbox.grid(row=row, column=1, sticky=tk.W, pady=5)
 
        row += 1
        ttk.Label(tab1, text="提示：水印文本中使用换行可绘制多行水印", foreground="gray").grid(row=row, column=0, columnspan=5, sticky=tk.W, pady=2)
 
        # ---------- 标签页2：布局与样式 ----------
        tab2 = ttk.Frame(notebook, padding="10")
        notebook.add(tab2, text="布局与样式")
 
        row = 0
        ttk.Label(tab2, text="旋转角度:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.angle_var = tk.IntVar(value=45)
        ttk.Spinbox(tab2, from_=-180, to=180, textvariable=self.angle_var, width=8).grid(row=row, column=1, sticky=tk.W, pady=5)
 
        ttk.Label(tab2, text="透明度:").grid(row=row, column=2, sticky=tk.W, padx=(20,0), pady=5)
        self.alpha_var = tk.DoubleVar(value=0.25)
        ttk.Spinbox(tab2, from_=0.0, to=1.0, increment=0.05, textvariable=self.alpha_var, width=8).grid(row=row, column=3, sticky=tk.W, pady=5)
 
        row += 1
        ttk.Label(tab2, text="行间距:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.spacing_var = tk.IntVar(value=80)
        ttk.Spinbox(tab2, from_=20, to=500, textvariable=self.spacing_var, width=8).grid(row=row, column=1, sticky=tk.W, pady=5)
 
        ttk.Label(tab2, text="列间距:").grid(row=row, column=2, sticky=tk.W, padx=(20,0), pady=5)
        self.column_var = tk.IntVar(value=500)
        ttk.Spinbox(tab2, from_=100, to=1000, textvariable=self.column_var, width=8).grid(row=row, column=3, sticky=tk.W, pady=5)
 
        row += 1
        self.use_relative_scale = tk.BooleanVar(value=False)
        ttk.Checkbutton(tab2, text="相对页面比例", variable=self.use_relative_scale).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.relative_scale_var = tk.IntVar(value=50)
        ttk.Spinbox(tab2, from_=1, to=100, textvariable=self.relative_scale_var, width=8).grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(tab2, text="%").grid(row=row, column=2, sticky=tk.W, pady=5)
 
        # ---------- 标签页3：位置与范围 ----------
        tab3 = ttk.Frame(notebook, padding="10")
        notebook.add(tab3, text="位置与范围")
 
        row = 0
        ttk.Label(tab3, text="垂直偏移 (毫米):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.offset_y_var = tk.DoubleVar(value=0.0)
        ttk.Spinbox(tab3, from_=-100.0, to=100.0, increment=1.0, textvariable=self.offset_y_var, width=8).grid(row=row, column=1, sticky=tk.W, pady=5)
 
        ttk.Label(tab3, text="水平偏移 (毫米):").grid(row=row, column=2, sticky=tk.W, padx=(20,0), pady=5)
        self.offset_x_var = tk.DoubleVar(value=0.0)
        ttk.Spinbox(tab3, from_=-100.0, to=100.0, increment=1.0, textvariable=self.offset_x_var, width=8).grid(row=row, column=3, sticky=tk.W, pady=5)
 
        row += 1
        ttk.Label(tab3, text="应用于:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.page_range_var = tk.StringVar(value="全部页面")
        range_combo = ttk.Combobox(tab3, textvariable=self.page_range_var, values=["全部页面", "仅首页", "自定义"], state="readonly", width=15)
        range_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.custom_range_var = tk.StringVar(value="1-3,5")
        self.custom_range_entry = ttk.Entry(tab3, textvariable=self.custom_range_var, width=20, state=tk.DISABLED)
        self.custom_range_entry.grid(row=row, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)
        range_combo.bind('<<ComboboxSelected>>', self.on_range_change)
 
        # 日志与进度条
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
 
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
 
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        self.start_btn = ttk.Button(btn_frame, text="开始加水印", command=self.start_watermark)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self.stop_watermark, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
 
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
 
    def on_mode_change(self):
        if self.input_mode.get() == 'folder':
            for w in self.folder_widgets:
                w.pack(fill=tk.X, pady=2, before=self.output_entry.master)
            for w in self.single_widgets:
                w.pack_forget()
        else:
            for w in self.folder_widgets:
                w.pack_forget()
            for w in self.single_widgets:
                w.pack(fill=tk.X, pady=2, before=self.output_entry.master)
 
    def on_range_change(self, event=None):
        if self.page_range_var.get() == "自定义":
            self.custom_range_entry.config(state=tk.NORMAL)
        else:
            self.custom_range_entry.config(state=tk.DISABLED)
 
    def browse_pdf_folder(self):
        path = filedialog.askdirectory(title="选择包含 PDF 的文件夹")
        if path:
            self.pdf_folder_var.set(path)
 
    def browse_pdf_file(self):
        path = filedialog.askopenfilename(title="选择 PDF 文件", filetypes=[("PDF 文件", "*.pdf")])
        if path:
            self.pdf_file_var.set(path)
 
    def browse_output_folder(self):
        path = filedialog.askdirectory(title="选择保存水印 PDF 的文件夹")
        if path:
            self.output_folder_var.set(path)
 
    def scan_fonts(self):
        self.log_message("正在扫描系统字体...")
        self.available_fonts = scan_available_fonts()
        font_names = sorted(self.available_fonts.keys())
        self.font_combo['values'] = font_names
        preferred = ['楷体', 'Kaiti SC', 'KaiTi', '宋体', 'Songti SC', 'SimSun', '微软雅黑', 'PingFang SC']
        for name in preferred:
            if name in font_names:
                self.font_var.set(name)
                break
        else:
            if font_names:
                self.font_var.set(font_names[0])
        preview = ', '.join(font_names[:5]) + ('...' if len(font_names) > 5 else '')
        self.log_message(f"字体扫描完成，共找到 {len(font_names)} 种字体：{preview}")
 
    def log_message(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.status_var.set(msg)
 
    def start_watermark(self):
        input_mode = self.input_mode.get()
        if input_mode == 'folder':
            if not self.pdf_folder_var.get():
                messagebox.showwarning("警告", "请选择 PDF 文件夹")
                return
        else:
            if not self.pdf_file_var.get():
                messagebox.showwarning("警告", "请选择 PDF 文件")
                return
 
        output_folder = self.output_folder_var.get().strip()
        if not self.font_var.get():
            messagebox.showwarning("警告", "请选择一种字体")
            return
        font_path = self.available_fonts.get(self.font_var.get())
        if font_path is None:
            messagebox.showwarning("警告", "所选字体路径无效")
            return
 
        watermark_text = self.watermark_entry.get("1.0", tk.END).strip()
        if not watermark_text:
            messagebox.showwarning("警告", "请输入水印文字")
            return
 
        range_type = self.page_range_var.get()
        page_range_str = "全部页面" if range_type == "全部页面" else ("1" if range_type == "仅首页" else self.custom_range_var.get().strip())
 
        settings = {
            'input_mode': input_mode,
            'pdf_folder': self.pdf_folder_var.get() if input_mode == 'folder' else '',
            'pdf_file': self.pdf_file_var.get() if input_mode == 'single' else '',
            'output_folder': output_folder,
            'watermark_text': watermark_text,
            'font_family': self.font_var.get(),
            'font_path': font_path,
            'font_size': self.font_size_var.get(),
            'use_relative_scale': self.use_relative_scale.get(),
            'relative_scale_percent': self.relative_scale_var.get(),
            'angle': self.angle_var.get(),
            'alpha': self.alpha_var.get(),
            'row_spacing': self.spacing_var.get(),
            'col_spacing': self.column_var.get(),
            'offset_x_mm': self.offset_x_var.get(),
            'offset_y_mm': self.offset_y_var.get(),
            'page_range': page_range_str,
        }
 
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
 
        self.watermark_thread = WatermarkThread(settings, self.progress_queue)
        self.watermark_thread.start()
 
    def stop_watermark(self):
        if self.watermark_thread and self.watermark_thread.is_alive():
            self.watermark_thread.stop_process()
            self.log_message("正在停止...")
        else:
            self.reset_ui()
 
    def reset_ui(self):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
 
    def check_queue(self):
        try:
            while True:
                progress, msg = self.progress_queue.get_nowait()
                self.progress_var.set(progress)
                self.log_message(msg)
                if progress == 100 or "所有任务完成" in msg or "用户中止" in msg:
                    self.reset_ui()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
 
 
if __name__ == '__main__':
    root = tk.Tk()
    app = PDFWatermarkApp(root)
    root.mainloop()