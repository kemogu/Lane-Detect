# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import math
import numpy as np
""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    window_title = "CSI Camera"

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()
                print(frame.shape)
                src = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                src = cv2.GaussianBlur(src, (7, 7), 0)
                dst = cv2.Canny(src, 120, 150, None, 3)
                cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
                cdstP = np.copy(cdst)
                    # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                linesP = cv2.HoughLinesP(
                            dst, # Input edge image
                            1, # Distance resolution in pixels
                            np.pi/180, # Angle resolution in radians
                            threshold=25, # Min number of votes for valid line
                            minLineLength=25, # Min allowed length of line
                            maxLineGap=25 # Max allowed gap between line for joining them
                )
                circles = cv2.HoughCircles(dst, 
                                           cv2.HOUGH_GRADIENT, 
                                           1, 
                                           50, 
                                           param1=50, 
                                           param2=30, 
                                           minRadius=10, 
                                           maxRadius=80)
                
                if linesP is not None:
                    for i in range(0, len(linesP)):
                        l = linesP[i][0]
                        cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv2.LINE_AA)
                if circles is not None:
                    circles = np.round(circles[0, :]).astype("int")
                    for (x, y, r) in circles:
                        pass
                    
                        #Yuvarlak cizme kodu
                        #cv2.circle(cdstP, (x, y), r, (0, 255, 0), 2)

                #Perspektif
                pts1 = np.float32([[0, 240], [640, 240],[0, 480], [640, 480]])
                pts2 = np.float32([[0, 0], [480, 0],[0, 640], [480, 640]])
                
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                pers = cv2.warpPerspective(frame, matrix, (500, 600))

                #Perspektif
                
                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, cdstP)
                    #cv2.imshow('Perspektif', pers) # Transformed Capture
                else:
                    break 
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()