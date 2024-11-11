import tkinter as tk
from tkinter import ttk
from components.color_picker import ColorPickerComponent
from components.link_popup import LinkPopupComponent
from ttkwidgets.autocomplete import AutocompleteEntryListbox
from utils.markdown_utils import MarkdownUtils
from utils.browser_utils import BrowserUtils

class IssueWindowComponent(tk.Toplevel):
    help_text = (
        "Shortcuts:\n"
        "Ctrl+B: Bold\n"
        "Ctrl+I: Italic\n"
        "Ctrl+U: Underline\n"
        "Ctrl+Shift+C: Insert color\n"
        "Ctrl+L: Insert link"
    )
    def __init__(self, master, app, issue_key, winfo_rootx=None, winfo_rooty=None):
        super().__init__(master)
        self.app = app
        self.issue_key = issue_key
        self.title(f"Issue: {issue_key}")
        self.wm_attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_skip)
        self.window_width = 400
        self.window_height = 800
        
        self.tags_input = AutocompleteEntryListbox(master=self, completevalues=list(self.app.state_manager.tag_hints))
        self.comment_input = tk.Text(self, height=10)

        # Position the window based on browser location
        self._set_window_position()
        self._setup_ui()
        self._bind_shortcuts()

    def _set_window_position(self, winfo_rootx=None, winfo_rooty=None):
        if winfo_rootx and winfo_rooty:
            self.geometry(f"{self.window_width}x{self.window_height}+{winfo_rootx}+{winfo_rooty}")
            self.update_idletasks()
            return
        """Sets the window position near the browser if detected."""
        browser_screen = BrowserUtils.get_browser_screen()
        if browser_screen:
            x_position = browser_screen.x + browser_screen.width - self.window_width - 10
            y_position = browser_screen.y + 150
        else:
            x_position, y_position = 100, 100  # Default position

        self.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")
        self.update_idletasks()

    def _setup_ui(self):
        ttk.Label(self, text="Tags:").pack(anchor='w', padx=10, pady=(10, 0))
        self.tags_input.pack(fill='x', padx=10)
        self.tags_list = tk.Listbox(self)
        self.tags_list.pack(fill='both', padx=10, pady=5)
        
        ttk.Label(self, text="Comment:").pack(anchor='w', padx=10, pady=(10, 0))
        self.comment_input.pack(fill='both', padx=10, pady=5)

        ttk.Label(self, text=self.help_text, justify='left', foreground='gray').pack(anchor='w', padx=10, pady=(10, 0))
        
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10)
        ttk.Button(buttons_frame, text="Submit", command=self.on_submit).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Skip", command=self.on_skip).pack(side='left', padx=5)

    def _bind_shortcuts(self):
        self.tags_input.bind("<Return>", self.on_add_tag)
        self.tags_input.bind('<KeyRelease>', self.on_tag_key_release)
        self.comment_input.bind('<Control-b>', self.on_bold_shortcut)
        self.comment_input.bind('<Control-i>', self.on_italic_shortcut)
        self.comment_input.bind('<Control-u>', self.on_underline_shortcut)
        self.comment_input.bind('<Control-Shift-c>', self.on_color_shortcut)
        self.comment_input.bind('<Control-l>', self.on_link_shortcut)
        self.tags_list.bind("<Delete>", self.on_delete_tag)
    
    def on_add_tag(self, event=None):
        tag = self.tags_input.entry.get().strip().strip(',')
        if tag and tag not in self.tags_list.get(0, tk.END):
            self.tags_list.insert(tk.END, tag)
    
    def on_delete_tag(self, event=None):
        """Deletes the selected tag from the tags list and tag hints."""
        selected_index = self.tags_list.curselection()
        if selected_index:
            tag = self.tags_list.get(selected_index)
            self.tags_list.delete(selected_index)

    def on_tag_key_release(self, event):
        """Updates the auto-complete suggestion dynamically as the user types."""
        typed_text = self.tags_input.entry.get().strip()
        if ',' in typed_text: # Add tag when user types a comma
            self.on_add_tag()

    def on_submit(self):
        tags = self.tags_list.get(0, tk.END)
        comment = self.comment_input.get("1.0", tk.END).strip()
        self.app.state_manager.add_result(self.issue_key, tags, comment)
        self.destroy()
        self.app.process_next_issue()

    def on_skip(self):
        self.app.state_manager.skip_issue(self.issue_key)
        self.destroy()
        self.app.process_next_issue()

    def on_bold_shortcut(self, event):
        self.insert_markdown('**', '**')
        return 'break'  # Prevent default behavior

    def on_italic_shortcut(self, event):
        self.insert_markdown('_', '_')
        return 'break'  # Prevent default behavior
    
    def on_underline_shortcut(self, event):
        self.insert_markdown('+', '+')
        return 'break'  # Prevent default behavior
    
    def on_color_shortcut(self, event):
        ColorPickerComponent(self, self.comment_input)
        return 'break'

    def on_link_shortcut(self, event):
        LinkPopupComponent(self, self.comment_input)
        return 'break'

    def show(self):
        self.deiconify()
