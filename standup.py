import sys
import time

from lib.naoqi import ALProxy
# import almath
import time

# from save_image import saveNaoImage

IP = '192.168.15.108'
PORT = 9559

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

time.sleep(1)

mp.setAngles(['HeadPitch'], [-0.35], 1)

time.sleep(2)

tts = ALProxy("ALTextToSpeech", "192.168.15.108", 9559)
# tts.say("i'll be back")

time.sleep(2)

# Sleep
# mp.rest()

# Watch for faces
try:
    faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
    print "Error when creating face detection proxy:"
    print str(e)
    exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 500
faceProxy.subscribe("Test_Face", period, 0.0)

memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
    memoryProxy = ALProxy("ALMemory", IP, PORT)
except Exception, e:
    print "Error when creating memory proxy:"
    print str(e)
    exit(1)

# A simple loop that reads the memValue and checks whether faces are detected.
length = 100
buffer = [("None",0)] * length
janezScore=0
jureScore=0
simonScore=0
treshhold = 2
simonTime = 0
janezTime = 0
jureTime = 0
treshTime=4
        #  1466703220.05

for i in range(0, 2000):
    time.sleep(0.2)
    val = memoryProxy.getData(memValue)

    print ""
    print "*****"
    print ""

    # Check whether we got a valid output.
    if (val and isinstance(val, list) and len(val) >= 2):

        # We detected faces !
        # For each face, we can read its shape info and ID.

        # First Field = TimeStamp.
        timeStamp = val[0]

        # Second Field = array of face_Info's.
        faceInfoArray = val[1]

        try:
            # Browse the faceInfoArray to get info on each detected face.
            for j in range(len(faceInfoArray) - 1):
                faceInfo = faceInfoArray[j]

                # First Field = Shape info.
                faceShapeInfo = faceInfo[0]

                # Second Field = Extra info (empty for now).
                faceExtraInfo = faceInfo[1]
                name = str(faceExtraInfo[2])
                print ("ID: " + str(faceExtraInfo[0]))
                print ("Natancnost: " + str(faceExtraInfo[1]))
                print ("Ime: " + name)

                # Make choice
                tmp = buffer.pop()
                if(str(tmp[0]).startswith("Simon")):
                    simonScore -= tmp[1]
                elif(str(tmp[0]).startswith("Janez")):
                    janezScore -= tmp[1]
                elif (str(tmp[0]).startswith("Jure")):
                    jureScore -= tmp[1]

                tmp = (name,faceExtraInfo[1])

                if (str(tmp[0]).startswith("Simon")):
                    simonScore += tmp[1]
                elif (str(tmp[0]).startswith("Janez")):
                    janezScore += tmp[1]
                elif (str(tmp[0]).startswith("Jure")):
                    jureScore += tmp[1]

                buffer.insert(0, tmp)

                tmpTime = time.time()
                print abs(janezTime-tmpTime)
                if(simonScore > treshhold and abs(simonTime-tmpTime) > treshTime):
                    tts.say("hello Simon")
                    buffer = [("None", 0)] * length
                    janezScore = 0
                    jureScore = 0
                    simonScore = 0
                    simonTime=tmpTime
                elif (janezScore > treshhold and abs(janezTime-tmpTime) > treshTime):
                    tts.say("hello iaanez")
                    buffer = [("None", 0)] * length
                    janezScore = 0
                    jureScore = 0
                    simonScore = 0
                    janezTime = tmpTime
                elif (jureScore > treshhold and abs(jureTime-tmpTime) > treshTime):
                    tts.say("hello Jure")
                    buffer = [("None", 0)] * length
                    janezScore = 0
                    jureScore = 0
                    simonScore = 0
                    jureTime=tmpTime


        except Exception, e:
            print "faces detected, but it seems getData is invalid. ALValue ="
            print val
            print "Error msg %s" % (str(e))
    else:
        print "No face detected"
faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."
