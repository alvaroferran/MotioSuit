#--------------------------------------------------------------
#--    MotioSuit
#--    IMU based motion capture suit
#--------------------------------------------------------------
#--    BQ
#--------------------------------------------------------------
#--    Created by 
#--        Alvaro Ferran (alvaroferran)
#--------------------------------------------------------------
#--    Released on January 2016
#--    under the GPL v2
#--------------------------------------------------------------

import bge
import math
from math import *
import mathutils
import time

import sys
#sys.path.append("/usr/lib/python3/dist-packages")
import serial
import glob

port=''.join(glob.glob("/dev/ttyACM*"))
#port=''.join(glob.glob("/dev/ttyUSB*"))
#port=''.join(glob.glob("/dev/rfcomm"))  
ser = serial.Serial(port,115200)
print("connected to: " + ser.portstr)

#Connect the suit first and after a ~second launch the script


# Get the whole bge scene
scene = bge.logic.getCurrentScene()
# Helper vars for convenience
source = scene.objects
# Get the whole Armature
main_arm = source.get('Armature')
ob = bge.logic.getCurrentController().owner


def updateAngles():
	ser.write("a".encode('UTF-8'))
	s=ser.readline()[:-3].decode('UTF-8') #delete ";\r\n"
	angles=[x.split(',') for x in s.split(';')]
	for i in range(len(angles)):
		angles[i] = [float(x) for x in angles[i]]


	trunk = mathutils.Quaternion((angles[4][0],angles[4][1],angles[4][2],angles[4][3]))
	correction = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0))
	trunk_out = correction*trunk

	upperLegR = mathutils.Quaternion((angles[5][0],angles[5][1],angles[5][2],angles[5][3]))
	correction = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0))
	upperLegR_out = correction*upperLegR

	lowerLegR = mathutils.Quaternion((angles[6][0],angles[6][1],angles[6][2],angles[6][3]))
	correction = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0))
	lowerLegR_out = correction*lowerLegR

	upperLegL = mathutils.Quaternion((angles[7][0],angles[7][1],angles[7][2],angles[7][3]))
	correction = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0))
	upperLegL_out = correction*upperLegL

	lowerLegL = mathutils.Quaternion((angles[8][0],angles[8][1],angles[8][2],angles[8][3]))
	correction = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(90.0))
	lowerLegL_out = correction*lowerLegL

	ob.channels['armR'].rotation_quaternion = mathutils.Vector([angles[0][0],angles[0][1],angles[0][2],angles[0][3]])
	ob.channels['forearmR'].rotation_quaternion = mathutils.Vector([angles[1][0],angles[1][1],angles[1][2],angles[1][3]])
	ob.channels['armL'].rotation_quaternion = mathutils.Vector([angles[2][0],angles[2][1],angles[2][2],angles[2][3]])
	ob.channels['forearmL'].rotation_quaternion = mathutils.Vector([angles[3][0],angles[3][1],angles[3][2],angles[3][3]])
	ob.channels['trunk'].rotation_quaternion = trunk_out
	ob.channels['upperLegR'].rotation_quaternion = upperLegR_out
	ob.channels['lowerLegR'].rotation_quaternion = lowerLegR_out
	ob.channels['upperLegL'].rotation_quaternion = upperLegL_out
	ob.channels['lowerLegL'].rotation_quaternion = lowerLegL_out

	ob.update()
	time.sleep(0.001)
