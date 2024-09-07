import tkinter as tk
from plyer import notification
from PIL import Image, ImageTk
import json
import os
import re


from widget_fact import *



class ApplicationView:
    def __init__(self, root, factory, model, controller):
        self.root = root
        self.factory = factory
        self.model = model
        self.controller = controller
 

        # Create validation command
        self.validate_command = root.register(self.validate_input)

        self.setup_ui()
        self.load_existing_data()

    def setup_ui(self):
        self.root.title("Dev Buddy")
        self.root.geometry("1000x600")
        self.root.config(bg=BACKGROUND_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self.controller.on_close)

        

        self.root.resizable(False, False)
        
        try:
            icon_image = ImageTk.PhotoImage(file="icon.png")
            self.root.iconphoto(False, icon_image)
        except FileNotFoundError:
            print("Icon image not found.")

        try:
            self.bg_image = Image.open("dev_bud.png")
            self.bg_label = tk.Label(self.root)
            self.bg_label.place(relwidth=1, relheight=1)
            self.root.bind("<Configure>", self.resize_background)
            self.resize_background()
        except FileNotFoundError:
            print("Background image not found.")

        self.combo_label = tk.Label(self.root, text="Add or Select User :", bg=BACKGROUND_COLOR, fg=LABEL_FONT_COLOR, font=LABEL_FONT)
        self.combo_label.place(relx= 0.0475, rely=0.05 ,anchor ="w")

        self.combo_box = self.factory.create_combobox(self.root, values=[""], state="open")
        self.combo_box.place(relx= 0.0775, rely=0.125 ,anchor ="w")

        self.combo_box.bind("<<ComboboxSelected>>", self.on_user_selection_change)
        self.combo_box.bind("<KeyRelease>", self.validate_combobox)  

        checkbuttons_label = tk.Label(self.root, text ="Choose the App/s \n you want to open:", bg =BACKGROUND_COLOR, fg=LABEL_FONT_COLOR, font = LABEL_FONT)
        checkbuttons_label.place(relx=0.7825, rely=0.7, anchor="e")

        time_unit_label = tk.Label(self.root, text="Choose Time Unit:", bg=BACKGROUND_COLOR, fg=LABEL_FONT_COLOR, font=LABEL_FONT)
        time_unit_label.place(relx= 0.0475, rely=0.625 ,anchor ="w")

        self.time_unit_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.time_unit_frame.place(relx= 0.225, rely=0.625 ,anchor ="w")


        self.hours_radio = self.factory.create_radiobutton(
            self.time_unit_frame,
            text="Hours", variable=self.model.time_unit_var,
            value="hours", command=self.update_spinboxes
        )
        self.hours_radio.pack(side="left")

        self.minutes_radio = self.factory.create_radiobutton(
            self.time_unit_frame,
            text="Minutes", variable=self.model.time_unit_var,
            value="minutes", command=self.update_spinboxes
        )
        self.minutes_radio.pack(side="left")

        time_label = tk.Label(self.root, text="Enter Working Time:", bg=BACKGROUND_COLOR, fg=LABEL_FONT_COLOR, font=LABEL_FONT)
        time_label.place(relx= 0.0475, rely=0.7 ,anchor ="w")


        self.time_entry = self.factory.create_spinbox(
            self.root,
            from_=1, to=24,
            width=6, relief=RELIEF,
            repeatdelay=500, repeatinterval=100,
            font=BUTTON_FONT,
            bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR,
            justify="center", wrap=True,
            validate="key", validatecommand=(self.validate_command, "%P", "hour")
        )
        self.time_entry.place(relx= 0.24, rely=0.7 ,anchor ="w")

        numbreak_label = tk.Label(self.root, text="Enter Number of Breaks:", bg=BACKGROUND_COLOR, fg=LABEL_FONT_COLOR, font=LABEL_FONT)
        numbreak_label.place(relx= 0.0475, rely=0.775 ,anchor ="w")

        self.numbreak_Spinbox = self.factory.create_spinbox(
            self.root,
            from_=0, to=10,
            width=6, relief=RELIEF,
            repeatdelay=500, repeatinterval=100,
            font=BUTTON_FONT,
            bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR,
            justify="center", wrap=True,
            validate="key", validatecommand=(self.validate_command, "%P", "break")
        )
        self.numbreak_Spinbox.place(relx= 0.275, rely=0.775 ,anchor ="w")

        self.create_scrollable_checkbuttons()

        self.countdown_label = tk.Label(self.root, text="Remaining Time: 00:00:00", bg=BACKGROUND_COLOR, fg="yellow", font=("Arial", 14))
        self.countdown_label.place(relx= .95, rely=0.05 ,anchor ="e")
       
        self.start_button = self.factory.create_button(self.root, "Start", self.controller.on_button_click)
        self.start_button.place(relx= 0.4525, rely=0.525,anchor ="center")

        self.stop_button = self.factory.create_button(self.root, "Stop", self.controller.on_stop_click)
        self.stop_button.place(relx= 0.575, rely=0.525,anchor ="center")

        self.time_entry.bind("<KeyRelease>", lambda e: self.update_start_button_state())
 

        """self.add_or_remove_label = tk.Label(self.root, text="To Customize the, App List" , bg=BACKGROUND_COLOR, fg=LABEL_FONT_COLOR, font=LABEL_FONT )
        self.add_or_remove_label.place(relx= 0.8375, rely=0.8575,anchor ="e")

        self.add_or_remove_button = self.factory.create_button(self.root, "Click This!", self.controller.on_add_or_remove_click)
        self.add_or_remove_button.place(relx= 0.95, rely=0.8575,anchor ="e")"""

        

    def validate_input(self, value, field_type):
        if value == "":
            return True
        try:
            number = int(value)
            if field_type == "hour":
                if self.model.time_unit_var.get() == "hours":
                    if 0 <= number <= 24:
                        return True
                    else:
                        self.show_error_message("Invalid hour", "Please enter a number between 1 and 24.")
                        return False
                else:  # minutes
                    if 0 <= number <= 60:
                        return True
                    else:
                        self.show_error_message("Invalid hour", "Please enter a number between 1 and 60.")
                        return False
            elif field_type == "break":
                if self.model.time_unit_var.get() == "hours":
                    if 0 <= number <= 10:
                        return True
                    else:
                        self.show_error_message("Invalid break", "Please enter a number between 0 and 10.")
                        return False
                else:  # minutes
                    if 0 <= number <= 5:
                        return True
                    else:
                        self.show_error_message("Invalid break", "Please enter a number between 0 and 5.")
                        return False
        except ValueError:
            self.show_error_message(field_type, "Please enter numbers only.")
            return False

    def validate_combobox(self, event):
        text = self.combo_box.get()
        
        # Check for special characters
        if re.search(r'[^\w\s]', text):
            self.show_error_message("Invalid user", "Special characters are not allowed.")
            # Remove special characters and limit length
            text = re.sub(r'[^\w\s]', '', text)
            text = text[:10]
        elif len(text) > 10:
            self.show_error_message("Invalid user", "Input cannot exceed 10 characters.")
            text = text[:10]

        self.combo_box.delete(0, tk.END)
        self.combo_box.insert(0, text)
        
        # Update start button state
    
        self.update_start_button_state()



    def update_spinboxes(self):
        time_unit = self.model.time_unit_var.get()
        if time_unit == "hours":
            self.time_entry.config(from_=1, to=24)
            self.numbreak_Spinbox.config(from_=0, to=10)
        else:
            self.time_entry.config(from_=1, to=60)
            self.numbreak_Spinbox.config(from_=0, to=5)
        # Update existing values in Spinboxes based on current time unit
        self.validate_input(self.time_entry.get(), "hour")
        self.validate_input(self.numbreak_Spinbox.get(), "break")

    def create_scrollable_checkbuttons(self):
 
        container = tk.Frame(self.root, bg=BUTTON_BG_COLOR, bd=2, relief=RELIEF)
        container.place(relx=0.95, rely=0.7, anchor="e", width=150, height=110, bordermode="inside")

        canvas = tk.Canvas(container, bg=BUTTON_BG_COLOR, bd=0, highlightthickness=0, relief="ridge")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview, bg=BUTTON_BG_COLOR, activebackground='white', troughcolor=BUTTON_BG_COLOR)


        checkbutton_frame = tk.Frame(canvas, bg=BUTTON_BG_COLOR)

        self.create_checkbuttons(checkbutton_frame)

        canvas.create_window((0, 0), window=checkbutton_frame, anchor="nw")

        checkbutton_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        checkbutton_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units")))
        checkbutton_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        for checkbutton in self.checkbuttons.values():
            checkbutton.config(
                bg=BUTTON_BG_COLOR,
                fg=BUTTON_FONT_COLOR,
                selectcolor='white',
                activebackground=BUTTON_BG_COLOR,
                font=("Arial", 10),
                relief="flat"
            )





    def create_checkbuttons(self, frame):
        self.checkbuttons = {
            "vscode": self.factory.create_checkbutton(frame, "Visual Studio Code", self.model.vscode_var),
            "terminal": self.factory.create_checkbutton(frame, "Terminal", self.model.terminal_var),
            "youtube": self.factory.create_checkbutton(frame, "YouTube", self.model.youtube_var),
            "google": self.factory.create_checkbutton(frame, "Google", self.model.google_var),
            "figma": self.factory.create_checkbutton(frame, "Figma", self.model.figma_var),
            "github": self.factory.create_checkbutton(frame, "GitHub", self.model.github_var),
        }
        for cb in self.checkbuttons.values():
            cb.pack(anchor="w", padx=5, pady=5)



    def resize_background(self, event=None):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        resized_image = self.bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=bg_photo)
        self.bg_label.image = bg_photo

    def load_existing_data(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)
                users = list(data.keys())
                self.combo_box['values'] = users
                if users:
                    selected_user = users[0]
                    self.combo_box.set(selected_user)
                    self.update_ui_from_user(selected_user)
                else:
                    self.combo_box.set("")  
        else:
            self.combo_box.set("") 
        
        self.update_start_button_state()

    def on_user_selection_change(self, event):
        selected_user = self.combo_box.get()
        self.update_ui_from_user(selected_user)

    def update_ui_from_user(self, username):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)
                user_data = data.get(username, {})
                self.time_entry.delete(0, tk.END)
                self.time_entry.insert(0, user_data.get("hours", 0))
                self.numbreak_Spinbox.delete(0, tk.END)
                self.numbreak_Spinbox.insert(0, user_data.get("breaks", 0))
                self.model.time_unit_var.set(user_data.get("time_unit", "hours"))
                self.update_spinboxes()  # Reflect time unit changes
                self.model.set_checkbutton_states(user_data.get("options", {}))
        else:
            raise FileNotFoundError("File doesn't exist")

    def update_combobox_values(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)
                users = list(data.keys())
                self.combo_box['values'] = users
                if users:
                    self.combo_box.set(users[-1])
                    self.update_ui_from_user(users[-1])
        else:
            raise FileNotFoundError("File doesn't exist")


    def show_error_message(self, field_type, message):
        error_window = tk.Toplevel(self.root)
        error_window.title(field_type)
        error_window.geometry("500x150")
        error_window.config(bg=BACKGROUND_COLOR)
        
        if field_type == "hours":
            text = f"Hour Error: {message}"
        elif field_type == "break":
            text = f"Break Error: {message}"
        else:
            text = message

        tk.Label(error_window, text=text, fg="red", bg=BACKGROUND_COLOR, font=LABEL_FONT).pack(pady=10)
        tk.Button(error_window, text="OK", command=error_window.destroy, bg=BUTTON_BG_COLOR, fg=BUTTON_FONT_COLOR, font=BUTTON_FONT).pack(pady=5)

    def update_countdown(self, remaining_seconds):
        hours, remainder = divmod(remaining_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.countdown_label.config(text=f"Remaining Time: {hours:02}:{minutes:02}:{seconds:02}")

    def update_start_button_state(self):
      
        try:
            hour_value = int(self.time_entry.get())
        except ValueError:
            hour_value = 0

        if hour_value == 0 or self.combo_box.get().strip() == "":
            self.start_button.config(state="disabled")
        else:
            self.start_button.config(state="normal")
