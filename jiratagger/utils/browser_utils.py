import win32gui
from screeninfo import get_monitors

class BrowserUtils:
    @staticmethod
    def get_browser_screen():
        """Finds and returns the screen where the majority of the browser window is located."""
        
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
        _, (left, top, right, bottom) = browser_windows[0]
        buffer = 20  # Allowable buffer zone

        max_overlap_area = 0
        best_monitor = None

        # Check each monitor and calculate overlap area with the browser window
        for monitor in get_monitors():
            monitor_left = monitor.x - buffer
            monitor_top = monitor.y - buffer
            monitor_right = monitor.x + monitor.width + buffer
            monitor_bottom = monitor.y + monitor.height + buffer

            # Calculate overlap rectangle boundaries
            overlap_left = max(left, monitor_left)
            overlap_top = max(top, monitor_top)
            overlap_right = min(right, monitor_right)
            overlap_bottom = min(bottom, monitor_bottom)

            # Calculate the overlap area
            overlap_width = max(0, overlap_right - overlap_left)
            overlap_height = max(0, overlap_bottom - overlap_top)
            overlap_area = overlap_width * overlap_height

            # Determine if this monitor has the largest overlap so far
            if overlap_area > max_overlap_area:
                max_overlap_area = overlap_area
                best_monitor = monitor

        if best_monitor:
            print(f"Browser window found on monitor: {best_monitor}")
        else:
            print("Browser screen not found within buffer zone. Using default position.")

        return best_monitor
