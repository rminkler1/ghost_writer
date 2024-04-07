import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext, filedialog

# Constants
APP_NAME = "Ghost Writer"
FONT = ("Arial", 30, "bold")
RED_GRAD = ["#FFFFFF", "#FFE2E2", "#FFC6C6", "#FFAAAA", "#FF8D8D", "#FF7171", "#FF5555", "#FF3838", "#FF1C1C",
            "#FF0000", "#00ff00"]

# Time tracking
start_time = None
last_key_press = datetime.now()
time_out_seconds = 10
seconds_till_safe_from_delete = 300  # five minutes == 300 seconds


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
            percent_to_wipe = seconds_since_key_press / time_out_seconds     # convert time to percentage 1 == 100%
            if percent_to_wipe >= 1:    # if percent to wipe >= 100% ... wipe text box and reset
                window_reset()
            else:
                # change color to red
                number = int(percent_to_wipe * 10)
                if number > 9:
                    number = 9
                color_index = number

                window.config(background=RED_GRAD[color_index])
                button_frame.config(background=RED_GRAD[color_index])
        else:
            # turn window green when safe
            window.config(background=RED_GRAD[10])
            button_frame.config(background=RED_GRAD[10])

    # check time every half second
    window.after(500, check_time_remaining)


def file_save():
    """
    Saves typed text to a txt file.
    Uses filedialog for naming and location.
    """
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f:  # asksaveasfile return `None` if dialog closed with "cancel".
        text2save = str(text_box.get(1.0, tk.END))
        f.write(text2save)
        f.close()


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
save_button = tk.Button(button_frame, text="Save", command=file_save, height=3, width=10)
save_button.pack(side=tk.RIGHT, padx=5)

# Reset Button
reset_button = tk.Button(button_frame, text="Reset", command=window_reset, height=3, width=10)
reset_button.pack(side=tk.LEFT, padx=5)

# button frame pack
button_frame.pack()

# Listen for Keypress
text_box.bind("<KeyPress>", timer_control)

check_time_remaining()

window.mainloop()
