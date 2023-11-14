import tkinter as tk
import time
import os
 
class ShutdownTimer:
    def __init__(self, master):
        self.master = master
        master.title("定时关机")
 
        self.hours_label = tk.Label(master, text="小时")
        self.hours_label.grid(row=0, column=0)
 
        self.hours_entry = tk.Entry(master)
        self.hours_entry.grid(row=0, column=1)
 
        self.minutes_label = tk.Label(master, text="分钟")
        self.minutes_label.grid(row=1, column=0)
 
        self.minutes_entry = tk.Entry(master)
        self.minutes_entry.grid(row=1, column=1)
 
        self.seconds_label = tk.Label(master, text="秒")
        self.seconds_label.grid(row=2, column=0)
 
        self.seconds_entry = tk.Entry(master)
        self.seconds_entry.grid(row=2, column=1)
 
        self.date_label = tk.Label(master, text="日期")
        self.date_label.grid(row=3, column=0)
 
        self.date_entry = tk.Entry(master)
        self.date_entry.grid(row=3, column=1)
 
        self.shutdown_button = tk.Button(master, text="开始关机", command=self.shutdown)
        self.shutdown_button.grid(row=4, column=0, columnspan=2)
 
        self.countdown_label = tk.Label(master, text="", font=("Helvetica", 36))
        self.countdown_label.grid(row=5, column=0, columnspan=2)
 
    def shutdown(self):
        hours = int(self.hours_entry.get())
        minutes = int(self.minutes_entry.get())
        seconds = int(self.seconds_entry.get())
        date = self.date_entry.get()
 
        shutdown_time = time.mktime(time.strptime(date, "%Y-%m-%d")) + hours * 3600 + minutes * 60 + seconds
 
        while True:
            remaining_time = shutdown_time - time.time()
 
            if remaining_time <= 0:
                os.system("shutdown /s /t 1")
                break
 
            hours, remaining_time = divmod(remaining_time, 3600)
            minutes, remaining_time = divmod(remaining_time, 60)
            seconds = remaining_time
 
            self.countdown_label.config(text="{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds)))
            self.master.update()
            time.sleep(0.1)
 
root = tk.Tk()
my_gui = ShutdownTimer(root)
root.mainloop()