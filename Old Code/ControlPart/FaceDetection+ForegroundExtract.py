import numpy as np
import cv2
from matplotlib import pyplot as plt

face_cascade = cv2.CascadeClassifier('/home/tianyiz/user/601project/c/haarcascade_frontalface_alt.xml')
#face_cascade = cv2.CascadeClassifier('/home/tianyiz/user/601project/c/haarcascade_upperbody.xml')

cap = cv2.VideoCapture(0)

while 1:
	ret, img = cap.read()
#foregroundextract
	mask = np.zeros(img.shape[:2],np.uint8)
	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)
	rect = (161,79,150,150)
#
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#foregroundextract
	cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	img = img*mask2[:,:,np.newaxis]
#
	for (x,y,w,h) in faces:
		print(x,y,w,h)
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]


	cv2.imshow('img',img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
