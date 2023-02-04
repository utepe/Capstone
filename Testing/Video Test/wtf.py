# importing libraries
import cv2
import numpy as np
  
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(r'C:\Users\gmari\Documents\Repos\Capstone\Testing\Video Test\wrist_angle_sample.mp4')

# get the frame width and height
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

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
  
# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video file")
  
# Read until video is completed
while(cap.isOpened()):
      
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        # Display the resulting frame
        frame = cv2.resize(frame, (desired_frame_width, desired_frame_height))
        cv2.imshow('Frame', frame)
          
    # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
  
# Break the loop
    else:
        break
  
# When everything done, release
# the video capture object
cap.release()
  
# Closes all the frames
cv2.destroyAllWindows()