import cv2
import imutils
import numpy as np
from math import sqrt

def abs (n):
  if n >= 0:
    return n
  return abs((-1 * n))

class CvImage:
  def __init__ (self, image, name):
    self.__name = name
    self.__originalImage = image
    self.__image = image
    self.__contours = False
    self.__contoursFeatures = False
  
  def getName (self):
    return self.__name

  def getOriginalImage (self):
    return self.__originalImage

  def getImage (self):
    return self.__image

  def drawCircle (self, center, radious = 1, color = (0, 255, 0), thickness = 2):
    cv2.circle(self.__image, center, radious, color, thickness)

  def drawContours (self, contours, color = (0, 255, 0), thickness = 2):
    cv2.drawContours(self.__image, contours, -1, color, thickness)

  def __show (self, name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)

  def showOriginal (self):
    self.__show(self.__name + "-original", self.getOriginalImage())
  
  def show (self):
    self.__show(self.__name, self.__image)

  def morphOperations (self, kernelSize = 3):
    # Open and close morph operations
    kernel = np.ones((kernelSize, kernelSize),np.uint8)
    self.__image = cv2.morphologyEx(self.__image, cv2.MORPH_OPEN, kernel)
    self.__image = cv2.morphologyEx(self.__image, cv2.MORPH_CLOSE, kernel)  

  def hsvFilter (self, lowerHSV, higherHSV):
    # Convert to HSV
    self.__image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2HSV)

    # InRange filter
    self.__image = cv2.inRange(self.__image, lowerHSV, higherHSV)
    

  def getContours(self):
    if self.__contours == False:
      self.__contours = self.__findCountours()
    return self.__contours

  def getContoursFeatures(self, n = 5):
    if self.__contoursFeatures == False:
      self.__contoursFeatures = self.__findContoursFeatures(n)
    return self.__contoursFeatures

  def gray2bgr (self):
    self.__image = cv2.cvtColor(self.__image, cv2.COLOR_GRAY2BGR)

  def bgr2gray (self):
    self.__image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)

  def __findCountours(self):
    # ConvertToGrayScale and filter
    gray = cv2.bilateralFilter(self.__image, 11, 17, 17)
    
    # Edge algoritm
    edged = cv2.Canny(gray, 30, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Sort by larger areas
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
    return cnts

  def __findContoursFeatures (self, n):
    contoursFeatures = []
    cnts = self.getContours()
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