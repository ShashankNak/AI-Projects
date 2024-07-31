import cv2 as cv
import numpy as np
import time
from ultralytics  import YOLO

# import yolo model
model = YOLO("yolov8n-seg.pt")

cap = cv.VideoCapture('data/cashew_train.mp4')

# Get the width and height of the original video frame
original_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# Define the new width and height
scale = 0.6
new_width = int(original_width*scale) #1 for width
new_height = int(original_height*scale) #0 for height

# Define the delay between displaying each frame (in seconds)
delay = 0.01  # Adjust this value to change the speed


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    # Resize the frame
    resized_frame = cv.resize(frame, (new_width, new_height))

    # # Display the resized frame
    # cv.imshow('Resized Frame', resized_frame)

    original_image = resized_frame[:new_height//2,:]

    results = model(original_image)

    #visulaize the results in the frame
    annoted_frame = results[0].plot()
    cv.imshow("Yolo model",annoted_frame)


    binary_image = resized_frame[new_height//2:,:]

    # Display the original image
    cv.imshow('Original Image', original_image)
    # #display binary image
    # cv.imshow('Binary Image', binary_image)
    # Introduce a delay to slow down the video
    time.sleep(delay)


    # Exit if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('d'):
        break

cv.waitKey(0)