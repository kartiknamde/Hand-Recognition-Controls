import os
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import pyautogui
import webbrowser
import subprocess
import tkinter as tk
import mysql.connector

# Disable GPU usage
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Configure TensorFlow to use CPU only
config = tf.compat.v1.ConfigProto(device_count={'GPU': 0})
sess = tf.compat.v1.Session(config=config)

# Initialize MediaPipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

# Initialize timestamp variables for volume control
last_volume_change_time = time.time()

# Initialize timestamp variables for browser control
last_browser_action_time = time.time()
browser_opened = False  # Track whether the browser is open or not
browser_cooldown_duration = 4.0  # Set the cooldown duration in seconds

last_media_player_action_time = time.time()
media_player_opened = False  # Track whether the media player is open or not
media_player_cooldown_duration = 4.0  # Set the cooldown duration in seconds

last_paint_app_action_time = time.time()
paint_app_opened = False  # Track whether the Paint app is open or not
paint_app_cooldown_duration = 4.0  # Set the cooldown duration in seconds

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize volume control variables
volume_increment = 0.02  # Adjust this value to control volume increment
delay_duration = 0.3  # Set the delay duration in seconds

# Get the default audio endpoint for the system
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

# Initialize timestamp variables
last_change_time = time.time()

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="os"
)

gesture_detection_delay = 0.08  # Delay in seconds


while True:
    _, frame = cap.read()
    x, y, c = frame.shape
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    display_text = ''
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            classID = np.argmax(prediction)
            className = classNames[classID]

            # Volume control based on gesture
            if className == 'thumbs up' and time.time() - last_volume_change_time >= delay_duration:
                # Increase volume with a delay
                current_volume = volume.GetMasterVolumeLevelScalar()
                new_volume = min(1.0, current_volume + volume_increment)
                volume.SetMasterVolumeLevelScalar(new_volume, None)
                last_volume_change_time = time.time()
                display_text = 'Increasing Volume'
            elif className == 'thumbs down' and time.time() - last_volume_change_time >= delay_duration:
                # Decrease volume with a delay
                current_volume = volume.GetMasterVolumeLevelScalar()
                new_volume = max(0.0, current_volume - volume_increment)
                volume.SetMasterVolumeLevelScalar(new_volume, None)
                last_volume_change_time = time.time()
                display_text = 'Decreasing Volume'

            # Browser control based on gesture
            elif className == 'peace' and time.time() - last_browser_action_time >= browser_cooldown_duration:
                # Toggle browser state (open/close) with a delay
                if browser_opened:
                    pyautogui.hotkey('ctrl', 'w')  # Close the current tab
                    browser_opened = False
                    display_text = 'Closing Browser'
                else:
                    os.system("start chrome")  # Open Chrome if not already open
                    browser_opened = True
                    display_text = 'Opening Browser'

                last_browser_action_time = time.time()
            # Browser control based on gesture
            elif className == 'smile' and time.time() - last_browser_action_time >= browser_cooldown_duration:
                if not browser_opened:
                    # Open YouTube in Chrome if it's not already open
                    webbrowser.open("https://www.youtube.com/")
                    browser_opened = True
                    display_text = 'Opening YouTube in Chrome'
                else:
                    # Close the Chrome tab if it's already open
                    pyautogui.hotkey('ctrl', 'w')
                    browser_opened = False
                    display_text = 'Closing YouTube in Chrome'

                last_browser_action_time = time.time()
            # Media player control based on gesture
            elif className == 'rock' and time.time() - last_media_player_action_time >= media_player_cooldown_duration:
                if not media_player_opened:
                    # Open Windows Media Player if it's not already open
                    subprocess.Popen(["C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe"])
                    media_player_opened = True
                    display_text = 'Opening Windows Media Player'
                else:
                    # Close Windows Media Player if it's already open
                    subprocess.Popen("taskkill /f /im wmplayer.exe", shell=True)
                    media_player_opened = False
                    display_text = 'Closing Windows Media Player'

                last_media_player_action_time = time.time()

            # Paint app control based on gesture
            elif className == 'stop' and time.time() - last_paint_app_action_time >= paint_app_cooldown_duration:
                if not paint_app_opened:
                    # Open Windows Paint app if it's not already open
                    subprocess.Popen(["mspaint.exe"])
                    paint_app_opened = True
                    display_text = 'Opening Paint App'
                else:
                    # Close Paint app if it's already open
                    subprocess.Popen("taskkill /f /im mspaint.exe", shell=True)
                    paint_app_opened = False
                    display_text = 'Closing Paint App'

                last_paint_app_action_time = time.time()

            # Insert data into MySQL table
            try:
                mycursor = mydb.cursor()
                sql = "INSERT INTO gesture_records (gesture_name, gesture_count) VALUES (%s, %s)"
                val = (className, 1)  # Set gesture_count to 1 for each record
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
            except mysql.connector.Error as err:
                print("Error:", err)

            time.sleep(gesture_detection_delay)  # Introduce delay

    # Show the prediction on the frame
    cv2.putText(frame, f'Gesture: {display_text}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Output", frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
