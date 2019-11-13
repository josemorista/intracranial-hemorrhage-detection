from math import pow, sqrt

def euclidianDistance (p1, p2):
   return sqrt((pow((p2[0] - p1[0]), 2)) + (pow((p2[1] - p1[1]), 2)))