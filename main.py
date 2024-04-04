import tkinter as tk
from tkinter import scrolledtext

# Constants
APP_NAME = "Ghost Writer"
FONT = ("Arial", 30, "bold")

# Window config
window = tk.Tk()
window.title(APP_NAME)
window.minsize(width=1000, height=600)
window.config(padx=20, pady=20)

# User input
text_box = scrolledtext.ScrolledText(height=15, width=50, font=FONT, wrap=tk.WORD)
text_box.focus()
text_box.config(pady=20, padx=20)
text_box.pack(pady=30)


window.mainloop()