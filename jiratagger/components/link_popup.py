import tkinter as tk
from tkinter import ttk

class LinkPopupComponent(tk.Toplevel):
    def __init__(self, master: tk.Widget, comment_input: tk.Text):
        super().__init__(master)
        self.comment_input = comment_input
        self.title("Enter URL")
        self.wm_attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.url_var = tk.StringVar()

        self.label = ttk.Label(self, text="Enter URL:")
        self.entry = ttk.Entry(self, textvariable=self.url_var)
        self.button = ttk.Button(self, text="Insert Link", command=self.insert_link)
        self.pack()
        # Focus on the URL entry box
        self.entry.focus_set()

    def insert_link(self):
        url = self.url_var.get().strip()
        if url:
            self.comment_input.insert(tk.INSERT, f"[{url}]")
        self.destroy()
    
    def pack(self):
        self.label.pack(pady=5)
        self.entry.pack(fill='x', padx=10, pady=5)
        self.button.pack(pady=10)
