from lib.getTraj import getTraj
from lib.getOverlap import getOverlap
from lib.getRepresentLine import getRepresentLine
from lib.get2points import get2points
from lib.draw2D import draw2D
from lib.getTraj2 import getTraj2

angDiffConst = 30  # Theta, direction difference 30 degree
distX = 0.00117  # Epsilon_x, Long distance 100 meters
distY = 0.0009  # Epsilon_y, Lat distance 100 meters
distTime = 3600  # Tau, time difference 3600 seconds
p = 0.1  # p
is2Ddraw = True  # draw on 2D plot to clearly see arrow.

dictionary = 'data/geolife/'

#traj, trajOri = getTraj(dictionary, distX, distY, distTime, isTest=True)
traj, trajOri = getTraj(dictionary, distX, distY, distTime, isTest=False)
#areaHur = getOverlap(traj.copy(), distX, distY, distTime, angDiffConst, False)
#cubes = getRepresentLine( areaHur,traj,p )
#get2points(cubes,distX,distY)
#draw2D(cubes,trajOri,'Geolife user 3')

#import pandas
#areaHurMLab = pandas.read_csv('areaHur.csv',header=None)
#trajMLab = pandas.read_csv('traj.csv',header=None)


myDict = {'area':area,'listJf':listJf, 'epLat':epLat, 'epLng':epLng,'epTime':epTime,
					'hist':hist, 'mostLatGap':mostLatGap,'mostLngGap':mostLngGap,
					'mostTimeGap':mostTimeGap,'trajList':trajList,'trajList2':trajList2,
					'trajOri':trajOri}

#
import pickle
with open('myDict.pickle','wb') as f:
	pickle.dump(myDict, f)

import pickle
with open('myDict.pickle','rb') as f:
	myDict = pickle.load(f)
#
[print('%s = myDict[\'%s\']'% (x,x) ) for x in myDict.keys()]
area = myDict['area']
listJf = myDict['listJf']
epLat = myDict['epLat']
epLng = myDict['epLng']
epTime = myDict['epTime']
hist = myDict['hist']
mostLatGap = myDict['mostLatGap']
mostLngGap = myDict['mostLngGap']
mostTimeGap = myDict['mostTimeGap']
trajList = myDict['trajList']
trajList2 = myDict['trajList2']
trajOri = myDict['trajOri']
# area.loc[area[5]==122,6]

trajList2 = traj.copy()
n = trajList2.shape[0]
trajList2[9] = list(range(n))
i = 60
from lib.getOverlap2 import getOverlayAreaTime

# area = getOverlayAreaTime(i,
# 													trajList2.loc[trajList2[5] == i,],
# 													trajList2.loc[trajList2[5] != i,],
# 													1000,
# 													epLng,
# 													epLat,
# 													50)

##################################################################
import numpy
import lib.getOverlap2
def getMaxGroup(trajList):
	aList = trajList[10] - trajList[9]
	arr = numpy.array(aList)
	result = numpy.zeros(arr.size)
	n = arr.size
	ratio = n // 2
	for i in range(n):
		x1 = abs(arr - arr[i])
		x2 = numpy.sort(x1)
		result[i] = sum(x2[:ratio])
	minLoc = numpy.where(result == numpy.amin(result))
	if minLoc[0][0] >= 0:
		return arr[minLoc[0][0]]
	else:
		raise Exception('ERROR: getMaxGroup: minLoc[0][0] = %i < 0' % minLoc[0][0])


targetTrajNo = 60
targetTraj = trajList.loc[trajList[5] == targetTrajNo,]

totalTime = 0
n = targetTraj.shape[0]
commonTime = 0
for i2 in range(n):
	cube = targetTraj.iloc[i2,]
	if i2 > 0:
		cube[9] = targetTraj.iloc[i2-1, 9] + commonTime
	area = lib.getOverlap2.getOverlayOneCube(cube,
													trajList2.loc[trajList2[5] != targetTrajNo,],
													1000,
													epLng,
													epLat,50)
	commonTime = getMaxGroup(trajList.loc[area[2],])
	totalTime += commonTime

##################################################################

#area[2]
#delta = trajList.loc[area[2],10]-trajList.loc[area[2],9]
#commonTimeIndex = getMaxGroup(delta)
#commonTime = getMaxGroup(trajList.loc[area[2],] )
#totalTime += delta[commonTime]
#totalTime += commonTime
#i2=1
#cube = targetTraj.iloc[i2+1,]
#cube[2] = targetTraj.iloc[i2,2]+commonTime

area = lib.getOverlap2.getOverlayOneCube(cube,
													trajList2.loc[trajList2[5] != 60,],
													1000,
													epLng,
													epLat,50)
x = area.loc[area[5]==122,2]



import importlib
importlib.reload(lib.getOverlap2)
