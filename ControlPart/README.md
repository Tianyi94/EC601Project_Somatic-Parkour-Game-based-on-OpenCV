# Control Part
### This is the control part of the project.
### In this part we will try to realize face detection, hands detection and body detection.
### face.py realizes face detection with using a trained haarcasscade model. However a little problem is that it has a bad performance when the head is rotated more than 45 degrees.
### To improve the performance, we also add foreground extraction and background reduction funtion to the face detection as TA's advice. However, they just make the program slower and won't bring any improvement on the performance.
### Next step, we will train the hand detection by ourselves and apply a skeleton detection technology made by CMU, to see which has a better perfromance.
