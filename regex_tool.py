import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
import json
from tkinter import font as tkfont
 
class RegexGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("正则表达式生成器 - Python工具")
        self.root.geometry("1200x800")
         
        # 设置中文字体
        self.setup_fonts()
         
        # 预设正则表达式模板
        self.regex_templates = {
            "常用匹配": {
                "邮箱地址": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                "手机号码": r"1[3-9]\d{9}",
                "身份证号码": r"\d{17}[\dXx]|\d{15}",
                "IP地址": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
                "URL链接": r"https?://[^\s]+",
                "日期格式": r"\d{4}[-/]\d{1,2}[-/]\d{1,2}",
                "时间格式": r"\d{1,2}:\d{2}:\d{2}",
                "中文字符": r"[\u4e00-\u9fa5]+",
                "数字": r"\d+",
                "英文字母": r"[a-zA-Z]+"
            },
              "高级匹配": {
                "HTML标签": r"<[^>]+>",
                "HTML注释": r"<!--.*?-->",
                "JSON字符串": r"\{[^{}]*\}",
                "XML标签": r"<[^>]*>",
                "Markdown链接": r"\[([^\]]+)\]\(([^)]+)\)",
                "图片标签": r"<img[^>]*>",
                "CSS样式": r"[.#]?[\w-]+\s*\{[^}]*\}",
                "JavaScript变量": r"var\s+[\w$]+\s*=",
                "SQL语句": r"SELECT\s+.*?\s+FROM\s+[\w_]+",
                "文件路径": r"[a-zA-Z]:\\[^*?\"<>|\n]*"  # 修复：转义双引号
            },
            "替换模板": {
                "去除HTML标签": r"<[^>]*>",
                "去除空白字符": r"\s+",
                "去除特殊字符": r"[^\w\s]",
                "提取数字": r"\D+",
                "提取字母": r"[^a-zA-Z]+",
                "提取中文": r"[^\u4e00-\u9fa5]+",
                "统一空格": r"\s+",
                "去除首尾空格": r"^\s+|\s+$"
            }
        }
         
        self.create_widgets()
        self.setup_layout()
         
    def setup_fonts(self):
        """设置字体"""
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Microsoft YaHei", size=10)
        self.text_font = tkfont.nametofont("TkTextFont") 
        self.text_font.configure(family="Microsoft YaHei", size=10)
        self.root.option_add("*Font", self.default_font)
         
    def create_widgets(self):
        """创建所有控件"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
         
        # 顶部工具栏
        self.create_toolbar()
         
        # 中间主要内容区域
        self.create_main_content()
         
        # 底部状态栏
        self.create_status_bar()
         
    def create_toolbar(self):
        """创建工具栏"""
        self.toolbar = ttk.Frame(self.main_frame)
         
        # 文件操作按钮
        ttk.Button(self.toolbar, text="新建", command=self.new_regex).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="保存", command=self.save_regex).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="加载", command=self.load_regex).pack(side=tk.LEFT, padx=5)
         
        # 分隔线
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
         
        # 常用操作按钮
        ttk.Button(self.toolbar, text="复制表达式", command=self.copy_regex).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="复制匹配结果", command=self.copy_matches).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="清除所有", command=self.clear_all).pack(side=tk.LEFT, padx=5)
         
        # 分隔线
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
         
        # 匹配选项
        self.case_var = tk.BooleanVar(value=False)
        self.multiline_var = tk.BooleanVar(value=False)
        self.dotall_var = tk.BooleanVar(value=False)
         
        ttk.Checkbutton(self.toolbar, text="忽略大小写", variable=self.case_var, command=self.test_regex).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(self.toolbar, text="多行模式", variable=self.multiline_var, command=self.test_regex).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(self.toolbar, text="点号匹配换行", variable=self.dotall_var, command=self.test_regex).pack(side=tk.LEFT, padx=5)
         
    def create_main_content(self):
        """创建主要内容区域"""
        # 使用PanedWindow创建可调整大小的区域
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
         
        # 左侧模板区域
        self.create_template_panel()
         
        # 中间编辑和测试区域
        self.create_editor_panel()
         
        # 右侧帮助区域
        self.create_help_panel()
         
    def create_template_panel(self):
        """创建模板面板"""
        self.template_frame = ttk.LabelFrame(self.paned_window, text="正则模板库", padding="10")
        self.paned_window.add(self.template_frame, weight=1)
         
        # 创建Treeview显示模板
        self.template_tree = ttk.Treeview(self.template_frame, height=20)
        self.template_tree.heading("#0", text="模板分类")
         
        # 添加模板到树形结构
        for category, templates in self.regex_templates.items():
            category_item = self.template_tree.insert("", "end", text=category)
            for name, pattern in templates.items():
                self.template_tree.insert(category_item, "end", text=name, values=(pattern,))
         
        # 绑定双击事件
        self.template_tree.bind("<Double-1>", self.on_template_double_click)
         
        # 滚动条
        template_scroll = ttk.Scrollbar(self.template_frame, orient=tk.VERTICAL, command=self.template_tree.yview)
        self.template_tree.configure(yscrollcommand=template_scroll.set)
         
        # 布局
        self.template_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        template_scroll.pack(side=tk.RIGHT, fill=tk.Y)
         
    def create_editor_panel(self):
        """创建编辑面板"""
        self.editor_frame = ttk.LabelFrame(self.paned_window, text="正则表达式编辑器", padding="10")
        self.paned_window.add(self.editor_frame, weight=2)
         
        # 正则表达式输入区域
        regex_frame = ttk.Frame(self.editor_frame)
        ttk.Label(regex_frame, text="正则表达式:").pack(anchor=tk.W)
        self.regex_entry = ttk.Entry(regex_frame, font=("Consolas", 12))
        self.regex_entry.pack(fill=tk.X, pady=(0, 10))
        self.regex_entry.bind("<KeyRelease>", lambda e: self.test_regex())
         
        # 替换表达式区域
        replace_frame = ttk.Frame(self.editor_frame)
        ttk.Label(replace_frame, text="替换表达式 (可选):").pack(anchor=tk.W)
        self.replace_entry = ttk.Entry(replace_frame, font=("Consolas", 12))
        self.replace_entry.pack(fill=tk.X, pady=(0, 10))
         
        # 测试文本区域
        test_frame = ttk.Frame(self.editor_frame)
        ttk.Label(test_frame, text="测试文本:").pack(anchor=tk.W)
         
        # 创建PanedWindow来分割测试文本和结果
        test_paned = ttk.PanedWindow(test_frame, orient=tk.VERTICAL)
         
        # 测试文本输入
        test_input_frame = ttk.LabelFrame(test_paned, text="输入文本")
        self.test_text = scrolledtext.ScrolledText(test_input_frame, height=10, font=("Consolas", 10))
        self.test_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.test_text.bind("<KeyRelease>", lambda e: self.test_regex())
         
        # 预设测试文本按钮
        test_buttons_frame = ttk.Frame(test_input_frame)
        test_buttons_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
         
        ttk.Button(test_buttons_frame, text="邮箱测试文本", 
                  command=lambda: self.set_test_text("测试邮箱：test@example.com, user.name+tag@domain.co.uk")).pack(side=tk.LEFT, padx=2)
        ttk.Button(test_buttons_frame, text="手机号测试文本", 
                  command=lambda: self.set_test_text("手机号：13812345678, 15987654321")).pack(side=tk.LEFT, padx=2)
        ttk.Button(test_buttons_frame, text="HTML测试文本", 
                  command=lambda: self.set_test_text('<div class="test"><p>Hello World</p></div>')).pack(side=tk.LEFT, padx=2)
         
        test_paned.add(test_input_frame, weight=1)
         
        # 匹配结果区域
        result_frame = ttk.LabelFrame(test_paned, text="匹配结果")
        self.result_text = scrolledtext.ScrolledText(result_frame, height=8, font=("Consolas", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
         
        test_paned.add(result_frame, weight=1)
         
        # 详细信息区域
        detail_frame = ttk.LabelFrame(test_paned, text="详细信息")
        self.detail_text = scrolledtext.ScrolledText(detail_frame, height=6, font=("Consolas", 10))
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
         
        test_paned.add(detail_frame, weight=1)
         
        # 布局
        regex_frame.pack(fill=tk.X)
        replace_frame.pack(fill=tk.X)
        test_frame.pack(fill=tk.BOTH, expand=True)
        test_paned.pack(fill=tk.BOTH, expand=True)
         
    def create_help_panel(self):
        """创建帮助面板"""
        self.help_frame = ttk.LabelFrame(self.paned_window, text="正则语法参考", padding="10")
        self.paned_window.add(self.help_frame, weight=1)
         
        # 创建Notebook用于多个帮助页面
        self.help_notebook = ttk.Notebook(self.help_frame)
         
        # 基础语法页面
        basic_frame = ttk.Frame(self.help_notebook)
        basic_help = """
基础语法:
.           匹配任意字符（除换行符）
^           匹配字符串开始
$           匹配字符串结束
*           匹配0次或多次
+           匹配1次或多次
?           匹配0次或1次
{n}         匹配n次
{n,}        匹配n次或更多
{n,m}       匹配n到m次
[]          字符集
[^]         反向字符集
|           或运算
()          分组
 
特殊字符:
\d          数字 [0-9]
\D          非数字 [^0-9]
\w          单词字符 [a-zA-Z0-9_]
\W          非单词字符
\s          空白字符
\S          非空白字符
\\b          单词边界
\B          非单词边界
"""
        basic_text = scrolledtext.ScrolledText(basic_frame, wrap=tk.WORD, font=("Consolas", 9))
        basic_text.insert(tk.END, basic_help)
        basic_text.config(state=tk.DISABLED)
        basic_text.pack(fill=tk.BOTH, expand=True)
        self.help_notebook.add(basic_frame, text="基础语法")
         
        # 高级语法页面
        advanced_frame = ttk.Frame(self.help_notebook)
        advanced_help = """
高级语法:
(?=)        正向预查
(?!)        负向预查
(?<=)       正向回顾
(?<!)       负向回顾
(?:)        非捕获分组
(?P<name>)  命名分组
(?P=name)   引用命名分组
 
标志:
re.I        忽略大小写
re.M        多行模式
re.S        点号匹配换行
re.X        详细模式
re.U        Unicode匹配
 
替换语法:
\\1          引用第1个分组
\g<1>       引用第1个分组
\g<name>    引用命名分组
$1          替换中的分组引用
"""
        advanced_text = scrolledtext.ScrolledText(advanced_frame, wrap=tk.WORD, font=("Consolas", 9))
        advanced_text.insert(tk.END, advanced_help)
        advanced_text.config(state=tk.DISABLED)
        advanced_text.pack(fill=tk.BOTH, expand=True)
        self.help_notebook.add(advanced_frame, text="高级语法")
         
        # 常用示例页面
        example_frame = ttk.Frame(self.help_notebook)
        example_help = """
常用示例:
匹配邮箱:     [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}
匹配手机号:   1[3-9]\\d{9}
匹配IP地址:   \\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}
匹配中文字符: [\\u4e00-\\u9fa5]+
匹配HTML标签: <[^>]+>
匹配身份证号: \\d{17}[\\dXx]|\\d{15}
 
提取分组:
(\\d{4})-(\\d{1,2})-(\\d{1,2})
可以提取年、月、日
 
替换示例:
将空格替换为下划线: \\s+ → _
提取数字: \\D+ → ""
去除HTML标签: <[^>]*> → ""
"""
        example_text = scrolledtext.ScrolledText(example_frame, wrap=tk.WORD, font=("Consolas", 9))
        example_text.insert(tk.END, example_help)
        example_text.config(state=tk.DISABLED)
        example_text.pack(fill=tk.BOTH, expand=True)
        self.help_notebook.add(example_frame, text="常用示例")
         
        self.help_notebook.pack(fill=tk.BOTH, expand=True)
         
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(self.status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)
         
        # 匹配统计
        self.match_count_label = ttk.Label(self.status_frame, text="匹配数: 0")
        self.match_count_label.pack(side=tk.RIGHT, padx=10)
         
    def setup_layout(self):
        """设置布局"""
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.toolbar.pack(fill=tk.X, pady=(0, 10))
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
         
    def on_template_double_click(self, event):
        """双击模板事件"""
        selection = self.template_tree.selection()
        if selection:
            item = self.template_tree.item(selection[0])
            values = item.get('values', [])
            if values:  # 有值的项才是具体的模板
                pattern = values[0]
                self.regex_entry.delete(0, tk.END)
                self.regex_entry.insert(0, pattern)
                self.test_regex()
                self.status_label.config(text=f"已加载模板: {item['text']}")
         
    def set_test_text(self, text):
        """设置测试文本"""
        self.test_text.delete("1.0", tk.END)
        self.test_text.insert(tk.END, text)
        self.test_regex()
         
    def test_regex(self):
        """测试正则表达式"""
        pattern = self.regex_entry.get()
        text = self.test_text.get("1.0", tk.END)
        replace_text = self.replace_entry.get()
         
        if not pattern or not text:
            self.result_text.delete("1.0", tk.END)
            self.detail_text.delete("1.0", tk.END)
            self.match_count_label.config(text="匹配数: 0")
            return
         
        try:
            # 编译正则表达式
            flags = 0
            if self.case_var.get():
                flags |= re.I
            if self.multiline_var.get():
                flags |= re.M
            if self.dotall_var.get():
                flags |= re.S
                 
            regex = re.compile(pattern, flags)
             
            # 查找所有匹配
            matches = list(regex.finditer(text))
             
            # 显示匹配结果
            self.result_text.delete("1.0", tk.END)
            self.detail_text.delete("1.0", tk.END)
             
            if matches:
                # 显示匹配到的文本
                for i, match in enumerate(matches):
                    self.result_text.insert(tk.END, f"匹配 {i+1}: {match.group()}\n")
                    if match.groups():
                        self.result_text.insert(tk.END, "  分组: " + ", ".join(f"组{j+1}={group}" for j, group in enumerate(match.groups()) if group) + "\n")
                 
                # 显示详细信息
                self.detail_text.insert(tk.END, f"找到 {len(matches)} 个匹配\n\n")
                for i, match in enumerate(matches):
                    self.detail_text.insert(tk.END, f"匹配 {i+1}:\n")
                    self.detail_text.insert(tk.END, f"  完整匹配: '{match.group()}'\n")
                    self.detail_text.insert(tk.END, f"  位置: {match.start()}-{match.end()}\n")
                    if match.groups():
                        self.detail_text.insert(tk.END, "  分组信息:\n")
                        for j, group in enumerate(match.groups()):
                            if group:
                                self.detail_text.insert(tk.END, f"    组{j+1}: '{group}' (位置: {match.start(j+1)}-{match.end(j+1)})\n")
                    self.detail_text.insert(tk.END, "\n")
                 
                # 如果有替换文本，显示替换结果
                if replace_text:
                    replaced = regex.sub(replace_text, text)
                    self.detail_text.insert(tk.END, "替换结果:\n")
                    self.detail_text.insert(tk.END, replaced + "\n")
                 
                # 高亮显示匹配
                self.highlight_matches(text, matches)
                 
            else:
                self.result_text.insert(tk.END, "没有找到匹配")
                self.detail_text.insert(tk.END, "没有找到匹配\n")
             
            self.match_count_label.config(text=f"匹配数: {len(matches)}")
            self.status_label.config(text="测试完成")
             
        except re.error as e:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"正则表达式错误: {str(e)}")
            self.status_label.config(text=f"正则表达式错误: {str(e)}")
            self.match_count_label.config(text="匹配数: 0")
         
    def highlight_matches(self, text, matches):
        """高亮显示匹配结果"""
        # 这里可以添加高亮逻辑
        pass
         
    def copy_regex(self):
        """复制正则表达式"""
        pattern = self.regex_entry.get()
        if pattern:
            self.root.clipboard_clear()
            self.root.clipboard_append(pattern)
            self.status_label.config(text="正则表达式已复制到剪贴板")
         
    def copy_matches(self):
        """复制匹配结果"""
        result = self.result_text.get("1.0", tk.END)
        if result.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_label.config(text="匹配结果已复制到剪贴板")
         
    def clear_all(self):
        """清除所有内容"""
        self.regex_entry.delete(0, tk.END)
        self.replace_entry.delete(0, tk.END)
        self.test_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
        self.detail_text.delete("1.0", tk.END)
        self.status_label.config(text="已清除所有内容")
        self.match_count_label.config(text="匹配数: 0")
         
    def new_regex(self):
        """新建正则表达式"""
        self.clear_all()
        self.status_label.config(text="新建正则表达式")
         
    def save_regex(self):
        """保存正则表达式"""
        pattern = self.regex_entry.get()
        if not pattern:
            messagebox.showwarning("警告", "没有可保存的正则表达式")
            return
             
        # 创建保存数据
        data = {
            "pattern": pattern,
            "replace": self.replace_entry.get(),
            "test_text": self.test_text.get("1.0", tk.END).strip(),
            "flags": {
                "ignore_case": self.case_var.get(),
                "multiline": self.multiline_var.get(),
                "dotall": self.dotall_var.get()
            }
        }
         
        # 保存到文件
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
         
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.status_label.config(text=f"已保存到: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
         
    def load_regex(self):
        """加载正则表达式"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
         
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                 
                # 恢复数据
                self.regex_entry.delete(0, tk.END)
                self.regex_entry.insert(0, data.get("pattern", ""))
                 
                self.replace_entry.delete(0, tk.END)
                self.replace_entry.insert(0, data.get("replace", ""))
                 
                self.test_text.delete("1.0", tk.END)
                self.test_text.insert(tk.END, data.get("test_text", ""))
                 
                # 恢复标志
                flags = data.get("flags", {})
                self.case_var.set(flags.get("ignore_case", False))
                self.multiline_var.set(flags.get("multiline", False))
                self.dotall_var.set(flags.get("dotall", False))
                 
                self.test_regex()
                self.status_label.config(text=f"已从 {filename} 加载")
                 
            except Exception as e:
                messagebox.showerror("错误", f"加载失败: {str(e)}")
 
def main():
    root = tk.Tk()
    app = RegexGenerator(root)
    root.mainloop()
 
if __name__ == "__main__":
    main()