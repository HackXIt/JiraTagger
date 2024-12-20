import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser as colorchooser
from jiratagger.utils.markdown_utils import MarkdownUtils

class ColorPickerComponent(tk.Toplevel):
    # Pre-set color options (colors from Jira comment field presets)
    preset_colors = {
        "#172B4D": "black",
        "#4C9AFF": "light-blue",
        "#FF8B00": "dark-orange",
        "#505F79": "dark-grey",
        "#00875A": "green",
        "#FFAB00": "light-orange",
        "#C1C7D0": "light-grey",
        "#57D9A3": "pale-green",
        "#403294": "purple",
        "#0747A6": "blue",
        "#DE350B": "red",
        "#FFBDAD": "peach"
    }

    def __init__(self, master: tk.Widget, comment_input: tk.Text):
        super().__init__(master)
        self.comment_input = comment_input
        self.title("Color Picker")
        self.wm_attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Place the color picker popup relative to the master (IssueWindowComponent)
        self.geometry(f"+{master.winfo_rootx() + 50}+{master.winfo_rooty() + 100}")

        # Add preset color buttons
        for hex_code, color_name in self.preset_colors.items():
            button = ttk.Button(self, text=color_name, command=lambda hc=hex_code: self.insert_color(hc))
            button.pack(fill='x', padx=10, pady=5)
        
        # Add color wheel button to open a color chooser dialog
        color_wheel_button = ttk.Button(self, text="Open Color Wheel", command=self.open_color_picker)
        color_wheel_button.pack(fill='x', padx=10, pady=5)

    # Function to insert the selected color
    def insert_color(self, hex_code):
        MarkdownUtils.insert_markdown(f'{{color:{hex_code}}}', '{color}', self.comment_input)
        self.destroy()

    def open_color_picker(self):
        color_code = colorchooser.askcolor()[1]
        if color_code:
            MarkdownUtils.insert_markdown(f'{{color:{color_code}}}', '{color}', self.comment_input)
            self.destroy()
