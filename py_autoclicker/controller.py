from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import threading
import time
import json

button = Button.left

# Reads the config from the json file

with open("config.json", 'r') as json_config:
    data = json.load(json_config)

# assigns the config to variables

start_stop_key = data["start_stop"]
exit_key_value = data["exit"]
cps = data["clicks"]

# assigns the config variables to be compatible with listeners

start_stop = KeyCode(char = start_stop_key)
exit_key = KeyCode(char = exit_key_value)

# cps = int(input("Enter the CPS you want: "))
print("press",start_stop_key," to start and stop the autoclicker, and press ",exit_key_value," to exit")

# calculates the delay before every click

delay = 1/cps

# creates the thread

class create_macro(threading.Thread):
    
    def __init__(self, delay, button):

        # allows us to access methods of the base class

        super(create_macro, self).__init__()

        # assigns values to the variables used in functions in this class

        self.delay = delay
        self.button = button
        self.program_status = True
        self.click_mouse_running = False

    # function to start clicking

    def start_clicking(self):
        self.click_mouse_running = True
    
    # function to stop clicking

    def stop_clicking(self):
        self.click_mouse_running = False
    
    # function to exit the program    

    def exit(self):
        self.stop_clicking()
        self.program_status = False

    # function to run the autoclicker
    
    def run(self):
        while self.program_status:
            while self.click_mouse_running:
                mouse.click(self.button)
                time.sleep(self.delay)

# creates the controller object

mouse = Controller()

# creates and starts the thread

clicker_thread = create_macro(delay, button)
clicker_thread.start()

# listener to check for keypress
 
def on_press(key):
    if key == start_stop:
        if clicker_thread.click_mouse_running:
            clicker_thread.stop_clicking()
        else:
            clicker_thread.start_clicking()
    elif key == exit_key:
        clicker_thread.exit()
        listener.stop()


with Listener(on_press=on_press) as listener:
    listener.join()
