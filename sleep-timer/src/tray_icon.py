import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image


class TrayIcon:
    def __init__(self, root, icon_path="your_icon.ico"):
        self.root = root
        self.icon_path = icon_path
        self.icon = None

    def show_window(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)

    def quit_app(self, icon, item):
        icon.stop()
        self.root.destroy()

    def run_tray(self):
        image = Image.open(self.icon_path)
        menu = Menu(
            MenuItem("Show", self.show_window, default=True),
            MenuItem("Quit", self.quit_app)
        )
        self.icon = Icon("tk_app", image, "Sleeper", menu)
        self.icon.run()

    def start(self):
        t = threading.Thread(target=self.run_tray, daemon=True)
        t.start()
