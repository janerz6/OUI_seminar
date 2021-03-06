from lib.naoqi import ALProxy
from random import randint
import sys

if(len(sys.argv) <= 2):
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

# Create a proxy to ALMotion.
try:
    mp = ALProxy("ALMotion", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

# Set stiffness on
mp.stiffnessInterpolation("Body", 1, 0.5)

# Stand up
mp.moveInit()
name = sys.argv[2]
#randNum = randint(10000000,99999999)
try:
    faceProxy.learnFace(name)
    print "Successfully learned " + str(name)
except Exception, e:
    print ("Napaka:" + str(e))
