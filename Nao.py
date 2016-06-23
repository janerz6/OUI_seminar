from Sensors import Sensors
from time import sleep, clock

from math import pi

from lib.naoqi import ALProxy

import sys
import signal

import Config

def signal_handler(signal, frame):
  t.run = False
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


mp = ALProxy('ALMotion', Config.nao_ip_port[0], Config.nao_ip_port[1])
#mp = ALProxy('ALMotion', '127.0.0.1', 9559)

# Set stiffness
pNames = "Body"
pStiffnessLists = 0.8
pTimeLists = 1.0
mp.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


t = Sensors()
t.start()

sleep(1)

RSRollOmejitve = (-1.6494, -0.0087)
RSPitchOmejitve = (-2.0857, 2.0857)
RERollOmejitve = (0.0087, 1.5621)
REYawOmejitve = (-2.0857, 2.0857)
RWYawOmejitve = (-1.8238, 1.8238)

i = 0
startTime = clock()
naoControll = False

dataI = t.forearm.i

while True:
  # Nadaljuje samo takrat, ko so novi podatki
  if dataI == t.forearm.i:
    continue
  else:
    dataI = t.forearm.i
  #print dataI, i  
  i += 1
  
  #if i%2 != 0:
  #  continue

  # POPRAVEK SMERI NEBA glede na podlaket
  fM = t.forearm.M.fromEulerXYZ(0, 0, -Config.forearm_z+pi/2) * t.forearm.M
  uM = t.forearm.M.fromEulerXYZ(0, 0, -Config.forearm_z+pi/2) * t.upperarm.M

  # PRESLIKAVA IZ KOORDINAT SENZORJEV V NAO KOORDINATE in popravek glede na montazo senzorjev
  fM = fM * t.forearm.M.fromEulerZYX(-Config.forearm_x, -Config.forearm_y, -pi/2)
  uM = uM * t.upperarm.M.fromEulerZYX(-Config.upperarm_x, -Config.upperarm_y, -(Config.upperarm_z-Config.forearm_z)-pi/2)
  
  
  #
  # NAO ROTACIJE
  #
  
  # upper arm
  (naoXupperarm, naoYupperarm, naoZupperarm) = (0, 0, 0)
  (naoXupperarm, naoYupperarm, naoZupperarm) = uM.toEulerXZY()
  naoXupperarm = -naoXupperarm
  

  if naoZupperarm < RSRollOmejitve[0]:
    naoZupperarm = RSRollOmejitve[0]
    print i, "R Shoulder Roll - premalo"
  elif naoZupperarm > RSRollOmejitve[1]:
    naoZupperarm = RSRollOmejitve[1]
    print i, "R Shoulder Roll - preveliko"
    
  if naoXupperarm < RSPitchOmejitve[0]:
    naoXupperarm = RSPitchOmejitve[0]
    print i, "R Shoulder Pitch - premalo"
  elif naoXupperarm > RSPitchOmejitve[1]:
    naoXupperarm = RSPitchOmejitve[1]
    print i, "R Shoulder Pitch - preveliko"
  
  
  # forearm
  # INVERZ OBRATA V NADLAKETU
  forearmM = t.forearm.M.fromEulerYZX(naoXupperarm, 0, -naoZupperarm) * fM # *t.forearm.M
  ### OBRAT ZA -90 stopin okrog Z
  ### Nato dobis kote X Z Y (YZX) in Z-ju pristejes 90
  forearmM = forearmM * t.forearm.M.fromEulerYZX(0, 0, -pi/2)
  (naoYwrist, naoYforearm, naoZforearm) = forearmM.toEulerYZX()
  naoZforearm = naoZforearm + pi/2
  naoYwrist = -naoYwrist
  ###
  
  if naoZforearm < RERollOmejitve[0]:
    naoZforearm = RERollOmejitve[0]
    print i, "R Elbow Roll - premalo"
  elif naoZforearm > RERollOmejitve[1]:
    naoZforearm = RERollOmejitve[1]
    print i, "R Elbow Roll - preveliko"
    
  if naoYforearm < REYawOmejitve[0]:
    naoYforearm = REYawOmejitve[0]
    print i, "R Elbow Yaw - premalo"
  elif naoYforearm > REYawOmejitve[1]:
    naoYforearm = REYawOmejitve[1]
    print i, "R Elbow Yaw - preveliko"
  
  if naoYwrist < RWYawOmejitve[0]:
    naoYwrist = RWYawOmejitve[0]
    print i, "R Wrist Yaw - premalo"
  elif naoYwrist > RWYawOmejitve[1]:
    naoYwrist = RWYawOmejitve[1]
    print i, "R Wrist Yaw - preveliko"
    
  # hand
  if not t.hand:
    naoHand = 1
  else:
    naoHand = 0
  
  if naoControll:
    mp.setAngles(['RShoulderRoll', 'RShoulderPitch', 'RElbowRoll', 'RElbowYaw', 'RWristYaw', 'RHand'], [naoZupperarm, naoXupperarm, naoZforearm, naoYforearm, naoYwrist, naoHand], 1)
  else:
    naoControll = (clock()-startTime) > 3
  #sleep(0.5)
  
  
  
