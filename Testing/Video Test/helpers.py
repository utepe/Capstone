import cv2
import math
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Wrist landmark
wrist = mp_hands.HandLandmark.WRIST

# Index finger landmarks
index_tip = mp_hands.HandLandmark.INDEX_FINGER_TIP
index_pip = mp_hands.HandLandmark.INDEX_FINGER_PIP
index_mcp = mp_hands.HandLandmark.INDEX_FINGER_MCP

# Ring finger landmarks
ring_tip = mp_hands.HandLandmark.RING_FINGER_TIP
ring_pip = mp_hands.HandLandmark.RING_FINGER_PIP
ring_mcp = mp_hands.HandLandmark.RING_FINGER_MCP    

def landmark_dict(hand_landmarks):
    landmarks = {
                "index": {
                            "tip": [hand_landmarks.landmark[index_tip].x,
                                    hand_landmarks.landmark[index_tip].y,
                                    hand_landmarks.landmark[index_tip].z],
                            "pip": [hand_landmarks.landmark[index_pip].x,
                                    hand_landmarks.landmark[index_pip].y,
                                    hand_landmarks.landmark[index_pip].z],
                            "mcp": [hand_landmarks.landmark[index_mcp].x,
                                    hand_landmarks.landmark[index_mcp].y,
                                    hand_landmarks.landmark[index_mcp].z]},
                "wrist":            [hand_landmarks.landmark[wrist].x,
                                    hand_landmarks.landmark[wrist].y,
                                    hand_landmarks.landmark[wrist].z],
                "ring": {
                            "tip": [hand_landmarks.landmark[ring_tip].x,
                                    hand_landmarks.landmark[ring_tip].y,
                                    hand_landmarks.landmark[ring_tip].z],
                            "pip": [hand_landmarks.landmark[ring_pip].x,
                                    hand_landmarks.landmark[ring_pip].y,
                                    hand_landmarks.landmark[ring_pip].z],
                            "mcp": [hand_landmarks.landmark[ring_mcp].x,
                                    hand_landmarks.landmark[ring_mcp].y,
                                    hand_landmarks.landmark[ring_mcp].z]}}
    return landmarks

def ring_pip_theta(landmarks):
    # Generate vectors of pip -> mcp and pip -> tip to find pip angle
    pip_mcp = np.subtract(landmarks["ring"]["pip"], landmarks["ring"]["mcp"])
    pip_tip = np.subtract(landmarks["ring"]["pip"], landmarks["ring"]["tip"])

    pip_mcp = np.multiply(200,pip_mcp)
    pip_tip = np.multiply(200,pip_tip)

    # Compute angle between them
    dot_prod = np.dot(pip_mcp, pip_tip)
    mag_prod = np.linalg.norm(pip_mcp)*np.linalg.norm(pip_tip)
    theta = math.acos(dot_prod / mag_prod) * 180 / (math.pi)

    return(theta)

def get_window_size(width, height):
	# get the frame width and height
	frame_width = int(width)
	frame_height = int(height)

	# specify the desired window size
	desired_window_width = 800
	desired_window_height = 600

	# calculate the aspect ratio of the video
	aspect_ratio = frame_width / frame_height

	# calculate the desired frame size based on the desired window size and aspect ratio
	if aspect_ratio > 1:
		desired_frame_width = desired_window_width
		desired_frame_height = int(desired_window_width / aspect_ratio)
	else:
		desired_frame_width = int(desired_window_height * aspect_ratio)
		desired_frame_height = desired_window_height
	
	return desired_frame_width, desired_frame_height