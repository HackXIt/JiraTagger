import webbrowser
import tkinter as tk
import time
from jiratagger.components.menu import MenuComponent
from jiratagger.components.issue_window import IssueWindowComponent
from jiratagger.utils.state_manager import StateManager

class JiraTagger:
    def __init__(self, path=None, issue_keys=None, jira_url=None, resume_file=None):
        self.state_manager = StateManager(path, issue_keys, jira_url, resume_file)
        self.menu = None
        self.issue_window = None
        self.root = tk.Tk()
        self.root.title("JiraTagger")
        self.root.geometry("300x150")
        self.root.withdraw()
        
        # Position variables
        self.initial_position_set = False
        self.window_x_pos = None
        self.window_y_pos = None

        # Timing data for current session
        self.issue_start_time = None
        self.issue_durations = []  # List to store time taken for each processed issue
    
    def open_issue_in_browser(self, issue_key):
        issue_url = f"{self.state_manager.jira_url}/browse/{issue_key}"
        webbrowser.open(issue_url)
    
    def start(self):
        if self.state_manager.remaining_issues_count() == 0:
            print("No issues left to process.")
            self.root.quit()
            return
        self.menu = MenuComponent(self.root, self)
        self.menu.show()
        self.process_next_issue()
        self.root.mainloop()
    
    def process_next_issue(self):
        issue_key = self.state_manager.get_next_issue()
        self.menu.update_labels()
        if not issue_key:
            self.state_manager.export_results()
            self.root.quit()
            return
        self.open_issue_in_browser(issue_key)
        self.issue_start_time = time.time()  # Timestamp for when the issue processing

        # Create the issue window and display it
        self.issue_window = IssueWindowComponent(self.root, self, self.window_x_pos, self.window_y_pos)
        self.issue_window.show()
        self.root.update_idletasks()

        # Set initial position if it hasn't been set yet
        if not self.initial_position_set:
            # Get the initial position of the issue window
            self.window_x_pos = self.issue_window.winfo_rootx()
            self.window_y_pos = self.issue_window.winfo_rooty()
            self.initial_position_set = True
            # Calculate the main window position directly below the issue window
            main_window_x = self.window_x_pos
            main_window_y = self.window_y_pos + self.issue_window.winfo_height() + 10  # 10px gap below issue window

            # Update the main window geometry to place it below the issue window
            self.root.geometry(f"+{main_window_x}+{main_window_y}")
        self.root.deiconify()  # Show the main window if it was hidden
    
    def submit_issue(self, tags, comment):
        # Called when an issue is submitted
        if self.issue_start_time is not None:
            duration = time.time() - self.issue_start_time  # Calculate time taken for this issue
            self.issue_durations.append(duration)  # Store the duration for calculating the average
            self.issue_start_time = None  # Reset start time for the next issue
        self.state_manager.add_result(tags, comment)
        self.menu.calculate_remaining_time(self.state_manager.remaining_issues_count(), self.issue_durations)
        self.menu.update_labels()
    
    def skip_issue(self):
        self.issue_start_time = None  # Reset start time for the next issue
        self.state_manager.skip_issue()
        self.menu.update_labels()