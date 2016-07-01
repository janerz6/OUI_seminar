from lib.naoqi import ALProxy
from random import randint
import sys

IP = "192.168.15.108"  # Replace here with your NaoQi's IP address.
PORT = 9559

# Create a proxy to ALFaceDetection

try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

if(len(sys.argv) <= 1):
    print "Napacna uporaba skripte!\n uporaba: python learnFace.py <ime>"

name = sys.argv[1]
#randNum = randint(10000000,99999999)
try:
    faceProxy.learnFace(name)
    print "Successfully learned" + str(name)
except Exception, e:
    print ("Napaka:" + str(e))


# print "Vnesite zeljeni ukaz. Seznam ukazov.learn <name>"
# while True:
#     print "-->",
#     try:
#         line = sys.stdin.readline()
#     except KeyboardInterrupt:
#         break
#
#     print line,
