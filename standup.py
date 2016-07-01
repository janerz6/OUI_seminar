import sys
import time

from lib.naoqi import ALProxy
# import almath
import time

# from save_image import saveNaoImage

if(len(sys.argv) <= 1):
    print "Napacna uporaba skripte!\n uporaba: python standup.py <IP>"
    sys.exit()

IP = sys.argv[1]
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

mp.setAngles(['HeadPitch'], [-0.0], 1)

time.sleep(2)

tts = ALProxy("ALTextToSpeech", IP, 9559)
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
buffer = [("None", 0)] * length
personScoreDict = {}
personTimeDict = {}
treshhold = 2
treshTime = 4
#  1466703220.05

for i in range(0, 2000):
    time.sleep(0.2)
    val = memoryProxy.getData(memValue)

    print ""
    print "*****"
    print ""
    print i

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
                id = faceExtraInfo[0]

                print ("ID: " + str(id))
                print ("Natancnost: " + str(faceExtraInfo[1]))
                print ("Ime: " + name)
                print personScoreDict

                if personScoreDict.has_key(id) and id >= 0:
                    print "here ",
                    print faceExtraInfo[1]
                    personScoreDict[id] += faceExtraInfo[1]
                else:
                    personScoreDict[id] = faceExtraInfo[1]
                    print "zaznal"
                    personTimeDict[id] = 0

                # Make choice
                tmp = buffer.pop()
                personScoreDict[id] -= tmp[1]

                tmp = (id, faceExtraInfo[1])
                buffer.insert(0, tmp)

                tmpTime = time.time()


                if (id >= 0 and personScoreDict[id] > treshhold and abs(personTimeDict[id] - tmpTime) > treshTime):
                    tts.say("hello "+ str(name))
                    personTimeDict[id] = tmpTime
                    personScoreDict[id] = 0


        except Exception, e:
            print "faces detected, but it seems getData is invalid. ALValue ="
            print val
            print "Error msg %s" % (str(e))
    else:
        print "No face detected"
faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."
