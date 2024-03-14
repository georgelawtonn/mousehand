import cv2
import mediapipe as mp

class Camera:
    def __init__(self, camera_id=0):
        """
        Initialize the camera and MediaPipe hands model.q
        :param camera_id: ID of the camera (default: 0)
        """
        self.camera = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        self.hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing_utils = mp.solutions.drawing_utils

    def __del__(self):
        """
        Release the camera when the object is destroyed.
        """
        self.camera.release()

    def get_frame(self):
        """
        Read a frame from the camera and perform hand detection using MediaPipe.
        :return: The original frame and the frame with hand landmarks
        """
        ret, frame = self.camera.read()
        if not ret:
            return None, None

        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform hand detection using MediaPipe
        results = self.hands.process(frame_rgb)

        # Check if a hand is detected
        if results.multi_hand_landmarks:
            # Iterate over detected hands
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                self.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                # Check if the index finger tip is closer to the thumb tip (clicking gesture)
                index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
                if index_tip.y < thumb_tip.y:
                    print("Clicking gesture detected!")

        return frame, frame

    def show_frame(self, frame, window_name='Camera Feed'):
        """
        Display the frame in a window.
        :param frame: The frame to be displayed.
        :param window_name: Name of the window (default: 'Camera Feed').
        """
        cv2.imshow(window_name, frame)

    def wait_for_key(self, delay=1):
        """
        Wait for a key press.
        :param delay: Delay in milliseconds (default: 1).
        :return: ASCII code of the pressed key.
        """
        return cv2.waitKey(delay) & 0xFF

    def cleanup(self):
        """
        Close all the windows created by OpenCV.
        """
        cv2.destroyAllWindows()


# Create an instance of the Camera class
camera = Camera()

# Start capturing frames from the camera
while True:
    # Get a frame from the camera
    frame, _ = camera.get_frame()

    # Check if the frame is None (indicates an error)
    if frame is None:
        break

    # Display the frame with hand landmarks
    camera.show_frame(frame)

    # Wait for a key press (delay of 1 ms)
    key = camera.wait_for_key(1)

    # If the 'q' key is pressed, break out of the loop
    if key == ord('q'):
        break

# Clean up and close all windows
camera.cleanup()