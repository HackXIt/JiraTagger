import win32gui
from screeninfo import get_monitors

class BrowserUtils:
    @staticmethod
    def get_browser_screen():
        """Finds and returns the screen where the browser window is located, based on common browser window classes."""
        def callback(hwnd, extra):
            class_name = win32gui.GetClassName(hwnd)
            if "MozillaWindowClass" in class_name:  # Adjust for the browser in use
                print(f"Found window: {hwnd} - {win32gui.GetWindowText(hwnd)} - {win32gui.GetClassName(hwnd)} - {win32gui.GetWindowRect(hwnd)}")
                rect = win32gui.GetWindowRect(hwnd)
                extra.append((hwnd, rect))

        browser_windows = []
        win32gui.EnumWindows(callback, browser_windows)

        if not browser_windows:
            print("Browser window not found. Defaulting to primary screen.")
            return None

        # Use the first matched browser window
        _, (left, top, _, _) = browser_windows[0]
        buffer = 20  # Allowable buffer zone

        # Determine which monitor contains the browser window, with a buffer zone
        for monitor in get_monitors():
            if ((monitor.x - buffer) <= left <= (monitor.x + monitor.width + buffer) and
                    (monitor.y - buffer) <= top <= (monitor.y + monitor.height + buffer)):
                print(f"Browser window found on monitor: {monitor}")
                return monitor  # Return the monitor that contains the browser window

        print("Browser screen not found within buffer zone. Using default position.")
        return None  # Fallback if no matching screen is found
