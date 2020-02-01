#Takes and saves a screenshot from a webcame, assuming one is attached.

import cv2

videoCapture = cv2.VideoCapture(0)
if not videoCapture.isOpened():
    print("Nope")
    raise Exception("Could not open video device.")
else:
    print("Success!")
ret, frame = videoCapture.read()
videoCapture.release()
cv2.imwrite("myImage.png",frame)