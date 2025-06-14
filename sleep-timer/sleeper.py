import os
import tkinter as tk
from tkinter import ttk, messagebox
import ctypes

"""
Resources:
https://stackoverflow.com/a/37009921
https://www.reddit.com/r/pythontips/comments/129ec3p/shutdown_pcmac_with_python/

"""

#####

"""
- BUG:
    
- TODO: 

    Icon tray
    Autostart at login - optional in settings
    Settings -> Default timer, autostart on login + auto-minimize -> Save settings
    Store last used timer
    Portable
    Cross platform?
    Packing/build
    
"""


class Config:
    DEBUGGING = True # Bool
    ONE_SECOND_IN_MS = 1000 # Default: 1000 -> Decrease for faster countdown

    SMALL = 5
    MEDIUM = 10
    WIDTH = 300
    HEIGHT = 300


class TimerInput(ttk.LabelFrame):

    def __init__(self):
        super().__init__(master=None, text='Sleep timer')

        self.hours_label = ttk.Label(self, text='Hours:')
        self.grid_with_padding(self.hours_label, row=0, column=0)

        self.hours_entry = ttk.Entry(self, width=Config.SMALL)
        self.grid_with_padding(self.hours_entry, row=0, column=1)
        self.hours_entry.insert(tk.END, '0')

        self.minutes_label = ttk.Label(self, text='Minutes:')
        self.grid_with_padding(self.minutes_label, row=0, column=2)

        self.minutes_entry = ttk.Entry(self, width=Config.SMALL)
        self.grid_with_padding(self.minutes_entry, row=0, column=3)
        self.minutes_entry.insert(tk.END, '0')

    def grid_with_padding(self, widget, **kwargs):
        widget.grid(padx=Config.SMALL, pady=Config.SMALL, **kwargs)

    def get_total_seconds(self):
        try:
            hours = int(self.hours_entry.get() or 0)
            minutes = int(self.minutes_entry.get() or 0)
            total_seconds = (hours * 3600) + (minutes * 60)
            return total_seconds
        except ValueError:
            return


class OptionHandler:
    def execute(option):
        app.log_message(f"Executing {option}")
        if Config.DEBUGGING:
            return

        try:
            if option == 'sleep':
                os.system("Powercfg -H OFF")
                os.system("Rundll32.exe Powrprof.dll,SetSuspendState Sleep")
            elif option == 'hibernate':
                os.system("Powercfg -H ON")
                os.system("Rundll32.exe Powrprof.dll,SetSuspendState Hibernate")
            elif option == 'shutdown':
                os.system("shutdown /s /t 0")
        except Exception as e:
            print(f"Error executing {option}: {e}")


class OptionFrame(ttk.LabelFrame):
    # ? Make the class smaller?
    def __init__(self):
        super().__init__(master=None)
        self.radio_var = tk.StringVar(value='sleep')

        self.radio_frame = ttk.LabelFrame(self, text='Options')
        self.radio_frame.pack(padx=Config.MEDIUM, pady=Config.MEDIUM)

        for mode in ('sleep', 'hibernate', 'shutdown'):
            self.radio_option = ttk.Radiobutton(
                master=self.radio_frame,
                text=mode.title(),
                variable=self.radio_var,
                value=mode
            )
            self.radio_option.pack(anchor='w')

        self.start_button = ttk.Button(
            self, text='Start', command=self.start_button_command)
        self.start_button.pack(pady=Config.MEDIUM)

        self.stop_button = ttk.Button(
            self, text='Stop', command=self.stop_button_command)

    def validate_timer(self):
        total_seconds = app.timer_input.get_total_seconds()
        if total_seconds is None:
            app.log_message(
                "Invalid input, please try again using only numbers.")
            return

        if total_seconds <= 0:
            confirm = messagebox.askokcancel(
                title="Do you want to continue?",
                message="To you want to execute the option immediately?"
            )
            if not confirm:
                return
        return total_seconds

    def start_button_command(self) -> None:
        # ? Auto minimize?
        # app.iconify()
        total_seconds = self.validate_timer()
        if total_seconds is None:
            return

        app.replace_widget(
            app.timer_input, app.countdown_timer, app.option_frame)
        app.replace_widget(self.start_button, self.stop_button)

        option = self.radio_var.get()
        if total_seconds > 0:  # ! Bug - total_seconds is None in some cases.
            app.countdown_timer.start(total_seconds)
            app.log_message(
                f"The system will {option} when the timer reaches zero.")
        else:
            OptionHandler.execute(option=option)
            #! Disabled for debugging
            # app.destroy()

    def stop_button_command(self) -> None:
        app.countdown_timer.stop()
        app.replace_widget(self.stop_button, self.start_button)
        app.replace_widget(app.countdown_timer,
                           app.timer_input, app.option_frame)
        if hasattr(app, 'log_label'):
            app.log_label.config(text='')


class CountdownTimer(ttk.LabelFrame):
    def __init__(self):
        super().__init__(master=None)
        self.is_running = False
        self.remaining_seconds = 0

        self.time_label = tk.Label(self, text="00:00:00", font=("Arial", 17))
        self.time_label.pack()
        # self.time_label.pack(pady=10)

    def start(self, total_seconds):
        self.remaining_seconds = total_seconds
        self.is_running = True
        self.update_display()
        self.master.after(Config.ONE_SECOND_IN_MS, self.update)

    def stop(self):
        self.is_running = False
        self.remaining_seconds = 0
        self.update_display()

    def update_display(self):
        hours, left_over = divmod(self.remaining_seconds, 60 * 60)
        minutes, seconds = divmod(left_over, 60)
        time_str = "{:02d}:{:02d}:{:02d}".format(
            int(hours), int(minutes), int(seconds))
        self.time_label.config(text=time_str)

    def update(self) -> None:
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            self.master.after(Config.ONE_SECOND_IN_MS, self.update)
        elif self.is_running:
            self.finish()

    def finish(self):
        self.is_running = False
        option = app.option_frame.radio_var.get()
        OptionHandler.execute(option)
        app.log_message(f"Executed option: {option}")
        app.replace_widget(app.countdown_timer,
                           app.timer_input, app.option_frame)
        app.replace_widget(app.option_frame.stop_button,
                           app.option_frame.start_button)


class App(tk.Tk):
    TITLE = "Sleeper"

    def __init__(self):
        super().__init__()

        self.title(App.TITLE)
        self.geometry(f"{Config.WIDTH}x{Config.HEIGHT}")

        self.timer_input = TimerInput()
        self.option_frame = OptionFrame()
        self.countdown_timer = CountdownTimer()

        self.timer_input.pack(padx=Config.SMALL, pady=Config.SMALL)
        self.option_frame.pack()

        self.center_window(self)

    def log_message(self, msg):
        #! For debugging purposes - it's now a feature.
        if not hasattr(self, 'log_label'):
            self.log_label = tk.Label(self, text="", fg="red", wraplength=300)
            self.log_label.pack(pady=5)
        self.log_label.config(text=msg)

    def center_window(self, window) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (Config.WIDTH // 2)
        y = (screen_height // 2) - (Config.HEIGHT // 2)

        window.geometry(f"{Config.WIDTH}x{Config.HEIGHT}+{x}+{y}")

    def replace_widget(self, old_widget, new_widget, before=None) -> None:
        padx = old_widget.pack_info()['padx']
        pady = old_widget.pack_info()['pady']

        old_widget.pack_forget()
        new_widget.pack(padx=padx, pady=pady, before=before)


def is_admin() -> bool:
    # Check if the current process has administrative privileges
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        app.log_message(e)
        return False


def no_admin_disclaimer() -> None:
    messagebox.showinfo(
        title="Info",
        message="Admin privileges not detected. Some features may not work as expected."
    )


def debugging_message():
    messagebox.showinfo(
        title="Info",
        message="Debugging enabled, execution features disabled."
    )


def hide_terminal() -> None:
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 0)


if __name__ == "__main__":
    if Config.DEBUGGING:
        debugging_message()
    elif is_admin():
        no_admin_disclaimer()

    app = App()
    app.focus_force()
    app.mainloop()
