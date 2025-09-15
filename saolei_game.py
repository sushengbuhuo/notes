import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import pygame
import random
import os
import time
 
from base64 import b64decode
 
ICON_BASE64 = 'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAHudAAB7nQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASzyQAEs8jwBLPI8ASzyPAEs8jwRLPI8BSz2PAEs8jwBLPI8ISzyPKks8j0hLPI9YSzyPWEs8j0dLPI8pSzyPB0s8jwBMPZAASzyPAUs8jwRLPI8ASzyPAEs8jwBMO44AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEs8jwBLPI8ASzyPAEs8jwJLPI8DSzyPAEs8jwZLPI9LSzyPoks8j9tLPI/4SzyP/0s8j/9LPI//SzyP/0s8j/hLPI/bSzyPoUs8j0lLPI8FSzyPAEs8jwNLPI8CSzyPAEs8jwBLPI8AAAAAAAAAAAAAAAAAAAAAAAAAAABLPI8ASzyPAEs8jwBLPI8CSzyPAkk8jwBLPI9vSzyP80s8j/9LPI/+SzyP+ks8j/lLPI/7SzyP/Eo7jvxKO478SzyP/Es8j/tLPI/5SzyP+ks8j/5LPI//SzyP8ks8j2xKPI4ASzyPAks8jwJLPI8ASzyPAEs9kAAAAAAAAAAAAAAAAABLPI8ASzyPAEs8jwBLPI8BSzyPA0s8jwBLPI8eSzyPlUs8j/BLPI//SzyP/ks8j/9LPI//Sz2P/0s9j/9LPI//SzyP/0s8j/5LPI//SzyP70s8j5NLPI8cSzyPAEs8jwNLPI8BSzyPAEs8jwBLPI8AAAAAAAAAAAAAAAAAAAAAAAAAAABLPJAASzyPAEs8jwBLPI8ASzyPA0s8jwFLPI8ASzyPFEs8j1tLPI+eSzyPy0s8j+NLPI/tSzyP7Us8j+NLPI/LSzyPnUs8j1pLPI8TSzyPAEs8jwFLPI8DSzyPAEs8jwBLPI8ASz2OAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASzyPAEs8jwBLPI8ASzyPAks8jwRIPIoATD2QAEw+kABMPY8BSzyPDUs8jxlLPI8ZSzyPDUo+jgBKP48ASz6PAEs6jwBLPI8ESzyPAks8jwBLPI8ASzyPAAAAAAAAAAAAAAAAAAAAAAAAAAAA+hAIX/SAAS/pAACX1AAAK6gAABVQAAAKIAAABCAAAARAAAACQAAAAoAAAAGAAAABgAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAGAAAABgAAAAUAAAAJAAAACoAAABRAAAAhQAAAKqAAABdIAAEvpAACX9EACL/kIEJ8='
 
# 初始化pygame音频 mixer
pygame.mixer.init()
  
  
class Minesweeper:
    """扫雷游戏主类"""
  
    def __init__(self, root):
        self.root = root
        self.root.title("Python扫雷游戏")
        self.root.configure(bg='white')
        self.root.minsize(800, 600)
  
        # 创建游戏主框架
        self.main_frame = tk.Frame(self.root, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
  
        # 游戏音乐 - 使用用户指定的路径
        self.music_file = None
  
        # 计时器ID
        self.timer_id = None
  
        # 游戏难度设置
        self.difficulties = {
            "简单": {"width": 9, "height": 9, "mines": 10, "weight": 1.0},
            "中等": {"width": 16, "height": 16, "mines": 40, "weight": 0.8},
            "困难": {"width": 24, "height": 20, "mines": 99, "weight": 0.6}
        }
  
        # 加载排名
        self.rankings_file = "minesweeper_rankings.txt"
        self.rankings = self.load_rankings()
  
        # 显示开始界面
        self.show_start_screen()
        self.set_icon()
  
        # 开始播放音乐
        self.play_background_music()
 
    def set_icon(self):
        icon_name = '.mine.ico'
        if not os.path.exists(icon_name):
            icon = open(icon_name, 'wb')
            icon.write(b64decode(ICON_BASE64))
            icon.close()
        self.root.iconbitmap(icon_name)
 
    def load_rankings(self):
        """从TXT文件加载排名数据"""
        rankings = {"简单": [], "中等": [], "困难": []}
  
        if os.path.exists(self.rankings_file):
            try:
                with open(self.rankings_file, 'r', encoding='utf-8') as f:
                    current_difficulty = None
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        # 检查是否为难度标题行
                        if line in rankings:
                            current_difficulty = line
                        elif current_difficulty and line.startswith("排名"):
                            # 跳过表头行
                            continue
                        elif current_difficulty and line:
                            # 解析数据行: 排名 | 姓名 | 用时 | 得分 | 日期
                            parts = line.split('|')
                            if len(parts) >= 5:
                                try:
                                    # 去除各部分的首尾空格
                                    cleaned_parts = [part.strip() for part in parts]
                                    # 提取数据 (跳过排名列，因为它只是显示顺序)
                                    name = cleaned_parts[1]
                                    time_str = cleaned_parts[2].replace('秒', '')
                                    score_str = cleaned_parts[3]
                                    date = cleaned_parts[4]
  
                                    rankings[current_difficulty].append({
                                        "name": name,
                                        "time": int(time_str),
                                        "score": int(score_str),
                                        "date": date
                                    })
                                except (ValueError, IndexError):
                                    continue
            except Exception as e:
                print(f"加载排名时出错: {e}")
                # 出错时返回空排名
                return {"简单": [], "中等": [], "困难": []}
  
        # 按得分排序
        for difficulty in rankings:
            rankings[difficulty].sort(key=lambda x: x["score"], reverse=True)
  
        return rankings
  
    def save_rankings(self):
        """保存排名数据到TXT文件"""
        try:
            with open(self.rankings_file, 'w', encoding='utf-8') as f:
                for difficulty, records in self.rankings.items():
                    # 写入难度标题
                    f.write(f"{difficulty}\n")
  
                    if not records:
                        f.write("暂无排名数据\n\n")
                        continue
  
                    # 写入表头
                    f.write("排名 | 姓名 | 用时 | 得分 | 日期\n")
  
                    # 写入排名数据
                    for i, record in enumerate(records, 1):
                        f.write(f"{i} | {record['name']} | {record['time']}秒 | {record['score']} | {record['date']}\n")
  
                    f.write("\n")  # 添加空行分隔不同难度
        except Exception as e:
            print(f"保存排名时出错: {e}")
  
    def play_background_music(self):
        """播放背景音乐"""
        if self.music_file:
            try:
                # 尝试播放当前音乐
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(-1)  # -1表示循环播放
            except Exception as e:
                print(f"播放音乐时出错: {e}")
  
    def control_music(self):
        """控制音乐播放"""
        if self.music_file:
            # 如果只有一首音乐，切换播放状态
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            else:
                self.play_background_music()
        else:
            filetypes = (("mp3", "*.mp3"), ("无损音乐", "*.flac"))
            filename = filedialog.askopenfilename(title="选择音乐文件", filetypes=filetypes)
            if filename:
                self.music_file = filename
                self.play_background_music()
  
    def show_start_screen(self):
        """显示开始界面"""
        # 清除现有内容
        for widget in self.main_frame.winfo_children():
            widget.destroy()
             
        # 取消现有计时器
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
 
        # 标题
        title_label = tk.Label(
            self.main_frame,
            text="扫雷游戏",
            font=("Arial", 32, "bold"),
            fg="#2c3e50",
            bg='white'
        )
        title_label.pack(pady=(80, 40))
  
        # 开始游戏按钮
        start_btn = ttk.Button(
            self.main_frame,
            text="开始游戏",
            command=self.show_difficulty_selection,
            width=20
        )
        start_btn.pack(pady=10)
  
        # 游戏排名按钮
        ranking_btn = ttk.Button(
            self.main_frame,
            text="游戏排名",
            command=self.show_rankings,
            width=20
        )
        ranking_btn.pack(pady=10)
  
        # 音乐控制按钮
        music_btn = ttk.Button(
            self.main_frame,
            text="播放/暂停BGM",
            command=self.control_music,
            width=20
        )
        music_btn.pack(pady=10)
  
        # 退出游戏按钮
        exit_btn = ttk.Button(
            self.main_frame,
            text="退出游戏",
            command=self.root.quit,
            width=20
        )
        exit_btn.pack(pady=10)
  
    def show_difficulty_selection(self):
        """显示难度选择界面"""
        # 清除现有内容
        for widget in self.main_frame.winfo_children():
            widget.destroy()
 
        # 取消现有计时器
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
 
        # 标题
        title_label = tk.Label(
            self.main_frame,
            text="选择难度",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg='white'
        )
        title_label.pack(pady=(40, 30))
  
        # 难度选择按钮
        for difficulty in self.difficulties:
            btn = ttk.Button(
                self.main_frame,
                text=difficulty,
                command=lambda d=difficulty: self.start_game(d),
                width=20
            )
            btn.pack(pady=10)
  
        # 返回按钮
        back_btn = ttk.Button(
            self.main_frame,
            text="返回主菜单",
            command=self.show_start_screen,
            width=20
        )
        back_btn.pack(pady=20)
  
    def start_game(self, difficulty):
        """开始游戏"""
        # 获取难度设置
        settings = self.difficulties[difficulty]
        width = settings["width"]
        height = settings["height"]
        mines = settings["mines"]
  
        # 清除现有内容
        for widget in self.main_frame.winfo_children():
            widget.destroy()
  
        # 创建游戏顶部信息栏
        info_frame = tk.Frame(self.main_frame, bg='white')
        info_frame.pack(pady=10)
  
        # 地雷计数器
        self.mines_label = tk.Label(
            info_frame,
            text=f"地雷: {mines}",
            font=("Arial", 14),
            bg='white'
        )
        self.mines_label.pack(side=tk.LEFT, padx=20)
  
        # 计时器
        self.time_label = tk.Label(
            info_frame,
            text="时间: 0秒",
            font=("Arial", 14),
            bg='white'
        )
        self.time_label.pack(side=tk.RIGHT, padx=20)
  
        # 难度显示
        self.diff_label = tk.Label(
            info_frame,
            text=f"难度: {difficulty}",
            font=("Arial", 14),
            bg='white'
        )
        self.diff_label.pack(side=tk.RIGHT, padx=20)
  
        # 创建游戏网格框架
        grid_container = ttk.LabelFrame(
            self.main_frame,
            text="雷场",
            padding=10,
            style='GameArea.TLabelframe'
        )
        grid_container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
         
        # 添加样式
        style = ttk.Style()
        style.configure('GameArea.TLabelframe', 
                       background='white',
                       borderwidth=2,
                       relief='solid')
        style.configure('GameArea.TLabelframe.Label', 
                      font=('Arial', 12, 'bold'),
                      background='white')
         
        # 创建内部框架用于网格
        grid_frame = tk.Frame(
            grid_container, 
            bg='#333',  # 深色边框
            padx=2,     # 内边距
            pady=2      # 内边距
        )
        grid_frame.pack(expand=True)
  
        # 初始化游戏状态
        self.difficulty = difficulty
        self.width = width
        self.height = height
        self.mine_count = mines
        self.flags = set()
        self.revealed = set()
        self.game_over = False
        self.start_time = time.time()
        self.elapsed_time = 0
  
        # 创建游戏板
        self.create_board()
  
        # 创建按钮网格
        self.buttons = [[None for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                btn = tk.Button(
                    grid_frame,
                    width=2,
                    height=1,
                    font=("Arial", 10, "bold"),
                    relief=tk.RAISED,
                    bg='#f0f0f0',
                    borderwidth=1,
                    command=lambda x=x, y=y: self.reveal_cell(x, y)
                )
                btn.grid(row=y, column=x, padx=0, pady=0, sticky='nsew')
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.flag_cell(x, y))
                self.buttons[y][x] = btn
                 
        # 设置网格权重，使按钮居中显示
        for i in range(width):
            grid_frame.columnconfigure(i, weight=1)
        for i in range(height):
            grid_frame.rowconfigure(i, weight=1)
  
        # 按钮框架
        button_frame = tk.Frame(self.main_frame, bg='white')
        button_frame.pack(pady=10)
  
        # 返回按钮
        back_btn = ttk.Button(
            button_frame,
            text="返回主菜单",
            command=self.show_start_screen,
            width=15
        )
        back_btn.pack(side=tk.LEFT, padx=10)
 
        # 重新选择难度
        difficulty_btn = ttk.Button(
            button_frame,
            text="重新选择难度",
            command=self.show_difficulty_selection,
            width=15
        )
        difficulty_btn.pack(side=tk.LEFT, padx=10)
  
        # 重新开始按钮
        restart_btn = ttk.Button(
            button_frame,
            text="重新开始",
            command=lambda: self.start_game(difficulty),
            width=15
        )
        restart_btn.pack(side=tk.LEFT, padx=10)
  
        # 开始计时
        self.update_timer()
  
    def create_board(self):
        """创建游戏板并随机放置地雷"""
        # 初始化空白板
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
  
        # 放置地雷
        mines_placed = 0
        while mines_placed < self.mine_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != -1:  # 如果不是地雷
                self.board[y][x] = -1  # -1表示地雷
                mines_placed += 1
  
                # 更新周围单元格的数字
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] != -1:
                            self.board[ny][nx] += 1
  
    def reveal_cell(self, x, y):
        """揭示单元格"""
        if self.game_over or (x, y) in self.flags or (x, y) in self.revealed:
            return
  
        # 添加到已揭示集合
        self.revealed.add((x, y))
        btn = self.buttons[y][x]
        btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
  
        # 检查是否踩到地雷
        if self.board[y][x] == -1:
            btn.config(bg='red', text='&#128163;')
            self.game_over = True
            self.show_game_over(False)
            return
  
        # 更新按钮文本
        if self.board[y][x] > 0:
            # 设置不同数字的颜色
            colors = ['blue', 'green', 'red', 'purple', 'maroon', 'turquoise', 'black', 'gray']
            btn.config(text=str(self.board[y][x]), bg='white', fg=colors[self.board[y][x] - 1], state=tk.NORMAL)
        else:
            # 如果是空白单元格，递归揭示周围的单元格
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal_cell(nx, ny)
  
        # 检查是否获胜
        if len(self.revealed) == self.width * self.height - self.mine_count:
            self.game_over = True
            self.show_game_over(True)
  
    def flag_cell(self, x, y):
        """标记/取消标记单元格为地雷"""
        if self.game_over or (x, y) in self.revealed:
            return
  
        btn = self.buttons[y][x]
        if (x, y) in self.flags:
            # 取消标记
            self.flags.remove((x, y))
            btn.config(text='', bg='#f0f0f0')
        else:
            # 标记
            self.flags.add((x, y))
            btn.config(text='&#128681;', bg='#ffec8b')
  
        # 更新地雷计数器
        self.mines_label.config(text=f"地雷: {self.mine_count - len(self.flags)}")
  
    def update_timer(self):
        """更新计时器"""
        if not self.game_over:
            self.elapsed_time = int(time.time() - self.start_time)
            self.time_label.config(text=f"时间: {self.elapsed_time}秒")
            self.timer_id = self.root.after(1000, self.update_timer)
  
    def show_game_over(self, won):
        """显示游戏结束界面"""
        if won:
            # 计算得分（考虑难度加权和时间）
            difficulty_weight = self.difficulties[self.difficulty]["weight"]
            score = int((10000 / (self.elapsed_time + 1)) * difficulty_weight)
  
            # 提示输入姓名
            name = simpledialog.askstring("游戏胜利",
                                          f"恭喜您赢了！用时: {self.elapsed_time}秒\n得分: {score}\n请输入您的姓名:",
                                          parent=self.root)
  
            if name:
                # 添加到排名
                if self.difficulty not in self.rankings:
                    self.rankings[self.difficulty] = []
  
                self.rankings[self.difficulty].append({
                    "name": name,
                    "time": self.elapsed_time,
                    "score": score,
                    "date": time.strftime("%Y-%m-%d %H:%M")
                })
  
                # 按得分排序
                self.rankings[self.difficulty].sort(key=lambda x: x["score"], reverse=True)
  
                # 只保留前10名
                if len(self.rankings[self.difficulty]) > 10:
                    self.rankings[self.difficulty] = self.rankings[self.difficulty][:10]
  
                # 保存排名
                self.save_rankings()
  
            messagebox.showinfo("游戏胜利", f"恭喜您赢了！用时: {self.elapsed_time}秒\n得分: {score}")
        else:
            # 游戏失败时显示所有地雷
            for y in range(self.height):
                for x in range(self.width):
                    if self.board[y][x] == -1 and (x, y) not in self.flags:
                        self.buttons[y][x].config(text='&#128163;', bg='#ffcccc')
                    elif self.board[y][x] == -1 and (x, y) in self.flags:
                        self.buttons[y][x].config(bg='#ccffcc')  # 正确标记的地雷
  
            messagebox.showinfo("游戏结束", "很遗憾，您踩到地雷了！")
  
    def show_rankings(self):
        """显示排名界面"""
        # 清除现有内容
        for widget in self.main_frame.winfo_children():
            widget.destroy()
  
        # 标题
        title_label = tk.Label(
            self.main_frame,
            text="游戏排名",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg='white'
        )
        title_label.pack(pady=(20, 20))
  
        # 创建笔记本式选项卡
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
  
        # 为每个难度创建排名选项卡
        for difficulty in self.difficulties:
            frame = tk.Frame(notebook, bg='white')
            notebook.add(frame, text=difficulty)
  
            # 创建文本控件显示排名
            text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12), bg='white')
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
  
            # 添加排名数据
            text_widget.insert(tk.END, f"{difficulty}难度排名\n\n")
  
            if difficulty in self.rankings and self.rankings[difficulty]:
                # 添加表头
                text_widget.insert(tk.END, "排名  姓名        用时      得分        日期\n")
                text_widget.insert(tk.END, "------------------------------------------------\n")
  
                # 添加排名数据
                for i, entry in enumerate(self.rankings[difficulty], 1):
                    text_widget.insert(tk.END,
                                       f"{i:<4} {entry['name']:<10} {entry['time']:>4}秒 {entry['score']:>8} {entry['date']:>16}\n")
            else:
                text_widget.insert(tk.END, "暂无排名数据\n")
  
            text_widget.config(state=tk.DISABLED)  # 设置为只读
  
            # 打包组件
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
  
        # 返回按钮
        back_btn = ttk.Button(
            self.main_frame,
            text="返回主菜单",
            command=self.show_start_screen,
            width=20
        )
        back_btn.pack(pady=20)
  
  
# 运行游戏
if __name__ == "__main__":
    # 打包命令 pyinstaller -F -w -i .mine.ico saolei.py
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()