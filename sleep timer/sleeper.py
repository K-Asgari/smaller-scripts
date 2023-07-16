import os
import tkinter as tk
from tkinter import ttk
import time

"""

Hibernation mode by default. Follow the link below to disable hibernation mode and set the computer in sleep instead. 

https://stackoverflow.com/a/37009921
"""

class TimerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Sleep timer')
        self.geometry('300x200')

        self.label_frame = ttk.LabelFrame(self, text='Sleep timer')
        self.label_frame.pack(padx=10, pady=10)

        self.hours_label = ttk.Label(self.label_frame, text='Hours:')
        self.hours_label.grid(row=0, column=0, padx=5, pady=5)

        self.hours_entry = ttk.Entry(self.label_frame, width=5)
        self.hours_entry.grid(row=0, column=1, padx=5, pady=5)

        self.minutes_label = ttk.Label(self.label_frame, text='Minutes:')
        self.minutes_label.grid(row=0, column=2, padx=5, pady=5)

        self.minutes_entry = ttk.Entry(self.label_frame, width=5)
        self.minutes_entry.grid(row=0, column=3, padx=5, pady=5)

        self.button = ttk.Button(self, text='Start')
        self.button['command'] = self.sleep
        self.button.pack(pady=10)

    def sleep(self):
        try:
            hours = int(self.hours_entry.get()) if self.hours_entry.get() else 0
            minutes = int(self.minutes_entry.get()) if self.minutes_entry.get() else 0
        except ValueError as e:
            print(e)
        else:
            total_minutes = (hours * 60) + minutes
            print("Timer started!")
            print(f"{total_minutes} minutes until sleep")
            self.iconify()
            time.sleep(60 * total_minutes)
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def center_window(window):
    window_width = 300
    window_height = 200

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")


if __name__ == "__main__":
    app = TimerGUI()
    center_window(app)
    app.mainloop()
