import tkinter as tk

class MarkdownUtils:
    @staticmethod
    def insert_markdown(before, after, comment_input: tk.Text):
        try:
            selection = comment_input.get(tk.SEL_FIRST, tk.SEL_LAST)
            comment_input.delete(tk.SEL_FIRST, tk.SEL_LAST)
            comment_input.insert(tk.INSERT, f"{before}{selection}{after}")
        except tk.TclError:
            comment_input.insert(tk.INSERT, f"{before}{after}")
            # Move cursor between the markdown symbols
            index = comment_input.index(tk.INSERT)
            new_index = f"{index}-{len(after)}c"
            comment_input.mark_set(tk.INSERT, new_index)
        comment_input.focus_set()
