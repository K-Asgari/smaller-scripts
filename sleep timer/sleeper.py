import os
import tkinter as tk
from tkinter import ttk
import time

"""
Resource:
https://stackoverflow.com/a/37009921
"""


class TimerGUI(tk.Tk):
    WIDTH = 300
    HEIGHT = 250

    def __init__(self):
        super().__init__()

        self.title('Sleep timer')
        self.geometry(f"{TimerGUI.WIDTH}x{TimerGUI.HEIGHT}")

        # tkinter widgets and placement
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

        self.radio_var = tk.StringVar()
        self.radio_var.set('sleep')

        self.radio_frame = ttk.LabelFrame(self, text='Options')
        self.radio_frame.pack(padx=10, pady=10)

        for mode in ('sleep', 'hibernate', 'shutdown'):
            self.radio_option = ttk.Radiobutton(
                self.radio_frame, text=mode.title(), variable=self.radio_var, value=mode)
            self.radio_option.pack(anchor='w')

        self.button = ttk.Button(self, text='Start')
        self.button['command'] = self.sleep
        self.button.pack(pady=10)

    def sleep(self):
        try:
            zero_minutes_error = "Please select a time duration of at least 1 minute or more."
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            if hours == 0 and minutes == 0:
                raise ValueError(zero_minutes_error)
        except ValueError as e:
            if str(e) == zero_minutes_error:
                print(e)
            else:
                print("Invalid input, please try again using only numbers.")
        else:
            total_minutes = (hours * 60) + minutes
            print("Timer started!")
            print(f"{total_minutes} minutes until sleep")
            print("Terminate terminal to cancel sleep timer.")
            self.iconify()
            time.sleep(60 * total_minutes)
            self.destroy()
            option = self.radio_var.get()
            if option == 'sleep':
                os.system("Powercfg -H OFF")
                os.system("Rundll32.exe Powrprof.dll,SetSuspendState Sleep")
            elif option == 'hibernate':
                os.system("Powercfg -H ON")
                os.system("Rundll32.exe Powrprof.dll,SetSuspendState Hibernate")
            elif option == 'shutdown':
                os.system("shutdown /s /t 0")


def center_window(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (window.WIDTH // 2)
    y = (screen_height // 2) - (window.HEIGHT // 2)

    window.geometry(f"{window.WIDTH}x{window.HEIGHT}+{x}+{y}")


def is_admin():
    try:
        # Check if the current process has administrative privileges
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


if __name__ == "__main__":
    if is_admin():
        exit(-1)

    app = TimerGUI()
    center_window(app)
    app.mainloop()
