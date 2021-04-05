from os import system
import threading
import time

# http://www.learningaboutelectronics.com/Articles/How-to-get-the-current-position-of-mouse-in-Python-using-pyautogui.php
import pyautogui

from pynput import keyboard


TARGET_POS_X = 0
TARGET_POS_Y = 0
START_STOP_KEY = keyboard.Key.f8
EXIT_KEY = keyboard.Key.f9


class CLickMouse(threading.Thread):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.running = False
        self.program_running = True
    
    def start_clicking(self):
        print("started clicking...")
        global TARGET_POS_X
        TARGET_POS_X = pyautogui.position().x
        global TARGET_POS_Y
        TARGET_POS_Y = pyautogui.position().y
        self.running = True
    
    def stop_clicking(self):
        print("stopped clicking.")
        self.running = False
    
    def exit(self):
        self.stop_clicking()
        self.program_running = False
        print("terminating...")
    
    def run(self):
        while self.program_running:
            while self.running:
                cacheX = pyautogui.position().x
                cacheY = pyautogui.position().y
                pyautogui.click(TARGET_POS_X, TARGET_POS_Y, _pause=False)
                pyautogui.moveTo(cacheX, cacheY, _pause=False)
                pyautogui.sleep(self.delay)
            time.sleep(0.1)


click_thread = CLickMouse(2)
click_thread.start()
print("Ready.")


def on_press(key):
    if key == START_STOP_KEY:
        if click_thread.running:
            click_thread.stop_clicking()
        else:
            click_thread.start_clicking()
    elif key == EXIT_KEY:
        click_thread.exit()
        listener.stop()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()