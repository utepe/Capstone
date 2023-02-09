import cv2
import mediapipe as mp
from helpers import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.5) as hands:

    finger_angles = {
    "thumb": {
        "pip": [], "mcp": []},
    "index": {
        "pip": [], "mcp": []},
    "middle": {
        "pip": [], "mcp": []},
    "ring": {
        "pip": [], "mcp": []},
    "pinky": {
        "pip": [], "mcp": []},
    }
        
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = landmark_dict(hand_landmarks)

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            for finger in finger_angles:
                finger_angles[finger]["pip"].append(pip_theta(landmarks, finger))
                finger_angles[finger]["mcp"].append(mcp_theta(landmarks, finger))

                if len(finger_angles[finger]["pip"]) > 10:
                    finger_angles[finger]["pip"].pop(0)
                if len(finger_angles[finger]["mcp"]) > 10:
                    finger_angles[finger]["mcp"].pop(0)

        image = cv2.flip(image, 1)
        cv2.putText(image, f'{"thumb"} IP {sum(finger_angles["thumb"]["pip"]) / (len(finger_angles["thumb"]["pip"])+0.001)}', (5, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        cv2.putText(image, f'{"index"} IP {sum(finger_angles["index"]["pip"]) / (len(finger_angles["index"]["pip"])+0.001)}', (5, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        cv2.putText(image, f'{"middle"} IP {sum(finger_angles["middle"]["pip"]) / (len(finger_angles["middle"]["pip"])+0.001)}', (5, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        cv2.putText(image, f'{"ring"} IP {sum(finger_angles["ring"]["pip"]) / (len(finger_angles["ring"]["pip"])+0.001)}', (5, 90), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        cv2.putText(image, f'{"pinky"} IP {sum(finger_angles["pinky"]["pip"]) / (len(finger_angles["pinky"]["pip"])+0.001)}', (5, 110), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
