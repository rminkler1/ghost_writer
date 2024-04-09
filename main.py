import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext, filedialog, simpledialog

# version check * tkinter causes Python Interpreter crash 3.12.0 and earlier
import sys
MIN_PYTHON = (3, 12, 1)
print(sys.version_info)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s.%s or later is required.\n" % MIN_PYTHON)

# Constants
APP_NAME = "Ghost Writer"
FONT = ("Arial", 30, "bold")
RED_GRAD = ["#FFFFFF", "#FFE2E2", "#FFC6C6", "#FFAAAA", "#FF8D8D", "#FF7171", "#FF5555", "#FF3838", "#FF1C1C",
            "#FF0000", "#00ff00"]

# Time tracking
start_time = None
last_key_press = datetime.now()

# prompt for settings
time_out_seconds = simpledialog.askinteger(title="Seconds until screen wipe",
                                           prompt="How many seconds of inactivity before the screen is wiped? "
                                                  "\nRecommendation of 5-15 seconds.",
                                           initialvalue=10,
                                           minvalue=1
                                           )
minutes_to_write = simpledialog.askinteger(title="Minutes to write.",
                                           prompt="Choose the duration in minutes until your work is secure. \n"
                                                  "The editor will delete your work if you pause typing "
                                                  "\nbefore the specified period has passed.",
                                           initialvalue=5,
                                           minvalue=1
                                           )

# set defaults if dialogs are cancelled
if not time_out_seconds:
    time_out_seconds = 10
if not minutes_to_write:
    minutes_to_write = 5

# convert minutes to seconds
seconds_till_safe_from_delete = minutes_to_write * 60  # five minutes == 300 seconds


def timer_control(key):
    """
    (KeyPress) -> NoneType

    Sets start_time and last_key_press
    """
    global start_time, last_key_press

    last_key_press = datetime.now()

    if not start_time:
        start_time = last_key_press


def check_time_remaining():
    """
    Program logic. Runs every 500 ms.
    """
    global start_time, last_key_press, seconds_till_safe_from_delete

    # Until 5 min have passed, delete text if no typing has occurred recently.
    if start_time:
        seconds_since_start = (datetime.now() - start_time).total_seconds()

        # if 5 min has not passed, check delete timer
        if seconds_since_start <= seconds_till_safe_from_delete:  # proceed if less than 5 min (or set time) has passed
            seconds_since_key_press = (datetime.now() - last_key_press).total_seconds()  # time since keypress
            percent_to_wipe = seconds_since_key_press / time_out_seconds  # convert time to percentage 1 == 100%
            if percent_to_wipe >= 1:  # if percent to wipe >= 100% ... wipe text box and reset
                window_reset()
            else:
                # set color. from white to red, or green once safe.
                color_index = int(percent_to_wipe * 10)  # set index from 0-9 for white to red. index 10 == green
                if color_index > 9:
                    color_index = 9

                window.config(background=RED_GRAD[color_index])
                button_frame.config(background=RED_GRAD[color_index])
        else:
            # turn window green when safe
            window.config(background=RED_GRAD[10])
            button_frame.config(background=RED_GRAD[10])

    # check time every half second
    window.after(500, check_time_remaining)


def save_to_file():
    """
    Saves typed text to a txt file.
    Uses filedialog for naming and location.
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),
                                                                                 ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            text_content = text_box.get("1.0", "end-1c")
            file.write(text_content)


def window_reset():
    """
    Resets the window on reset button press.
    Text and counters cleared.
    """
    global start_time
    # clear text box text
    text_box.delete("1.0", tk.END)
    # change color to white
    window.config(background=RED_GRAD[0])
    button_frame.config(background=RED_GRAD[0])
    # reset timer
    start_time = None


# Window config
window = tk.Tk()
window.title(APP_NAME)
window.minsize(width=500, height=500)
window.config(padx=20, pady=20, background=RED_GRAD[0])

# User input
text_box = scrolledtext.ScrolledText(height=15, width=50, font=FONT, wrap=tk.WORD)
text_box.focus()
text_box.config(pady=20, padx=20)
text_box.pack()

# button frame begin
button_frame = tk.Frame(window, bg=RED_GRAD[0])

# Save Button
save_button = tk.Button(button_frame, text="Save", command=save_to_file, height=3, width=10)
save_button.pack(side=tk.RIGHT, padx=5)

# Reset Button
reset_button = tk.Button(button_frame, text="Reset", command=window_reset, height=3, width=10)
reset_button.pack(side=tk.LEFT, padx=5)

# button frame pack
button_frame.pack(pady=10)

# Listen for Keypress
text_box.bind("<KeyPress>", timer_control)

# Begin timers. check every 500ms
check_time_remaining()

window.mainloop()
