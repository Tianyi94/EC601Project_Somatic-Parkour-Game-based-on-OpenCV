#!/usr/bin/env python
import sys
import numpy as np


class median_2d_time_filter:

#initialize to all zero
  def __init__(self,n=8):
    self.size=n
    self.x=np.zeros(self.size)
    self.y=np.zeros(self.size)
    self.h=np.zeros(self.size)
    self.w=np.zeros(self.size)

#push new data into hstack
  def push(self, x, y, h, w):
  #def push(self, h, w):
    self.h=np.hstack((self.h[1:],[h]))
    self.w=np.hstack((self.w[1:],[w]))
    self.x=np.hstack((self.x[1:],[x]))
    self.y=np.hstack((self.y[1:],[y]))

#get the median of last n data
  def median(self):
    #return (np.median(self.h), np.median(self.w))
    return (np.median(self.x), np.median(self.y),
            np.median(self.h), np.median(self.w))
