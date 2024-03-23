import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import subprocess
import time
import tkinter as tk
from tkinter import filedialog

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

gestures = ["Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up", "Victory"]
ahk_files = {}
cooldown_times = {}

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global last_execution_times, cooldown_times, ahk_files
    if result.gestures:
        gesture = result.gestures[0][0].category_name
        if gesture in ahk_files and ahk_files[gesture]:
            current_time = time.time()
            if current_time - last_execution_times.get(gesture, 0) >= cooldown_times[gesture]:
                print(f"{gesture} gesture detected. Executing AHK script.")
                try:
                    subprocess.Popen(["C:\\Program Files\\AutoHotkey\\AutoHotkey.exe", ahk_files[gesture]])
                    last_execution_times[gesture] = current_time
                except Exception as e:
                    print(f"Error executing AHK script: {e}")
            else:
                print(f"{gesture} gesture detected. Cooldown time not elapsed.")

def select_file(gesture):
    file_path = filedialog.askopenfilename(filetypes=[("AutoHotkey Script", "*.ahk")])
    ahk_files[gesture] = file_path
    file_labels[gesture].config(text=f"{gesture}: {file_path}")

def start_recognition():
    global cooldown_times
    for gesture in gestures:
        cooldown_times[gesture] = int(cooldown_entries[gesture].get())
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Gesture Recognition")

# Set the window size
window_width = int(root.winfo_screenwidth() * 0.3)  # 30% of the screen width
window_height = int(root.winfo_screenheight() * 0.75)  # 70% of the screen height
root.geometry(f"{window_width}x{window_height}")

# Create labels and buttons for each gesture
file_labels = {}
cooldown_entries = {}
for gesture in gestures:
    gesture_label = tk.Label(root, text=f"{gesture}:")
    gesture_label.pack()

    file_labels[gesture] = tk.Label(root, text="No file selected")
    file_labels[gesture].pack()

    file_button = tk.Button(root, text="Select AHK File", command=lambda g=gesture: select_file(g))
    file_button.pack(pady=5)

    cooldown_label = tk.Label(root, text=f"{gesture} Cooldown Time (seconds):")
    cooldown_label.pack()

    cooldown_entries[gesture] = tk.Entry(root)
    cooldown_entries[gesture].insert(0, "5")
    cooldown_entries[gesture].pack()

start_button = tk.Button(root, text="Start Recognition", command=start_recognition)
start_button.pack(pady=20)

note_label = tk.Label(root, text="Note: To close the application, press 'q' on the video window.")
note_label.pack()

# Run the main loop
root.mainloop()

last_execution_times = {}

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result,
    num_hands=1)

with GestureRecognizer.create_from_options(options) as recognizer:
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to MediaPipe's Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Get the current timestamp in milliseconds
        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

        # Recognize gestures in the frame
        recognizer.recognize_async(mp_image, timestamp_ms)

        # Display the frame
        cv2.imshow('Gesture Recognition', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()