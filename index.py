# Our imports
import cv2
import numpy as np
from Point import Point
from Dicom import Dicom
from os import listdir
from os.path import isfile, join
import imutils

def abs (n):
  if n >= 0:
    return n
  return abs((-1 * n))

# Here it comes!
path = './data/'
dcmFiles = [f for f in listdir(path) if isfile(join(path, f))]

for filename in dcmFiles:
  ds = Dicom(path+filename)
  image = ds.getFilteredRGB([(-15, 15, (0, 0, 255))])
  
  kernel = np.ones((3,3),np.uint8)
  image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
  image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  gray = cv2.bilateralFilter(gray, 11, 17, 17)
  edged = cv2.Canny(gray, 30, 200)
  cv2.imshow('gray', gray)

  cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
  
  larger = []
  for i in range(0, 5):
    if len(cnts) > abs(i):
      larger.append(cnts[i])

  cv2.drawContours(image, larger, -1, (0, 255, 0), 2)
  cv2.imshow("Contours", image)
  cv2.waitKey(0)