import tkinter as tk
from tkinter import scrolledtext, messagebox
from pynput.keyboard import Controller
import threading
import random
import time
import subprocess
import sys
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np
import json
from pathlib import Path

# Try to import pytesseract, if not available, provide installation instructions
try:
    import pytesseract
except ImportError:
    messagebox.showerror("Missing Dependency", 
        "pytesseract is not installed.\n\n"
        "On Windows, install Tesseract from:\n"
        "https://github.com/UB-Mannheim/tesseract/wiki\n\n"
        "Then install pytesseract: pip install pytesseract pillow opencv-python")
    sys.exit(1)

# Globals
is_typing = False
current_position = 0
min_wpm = 40
max_wpm = 60
typing_thread = None
keyboard = Controller()
extracted_text = ""
window_selection_active = False

def select_window_region():
    """Allow user to select a window region for OCR."""
    global window_selection_active, extracted_text
    
    def on_button_press(event):
        event.widget.start_x = event.x
        event.widget.start_y = event.y
    
    def on_button_release(event):
        end_x = event.x
        end_y = event.y
        start_x = event.widget.start_x
        start_y = event.widget.start_y
        
        # Ensure coordinates are in correct order
        x1, x2 = min(start_x, end_x), max(start_x, end_x)
        y1, y2 = min(start_y, end_y), max(start_y, end_y)
        
        if x2 - x1 > 10 and y2 - y1 > 10:  # Minimum region size
            # Capture the selected region
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            
            # Convert PIL image to numpy array for OpenCV
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Preprocess image for better OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
            
            # Extract text using Tesseract
            try:
                text = pytesseract.image_to_string(processed)
                extracted_text = text
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", text)
                update_status(f"Extracted {len(text)} characters from selected region")
            except Exception as e:
                update_status(f"OCR Error: {str(e)}")
        
        # Clean up
        selection_window.destroy()
        window_selection_active = False
    
    # Create a transparent selection window
    selection_window = tk.Toplevel(root)
    selection_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    selection_window.attributes('-alpha', 0.3)
    selection_window.attributes('-topmost', True)
    
    canvas = tk.Canvas(selection_window, bg='gray', cursor='crosshair')
    canvas.pack(fill=tk.BOTH, expand=True)
    
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)
    
    update_status("Click and drag to select a region for OCR")
    window_selection_active = True

def auto_type(text_widget):
    """Simulates typing with optimized speed using pynput."""
    global is_typing, current_position, min_wpm, max_wpm
    text = text_widget.get("1.0", tk.END).strip()
    while current_position < len(text):
        if not is_typing:
            break
        keyboard.type(text[current_position])
        current_position += 1
        delay = 60 / (random.uniform(min_wpm, max_wpm) * 5)
        time.sleep(delay)

def start_typing(text_widget, min_wpm_input, max_wpm_input):
    """Starts the typing process."""
    global is_typing, typing_thread, min_wpm, max_wpm
    if is_typing:
        return
    try:
        min_wpm = int(min_wpm_input.get())
        max_wpm = int(max_wpm_input.get())
        update_status("Starting in 2 seconds...")
        time.sleep(2)
        is_typing = True
        if typing_thread is None or not typing_thread.is_alive():
            typing_thread = threading.Thread(
                target=auto_type, args=(text_widget,), daemon=True
            )
            typing_thread.start()
        update_status("Typing started.")
    except ValueError:
        update_status("Please enter valid WPM values.")

def pause_typing():
    """Pauses the typing process."""
    global is_typing
    if is_typing:
        is_typing = False
        update_status("Typing paused.")

def continue_typing():
    """Continues the typing process."""
    global is_typing, typing_thread
    if not is_typing:
        update_status("Continuing in 2 seconds...")
        time.sleep(2)
        is_typing = True
        if typing_thread is None or not typing_thread.is_alive():
            typing_thread = threading.Thread(
                target=auto_type, args=(text_widget,), daemon=True
            )
            typing_thread.start()
        update_status("Typing continued.")

def stop_typing():
    """Stops the typing process and resets progress."""
    global is_typing, current_position
    is_typing = False
    current_position = 0
    update_status("Typing stopped. Progress reset.")

def increase_speed(min_wpm_input, max_wpm_input):
    """Increases typing speed by 1.5x."""
    global min_wpm, max_wpm
    try:
        min_wpm = int(min_wpm_input.get())
        max_wpm = int(max_wpm_input.get())
        min_wpm = int(min_wpm * 1.5)
        max_wpm = int(max_wpm * 1.5)
        min_wpm_input.delete(0, tk.END)
        min_wpm_input.insert(0, str(min_wpm))
        max_wpm_input.delete(0, tk.END)
        max_wpm_input.insert(0, str(max_wpm))
        update_status(f"Speed increased: Min WPM = {min_wpm}, Max WPM = {max_wpm}")
    except ValueError:
        update_status("Please enter valid WPM values.")

def update_status(message):
    """Updates the status label."""
    status_label.config(text=message)

# Create the GUI
root = tk.Tk()
root.title("Auto Typing Tool with OCR")
root.geometry("600x750")

# Title Label
title_label = tk.Label(root, text="Auto Typing Tool with OCR", font=("Arial", 14, "bold"))
title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Min WPM and Max WPM Inputs
tk.Label(root, text="Min WPM:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
min_wpm_input = tk.Entry(root, width=10)
min_wpm_input.grid(row=1, column=1, padx=10, pady=5)
min_wpm_input.insert(0, "40")

tk.Label(root, text="Max WPM:").grid(row=1, column=2, padx=10, pady=5, sticky="e")
max_wpm_input = tk.Entry(root, width=10)
max_wpm_input.grid(row=1, column=3, padx=10, pady=5)
max_wpm_input.insert(0, "60")

# OCR Button
ocr_button = tk.Button(
    root, text="📸 Select Region for OCR", 
    command=select_window_region,
    bg="#4CAF50", fg="white", font=("Arial", 10, "bold")
)
ocr_button.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

# Text Area for Main Text
tk.Label(root, text="Text to Type:").grid(row=3, column=0, columnspan=4, padx=10, pady=5)
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
text_widget.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

# Control Buttons
start_button = tk.Button(
    root, text="Start", command=lambda: start_typing(text_widget, min_wpm_input, max_wpm_input),
    bg="#2196F3", fg="white"
)
start_button.grid(row=5, column=0, padx=10, pady=10)

pause_button = tk.Button(root, text="Pause", command=pause_typing, bg="#FF9800", fg="white")
pause_button.grid(row=5, column=1, padx=10, pady=10)

continue_button = tk.Button(root, text="Continue", command=continue_typing, bg="#2196F3", fg="white")
continue_button.grid(row=5, column=2, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_typing, bg="#f44336", fg="white")
stop_button.grid(row=5, column=3, padx=10, pady=10)

increase_speed_button = tk.Button(
    root, text="Increase Speed", 
    command=lambda: increase_speed(min_wpm_input, max_wpm_input),
    bg="#9C27B0", fg="white"
)
increase_speed_button.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

# Status Label
status_label = tk.Label(root, text="Status: Ready", fg="blue")
status_label.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

# Run the GUI
if __name__ == "__main__":
    root.mainloop()
