from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import os

debug = True

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

filename = "example.jpg"
absolute_path = os.path.join(os.getcwd(),filename)

print(absolute_path)
# print(os.listdir())
image = cv2.imread(absolute_path)

print(type(image))

image = imutils.resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(gray)
#Was gray for input image previously
# blurred = cv2.bilateralFilter(cl1,9,75,75) #Preserves edges better, a bit slower to run
blurred = cv2.GaussianBlur(cl1, (5,5), 0) 

edged = cv2.Canny(cl1,50,200,255)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(gray)

cv2.imwrite('clahe_2.jpg',cl1)

cv2.imwrite("gray.jpg",gray)
cv2.imwrite("edged.jpg",edged)
cv2.imwrite("blurred.jpg",blurred)

print(str(type(gray)))

if debug:
    cv2.imshow("Edged", edged)
    cv2.imshow("Gray", gray)
    cv2.imshow("CLAHE",cl1)
    cv2.imshow("Blurred",blurred)
    # cv2.waitKey(0)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.03 * peri, True)

    if len(approx) == 4:
        displayCnt = approx
        break
    
print(str(type(displayCnt)))
# print(str(displayCnt))
cv2.waitKey(0)

if displayCnt != None:
    warped = four_point_transform(gray, displayCnt.reshape(4,2))
    output = four_point_transform(image, displayCnt.reshape(4,2))
    
    if debug:
        cv2.imshow("Input", image)
        cv2.imshow("Warped", warped)
        cv2.waitKey(0)
else:
    print("displayCnt was None type")
    
    
    
#Attempt at bluring the edges, then eroding them.   
# blur=((3,3),3,21)
# erode_=(5,5)
# dilate_=(3, 3)
# edged = cv2.GaussianBlur(edged, blur[0], blur[1],sigmaY=blur[2])
# edged = cv2.Canny(blurred,50,200,255)
# edged = cv2.erode(edged,erode_)
# edged = cv2.dilate(cv2.erode(), np.ones(dilate_))*255
#cv2.imwrite('imgBool_erode_dilated_blured.png',cv2.dilate(cv2.erode(cv2.GaussianBlur(cv2.imread('so-br-in.png',0)/255, blur[0], blur[1]), np.ones(erode_)), np.ones(dilate_))*255)  