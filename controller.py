from widget_fact import *
from web_closer import *
from plyer import notification
import subprocess
import webbrowser
import json
import os
import time

from countdown import CountdownWindow
from web_closer import WebCloser

class ApplicationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.last_selected_user = None
        self.start_time = None
        self.break_times = []
        self.end_time = None
        self.stopped = False
        self.processes = []
        self.web_closer = WebCloser()
        self.countdown_window = None

    def on_button_click(self):
        self.stopped = False
        try:
            self.web_closer.stop()
        except Exception as e:
            print(f"No Monitoring yet")
        if self.view.start_button:
            self.view.start_button.config(state="disabled")
    
        try:
            hour = int(self.view.time_entry.get())
            selected_option = self.view.combo_box.get()
            num_breaks = int(self.view.numbreak_Spinbox.get())
            time_unit = self.model.time_unit_var.get()
            states = self.model.get_checkbutton_states()

            self.last_selected_user = selected_option

            if time_unit == "hours":
                total_time = hour * 3600
            else:  # minutes
                total_time = hour * 60

            self.start_time = time.time()
            self.end_time = self.start_time + total_time

            if num_breaks > 0:
                break_interval = total_time / (num_breaks + 1)
                self.break_times = [self.start_time + (i + 1) * break_interval for i in range(num_breaks)]
            else:
                self.break_times = []

            self.start_applications()

            self.view.update_countdown(0)

            data = {
                "hours": hour,
                "breaks": num_breaks,
                "time_unit": time_unit,
                "options": states
            }

            self.save_to_json(selected_option, data)

            if self.last_selected_user:
                self.view.combo_box.set(self.last_selected_user)
                self.view.update_ui_from_user(self.last_selected_user)

            self.check_time()

        except Exception as e:
            print(f"Error during start: {e}")

    def close_applications(self):
        states = self.model.get_checkbutton_states()
        browser_exes = ["chrome.exe", "firefox.exe", "msedge.exe", "brave.exe", "opera.exe", "iexplore.exe"]


        if states.get("terminal"):
            os.system('taskkill /F /IM cmd.exe')


        for exe in browser_exes:
            os.system(f'taskkill /F /IM {exe}')
        
        if states.get("vscode"):
            os.system('taskkill /F /IM Code.exe')

    def on_stop_click(self):
        self.stopped = True
        self.end_time = time.time()
        self.view.update_countdown(0)
        self.terminate_processes()
        self.close_applications()
        try:
            self.web_closer.stop()
        except Exception as e:
            print(f"No Monitoring yet")

        if self.view.start_button:
            self.view.start_button.config(state="normal")


    def start_applications(self):
        states = self.model.get_checkbutton_states()
        vscode_path = r"C:\Users\user\AppData\Local\Programs\Microsoft VS Code\Code.exe"

        if states.get("vscode") and os.path.exists(vscode_path):
            try:
                process = subprocess.Popen([vscode_path])
                self.processes.append(process)
            except Exception as e:
                print(f"Error occurred while trying to open Visual Studio Code: {e}")

        if states.get("terminal"):
            try:
                # Open cmd.exe and change directory
                command = 'start cmd /k "cd C:\\Users\\user"'
                process = subprocess.Popen(command, shell=True)
                self.processes.append(process)
            except Exception as e:
                print(f"Error occurred while trying to open Terminal: {e}")

        for app in ["youtube", "google", "figma", "github"]:
            if states.get(app):
                url = {
                    "youtube": "https://youtube.com",
                    "google": "https://Google.com",
                    "figma": "https://Figma.com",
                    "github": "https://Github.com"
                }.get(app)
                webbrowser.open(url)

    def check_time(self):
        if self.stopped:
            return

        current_time = time.time()
        remaining_time = self.end_time - current_time

        if remaining_time <= 0:
            remaining_time = 0
            self.notify_user("Session Complete", f"Hey {self.last_selected_user}, you've reached your session time limit.")
            if self.view.start_button:
                self.view.start_button.config(state="normal")

            print("Session complete. Starting countdown timer for ending the session.")
            self.countdown_window = CountdownWindow(self.view.root, 90, self.end_timer)
            return

        if self.view:
            self.view.update_countdown(int(remaining_time))

        if self.break_times and current_time >= self.break_times[0]:
            self.notify_user("Break Time!", f"Hey {self.last_selected_user}, it's time to take a break.")
            self.break_times.pop(0)

        self.view.root.after(1000, self.check_time)

    def terminate_processes(self):
        for process in self.processes:
            process.terminate()

    def notify_user(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_icon='icon.ico',
            timeout=10
        )

    def save_to_json(self, selected_option, data):
        config_path = 'config.json'
        if not os.path.exists(config_path):
            with open(config_path, 'w') as json_file:
                json.dump({}, json_file, indent=4)

        with open(config_path, 'r') as json_file:
            all_data = json.load(json_file)

        all_data[selected_option] = data

        with open(config_path, 'w') as json_file:
            json.dump(all_data, json_file, indent=4)

    def close_browser_if_open(self):
        self.web_closer.monitor()

    def end_timer(self):
        print("Ending session and closing applications.")
        self.close_applications()
        self.monitoring_stater()
        
        print("Monitoring started for closing browsers.")


    def monitoring_stopper(self):
        self.web_closer.stop()
        print("Monitoring Stopped")

    def monitoring_stater(self):
        self.web_closer.start()

    def on_close(self):
        try:
            self.monitoring_stopper()
        except Exception:
            pass
        
        self.view.root.destroy()
        os.system("cls")




