#!/usr/bin/env python
import numpy as np
import cv2
#from time import sleep
from medianFilter import median_2d_time_filter
median = median_2d_time_filter()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# capture video
#cap = cv2.VideoCapture(0)
# make sure it is front camera instead of rear camera
cap = cv2.VideoCapture(1)
# data from face_cascade
x = 0
y = 0
w = 0
h = 0
# center of the face
x_mid = 0
y_mid = 0
# left / right / up flag
x_axis = 0
y_axis = 0
# store data after midian filter
facesmedian = [()]
faceslist = [[]]

while True:
#	sleep(0.02) # Time in seconds.

# read captured images
	ret,img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# detect face
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# if success to get face, push it into median
    	if type(faces) != tuple:
		median.push(faces[0][0], faces[0][1], faces[0][2], faces[0][3])
	if type(faces) == tuple:
		median.push(0,0,0,0)

#	print 'faces=',faces

# store data after median filter into faceslist
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

# draw blue left line
		cv2.line(img,(250,0),(250,480),(255,0,0),2)
# draw blue right line
		cv2.line(img,(390,0),(390,480),(255,0,0),2)
# draw green up line
		cv2.line(img,(0,200),(640,200),(0,255,0),2)

# find the center of the face
		x_mid = x + w/2
		y_mid = y + h/2

# the img is 640 x 480
# find the position of center to determain left / right / up
# note : the img showed is mirrored from actual movement
# x axis
		# left side
		if (x_mid > 390):
			x_axis = 1
			print 'left ', x_axis
		# right side
		elif (x_mid < 250):
			x_axis = 2
			print 'right ', x_axis
		else:
			x_axis = 0
			print 'middle ', x_axis
# y axis		
		# upper side
		if (y_mid < 200):
			y_axis = 3
			print 'up ', y_axis
		# lower side
		else:
			y_axis = 0
			print 'down ', y_axis

		print 'x = ', x
		print 'y = ', y
		print 'w = ', w
		print 'h = ', h
# show image
	cv2.imshow('img', img)	

# press q to quit
	if (cv2.waitKey(1) == ord('q')):
		break
# free and close
cap.release()
cv2.destroyAllWindows()
