from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import os

#Takes a path to an image, and returns a cropped rectangle inside the image.
def cropImage(filePath,debug=False):
    if filePath is None:
        raise TypeError("None Type Object was passed into cropImage.")
        return None
    elif not isinstance(filePath,str):
        raise TypeError("Param for cropImage is not a string: " + str(type(filePath)))
        return None
    try:
        image = cv2.imread(filePath)
        image = imutils.resize(image, height=500)
        edged = _getEdges(image,debug)
        # _showcase(image,edged)
        displayCnt = _findRectangle(edged,image,debug)
        if displayCnt is None:
            return None
        output = four_point_transform(image, displayCnt.reshape(4, 2))
        
        # if(debug):
        cv2.imshow("output",output)
        print("Press a key to continue. Need to have one of the images selected!")
        cv2.waitKey(0) #Doesn't work in debug mode for some reason.
        
        return output
    except:
        raise TypeError("Image failed to load. Directory : " + filePath)
        return None
    
#Takes in two image objects as a param, and shows them. Press 0 to move on.
def _showcase(image, edged):
    cv2.imshow("Original",image)
    cv2.imshow("Edged",edged)
    print("Press a key to continue. Need to have one of the images selected!")
    cv2.waitKey(0) #Doesn't work in debug mode for some reason.

#Takes an image object, and returns an image object of the edges.
def _getEdges(image,debug):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray,(3,3),cv2.BORDER_DEFAULT)
        blurred = cv2.GaussianBlur(blurred,(3,3),cv2.BORDER_DEFAULT)
        # blurred = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(blurred, 30, 200)
        
        if(debug):
            cv2.imshow("Blurred",blurred)
            cv2.imshow("Edged",edged)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return edged
    except IOError:
        raise TypeError("Image failed to load. Directory : " + os.getcwd())
        return None

#Takes an edged image object, and returns the contours for the screen (hopefully)
def _findRectangle(edged, image, debug):
    try:
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        displayCnt = None

        if(debug):
            _showContours(cnts,image)

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.03 * peri, True)

            if len(approx) == 4:
                return approx
        
        print("No Contour was found.")
        return None
    except IOError:
        raise TypeError("Image failed to load. Directory : " + os.getcwd())
        return None
    
def _showContours(cnts,image):
    i = 0
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)
        print("i: " + str(i))
        _showContour(c,peri,approx,image)
        i+=1
    
def _showContour(c,peri,approx,image):
    print("peri: " + str(peri))
    print("len(approx): " + str(len(approx)))
    print("Contour Area: " + str(cv2.contourArea(c)))
    
    temp = image.copy()
    cv2.drawContours(temp,[c],0,(0,255,0),2)
    cv2.imshow("Outline",temp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()