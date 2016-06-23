import time
from lib.naoqi import ALProxy

IP = "192.168.15.108"  # Replace here with your NaoQi's IP address.
PORT = 9559

# Create a proxy to ALFaceDetection
try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)
