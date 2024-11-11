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
        self.issues_left_label.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=5)
        self.issues_done_label.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
        self.issues_skipped_label.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=5)

        save_button = ttk.Button(self, text="Save Progress", command=self.app.state_manager.save_state)
        export_button = ttk.Button(self, text="Export Results", command=self.app.state_manager.export_results)
        exit_button = ttk.Button(self, text="Exit", command=self.app.root.quit)

        save_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        export_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        exit_button.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    
    def update_labels(self):
        self.issues_left_label.config(text=f"Issues Left: {self.app.state_manager.get_remaining_issues_count()}")
        self.issues_done_label.config(text=f"Issues Done: {self.app.state_manager.get_done_issues_count()}")
        self.issues_skipped_label.config(text=f"Issues Skipped: {self.app.state_manager.get_skipped_issues_count()}")

    def show(self):
        self.pack()