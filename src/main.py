import os
import tkinter as tk
from tkinter import ttk, messagebox
from tray_icon import TrayIcon

import system_utils

"""
Resources:
https://stackoverflow.com/a/37009921
https://www.reddit.com/r/pythontips/comments/129ec3p/shutdown_pcmac_with_python/

"""

#####


class Config:
    DEBUGGING = True

    ###
    SMALL = 5
    MEDIUM = 10
    APP_WIDTH = 300
    APP_HEIGHT = 250
    ONE_SECOND_IN_MS = 1000 if not DEBUGGING else 10


class App(tk.Tk):
    TITLE = "Sleeper"

    def __init__(self):
        super().__init__()

        self.title(App.TITLE)
        self.geometry(f"{Config.APP_WIDTH}x{Config.APP_HEIGHT}")

        self.timer_input = TimerInput(self)
        self.option_frame = OptionFrame(self)
        self.countdown_timer = CountdownTimer(self)

        self.timer_input.pack(padx=Config.SMALL, pady=Config.SMALL)
        self.option_frame.pack()

        self.center_window(self)

        self.tray = TrayIcon(self, icon_path="sleeper-icon.ico")
        self.tray.start()
        self.protocol("WM_DELETE_WINDOW", self.withdraw)



    def log_message(self, msg):
        # ! For debugging purposes - it's now a feature.
        if not hasattr(self, 'log_label'):
            self.log_label = tk.Label(self, text="", fg="red", wraplength=300)
            self.log_label.pack(padx=Config.SMALL, pady=Config.SMALL)
        self.log_label.config(text=msg)

    def center_window(self, window) -> None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (Config.APP_WIDTH // 2)
        y = (screen_height // 2) - (Config.APP_HEIGHT // 2)

        window.geometry(f"{Config.APP_WIDTH}x{Config.APP_HEIGHT}+{x}+{y}")

    def replace_widget(self, old_widget, new_widget, before=None) -> None:
        padx = old_widget.pack_info()['padx']
        pady = old_widget.pack_info()['pady']

        old_widget.pack_forget()
        new_widget.pack(padx=padx, pady=pady, before=before)

    @staticmethod
    def change_children_state(master, new_state):
        if new_state not in (tk.NORMAL, tk.DISABLED):
            raise ValueError("new_state should only be normal or active")

        for button in master.winfo_children():
            button.configure(state=new_state)


class TimerInput(ttk.LabelFrame):

    def __init__(self, app):
        super().__init__(master=app, text='Sleep timer')

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
            hours = int(self.hours_entry.get().strip() or 0)
            minutes = int(self.minutes_entry.get().strip() or 0)
            total_seconds = (hours * 3600) + (minutes * 60)
            return total_seconds
        except ValueError:
            return


class OptionFrame(ttk.LabelFrame):
    # ? Make the class smaller?
    def __init__(self, app):
        self.app = app
        super().__init__(master=app)
        self.radio_var = tk.StringVar(value='sleep')

        self.radio_frame = ttk.LabelFrame(self, text='Options')
        self.radio_frame.pack(padx=Config.SMALL, pady=Config.SMALL)

        for option in ('sleep', 'hibernate', 'shutdown'):
            self.radio_option = ttk.Radiobutton(
                master=self.radio_frame,
                text=option.title(),
                variable=self.radio_var,
                value=option
            )
            self.radio_option.pack(anchor='w')

        self.start_button = ttk.Button(
            self, text='Start', command=self.start_button_command)
        self.start_button.pack(pady=Config.SMALL)

        self.stop_button = ttk.Button(
            self, text='Stop', command=self.stop_button_command)

    def validate_timer(self):
        total_seconds = self.app.timer_input.get_total_seconds()
        if total_seconds is None:
            self.app.log_message(
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

        self.app.replace_widget(self.app.timer_input,
                                self.app.countdown_timer,
                                before=self.app.option_frame
                                )
        self.app.replace_widget(self.start_button, self.stop_button)

        option = self.radio_var.get()
        App.change_children_state(self.radio_frame, tk.DISABLED)

        if total_seconds > 0:
            self.app.countdown_timer.start(total_seconds)
            self.app.log_message(
                f"The system will {option} when the timer reaches zero.")
        else:
            OptionHandler.execute(self, option=option)
            # ? Should the window close on execute?
            # app.destroy()

    def stop_button_command(self) -> None:
        self.app.countdown_timer.stop()
        self.app.replace_widget(self.stop_button, self.start_button)
        self.app.replace_widget(self.app.countdown_timer,
                                self.app.timer_input,
                                before=self.app.option_frame
                                )
        if hasattr(self.app, 'log_label'):
            self.app.log_label.config(text='')
        App.change_children_state(self.radio_frame, tk.NORMAL)


class OptionHandler:
    def __init__(self, app):
        self.app = app

    def execute(self, option):
        self.app.log_message(f"Executing {option}")
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
            raise Exception(f"Error executing {option}: {e}")


class CountdownTimer(ttk.LabelFrame):
    def __init__(self, app):
        self.app = app
        super().__init__(master=app)
        self.is_running = False
        self.remaining_seconds = 0

        self.time_label = tk.Label(self, text="00:00:00", font=("Arial", 17))
        self.time_label.pack()

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
        option = self.app.option_frame.radio_var.get()
        OptionHandler.execute(self, option=option)
        self.app.log_message(f"Executed option: {option}")
        self.app.replace_widget(self.app.countdown_timer,
                                self.app.timer_input,
                                before=self.app.option_frame
                                )
        self.app.replace_widget(self.app.option_frame.stop_button,
                                self.app.option_frame.start_button
                                )
        App.change_children_state(self.app.option_frame.radio_frame, tk.NORMAL)


def main():
    app = App()
    if Config.DEBUGGING:
        system_utils.debugging_message()
    elif system_utils.is_admin():
        system_utils.no_admin_disclaimer()

    app.focus_force()
    app.mainloop()


if __name__ == "__main__":
    main()
