class Segment:
  def __init__(self, name):
    self.__name = name
    self.__rgb = (255, 255, 255)

  def getName(self):
    return self.__name

  def setMinSegmentArea(self, area):
    self.__minSegmentArea = area

  def getMinSegmentArea(self):
    return self.__minSegmentArea

  def setHUInterval(self, lowHU, highHU):
    self.__lowerHU = lowHU
    self.__higherHU = highHU

  def getLowerHU(self):
    return self.__lowerHU

  def getHigherHU(self):
    return self.__higherHU

  def setRGB(self, r, g, b):
    self.__rgb = (r, g, b)
  
  def getRGB(self):
    return self.__rgb

  def getBGR(self):
    return (self.__rgb[2], self.__rgb[1], self.__rgb[0])
  
  def setHSVFilter(self, lowH, lowS, lowV, highH, highS, highV):
    self.__lowerHSV = (lowH, lowS, lowV)
    self.__higherHSV = (highH, highS, highV)
  
  def getLowerHSV(self):
    return self.__lowerHSV

  def gethigherHSV(self):
    return self.__higherHSV