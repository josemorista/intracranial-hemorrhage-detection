# Our imports
from Dicom import Dicom
from CvImage import CvImage
from Segment import Segment
from geometry import distanceToPolygon, isPointsInsidePolygon
import pandas as pd
from os import listdir
from os.path import isfile, join

# Our interest segments
# Bone
bone = Segment("Bone")
bone.setMinSegmentArea(200)
bone.setHUInterval(700, 3000)
bone.setRGB(0,0,255)
bone.setHSVFilter(100, 50, 0, 130, 255, 255)

# Blood
blood = Segment("Blood")
blood.setMinSegmentArea(100)
blood.setHUInterval(60, 100)
blood.setRGB(255,0,0)
blood.setHSVFilter(0, 60, 0, 10, 255, 255)

# Ventricle
ventricle = Segment("Ventricle")
ventricle.setMinSegmentArea(100)
ventricle.setHUInterval(-15, 15)
ventricle.setRGB(0,255,0)
ventricle.setHSVFilter(50,100, 0, 70, 255, 255)

# BrainMass
brainMass = Segment("BrainMass")
brainMass.setMinSegmentArea(200)
brainMass.setHUInterval(20, 50)
brainMass.setRGB(255,255,0)
brainMass.setHSVFilter(25, 50, 0, 35, 255, 255)

labels = pd.read_csv('D:/Downloads/stage2train.csv')

# Here it comes!
path = "D:/Downloads/stage2train/"
dcmFiles = []
dirFiles = listdir(path)
i = 0
while i < len(dirFiles) and i < 1:
  if isfile(join(path, dirFiles[i])):
    dcmFiles.append(dirFiles[i])
  i = i + 1

results = open("./results/results.txt", "a")

for filename in dcmFiles:
  ds = Dicom(path+filename)
  
  # Print labels and ID
  results.write(filename[:-4])
  for label in ["epidural", "intraparenchymal", "intraventricular", "subarachnoid", "subdural", "any"]:
    results.write("," + str(labels.loc[labels["ID"] == (filename[:-4]+"_"+label)].values[0][1]))

  # Filter by Hounsfield units (HU)
  segmentedRGB = ds.getSegmentedRGB([
    (bone.getLowerHU(), bone.getHigherHU(), bone.getBGR()), 
    (ventricle.getLowerHU(), ventricle.getHigherHU(), ventricle.getBGR()),
    (blood.getLowerHU(), blood.getHigherHU(), blood.getBGR()),
    (brainMass.getLowerHU(), brainMass.getHigherHU(), brainMass.getBGR())
  ])
  
  # Array of segments and their features
  segments = {
    bone.getName():{
      "segment": bone,
      "extractedFeatures": {}
    },
    brainMass.getName(): {
      "segment": brainMass,
      "extractedFeatures": {}
    },
    ventricle.getName(): {
      "segment": ventricle,
      "extractedFeatures": {}
    },
    blood.getName(): {
      "segment": blood,
      "extractedFeatures": {}
    }
  }

  for key in segments:
    
    segment = segments[key]["segment"]

    image = CvImage(segmentedRGB, segment.getName())

    image.hsvFilter(segment.getLowerHSV(), segment.gethigherHSV())

    # Perform some morph operations
    image.morphOperations()

    # Let's get all we want
    features = image.getContoursFeatures(segment.getMinSegmentArea())

    # RGB to see green contour
    image.gray2bgr()

    if (key == "Ventricle" or key == "BrainMass"):
      for atrib in ["area", "eccentricity"]:
        results.write("," + str(features[0][atrib]))

    for i in range(len(features)):
      # Blood only features
      if key == "Blood":
        distanceToBone = distanceToPolygon(features[i]["centroid"], segments["Bone"]["extractedFeatures"][0]["convexHull"])
        
        j = 0
        isInsideVentricle = False
        while isInsideVentricle == False and j < len(segments["Ventricle"]["extractedFeatures"]):
          isInsideVentricle = isPointsInsidePolygon(features[i]["convexHull"], segments["Ventricle"]["extractedFeatures"][j]["convexHull"]).all()
          j = j + 1
        
        isInsideBrainMass = False
        if isInsideVentricle == False:
          j = 0
          while isInsideBrainMass == False and j < len(segments["BrainMass"]["extractedFeatures"]):
            isInsideBrainMass = isPointsInsidePolygon(features[i]["convexHull"], segments["BrainMass"]["extractedFeatures"][j]["convexHull"]).all()
            j = j + 1
        
        features[i]["distanceToBone"] = distanceToBone
        features[i]["isInsideVentricle"] = isInsideVentricle
        features[i]["isInsideBrainMass"] = isInsideBrainMass
        
        results.write("\n\t")
        for atrib in ["area", "eccentricity", "distanceToBone", "isInsideVentricle", "isInsideBrainMass"]:
          if (features[i][atrib] == False or features[i][atrib] == True):
            if (features[i][atrib] == True):
              results.write(str(1))
            else:
              results.write(str(0))
          else:
            results.write(str(features[i][atrib]))
          if atrib != "isInsideBrainMass":
             results.write(",")
        

      image.drawCircle(features[i]["centroid"])
      image.drawContours([features[i]["convexHull"]])

    segments[key]["extractedFeatures"] = features
  results.write("\n")
results.close()