# Our imports
import cv2
import numpy as np
from Point import Point
from Dicom import Dicom
from os import listdir
from os.path import isfile, join
import imutils
from math import sqrt

def abs (n):
  if n >= 0:
    return n
  return abs((-1 * n))

def getCountoursFeatures (cnts, n = 5):
  contoursFeatures = []
  for i in range(0, n):
    if len(cnts) > abs(i):
      
      # Compute the center of the contour
      M = cv2.moments(cnts[i])
      cx = int(M["m10"] / M["m00"])
      cy = int(M["m01"] / M["m00"])

      # Get some basic features
      perimeter = cv2.arcLength(cnts[i], True)
      epsilon = 0.1*perimeter
      approx = cv2.approxPolyDP(cnts[i],epsilon,True)

      # Calculate eccentricity
      (x, y), (MA, ma), angle = cv2.fitEllipse(cnts[i])
      a = ma/2
      b = MA/2
      
      if (a > b):
        eccentricity = sqrt(pow(a, 2)-pow(b, 2))
        eccentricity = round(eccentricity/a, 2)
      else:
        eccentricity = sqrt(pow(b, 2)-pow(a, 2))
        eccentricity = round(eccentricity/b, 2)

      # Append features
      contoursFeatures.append({
        "area": cv2.contourArea(cnts[i]),
        "perimeter": perimeter,
        "eccentricity": eccentricity,
        "centroid": (cx, cy),
        "approxDp": approx,
        "convexHull": cv2.convexHull(cnts[i])
      })
    else:
      break
    return contoursFeatures

# Here it comes!
path = "./data/"
dcmFiles = [f for f in listdir(path) if isfile(join(path, f))]

for filename in dcmFiles:
  ds = Dicom(path+filename)

  # Filter by Hounsfield units (HU)
  image = ds.getFilteredRGB([(-15, 15, (0, 0, 255))])
  
  # Open and close morph operations
  kernel = np.ones((3,3),np.uint8)
  image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
  image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  gray = cv2.bilateralFilter(gray, 11, 17, 17)
  
  # Edge algoritm
  edged = cv2.Canny(gray, 30, 200)

  cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  
  # Sort by larger areas
  cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
  
  # Let's get all we want
  contoursFeatures = getCountoursFeatures(cnts, 5)

  cv2.circle(image,contoursFeatures[0]["centroid"],1,(0,255,0),2)
  cv2.drawContours(image, [contoursFeatures[0]["convexHull"]], -1, (0, 255, 0), 2)
  cv2.imshow("Contours", image)
  cv2.waitKey(0)