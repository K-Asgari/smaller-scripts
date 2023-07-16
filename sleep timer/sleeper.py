import os
import tkinter as tk
from tkinter import ttk
import time

"""
Footnotes:
1) https://stackoverflow.com/a/37009921
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
        self.hours_entry.insert(tk.END, '0')

        self.minutes_label = ttk.Label(self.label_frame, text='Minutes:')
        self.minutes_label.grid(row=0, column=2, padx=5, pady=5)

        self.minutes_entry = ttk.Entry(self.label_frame, width=5)
        self.minutes_entry.grid(row=0, column=3, padx=5, pady=5)
        self.minutes_entry.insert(tk.END, '0')

        self.button = ttk.Button(self, text='Start')
        self.button['command'] = self.sleep
        self.button.pack(pady=10)

    def sleep(self):
        try:
            hours = int(self.hours_entry.get()) 
            minutes = int(self.minutes_entry.get())
            if hours == 0 and minutes == 0:
                raise ValueError(
                    "Please set a value greater than zero for hours or minutes.")
        except ValueError as e:
            print(e)
        else:
            total_minutes = (hours * 60) + minutes
            print("Timer started!")
            print(f"{total_minutes} minutes until sleep")
            print("Terminate terminal to cancel sleep timer.")
            self.iconify()
            time.sleep(60 * total_minutes)

            
            os.system("Rundll32.exe Powrprof.dll,SetSuspendState Sleep") # Footnote 1


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
