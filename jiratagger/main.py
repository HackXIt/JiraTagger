import sys
import webbrowser
import argparse
import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from ttkwidgets.autocomplete import AutocompleteEntryListbox
import win32gui
from screeninfo import get_monitors
import tkinter.colorchooser as colorchooser
import json

class JiraTagger:
    def __init__(self, path=None, issue_keys=None, jira_url=None, resume_file=None):
        self.jira_url = jira_url.rstrip('/') if jira_url else None
        self.results = {}
        self.issues_skipped = []
        self.current_index = 0
        self.tag_hints = set() # Stores unique tags as hints

        # If resuming, load saved state
        if resume_file and os.path.exists(resume_file):
            self.load_state(resume_file)
            self.state_file = resume_file
        else:
            self.issue_keys = issue_keys
            # Statefile either in path or cwd
            self.state_file = os.path.join(path, 'jira_tagger_state.json') if path else os.path.join(os.path.abspath('.'), 'jira_tagger_state.json')

        # Initialize the main Tkinter application
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

    def open_issue_in_browser(self, issue_key):
        issue_url = f"{self.jira_url}/browse/{issue_key}"
        webbrowser.open(issue_url)

    def start(self):
        if not self.issue_keys or len(self.issue_keys) == 0:
            print("No issues left to process.")
            self.root.quit()
            return

        self.create_menu()
        self.process_next_issue()
        self.root.mainloop()

    def create_menu(self):
        self.root.deiconify()  # Show the root window for the main UI
        self.root.title("JiraTagger")
        self.root.wm_attributes("-topmost", True)  # Keep window on top
        # Create a frame for the main menu buttons
        menu_frame = ttk.Frame(self.root, padding="10")
        menu_frame.pack(fill='both', expand=True)
        # Save Progress button
        save_button = ttk.Button(menu_frame, text="Save Progress", command=self.save_state)
        save_button.pack(pady=10)
        # Export Results button
        export_button = ttk.Button(menu_frame, text="Export Results", command=self.export_results)
        export_button.pack(pady=10)
        # Exit button
        exit_button = ttk.Button(menu_frame, text="Exit", command=self.root.quit)
        exit_button.pack(pady=10)

    def process_next_issue(self):
        if self.current_index >= len(self.issue_keys):
            print("All issues processed.")
            self.export_results()
            self.root.quit()
            return

        issue_key = self.issue_keys[self.current_index]
        self.open_issue_in_browser(issue_key)

        # Create the input window
        self.window = tk.Toplevel(self.root)
        self.window.title(f"Issue: {issue_key}")
        self.window.wm_attributes("-topmost", True)  # Keep window on top
        self.window.protocol("WM_DELETE_WINDOW", self.on_skip)

        # Set window width and height
        window_width = 400
        window_height = 800

        # Determine window position only on the first run
        if not hasattr(self, 'window_x_position') or not hasattr(self, 'window_y_position'):
            # Determine the screen where the browser is located
            browser_screen = self.get_browser_screen()

            if browser_screen:
                self.window_x_position = browser_screen.x + browser_screen.width - window_width - 10
                self.window_y_position = browser_screen.y + 150
            else:
                self.window_x_position = 100
                self.window_y_position = 100

        # Apply the absolute position explicitly each time
        self.window.geometry(f"{window_width}x{window_height}+{self.window_x_position}+{self.window_y_position}")

        # Update position attributes based on absolute position after setting geometry (only on the first window)
        if not hasattr(self, 'window_x_position') or not hasattr(self, 'window_y_position'):
            self.window.update_idletasks()  # Ensure geometry is applied
            self.window_x_position = self.window.winfo_rootx()
            self.window_y_position = self.window.winfo_rooty()

        # Tags input
        tags_label = ttk.Label(self.window, text="Tags:")
        tags_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.tags_input = AutocompleteEntryListbox(master=self.window, allow_other_values=True, completevalues=list(self.tag_hints))
        self.tags_input.pack(fill='x', padx=10)
        self.tags_input.entry.bind('<Return>', self.on_add_tag)
        self.tags_input.entry.bind('<KeyRelease>', self.on_tag_key_release)

        self.tags_list = tk.Listbox(self.window)
        self.tags_list.pack(fill='both', padx=10, pady=5)
        self.tags_list.bind('<Delete>', self.on_delete_tag)

        # Comment input
        comment_label = ttk.Label(self.window, text="Comment:")
        comment_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.comment_input = tk.Text(self.window, height=10)
        self.comment_input.pack(fill='both', padx=10, pady=5)

        # Shortcut help text
        help_text = (
            "Shortcuts:\n"
            "Ctrl+B: Bold\n"
            "Ctrl+I: Italic\n"
            "Ctrl+U: Underline\n"
            "Ctrl+Shift+C: Insert color\n"
            "Ctrl+L: Insert link"
        )
        help_label = ttk.Label(self.window, text=help_text, justify='left', foreground='gray')
        help_label.pack(anchor='w', padx=10, pady=(5, 10))

        # Buttons
        buttons_frame = ttk.Frame(self.window)
        buttons_frame.pack(pady=10)

        submit_button = ttk.Button(buttons_frame, text="Submit", command=self.on_submit)
        skip_button = ttk.Button(buttons_frame, text="Skip", command=self.on_skip)

        submit_button.pack(side='left', padx=5)
        skip_button.pack(side='left', padx=5)

        # Keyboard shortcuts
        self.comment_input.bind('<Control-b>', self.on_bold_shortcut)
        self.comment_input.bind('<Control-i>', self.on_italic_shortcut)
        self.comment_input.bind('<Control-u>', self.on_underline_shortcut)
        self.comment_input.bind('<Control-Shift-c>', self.on_color_shortcut)
        self.comment_input.bind('<Control-l>', self.on_link_shortcut)

        # Focus on tags input
        self.tags_input.focus_set()

    def on_add_tag(self, event=None):
        tag = self.tags_input.get().strip().strip(',')
        if tag and tag not in self.tags_list.get(0, tk.END):
            self.tags_list.insert(tk.END, tag)
            self.tag_hints.add(tag)
    
    def on_delete_tag(self, event=None):
        """Deletes the selected tag from the tags list and tag hints."""
        selected_index = self.tags_list.curselection()
        if selected_index:
            tag = self.tags_list.get(selected_index)
            self.tags_list.delete(selected_index)

    def on_tag_key_release(self, event):
        """Updates the auto-complete suggestion dynamically as the user types."""
        typed_text = self.tags_input.get().strip()
        if ',' in typed_text: # Add tag when user types a comma
            self.on_add_tag()

    def on_submit(self):
        tags = self.tags_list.get(0, tk.END)
        comment = self.comment_input.get("1.0", tk.END).strip()
        issue_key = self.issue_keys[self.current_index]
        self.results[issue_key] = {
            "tags": list(tags),
            "comment": comment
        }
        self.current_index += 1
        self.window.destroy()
        self.save_state()  # Always save the state after submitting
        self.process_next_issue()

    def on_skip(self, event=None):
        issue_key = self.issue_keys[self.current_index]
        self.issues_skipped.append(issue_key)
        self.current_index += 1
        self.window.destroy()
        self.save_state()  # Always save the state after skipping
        self.process_next_issue()

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
        self.open_color_picker()
        return 'break'

    def on_link_shortcut(self, event):
        self.open_link_popup()
        return 'break'

    def open_color_picker(self):
        # Create a popup window for color selection
        color_popup = tk.Toplevel(self.window)
        color_popup.title("Select Color")

        # Pre-set color options
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

        # Function to insert the selected color
        def insert_color(hex_code):
            self.insert_markdown(f'{{color:{hex_code}}}', '{color}')
            color_popup.destroy()

        # Add preset color buttons
        for hex_code, color_name in preset_colors.items():
            button = ttk.Button(color_popup, text=color_name, command=lambda hc=hex_code: insert_color(hc))
            button.pack(fill='x', padx=10, pady=5)

        # Add a color wheel chooser button
        def open_color_wheel():
            color_code = colorchooser.askcolor()[1]  # Get color hex value
            if color_code:
                insert_color(color_code)

        color_wheel_button = ttk.Button(color_popup, text="Open Color Wheel", command=open_color_wheel)
        color_wheel_button.pack(fill='x', padx=10, pady=5)

    def open_link_popup(self):
        # Create a popup window to input the URL
        link_popup = tk.Toplevel(self.window)
        link_popup.title("Enter URL")

        # Label and text entry for the URL
        label = ttk.Label(link_popup, text="Enter URL:")
        label.pack(pady=5)

        url_var = tk.StringVar()
        url_entry = ttk.Entry(link_popup, textvariable=url_var)
        url_entry.pack(fill='x', padx=10, pady=5)

        # Function to insert the link
        def insert_link():
            url = url_var.get().strip()
            if url:
                self.insert_markdown('[', f'|{url}]')
                link_popup.destroy()

        # Add a button to submit the URL
        submit_button = ttk.Button(link_popup, text="Insert Link", command=insert_link)
        submit_button.pack(pady=10)

        # Focus on the URL entry box
        url_entry.focus_set()

    def insert_markdown(self, before, after):
        try:
            selection = self.comment_input.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.comment_input.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.comment_input.insert(tk.INSERT, f"{before}{selection}{after}")
        except tk.TclError:
            # No selection, insert at cursor
            self.comment_input.insert(tk.INSERT, f"{before}{after}")
            # Move cursor between the markdown symbols
            index = self.comment_input.index(tk.INSERT)
            new_index = f"{index}-{len(after)}c"
            self.comment_input.mark_set(tk.INSERT, new_index)
        self.comment_input.focus_set()

    def get_browser_screen(self):
        """Find the screen where the browser is located."""
        def callback(hwnd, extra):
            class_name = win32gui.GetClassName(hwnd)
            if class_name in ["Chrome_WidgetWin_1", "MozillaWindowClass"]:
                rect = win32gui.GetWindowRect(hwnd)
                extra.append((hwnd, rect))

        browser_windows = []
        win32gui.EnumWindows(callback, browser_windows)

        if not browser_windows:
            print("Browser window not found. Defaulting to primary screen.")
            return None

        # Use the first matched browser window
        _, (left, top, right, bottom) = browser_windows[0]
        browser_x, browser_y = left, top

        # Determine which screen contains the browser window
        for monitor in get_monitors():
            if (monitor.x <= browser_x < monitor.x + monitor.width and
                    monitor.y <= browser_y < monitor.y + monitor.height):
                return monitor
        return None  # Fallback if no matching screen is found

    def save_state(self):
        """Saves the current state (index and results) to a file."""
        save_data = {
            "jira-url": self.jira_url,
            "issues-left": self.issue_keys[self.current_index:],
            "issues-skipped": self.issues_skipped,
            "issues-done": self.results,
            "tag-hints": list(self.tag_hints)
        }
        with open(self.state_file, 'w') as file:
            json.dump(save_data, file, indent=4)
        print("Progress saved.")

    def load_state(self, resume_file):
        """Loads the saved state from a file."""
        with open(resume_file, 'r') as file:
            saved_data = json.load(file)
            self.jira_url = saved_data.get("jira-url", None)
            if not self.jira_url:
                # Open the file dialog to select the Jira URL
                self.jira_url = filedialog.askstring("Jira URL", "Enter the base URL of the Jira instance:")
            self.issue_keys = saved_data.get("issues-left", [])
            self.issues_skipped = saved_data.get("issues-skipped", [])
            self.results = saved_data.get("issues-done", {})
            self.tag_hints.update(saved_data.get("tag-hints", []))
            self.current_index = 0 if len(self.issue_keys) == 0 else 0

    def export_results(self):
        """Exports the results to a file chosen by the user."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.results, file, indent=4)
            print(f"Results exported to {file_path}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='JiraTagger - Label Jira issues with tags and comments.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('issue_keys_file', nargs='?', help='Path to the file containing Jira issue keys.')
    group.add_argument('--resume', help='Resume from a saved state file.')
    parser.add_argument('jira_url', nargs='?', help='Base URL of the Jira instance.')
    args = parser.parse_args()

    # Ensure jira_url is provided when not resuming
    if not args.resume and not args.jira_url:
        parser.error("jira_url is required when issue_keys_file is provided.")
    
    return args

def read_issue_keys(file_path):
    try:
        with open(os.path.abspath(file_path), 'r') as file:
            issue_keys = [line.strip() for line in file if line.strip()]
        path = os.path.dirname(file_path)
        return issue_keys, path
    except Exception as e:
        print(f"Error reading issue keys file: {e}")
        sys.exit(1)

def main():
    args = parse_arguments()

    if args.resume:
        app = JiraTagger(resume_file=args.resume)
    else:
        issue_keys, path = read_issue_keys(args.issue_keys_file)
        jira_url = args.jira_url
        app = JiraTagger(path=path, issue_keys=issue_keys, jira_url=jira_url)
    
    app.start()

if __name__ == '__main__':
    main()
