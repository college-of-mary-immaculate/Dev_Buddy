import tkinter as tk


class ApplicationModel:
    def __init__(self):
        self.vscode_var = tk.BooleanVar()
        self.terminal_var = tk.BooleanVar()
        self.youtube_var = tk.BooleanVar()
        self.google_var = tk.BooleanVar()
        self.figma_var = tk.BooleanVar()
        self.github_var = tk.BooleanVar()
        self.time_unit_var = tk.StringVar(value="hours")

    def get_checkbutton_states(self):
        return {
            "vscode": self.vscode_var.get(),
            "terminal": self.terminal_var.get(),
            "youtube": self.youtube_var.get(),
            "google": self.google_var.get(),
            "figma": self.figma_var.get(),
            "github": self.github_var.get()
        }

    def set_checkbutton_states(self, states):
        self.vscode_var.set(states.get("vscode", False))
        self.terminal_var.set(states.get("terminal", False))
        self.youtube_var.set(states.get("youtube", False))
        self.google_var.set(states.get("google", False))
        self.figma_var.set(states.get("figma", False))
        self.github_var.set(states.get("github", False))
