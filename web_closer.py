import threading
import os
import time
import psutil
import pyautogui

class WebCloser:
    def __init__(self, interval=3):
        self.interval = interval
        self.stop_event = threading.Event()

    def start(self):
        """Starts the web browser monitoring in a separate thread."""
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    def stop(self):
        """Stops the web browser monitoring."""
        self.stop_event.set()
        self.thread.join()

    def monitor(self):
        """Monitors running processes for web browsers and closes them if found."""
        browser_exes = ["chrome.exe", "firefox.exe", "msedge.exe", "brave.exe", "opera.exe", "cmd.exe"]

        while not self.stop_event.is_set():
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    if process.info['name'].lower() in browser_exes:
                        print(f"Closing {process.info['name']}")
                        os.system(f'taskkill /F /PID {process.info["pid"]}')
                        pyautogui.hotkey('ctrl', 'w')  # Close the current browser tab
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            time.sleep(self.interval)



