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

        ttk.Button(self, text="Save Progress", command=self.app.state_manager.save_state).pack(pady=10)
        ttk.Button(self, text="Export Results", command=self.app.state_manager.export_results).pack(pady=10)
        ttk.Button(self, text="Exit", command=self.app.root.quit).pack(pady=10)

    def show(self):
        self.pack()
