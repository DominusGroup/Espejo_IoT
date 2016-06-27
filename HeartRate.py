import cv2
import numpy as np

import picamera.array import PiRGBArray
from picamera import PiCamera
import time

print cv2.__version__

success = True
count = 0
    
# Init camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size = (640, 480))

# Warning up
time.sleep(0.1)

# Capture video from camera
for frame in camera.capture_continuos(rawCapture, format = "bgr", use_video_port = True) : 
    # Grab the raw Numpy array representing the image
    stream = frame.array # stream is the output

################# ROI ############################
        
    # Creates an OpenCV image
    CVimage = cv2.imdecode(stream, 1)

    # Load file for detecting faces (training)
    face_cascade = cv2.CascadeClassifier('/home/pi/face.xml')

    # Convert to grayscale
    gray = cv2.cvtColor(CVimage, cv2.COLOR_BGR2GRAY)

    # Look for faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    print " Se encontraron " + str(len(faces)) + " rostros "

    # Draw a rectangle around every found face
    for(x, y, w, h) in faces :
        cv2.rectangle(CVimage, (x, y), (x+w, y+h), (255, 0, 255), 2)

    # Crop the ROI
    crop_CVimage = CVimage[y+10: y+h-134, x+50: x+w-60]
    cv2.waitKey(0)

############# Green Filter ####################
    crop_CVimage[:, :, 2] = 0
    crop_CVimage[:, :, 0] = 0
############## Save frame #####################
    cv2.imwrite("frame%d.jpg" %count, crop_CVimage)
    count += 1            
############# Show the frame ##################
    cv2.imshow("Frame", crop_CVimage)
    key = cv2.waitKey(1) & 0xFF

    # Clear the stream for the next frame
    rawCapture.truncate(0)
    # Break the loop
    if key == ord("q") :
        break

     

 

