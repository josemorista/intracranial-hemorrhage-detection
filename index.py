# Our imports
import cv2
from Point import Point
from Dicom import Dicom
from os import listdir
from os.path import isfile, join

# Here it comes!
path = './data/'
dcmFiles = [f for f in listdir(path) if isfile(join(path, f))]

for filename in dcmFiles:
  ds = Dicom(path+filename)
  image = cv2.cvtColor(ds.getFilteredRGB(), cv2.COLOR_BGR2GRAY)
  cv2.imshow('image', image)
  cv2.waitKey(0)
  ds.showHistogram()