from lib.naoqi import ALProxy
from random import randint
import sys

if(len(sys.argv) <= 1):
    print "Napacna uporaba skripte!\n uporaba: python learnFace.py <IP> <name>"
    sys.exit()

IP = sys.argv[1]
PORT = 9559

# Create a proxy to ALFaceDetection

try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

try:
    success = faceProxy.clearDatabase()
    if success:
        print "Successfully cleared DB"
    else:
        print "Error clearing db"
except Exception, e:
    print ("Napaka:" + str(e))
