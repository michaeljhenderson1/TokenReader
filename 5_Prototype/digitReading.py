from imutils import contours
import imutils
import cv2
import numpy as np

def getDigits(cropped,debug=False):
    warped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    
    thresh = cv2.threshold(warped,0,255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    # if(debug):
    #     cv2.imshow("Threshold",thresh)
    #     cv2.imshow("Warped",warped)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    
    # #Cleans up the image further
    # cv2.imwrite("thresh1.png",thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
    # thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)
    dilation = cv2.dilate(thresh,kernel,iterations = 1)
        
    # kernel = np.ones((1,3),np.uint8)
    # erosion = cv2.erode(dilation,kernel,iterations = 1)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,5))
    # thresh = cv2.morphologyEx(erosion,cv2.MORPH_OPEN,kernel)
        
    if(debug):
        cv2.imshow("dilation",dilation)
        # cv2.imshow("d-erosion",erosion)
        # cv2.imshow("d-e-thresh",thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,
    #                         cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(dilation.copy(),cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = []
    
    if(debug):
        _debugDigitContours(cropped,cnts)
        _debugDigitBoundingBoxes(cnts,cropped)
    
    for c in cnts:
        (x,y,w,h) = cv2.boundingRect(c)
        minWidth = 15
        if (w>=minWidth and w<=30) and (h>=35 and h<=55):
            digitCnts.append(c)
        #For the number 1
        elif ((w>=4 and w<=8) and (h>=30 and h<=45)):
            digitCnts.append(c)
        
    digitCnts = contours.sort_contours(digitCnts,
                                       method="left-to-right")[0]
    
    # if(debug):
    #     _debugDigitContours(cropped,digitCnts)
    #     _debugDigitBoundingBoxes(digitCnts,cropped)
        
    digits = _contoursToDigits(digitCnts,thresh,cropped,minWidth,debug)
    
    digitsStr = ""
    for i in digits: 
        digitsStr .= i
    
    return digitsStr   
        
def _contoursToDigits(digitCnts,thresh,cropped,minWidth,debug):
    DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 1, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
    }
    
    output = cropped.copy()
    
    digits=[]
    for c in digitCnts:
        im = cropped.copy()
        (x,y,w,h) = cv2.boundingRect(c)  
        
        if(w < minWidth):
            digits.append(1)
            cv2.rectangle(output, (x,y), (x+w, y+h), (0,255,0), 1)
            # cv2.putText(output, str(digit), (x-10, y-10),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0), 2)
        else:
            roi = thresh[y:y + h, x:x + w]
            segments = _defineSegments(x,y,w,h,thresh)
            on = [0]*len(segments)
            
            for(i, ((x1,y1), (x2,y2))) in enumerate(segments):
                segROI = roi[y1:y2, x1:x2]
                total = cv2.countNonZero(segROI)
                area = (x2-x1)*(y2-y1)
                
                if(total / float(area) > 0.35):
                    on[i] = 1
                
            #Throws up an error when a bogus number is found.
            try:
                digit = DIGITS_LOOKUP[tuple(on)]
                digits.append(digit)
                cv2.rectangle(output, (x,y), (x+w, y+h), (0,255,0), 1)
                cv2.putText(output, str(digit), (x-10, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0), 2)
            except Exception:
                pass
            
    #Edge case for progress bar being read as a digit:
    if(len(digits) > 6):
        i = len(digits) - 6
        for x in range (i):
            digits.pop(0)
        if(debug):
            print("Removed leading digit")
    
    return digits
        
def _debugDigitBoundingBoxes(digitCnts,cropped):
    for c in digitCnts:
        im = cropped.copy()
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow("Show",im)
        cv2.waitKey()  
        cv2.destroyAllWindows()
      
def _defineSegments(x,y,w,h,thresh):
    roi = thresh[y:y+h,x:x+w]
    (roiH,roiW)=roi.shape
    (dW,dH)=(int(roiW*0.25),int(roiH*0.15))
    dHC = int(roiH*0.05)
    
    segments = [
        ((0, 0), (w, dH)),	# top
        ((0, 0), (dW, h // 2)),	# top-left
        ((w - dW, 0), (w, h // 2)),	# top-right
        ((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
        ((0, h // 2), (dW, h)),	# bottom-left
        ((w - dW, h // 2), (w, h)),	# bottom-right
        ((0, h - dH), (w, h))	# bottom
	]
    return segments
    
def _debugDigitContours(image,cnts):
    i = 0
    for c in cnts:
        (x,y,w,h) = cv2.boundingRect(c)
        print("i: " + str(i))
        print("Height: " + str(h))
        print("Width: " + str(w))
        i+=1
        temp = image.copy()
        cv2.drawContours(temp,[c],0,(0,255,0),2)
        cv2.imshow("Outline",temp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()