#!/usr/bin/env python
import numpy as np
import cv2
from time import sleep
from medianFilter import median_2d_time_filter

median = median_2d_time_filter()
median0 = median_2d_time_filter()
median1 = median_2d_time_filter()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#capture video
cap = cv2.VideoCapture(0)
x=0
y=0
w=0
h=0
m=10
n=340
go=0
num=0
facesmedian=[()]
faceslist=[[]]
eyesmedian=[(),()]
eyeslist=[[],[]]
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	left=0
	right=0
	goleft=0
	goright=0
#	sleep(0.02) # Time in seconds.
#read captured images
	ret,img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#detect face
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

#if success to get face
    	if type(faces) != tuple:
		median.push(faces[0][0], faces[0][1], faces[0][2], faces[0][3])
	if type(faces) == tuple:
		median.push(0,0,0,0)

#	print 'faces=',faces

#store data after median filter
	facesmedian[0] = median.median()
	faceslist[0] = list(facesmedian[0])
	for i in range(4):
		faceslist[0][i] = int(faceslist[0][i])
#	print 'facesmedian =',facesmedian

	for (x,y,w,h) in faceslist:
#	for (x,y,w,h) in faces:
#draw face rectangle
    		cv2.rectangle(img,(x,y),(x+w/2,y+h),(255,0,255),2)
    		cv2.rectangle(img,(x+w/2,y),(x+w,y+h),(255,0,255),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = img[y:y+h, x:x+w]

#if success to get eyes
#    	if type(eyes) != tuple:two eyes
	if (type(eyes) != tuple)&(len(eyes)==2):
		median0.push(eyes[0][0], eyes[0][1], eyes[0][2], eyes[0][3])
		median1.push(eyes[1][0], eyes[1][1], eyes[1][2], eyes[1][3])

#    	if type(eyes) != tuple:one eyes		
	if (type(eyes) != tuple)&(len(eyes)==1):
		if ((eyes[0][0]+eyes[0][2]) < (x+w/2)):
			median0.push(eyes[0][0], eyes[0][1], eyes[0][2], eyes[0][3])
			median1.push(0,0,0,0)
		if (eyes[0][0] > (x+w/2)):
			median1.push(eyes[0][0], eyes[0][1], eyes[0][2], eyes[0][3])
			median0.push(0,0,0,0)

#	if type(eyes)==tuple: no eyes
	if type(eyes)==tuple: 
		median0.push(0,0,0,0)
		median1.push(0,0,0,0)

#store data after median filter
	eyesmedian[0] = median0.median()
	eyesmedian[1] = median1.median()
	eyeslist[0] = list(eyesmedian[0])
	eyeslist[1] = list(eyesmedian[1])

#	print 'eyeslist[0] =',eyeslist[0]
#	print 'eyeslist[1] =',eyeslist[1],'\n'

	for i in range(4):
		eyeslist[0][i] = int(eyeslist[0][i])
		eyeslist[1][i] = int(eyeslist[1][i])
#	print 'eyeslist=',eyeslist	

#	for (ex,ey,ew,eh) in eyeslist:
#separate right eye green
	ex0 = eyeslist[0][0]
	ey0 = eyeslist[0][1]
	ew0 = eyeslist[0][2]
	eh0 = eyeslist[0][3]

	ex1 = eyeslist[1][0]
	ey1 = eyeslist[1][1]
	ew1 = eyeslist[1][2]
	eh1 = eyeslist[1][3]

#reparate right G+R
	if ((ex0+ew0) < (x+w/2))&(ex0>x):
		cv2.rectangle(img,(ex0,ey0),(ex0+ew0,ey0+eh0),(0,255,255),2)
		right = 1
#reparate left B+G
	if (ex1 > (x+w/2)):
		cv2.rectangle(img,(ex1,ey1),(ex1+ew1,ey1+eh1),(255,255,0),2)
		left = 1

	if type(eyes)==tuple: 
		left=0
		right=0

# Create a black image 700x700
	img2 = np.zeros((700,700,3), np.uint8)
#	img2 = np.zeros((80,320,3), np.uint8)

# move the car at location: (m,n)

	if (left==0)&(right==0):
		num+=1
	if (left==1)&(right==0):
		goleft=1
	if (left==0)&(right==1):
		goright=1

#confirm blink which lasts 8 times	
	if num%8==0:
		if go==0:
			go=1
		elif go==1:
			go=0
		num+=1#avoid staying in 8n

	print 'left =',left
	print 'right=',right,'\n'
	print 'goleft =',goleft
	print 'goright=',goright,'\n'
	print 'go =',go,'\n'

	if go==1:
		n-=20
		cv2.putText(img2,'Blink Control: Go',(10,30), font, 1,(0,255,0),2,cv2.LINE_AA)
		if goleft == 1:
			m-=5
			cv2.putText(img2,'Direction: Left',(10,60), font, 1,(255,255,0),2,cv2.LINE_AA)
		if goright == 1:
			m+=5
			cv2.putText(img2,'Direction: Right',(10,60), font, 1,(0,255,255),2,cv2.LINE_AA)

	if go==0:
		cv2.putText(img2,'Blink Control: Stop',(10,30), font, 1,(0,0,255),2,cv2.LINE_AA)


#limit the car inside the window
	if m<10:
		m=600
	if m>690:
		m=10

	if n<10:
		n=690
	if n>690:
		n=10

#cv2.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[,bottomLeftOrigin]]]) 
	cv2.putText(img2,'Car',(m,n), font, 2,(255,255,255),2,cv2.LINE_AA)

	cv2.imshow('img2',img2)

	cv2.imshow('img',img)	
#	print 'right open',right
#	print 'left open ',left
#press q to quit
	if (cv2.waitKey(1)==ord('q')):
		break
#free and close
cap.release()
cv2.destroyAllWindows()
