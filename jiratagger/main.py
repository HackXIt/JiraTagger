# jira_tagger/main.py

import sys
import webbrowser
import argparse
import os
import tkinter as tk
from tkinter import messagebox, ttk
import json

class JiraTagger:
    def __init__(self, issue_keys, jira_url):
        self.issue_keys = issue_keys
        self.jira_url = jira_url.rstrip('/')  # Remove trailing slash if any
        self.current_index = 0
        self.results = {}

        # Initialize the main Tkinter application
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

    def open_issue_in_browser(self, issue_key):
        issue_url = f"{self.jira_url}/browse/{issue_key}"
        webbrowser.open(issue_url)

    def start(self):
        self.process_next_issue()
        self.root.mainloop()

    def process_next_issue(self):
        if self.current_index >= len(self.issue_keys):
            print("All issues processed.")
            print("Results:")
            print(json.dumps(self.results, indent=4))
            # Optionally, save results to a file
            with open('results.json', 'w') as outfile:
                json.dump(self.results, outfile, indent=4)
            self.root.quit()
            return

        issue_key = self.issue_keys[self.current_index]
        self.open_issue_in_browser(issue_key)

        # Create the input window
        self.window = tk.Toplevel(self.root)
        self.window.title(f"Issue: {issue_key}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_skip)

        # Tags input
        tags_label = ttk.Label(self.window, text="Tags:")
        tags_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.tags_var = tk.StringVar()
        self.tags_input = ttk.Entry(self.window, textvariable=self.tags_var)
        self.tags_input.pack(fill='x', padx=10)
        self.tags_input.bind('<Return>', self.on_add_tag)
        self.tags_input.bind('<KeyRelease>', self.on_tag_key_release)

        self.tags_list = tk.Listbox(self.window)
        self.tags_list.pack(fill='both', padx=10, pady=5)

        # Comment input
        comment_label = ttk.Label(self.window, text="Comment:")
        comment_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.comment_input = tk.Text(self.window, height=10)
        self.comment_input.pack(fill='both', padx=10, pady=5)

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

        # Focus on tags input
        self.tags_input.focus_set()

    def on_add_tag(self, event=None):
        tag = self.tags_var.get().strip().strip(',')
        if tag and tag not in self.tags_list.get(0, tk.END):
            self.tags_list.insert(tk.END, tag)
            self.tags_var.set('')

    def on_tag_key_release(self, event):
        if ',' in self.tags_var.get():
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
        self.process_next_issue()

    def on_skip(self, event=None):
        self.current_index += 1
        self.window.destroy()
        self.process_next_issue()

    def on_bold_shortcut(self, event):
        self.insert_markdown('**', '**')
        return 'break'  # Prevent default behavior

    def on_italic_shortcut(self, event):
        self.insert_markdown('_', '_')
        return 'break'  # Prevent default behavior

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

def parse_arguments():
    parser = argparse.ArgumentParser(description='JiraTagger - Label Jira issues with tags and comments.')
    parser.add_argument('issue_keys_file', help='Path to the file containing Jira issue keys.')
    parser.add_argument('jira_url', help='Base URL of the Jira instance.')
    args = parser.parse_args()
    return args

def read_issue_keys(file_path):
    try:
        with open(os.path.abspath(file_path), 'r') as file:
            issue_keys = [line.strip() for line in file if line.strip()]
        return issue_keys
    except Exception as e:
        print(f"Error reading issue keys file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    args = parse_arguments()
    issue_keys = read_issue_keys(args.issue_keys_file)
    jira_url = args.jira_url
    app = JiraTagger(issue_keys, jira_url)
    app.start()
