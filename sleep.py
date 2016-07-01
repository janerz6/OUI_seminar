import sys
import time

from lib.naoqi import ALProxy
# import almath
import time

# from save_image import saveNaoImage
if(len(sys.argv) <= 1):
    print "Napacna uporaba skripte!\n uporaba: python sleep.py <IP>"

IP = sys.argv[1]
PORT = 9559

# Create a proxy to ALMotion.
try:
    mp = ALProxy("ALMotion", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

mp.rest()
