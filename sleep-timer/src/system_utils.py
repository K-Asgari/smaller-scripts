import ctypes
from tkinter import messagebox
    
def is_admin() -> bool:
    # Check if the current process has administrative privileges
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        messagebox.showerror(
            title="Exception",
            message=f"Exception error: {e}"
        )
        print(f"is_admin() Exception error: {e}")
        return False
    

def no_admin_disclaimer() -> None:
    messagebox.showinfo(
        title="Info",
        message="Admin privileges not detected. Some features may not work as expected."
    )
    
def debugging_message() -> None:
    messagebox.showinfo(
        title="Info",
        message="Debugging enabled. Execution features disabled. Faster countdown timer enabled."
    )

def hide_terminal() -> None:
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 0)
