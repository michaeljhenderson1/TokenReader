import os, cv2, imutils, sys, getopt
from cropByParam import cropSection
from digitReading import getDigits
from edgeUtils import cropScreen

minSection = 1
maxSection = 9

def getImg(section,debug=False):
    tokenImg = cropSection(section,minSection,maxSection,debug)
    screen = cropScreen(tokenImg,debug=False)
    return screen
    
def getCode(section,debug=False):
    screen = getImg(section,debug)
    digits = getDigits(screen,debug=False)
    return digits