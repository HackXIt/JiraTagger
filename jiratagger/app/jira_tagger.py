import webbrowser
import tkinter as tk
from jiratagger.components.menu import MenuComponent
from jiratagger.components.issue_window import IssueWindowComponent
from jiratagger.utils.state_manager import StateManager

class JiraTagger:
    def __init__(self, path=None, issue_keys=None, jira_url=None, resume_file=None):
        self.jira_url = jira_url.rstrip('/') if jira_url else None
        self.state_manager = StateManager(path, issue_keys, resume_file)
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
    
    def open_issue_in_browser(self, issue_key):
        issue_url = f"{self.state_manager.jira_url}/browse/{issue_key}"
        webbrowser.open(issue_url)
    
    def start(self):
        if not self.state_manager.issue_keys:
            print("No issues left to process.")
            self.root.quit()
            return
        self.menu = MenuComponent(self.root, self)
        self.menu.show()
        self.process_next_issue()
        self.root.mainloop()
    
    def process_next_issue(self):
        self.menu.update_labels()
        issue_key = self.state_manager.get_next_issue()
        if not issue_key:
            self.state_manager.export_results()
            self.root.quit()
            return
        self.open_issue_in_browser(issue_key)

        # Create the issue window and display it
        self.issue_window = IssueWindowComponent(self.root, self, issue_key)
        self.issue_window.show()
        self.root.update_idletasks()

        # Set initial position if it hasn't been set yet
        if not self.initial_position_set:
            # Get the initial position of the issue window
            self.window_x_pos = self.issue_window.winfo_rootx()
            self.window_y_pos = self.issue_window.winfo_rooty()
            self.initial_position_set = True

        # Set the position of the issue window
        self.issue_window.geometry(f"+{self.window_x_pos}+{self.window_y_pos}")

        # Calculate the main window position directly below the issue window
        main_window_x = self.window_x_pos
        main_window_y = self.window_y_pos + self.issue_window.winfo_height() + 10  # 10px gap below issue window

        # Update the main window geometry to place it below the issue window
        self.root.geometry(f"+{main_window_x}+{main_window_y}")
        self.root.deiconify()  # Show the main window if it was hidden
