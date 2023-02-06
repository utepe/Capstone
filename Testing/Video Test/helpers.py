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

# Middle finger landmarks
middle_tip = mp_hands.HandLandmark.MIDDLE_FINGER_TIP
middle_pip = mp_hands.HandLandmark.MIDDLE_FINGER_PIP
middle_mcp = mp_hands.HandLandmark.MIDDLE_FINGER_MCP

# Pinky finger landmarks
pinky_tip = mp_hands.HandLandmark.PINKY_TIP
pinky_pip = mp_hands.HandLandmark.PINKY_PIP
pinky_mcp = mp_hands.HandLandmark.PINKY_MCP

# Thumb landmarks
thumb_tip = mp_hands.HandLandmark.THUMB_TIP
thumb_ip = mp_hands.HandLandmark.THUMB_IP
thumb_mcp = mp_hands.HandLandmark.THUMB_MCP
thumb_cmc = mp_hands.HandLandmark.THUMB_CMC

def landmark_dict(hand_landmarks):
	landmarks = {
				"thumb": {
					"tip": [thumb_tip], "ip": [thumb_ip], "mcp": [thumb_mcp], "cmc": [thumb_cmc]},
				"index": {
					"tip": [index_tip], "pip": [index_pip], "mcp": [index_mcp]},
				"middle": {
					"tip": [middle_tip], "pip": [middle_pip], "mcp": [middle_mcp]},
				"ring": {
					"tip": [ring_tip], "pip": [ring_pip], "mcp": [ring_mcp]},
				"pinky": {
					"tip": [pinky_tip], "pip": [pinky_pip], "mcp": [pinky_mcp]},
				"wrist": {
					"wrist": [wrist]}
				}

	for item in landmarks:
		for sub_item in landmarks[item]:
			landmarks[item][sub_item].append(hand_landmarks.landmark[landmarks[item][sub_item][0]].x)
			landmarks[item][sub_item].append(hand_landmarks.landmark[landmarks[item][sub_item][0]].y)
			landmarks[item][sub_item].append(hand_landmarks.landmark[landmarks[item][sub_item][0]].z)
			landmarks[item][sub_item].pop(0)
	
	return landmarks

def mcp_theta(landmarks, finger):
	# Generate vectors of mcp -> wrist and mcp -> pip to find mcp angle

	if finger == "thumb":
		mcp_pip = np.subtract(landmarks[finger]["mcp"], landmarks[finger]["ip"])
	else:
		mcp_pip = np.subtract(landmarks[finger]["mcp"], landmarks[finger]["pip"])

	mcp_wrist = np.subtract(landmarks[finger]["mcp"], landmarks["wrist"]["wrist"])

	# Compute angle between them
	dot_prod = np.dot(mcp_wrist, mcp_pip)
	mag_prod = np.linalg.norm(mcp_wrist)*np.linalg.norm(mcp_pip)
	theta = math.acos(dot_prod / mag_prod) * 180 / (math.pi)

	return(theta)

def pip_theta(landmarks, finger):
    # Generate vectors of pip -> mcp and pip -> tip to find pip angle

	if finger == "thumb":
		pip_tip = np.subtract(landmarks[finger]["ip"], landmarks[finger]["tip"])
		pip_mcp = np.subtract(landmarks[finger]["ip"], landmarks[finger]["mcp"])
	else:
		pip_tip = np.subtract(landmarks[finger]["pip"], landmarks[finger]["tip"])
		pip_mcp = np.subtract(landmarks[finger]["pip"], landmarks[finger]["mcp"])

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