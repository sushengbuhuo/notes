import time
import pyautogui


def main():
    print("鼠标位置监控已启动，按 Ctrl+C 可停止程序\n")
    print(f"{'时间':<20} | {'鼠标坐标 (X, Y)'}")
    print("-" * 45)

    try:
        while True:
            # 获取当前鼠标位置
            x, y = pyautogui.position()

            # 获取当前时间并格式化输出
            current_time = time.strftime("%H:%M:%S")
            print(f"{current_time:<20} | ({x}, {y})")

            # 等待 2 秒
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n\n程序已结束。")


if __name__ == "__main__":
    main()
