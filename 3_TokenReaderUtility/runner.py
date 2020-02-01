import os, cv2
from edgeUtils import cropImage
from digitReading import getToken

filename = "IMG_0220.JPG"
absolute_path = os.path.join(os.getcwd(),filename)
# print("Absolute Path: " + absolute_path)
cropped = cropImage(absolute_path,debug=False)
digits = getToken(cropped,debug=False)
print(str(digits))

#220 next