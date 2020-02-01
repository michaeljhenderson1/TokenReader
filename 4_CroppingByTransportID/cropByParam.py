import os, cv2, imutils, sys, getopt

def main(argv):
   selection = ''
   try:
      opts, args = getopt.getopt(argv,"hs:",["select="])
   except getopt.GetoptError:
      print('cropByParam.py -s <section>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('cropByParam.py -s <section>')
         sys.exit()
      elif opt in ("-s", "--select"):
         selection = arg
   print('Selection is', selection)
   
   if(isValidSelection(selection)):
       cropSection(int(selection))
   
def isValidSelection(selection,min=1,max=9):
    return _RepresentsInt(selection) and (int(selection) >= min and int(selection) <= max)
            
def _RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def cropSection(section):
    filename = "ttt.jpg"
    filePath = os.path.join(os.getcwd(),filename)

    im = cv2.imread(filePath)
    im = imutils.resize(im, height=500)
        
    Coords = {
        1: (0,0),
        2: (170,0),
        3: (350,0),
        4: (0,180),
        5: (170,180),
        6: (350,180),
        7: (0,360),
        8: (170,360),
        9: (350,360),
    }

    (x,y) = Coords[section]

    h = 150
    w = 140

    cropImg = im.copy()[y:y+h, x:x+w]
    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("Cropped",cropImg)
    cv2.imshow("BoundingBox",im)
    cv2.waitKey()  
    cv2.destroyAllWindows()

if __name__ == "__main__":
   main(sys.argv[1:])