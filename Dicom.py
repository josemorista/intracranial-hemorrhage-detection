import numpy as np
import pydicom as dicom

def getSegmentedPixelColor (value, intervals):
  for i in range(len(intervals)):
    if value >= intervals[i][0] and value <= intervals[i][1]:
      return intervals[i][2]
  return [0,0,0]

# Linear transformation : from [bt < pxvalue < wt] linear to [0 <pyvalue< 255] !important: has loss of information
def linearTransform(pxvalue, bt, wt):
    if pxvalue < bt:
        y=0
    elif pxvalue > wt:
        y=255
    else:
        y=pxvalue*255/(wt-bt)-255*bt/(wt-bt)
    return y

# Linear transformation : convert to Hounsfield units (HU)
def getHuPixels (pixels_array, rows, cols, intercept, slope):
    m = np.zeros((rows, cols), np.int16)
    for i in range(rows):
      for j in range(cols):
        m[i][j] = pixels_array[i][j] * slope + intercept
    return m

class Dicom:
  def __init__(self, src):
    self.__ds = dicom.dcmread(src)
    self.__patientId = self.__ds.PatientID
    self.__cols = self.__ds.Columns
    self.__rows = self.__ds.Rows
    self.__huPixelsArray = getHuPixels(self.__ds.pixel_array, self.__rows, self.__cols, self.__ds.RescaleIntercept, self.__ds.RescaleSlope)

  def getPatientId (self):
    return self.__patientId

  def getPixelsArray (self):
    return self.__huPixelsArray

  def getRawPixelsArray (self):
    return self.__ds.pixel_array

  def getLinearRGB (self, bt, wt):
    image = np.zeros((self.__rows, self.__cols, 3), np.uint8)
    for i in range(self.__rows):
      for j in range(self.__cols):
        color = linearTransform(self.getPixelsArray()[i][j], bt, wt)
        image[i][j] = (color,color,color)
    return image
  
  # Remember, open-cv uses BGR color system
  def getSegmentedRGB (self, intervals = [(-3000,-1000,[0,0,0]),(-15,15,[255,0,128]),(20,50,[255,0,0]),(60,100,[0,0,255]),(101,3000,[255,255,255])]): # List of intervals to filter
    image = np.zeros((self.__rows, self.__cols, 3), np.uint8)
    for i in range(self.__rows):
      for j in range(self.__cols):
          image[i][j] = getSegmentedPixelColor(self.getPixelsArray()[i][j], intervals)
    return image

  def showHistogram (self):
    import matplotlib.pyplot as plt
    plt.hist(self.getPixelsArray().flatten(), bins=50, color='c')
    plt.xlabel("Hounsfield Units (HU)")
    plt.ylabel("Frequency")
    plt.show()
