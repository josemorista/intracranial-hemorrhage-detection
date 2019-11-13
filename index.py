# Our imports
from Dicom import Dicom
from CvImage import CvImage
from Segment import Segment

from os import listdir
from os.path import isfile, join

# Our interest segments
# Bone
bone = Segment("Bone")
bone.setMaxSegments(1)
bone.setHUInterval(700, 3000)
bone.setRGB(0,0,255)
bone.setHSVFilter(100, 50, 0, 130, 255, 255)

# Blood
blood = Segment("Blood")
blood.setMaxSegments(5)
blood.setHUInterval(60, 100)
blood.setRGB(255,0,0)
blood.setHSVFilter(0, 60, 0, 10, 255, 255)

# Ventricle
ventricle = Segment("Ventricle")
ventricle.setMaxSegments(5)
ventricle.setHUInterval(-15, 15)
ventricle.setRGB(0,255,0)
ventricle.setHSVFilter(50,100, 0, 70, 255, 255)

# Ventricle
brainMass = Segment("brainMass")
brainMass.setMaxSegments(1)
brainMass.setHUInterval(20, 50)
brainMass.setRGB(255,255,0)
brainMass.setHSVFilter(25, 50, 0, 35, 255, 255)

# Here it comes!
path = "./data/"
dcmFiles = [f for f in listdir(path) if isfile(join(path, f))]

for filename in dcmFiles:
  ds = Dicom(path+filename)

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

    image.show()

    # Let's get all we want
    contoursFeatures = image.getContoursFeatures(segment.getMaxSegments())

    segments[key]["extractedFeatures"] = contoursFeatures

    #if key == "Blood":
      # Discover if isInside Ventricle or BrainMass, get Distance to Bone

    # Print some features
    image.gray2bgr()
    for i in range(len(contoursFeatures)):
      image.drawCircle(contoursFeatures[i]["centroid"])
      image.drawContours([contoursFeatures[i]["convexHull"]])

    image.show()
  
