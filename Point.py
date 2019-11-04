from math import pow, sqrt

class Point:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def euclidianDistance(self, p2):
    return sqrt((pow((p2.x - self.x), 2)) + (pow((p2.y - self.y), 2)))
