import win32gui
from screeninfo import get_monitors

class BrowserUtils:
    @staticmethod
    def get_browser_screen():
        """Finds the screen where the browser window is located, based on common browser window classes."""
        def callback(hwnd, extra):
            class_name = win32gui.GetClassName(hwnd)
            if class_name in ["MozillaWindowClass"]:
                rect = win32gui.GetWindowRect(hwnd)
                extra.append((hwnd, rect))

        browser_windows = []
        win32gui.EnumWindows(callback, browser_windows)

        if not browser_windows:
            print("Browser window not found. Defaulting to primary screen.")
            return None
        print(f"Found {len(browser_windows)} browser windows: {browser_windows}")
        # Use the first matched browser window
        _, (left, top, right, bottom) = browser_windows[0]
        browser_x, browser_y = left, top

        # Determine which screen contains the browser window
        for monitor in get_monitors():
            if (monitor.x <= browser_x < monitor.x + monitor.width and
                    monitor.y <= browser_y < monitor.y + monitor.height):
                return monitor
        return None  # Fallback if no matching screen is found
