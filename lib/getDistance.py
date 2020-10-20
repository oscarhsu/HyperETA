#get distance by chord fomula from GPS coordinate
#return in meter
from math import cos
from math import sin
from math import radians
from math import asin
import numpy
#from numpy import linalg as LA


def getDistance(Lat1,Long1,Lat2,Long2):
	deltaX = cos(radians(Lat2))*cos(radians(Long2)) \
			 - cos(radians(Lat1)) * cos(radians(Long1))
	deltaY = cos(radians(Lat2))*sin(radians(Long2)) \
			 - cos(radians(Lat1)) * sin(radians(Long1))
	deltaZ = sin(radians(Lat2)) - sin(radians(Lat1))
	C = numpy.linalg.norm(numpy.array([deltaX, deltaY, deltaZ]))
	deltaSigma = 2 * asin(C/2)
	d = round( 6371 * 1000 * deltaSigma )
	return d