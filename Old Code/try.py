import sys
#Change the following line
sys.path.append('D:\opencv\opencv\sources\samples\python')

import numpy as np
import cv2

import socket
import time

import subprocess
#Change the following line
face_cascade = cv2.CascadeClassifier('D:\opencv\haarcascade_frontalface_alt.xml')

#Use socket to communicate with Unity3D
UDP_IP = "127.0.0.1"
UDP_PORT = 5065
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


class App(object):
    def __init__(self, video_src):
        self.cam = cv2.VideoCapture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('camshift')
        #cv2.setMouseCallback('camshift', self.onmouse)

        self.selection = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False


    def facedetection(self):
    #Face detection by using Haar cascade.
        if self.tracking_state == 0:
            flag = 1;
            while flag < 10:
            #Find face in first ten frames
                ret, img = self.cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    print(x,y,w,h)
                    self.selection = (x, y, x+w, y+h)
                flag= flag +1
            self.tracking_state = 1

    def show_hist(self):
    #Show the hist
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)

    def run(self):
        while True:
            ret, self.frame = self.cam.read()
            vis = self.frame.copy()
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
            self.facedetection()

            cv2.line(vis, (200, 0), (200, 480), (255, 0, 0), 1)
            cv2.line(vis, (440, 0), (440, 480), (255, 0, 0), 1)
            cv2.line(vis, (0, 150), (640, 150), (0, 255, 0), 1)

            if self.selection:
                x0, y0, x1, y1 = self.selection
                self.track_window = (x0, y0, x1-x0, y1-y0)
                hsv_roi = hsv[y0:y1, x0:x1]
                mask_roi = mask[y0:y1, x0:x1]
                hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
                self.hist = hist.reshape(-1)
                #self.show_hist()

                vis_roi = vis[y0:y1, x0:x1]
                cv2.bitwise_not(vis_roi, vis_roi)
                vis[mask == 0] = 0

            if self.tracking_state == 1:
            #If find the face
                self.selection = None
                prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
                prob &= mask
                term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
                track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)

                xPos = track_box[0][0]
                yPos = track_box[0][1]

                command = 0
                #Translate positon to command for the game
                if yPos < 150:
                    command = 2
                    word = 'jump'
                    print 'jump', str(command)
                elif xPos > 440:
                    command = -1
                    word = 'left'
                    print 'left ', str(command)
                elif xPos < 200:
                    command = 1
                    word = 'right'
                    print 'right ', str(command)
                else:
                    command = 0
                    word = 'middle'
                    print 'middle ', str(command)

                sock.sendto(str(command), (UDP_IP, UDP_PORT))

                #word = 'haha'
                cv2.rectangle(vis, (0, 0), (250, 100), (0, 23, 237), -1)
                cv2.rectangle(vis, (2, 2), (250, 100), (11, 235, 239), 3)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(vis, word, (20, 60), font, 2, (200, 255, 155), 5, cv2.CV_AA)

                #If you want to see Y Position
                #yPos = track_box[0][1]
                #print "position - Y:", str(yPos)

                if self.show_backproj:
                    vis[:] = prob[...,np.newaxis]
                try: cv2.ellipse(vis, track_box, (0, 0, 255), 2)
                except: print track_box

            cv2.imshow('camshift', vis)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv2.destroyAllWindows()


if __name__ == '__main__':
    import sys
    try: video_src = sys.argv[1]
    except: video_src = 0
    print __doc__
    #subprocess.Popen([r"..\exegame\run.exe"])
    App(video_src).run()