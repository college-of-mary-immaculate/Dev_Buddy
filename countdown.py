from widget_fact import *
from web_closer import *
import tkinter as tk



class CountdownWindow:
    def __init__(self, root, countdown_seconds, callback):
        self.root = root
        self.countdown_seconds = countdown_seconds
        self.callback = callback
        self.user_stopped = False 

        self.window = tk.Toplevel(self.root)
        self.window.title("Countdown Timer")
        self.window.geometry("1200x800")
        self.window.attributes("-topmost", True) 
        self.window.config(bg=BACKGROUND_COLOR)


        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.warning_label = tk.Label(self.window, text="\nWarning!", bg=BACKGROUND_COLOR, fg="red", font=("Arial", 46))
        self.warning_label.pack()

        self.warning_label1 = tk.Label(self.window, text="Your device will close tabs and applications automatically\n when the timer runs out.\nStart saving your progress!"
                                       , bg=BACKGROUND_COLOR, fg="white", font=("Arial", 24))
        self.warning_label1.pack()

        self.warning_label = tk.Label(self.window, text='\n(Press "STOP" to Cancel the Timer!)', bg=BACKGROUND_COLOR, fg="red", font=("Arial", 20))
        self.warning_label.pack()

        self.label = tk.Label(self.window, text=self.format_time(self.countdown_seconds), 
                              fg="white", bg=BACKGROUND_COLOR, font=("Arial", 24))
        
        self.label.pack(pady=10)
       
        self.stop_button = tk.Button(self.window, text="STOP", command=self.stop_timer, 
                                     bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR, font=("Arial", 18))
        self.stop_button.pack(pady=10)

        self.update_countdown()

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def update_countdown(self):
        if self.countdown_seconds > 0:
            self.countdown_seconds -= 1
            self.label.config(text=self.format_time(self.countdown_seconds))
            self.root.after(1000, self.update_countdown)
        else:
            if not self.user_stopped:
                self.callback()
            self.window.destroy()

    def stop_timer(self):
        self.user_stopped = True
        self.countdown_seconds = 0
        self.window.destroy()

    def on_close(self):
        pass