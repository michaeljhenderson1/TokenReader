import os, cv2, imutils, sys, getopt
from cropByParam import cropSection
from digitReading import getToken
from edgeUtils import cropImage

def main(argv):
    section = ''
    requestType = ''
    try:
        opts, args = getopt.getopt(argv,"hs:r:",["section=","request="])
    except getopt.GetoptError:
        print('cropByParam.py -s <section>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('cropByParam.py -s <section> -r <requestType>\nrequestType: im for image, tok for token code.')
            sys.exit()
        elif opt in ("-s", "--section"):
            section = arg
        elif opt in ("-r", "--request"):
            requestType = arg
    print('Section is', section)
   
    tokenImg = cropSection(section,debug=False)
    
    if(requestType == 'im')
        return tokenImg
    elif(requestType == 'tok')
        cropped = cropImage(tokenImg,debug=False)
        digits = getToken(tokenImg,debug=False)
        return digits
    else:
        print("Invalid request type")
   
if __name__ == "__main__":
    main(sys.argv[1:])