# Gesture Recognition Application

This application uses computer vision techniques to recognize hand gestures and execute corresponding AutoHotkey scripts. It provides a user-friendly interface for selecting gesture-specific AutoHotkey files and setting individual cooldown times for each gesture.

## Features

- Recognize hand gestures in real-time using the device's camera
- Execute AutoHotkey scripts based on recognized gestures
- Customizable AutoHotkey file selection for each gesture
- Individual cooldown times for each gesture to prevent rapid script execution
- Simple and intuitive user interface

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- MediaPipe
- tkinter
- AutoHotkey

## Installation

1. Clone the repository or download the source code files.

2. Install the required dependencies by running the following command: pip install opencv-python mediapipe tkinter

3. Make sure you have AutoHotkey installed on your system. You can download it from the official website: [AutoHotkey](https://www.autohotkey.com/)

## Usage

1. Run the `camera.py` script using Python: python camera.py

2. The Gesture Recognition application window will appear.

3. For each available gesture, click on the "Select AHK File" button to choose the corresponding AutoHotkey script file you want to execute when the gesture is recognized.

4. Set the desired cooldown time (in seconds) for each gesture using the provided input fields. This determines the minimum time interval between consecutive executions of the same gesture's script.

5. Click the "Start Recognition" button to begin the gesture recognition process.

6. The camera feed will be displayed in a new window, showing the real-time video with gesture recognition.

7. Perform the configured gestures in front of the camera to trigger the execution of the associated AutoHotkey scripts.

8. To close the application, press the 'q' key on the video window.

## Customization

- You can modify the list of available gestures in the `gestures` list within the script.

- Adjust the window size and layout by modifying the `window_width` and `window_height` variables in the script.

- Customize the AutoHotkey scripts executed for each gesture by selecting the appropriate files using the application's user interface.

## Troubleshooting

- If the application fails to start or crashes, ensure that all the required dependencies are properly installed.

- If the gesture recognition is not working as expected, check the camera connection and ensure sufficient lighting conditions.

- If the AutoHotkey scripts are not executing correctly, verify that the script files are valid and properly formatted.
