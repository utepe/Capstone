import cv2
import mediapipe as mp
from helpers import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
path = r'C:/Users/gmari/Documents/Repos/Capstone/Testing/Video Test/wrist_angle_sample.mp4'
cap = cv2.VideoCapture(path)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      break
    
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    theta = 0
    buffer = []
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        landmarks = landmark_dict(hand_landmarks)
        theta = ring_pip_theta(landmarks)
        buffer.append(theta)

        if len(buffer) > 500:
          buffer.pop(0)

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        
    # Flip the image horizontally for a selfie-view display.
    if len(buffer) > 1:
      theta = sum(buffer) / len(buffer)

    image = cv2.flip(image, 1)
    cv2.putText(image, str(int(theta)), (100,100), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2, cv2.LINE_AA)
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break

cap.release()

# Closes all the frames
cv2.destroyAllWindows()