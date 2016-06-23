import sys
import time

from lib.naoqi import ALProxy
import lib.almath
import time

IP = '192.168.15.108'
PORT = 9559  
 
# Create a proxy to ALMotion.
try:
	mp = ALProxy("ALMotion", IP, PORT)
except Exception,e:
	print "Could not create proxy to ALMotion"
	print "Error was: ",e

# Set stiffness on.
mp.stiffnessInterpolation("Body", 1, 0.5)

# Stand up.
mp.moveInit()

time.sleep(1)

mp.setAngles(['HeadPitch'],[-0.1],1)

time.sleep(2)

tts = ALProxy("ALTextToSpeech", "192.168.15.108",9559)
tts.say("i'll be back")
