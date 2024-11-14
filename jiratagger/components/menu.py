from tkinter import ttk

class MenuComponent(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.pack(fill='both', expand=True, padx=10, pady=10)
        self.create_widgets()
    
    def create_widgets(self):
        self.app.root.deiconify()
        self.app.root.title("JiraTagger")
        self.app.root.wm_attributes("-topmost", True)

        # Labels and Buttons in a Grid
        self.issues_left_label = ttk.Label(self, text=f"Issues Left: -")
        self.issues_done_label = ttk.Label(self, text=f"Issues Done: -")
        self.issues_skipped_label = ttk.Label(self, text=f"Issues Skipped: -")
        self.time_estimate_label = ttk.Label(self, text=f"Time Estimate: -")
        self.current_issue_label = ttk.Label(self, text=f"Current: -")
        self.issues_left_label.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
        self.issues_done_label.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
        self.issues_skipped_label.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=5)
        self.time_estimate_label.grid(row=3, column=0, sticky="w", padx=(10, 5), pady=5)
        self.current_issue_label.grid(row=3, column=1, sticky="w", padx=(10, 5), pady=5)

        save_button = ttk.Button(self, text="Save Progress", command=self.app.state_manager.save_state)
        export_button = ttk.Button(self, text="Export Results", command=self.app.state_manager.export_results)
        exit_button = ttk.Button(self, text="Exit", command=self.app.root.quit)

        save_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        export_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        exit_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    
    def update_labels(self):
        self.issues_left_label.config(text=f"Issues Left: {self.app.state_manager.remaining_issues_count()}")
        self.issues_done_label.config(text=f"Issues Done: {self.app.state_manager.done_issues_count()}")
        self.issues_skipped_label.config(text=f"Issues Skipped: {self.app.state_manager.skipped_issues_count()}")
        self.current_issue_label.config(text=f"Current: {self.app.state_manager.current_issue}")
    
    def calculate_remaining_time(self, remaining_issues: int, issue_durations=None):
        # Calculate the remaining time based on the average duration
        if not issue_durations:
            self.time_estimate_label.config(text="Time Estimate: -")
            return

        avg_duration = sum(issue_durations) / len(issue_durations)
        estimated_time = remaining_issues * avg_duration

        # Format the time in hours, minutes, and seconds for better readability
        hours, remainder = divmod(int(estimated_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_estimate_label.config(text=f"Time Estimate: {hours}h {minutes}m {seconds}s")

    def show(self):
        self.pack()
