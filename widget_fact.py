import tkinter as tk
from tkinter import ttk


BACKGROUND_COLOR = "#0f0f0f"
LABEL_FONT_COLOR = "white"
LABEL_FONT = ("Arial", 14)
BUTTON_FONT = ("Arial", 12, )
BUTTON_BG_COLOR = "lightgrey"
BUTTON_FONT_COLOR = "black"
BORDER_WIDTH = 3
RELIEF = "sunken"

class WidgetFactory:
    @staticmethod
    def create_spinbox(parent, from_, to, width, relief, repeatdelay, repeatinterval, font, bg, fg, justify, wrap, validatecommand, validate, state="normal"):
        spinbox = tk.Spinbox(parent, from_=from_, to=to, width=width, relief=relief,
                             repeatdelay=repeatdelay, repeatinterval=repeatinterval,
                             font=font, bg=bg, fg=fg, justify=justify, cursor="hand2", wrap=wrap,
                             validate=validate, validatecommand=validatecommand)
        spinbox.config(state=state, bd=BORDER_WIDTH, relief=RELIEF)
        return spinbox

    @staticmethod
    def create_checkbutton(parent, text, variable):
        checkbutton = tk.Checkbutton(parent, text=text, variable=variable, bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR,
                                     selectcolor=BUTTON_BG_COLOR, highlightbackground="black", highlightcolor="black",
                                     cursor="hand2", borderwidth=BORDER_WIDTH, relief=RELIEF)
        return checkbutton

    @staticmethod
    def create_radiobutton(parent, text, variable, value, command=None):
        radiobutton = tk.Radiobutton(parent, text=text, variable=variable, value=value, bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR,
                                     command=command, cursor="hand2", borderwidth=BORDER_WIDTH, relief=RELIEF, width=9)
        return radiobutton

    @staticmethod
    def create_button(parent, text, command):
        button = tk.Button(parent, text=text, command=command, cursor="hand2", font=BUTTON_FONT, bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR,
                           borderwidth=BORDER_WIDTH, relief=RELIEF, width=9)
        return button

    @staticmethod
    def create_combobox(parent, values, **kwargs):
        combobox = ttk.Combobox(parent, values=values, **kwargs)
        combobox.set(values[0] if values else "")
        combobox.config(font=BUTTON_FONT, background=BACKGROUND_COLOR, width=10)
        return combobox

    @staticmethod
    def create_scrollbar(parent, orient, command):
        scrollbar = tk.Scrollbar(parent, orient=orient, command=command, bg=BUTTON_BG_COLOR)
        scrollbar.config(borderwidth=BORDER_WIDTH, relief=RELIEF)
        return scrollbar

