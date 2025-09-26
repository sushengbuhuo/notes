
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import sys
import platform
import numpy as np
import time
#https://www.52pojie.cn/thread-2050054-1-1.html 摸鱼的时候可以调用电脑的摄像头事实查看背后的情况，同时可以画出一个监控区域，如果该区域出现画面变动时则抖动屏幕提醒自己该注意是否有人过来了。
class CameraFloatingWindow:
    def __init__(self, width=640):
        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("错误：无法打开摄像头！")
            sys.exit(1)

        # 获取原始分辨率并计算比例
        _, frame = self.cap.read()
        self.orig_height, self.orig_width = frame.shape[:2]
        self.aspect_ratio = self.orig_height / self.orig_width

        # 设置显示尺寸
        self.display_width = width
        self.display_height = int(width * self.aspect_ratio)

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("智能监控悬浮窗")
        self.root.geometry(f"{self.display_width}x{self.display_height + 40}")
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.95)  # 90%透明度
        self.root.attributes("-topmost", True)

        # 添加标题栏
        self.title_bar = ttk.Frame(self.root, height=30)
        self.title_bar.pack(fill=tk.X)
        ttk.Label(self.title_bar, text="智能监控 (ESC退出)").pack(side=tk.LEFT, padx=10)

        # 添加拖拽功能
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

        # 创建控制按钮框架
        control_frame = ttk.Frame(self.title_bar)
        control_frame.pack(side=tk.RIGHT, padx=5)

        # 添加控制按钮
        ttk.Button(
            control_frame, 
            text="选择区域", 
            width=8,
            command=self.start_area_selection
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            control_frame, 
            text="清除", 
            width=5,
            command=self.clear_selection
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            control_frame, 
            text="X", 
            width=3, 
            command=self.close_app
        ).pack(side=tk.LEFT, padx=2)

        # 创建图像显示区域
        self.canvas = tk.Canvas(self.root, width=self.display_width, height=self.display_height)
        self.canvas.pack()

        # 区域选择相关变量
        self.selection_start = None
        self.selection_end = None
        self.monitor_rect = None
        self.monitor_active = False
        self.previous_roi = None
        self.detection_threshold = 500  # 变动检测阈值
        self.highlight_timer = 0
        self.alert_active = False

        # 防抖动相关参数 [1](@ref)
        self.stabilizer = VideoStabilizer()

        # 绑定鼠标事件用于区域选择
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # 启动摄像头线程
        self.running = True
        self.thread = threading.Thread(target=self.update_frame)
        self.thread.daemon = True
        self.thread.start()

        # 绑定ESC退出
        self.root.bind("<Escape>", lambda e: self.close_app())

        # 启动主循环
        self.root.mainloop()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def start_area_selection(self):
        self.monitor_active = True
        messagebox.showinfo("操作提示", "请在预览画面中拖动鼠标选择监控区域")

    def clear_selection(self):
        self.selection_start = None
        self.selection_end = None
        self.monitor_rect = None
        self.monitor_active = False
        self.alert_active = False
        self.canvas.delete("selection")
        self.canvas.delete("highlight")

    def on_mouse_press(self, event):
        if self.monitor_active:
            self.selection_start = (event.x, event.y)
            self.canvas.delete("selection")

    def on_mouse_drag(self, event):
        if self.monitor_active and self.selection_start:
            self.selection_end = (event.x, event.y)
            self.canvas.delete("selection")

            # 绘制半透明选择矩形
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            self.monitor_rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="red",
                fill="",
                dash=(4, 4),
                tags="selection"
            )

    def on_mouse_release(self, event):
        if self.monitor_active and self.selection_start and self.selection_end:
            # 约束坐标在画布范围内
            x1, y1 = self.selection_start
            x2, y2 = event.x, event.y
            x1 = max(0, min(x1, self.display_width-1))
            y1 = max(0, min(y1, self.display_height-1))
            x2 = max(0, min(x2, self.display_width-1))
            y2 = max(0, min(y2, self.display_height-1))
            self.selection_start = (min(x1, x2), min(y1, y2))
            self.selection_end = (max(x1, x2), max(y1, y2))

            # 更新矩形坐标
            if self.monitor_rect:
                self.canvas.coords(
                    self.monitor_rect,
                    self.selection_start[0], self.selection_start[1],
                    self.selection_end[0], self.selection_end[1]
                )

            # 初始化前一帧（灰度图）
            _, frame = self.cap.read()
            if frame is not None:
                frame = cv2.resize(frame, (self.display_width, self.display_height))
                self.previous_roi = self.get_roi_frame(frame)

    def get_roi_frame(self, frame):
        """获取选择的监控区域（直接返回灰度图）"""
        if self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end

            # 确保坐标在有效范围内
            x1 = max(0, min(x1, self.display_width-1))
            y1 = max(0, min(y1, self.display_height-1))
            x2 = max(0, min(x2, self.display_width-1))
            y2 = max(0, min(y2, self.display_height-1))

            # 确保区域有效
            if x2 > x1 and y2 > y1:
                roi = frame[int(y1):int(y2), int(x1):int(x2)]
                return cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        return None

    def detect_movement(self, current_roi):
        """检测区域内的变动（增强鲁棒性）[1](@ref)"""
        if current_roi is None or self.previous_roi is None:
            return False

        # 确保两帧尺寸相同（防止区域变化导致尺寸不一致）
        if current_roi.shape != self.previous_roi.shape:
            current_roi = cv2.resize(current_roi, (self.previous_roi.shape[1], self.previous_roi.shape[0]))

        # 计算差异（两帧均为灰度图）
        diff = cv2.absdiff(current_roi, self.previous_roi)
        _, diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # 计算变动像素数量
        changed_pixels = cv2.countNonZero(diff)

        # 更新前一帧
        self.previous_roi = current_roi.copy()

        return changed_pixels > self.detection_threshold

    def highlight_area(self):
        """高亮显示监控区域"""
        if self.selection_start and self.selection_end:
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end

            # 删除旧的高亮
            self.canvas.delete("highlight")

            # 创建闪烁的高亮矩形
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="yellow",
                width=3,
                tags="highlight"
            )

    def window_shake(self):
        """窗口抖动效果 [3](@ref)"""
        if not self.alert_active:
            self.alert_active = True
            orig_x = self.root.winfo_x()
            orig_y = self.root.winfo_y()

            # 抖动动画
            for i in range(10):
                offset = 5 if i % 2 == 0 else -5
                self.root.geometry(f"+{orig_x + offset}+{orig_y}")
                self.root.update()
                time.sleep(0.02)

            # 恢复原位
            self.root.geometry(f"+{orig_x}+{orig_y}")
            self.alert_active = False

    def update_frame(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # 应用视频防抖动处理 [1](@ref)
                frame = self.stabilizer.stabilize(frame)

                # 调整尺寸并转换颜色空间
                frame = cv2.resize(frame, (self.display_width, self.display_height))
                display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 检测区域变动
                if self.monitor_active and self.selection_start and self.selection_end:
                    try:
                        roi_frame = self.get_roi_frame(frame)

                        if roi_frame is not None and self.previous_roi is not None:
                            if self.detect_movement(roi_frame):
                                self.highlight_timer = 10  # 设置高亮持续时间
                                self.window_shake()  # 触发窗口抖动
                    except Exception as e:
                        print(f"检测错误: {e}")
                        self.clear_selection()

                # 处理高亮显示
                if self.highlight_timer > 0:
                    self.highlight_area()
                    self.highlight_timer -= 1
                else:
                    self.canvas.delete("highlight")

                # 转换为Tkinter图像
                img = Image.fromarray(display_frame)
                imgtk = ImageTk.PhotoImage(image=img)

                # 更新Canvas
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.image = imgtk  # 保持引用

    def close_app(self):
        self.running = False
        self.cap.release()
        self.root.destroy()

class VideoStabilizer:
    """视频防抖动处理类 [1,2](@ref)"""
    def __init__(self, smooth_radius=10):
        self.smooth_radius = smooth_radius
        self.prev_gray = None
        self.transforms = []
        self.max_frames = 50

    def stabilize(self, frame):
        if frame is None:
            return frame

        # 转换为灰度图
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 如果是第一帧，只需保存灰度图并返回原帧
        if self.prev_gray is None:
            self.prev_gray = curr_gray
            return frame

        # 检测前一帧的特征点
        prev_pts = cv2.goodFeaturesToTrack(
            self.prev_gray, 
            maxCorners=200,
            qualityLevel=0.01,
            minDistance=30,
            blockSize=3
        )

        if prev_pts is None:
            self.prev_gray = curr_gray
            return frame

        # 计算光流
        curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(
            self.prev_gray, curr_gray, prev_pts, None
        )

        # 筛选有效点
        if status is not None:
            idx = np.where(status == 1)[0]
            prev_pts = prev_pts[idx]
            curr_pts = curr_pts[idx]

        # 估计仿射变换
        if len(prev_pts) >= 3:
            m, _ = cv2.estimateAffinePartial2D(prev_pts, curr_pts)
        else:
            m = np.eye(2, 3, dtype=np.float32)

        if m is None:
            m = np.eye(2, 3, dtype=np.float32)

        # 提取变换参数
        dx = m[0, 2]
        dy = m[1, 2]
        da = np.arctan2(m[1, 0], m[0, 0])

        # 存储变换
        self.transforms.append([dx, dy, da])
        if len(self.transforms) > self.max_frames:
            self.transforms.pop(0)

        # 平滑变换
        if len(self.transforms) > 0:
            smoothed = self.smooth_trajectory()
            # 应用平滑后的变换
            m = self.get_smoothed_transform(smoothed)
            frame_stabilized = cv2.warpAffine(frame, m, (frame.shape[1], frame.shape[0]))
        else:
            frame_stabilized = frame

        self.prev_gray = curr_gray
        return frame_stabilized

    def smooth_trajectory(self):
        trajectory = np.array(self.transforms)
        smoothed = np.copy(trajectory)

        for i in range(3):
            smoothed[:, i] = self.moving_average(trajectory[:, i], self.smooth_radius)

        return smoothed

    def moving_average(self, curve, radius):
        window_size = 2 * radius + 1
        f = np.ones(window_size) / window_size
        # curve_pad = np.pad(curve, (radius, radius), mode='edge')
        curve_pad = np.lib.pad(curve, (radius, radius), 'edge')
        curve_smoothed = np.convolve(curve_pad, f, mode='same')
        return curve_smoothed[radius:-radius]

    def get_smoothed_transform(self, smoothed):
        # 获取最新的平滑变换
        dx, dy, da = smoothed[-1]

        # 重构变换矩阵
        m = np.zeros((2, 3), np.float32)
        m[0, 0] = np.cos(da)
        m[0, 1] = -np.sin(da)
        m[1, 0] = np.sin(da)
        m[1, 1] = np.cos(da)
        m[0, 2] = -dx
        m[1, 2] = -dy

        return m

if __name__ == "__main__":
    # 根据操作系统调整DPI
    if platform.system() == "Windows":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)

    # 启动悬浮窗
    app = CameraFloatingWindow(width=600)
