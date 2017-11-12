#!/usr/bin/env python
import numpy as np
import cv2
from time import sleep
from medianFilter import median_2d_time_filter

median = median_2d_time_filter()
median0 = median_2d_time_filter()
median1 = median_2d_time_filter()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# capture video
cap = cv2.VideoCapture(0)
x=0
y=0
w=0
h=0
facesmedian=[()]
faceslist=[[]]
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	left=0
	right=0
#	sleep(0.02) # Time in seconds.
# read captured images
	ret,img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# detect face
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# if success to get face
    	if type(faces) != tuple:
		median.push(faces[0][0], faces[0][1], faces[0][2], faces[0][3])
	if type(faces) == tuple:
		median.push(0,0,0,0)

#	print 'faces=',faces

# store data after median filter
	facesmedian[0] = median.median()
	faceslist[0] = list(facesmedian[0])
	for i in range(4):
		faceslist[0][i] = int(faceslist[0][i])
#	print 'facesmedian =',facesmedian

	for (x,y,w,h) in faceslist:
#	for (x,y,w,h) in faces:

# draw face rectangle
    		cv2.rectangle(img,(x,y),(x+w/2,y+h),(255,0,255),2)
    		cv2.rectangle(img,(x+w/2,y),(x+w,y+h),(255,0,255),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = img[y:y+h, x:x+w]

# show image
	cv2.imshow('img',img)	

# press q to quit
	if (cv2.waitKey(1)==ord('q')):
		break
# free and close
cap.release()
cv2.destroyAllWindows()
