# !/usr/bin/env python
# -*- coding: utf-8 -*-
# https://www.52pojie.cn/thread-2049426-1-1.html
from typing import List, Union
from pydantic import BaseModel
from pypinyin import pinyin, lazy_pinyin, Style
import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
 
 
class TextRequest(BaseModel):
    text: Union[str, List[str]]
    style: str = "normal"
    keep_punctuation: bool = False
 
 
class PinyinConverter:
    def __init__(self, text):
        self.text = text
 
    def replace(self):
        """替换中文标点为英文标点，保留换行"""
        replace_map = str.maketrans('。，！？；："”‘’', '.,!?;:""\'\'')
        if isinstance(self.text, str):
            lines = self.text.split('\n')
            processed_lines = []
            for line in lines:
                line = line.translate(replace_map)
                line = re.sub(r'\s+', ' ', line).strip()
                if line:  # 只保留非空行
                    processed_lines.append(line)
            self.text = '\n'.join(processed_lines)
        elif isinstance(self.text, list):
            cleaned = []
            for item in self.text:
                if isinstance(item, str):
                    item = item.translate(replace_map)
                    item = re.sub(r'\s+', ' ', item).strip()
                    if item:
                        cleaned.append(item)
            self.text = ' '.join(cleaned)
        else:
            raise TypeError("Unsupported type for self.text. Expected str or list.")
 
    def del_biandian(self):
        """删除所有标点符号，保留换行"""
        lines = self.text.split('\n')
        processed_lines = []
        for line in lines:
            line = re.sub(r'[^\w\s]', '', line)
            line = re.sub(r'\s+', ' ', line).strip()
            if line:  # 只保留非空行
                processed_lines.append(line)
        self.text = '\n'.join(processed_lines)
 
    def out_lazy_pinyin(self, style=Style.NORMAL):
        """输出不带声调的拼音，保留换行"""
        lines = self.text.split('\n')
        pinyin_lines = []
        for line in lines:
            pinyin_list = lazy_pinyin(hans=line, style=style, v_to_u=True)
            filtered = [p for p in pinyin_list if p.strip()]
            if filtered:  # 只保留非空行
                pinyin_lines.append(' '.join(filtered))
        return '\n'.join(pinyin_lines)
 
    def out_pinyin(self, style=Style.NORMAL):
        """输出带声调的拼音，保留换行"""
        lines = self.text.split('\n')
        pinyin_lines = []
        for line in lines:
            pinyin_date = pinyin(hans=line, style=style, v_to_u=True)
            pinyin_date_flat = [item for sublist in pinyin_date for item in sublist]
            filtered = [p for p in pinyin_date_flat if p.strip()]
            if filtered:  # 只保留非空行
                pinyin_lines.append(' '.join(filtered))
        return '\n'.join(pinyin_lines)
 
 
class PinyinConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("汉字转拼音工具")
        self.root.geometry("600x500")
 
        self.create_widgets()
 
    def create_widgets(self):
        # 输入区域
        input_frame = ttk.LabelFrame(self.root, text="输入汉字", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
 
        self.input_text = scrolledtext.ScrolledText(input_frame, height=10, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)
 
        # 选项区域
        options_frame = ttk.Frame(self.root)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
 
        # 拼音风格选择
        ttk.Label(options_frame, text="拼音风格:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.style_var = tk.StringVar(value="normal")
        styles = [
            ("普通 (不带声调)", "normal"),
            ("带声调", "tone"),
            ("数字声调", "tone2"),
            ("声调在拼音后", "tone3")
        ]
 
        for i, (text, value) in enumerate(styles):
            rb = ttk.Radiobutton(options_frame, text=text, variable=self.style_var, value=value)
            rb.grid(row=0, column=i + 1, padx=5, sticky=tk.W)
 
        # 标点符号选项
        self.punctuation_var = tk.BooleanVar(value=False)
        punctuation_cb = ttk.Checkbutton(options_frame, text="保留标点符号", variable=self.punctuation_var)
        punctuation_cb.grid(row=0, column=len(styles) + 1, padx=10, sticky=tk.W)
 
        # 转换按钮
        convert_btn = ttk.Button(self.root, text="转换为拼音", command=self.convert_text)
        convert_btn.pack(pady=5)
 
        # 输出区域
        output_frame = ttk.LabelFrame(self.root, text="拼音结果", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
 
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
 
        # 底部按钮
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=5, pady=10)
 
        clear_btn = ttk.Button(bottom_frame, text="清空", command=self.clear_text)
        clear_btn.pack(side=tk.LEFT, padx=5)
 
        copy_btn = ttk.Button(bottom_frame, text="复制结果", command=self.copy_result)
        copy_btn.pack(side=tk.LEFT, padx=5)
 
        exit_btn = ttk.Button(bottom_frame, text="退出", command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT, padx=5)
 
    def convert_text(self):
        input_text = self.input_text.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("警告", "请输入要转换的汉字内容！")
            return
 
        try:
            request = TextRequest(
                text=input_text,
                style=self.style_var.get(),
                keep_punctuation=self.punctuation_var.get()
            )
 
            converter = PinyinConverter(request.text)
 
            style_map = {
                "normal": Style.NORMAL,
                "tone": Style.TONE,
                "tone2": Style.TONE2,
                "tone3": Style.TONE3
            }
            style = style_map.get(request.style, Style.NORMAL)
 
            if request.keep_punctuation:
                converter.replace()
                result = converter.out_pinyin(style=style)
            else:
                converter.del_biandian()
                result = converter.out_lazy_pinyin(style=style)
 
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
 
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中出现错误:\n{str(e)}")
 
    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
 
    def copy_result(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "结果已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "没有可复制的结果！")
 
 
if __name__ == "__main__":
    root = tk.Tk()    
    app = PinyinConverterApp(root)
    root.mainloop()