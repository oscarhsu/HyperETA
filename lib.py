# TODO: getTraj() use apply

import numpy
import pandas
from pandas import DataFrame

import math
from math import cos
from math import sin
from math import radians
from math import asin

from dtw import accelerated_dtw


LongColNum = 3
LatColNum = 4
TimeColNum = 2

def getTraj( aList, distX, distY , distTime ,isTest = False):
	myMat = DataFrame()
	mapping = DataFrame()
	trajsOri = DataFrame()
	j = 0
	for obj in aList:
			#print("ID：", j)
			#obj['lats']
			#obj['lngs']
			times = numpy.array(obj['time_gap']) + obj['time']
			idList = list(range(len(obj['lats'])))
			df = DataFrame({1:idList, 2:times,3:obj['lngs'],4:obj['lats']})
			#,dtype={1:numpy.int, 2:numpy.int, 3:numpy.float, 4:numpy.float}
			df.insert(0,0,0)
			tempMat,tempMapping = points2cubes(df, distX, distY, distTime)
			j = j + 1
			tempMat[5] = j # add traj number
			tempMapping[2] = j
			df[5] = j # add traj number
			n2 = tempMat.shape[0]
			tempMat[1] = list(range(n2))
			myMat    = myMat.append(tempMat, ignore_index=True)
			mapping = mapping.append(tempMapping, ignore_index=True)
			trajsOri = trajsOri.append(df, ignore_index=True)
	myMat[1] = myMat[1].astype(dtype=numpy.int)
	myMat[2] = myMat[2].astype(dtype=numpy.int)
	myMat[6] = myMat[6].astype(dtype=numpy.int)
	myMat[7] = myMat[7].astype(dtype=numpy.int)
	myMat[9] = myMat[9].astype(dtype=numpy.int)
	myMat[10] = myMat[10].astype(dtype=numpy.int)
	return (myMat,trajsOri,mapping)



def getDegree(p1, p2):
	a = getDistance(p1[LatColNum],
									p2[LongColNum],
									p1[LatColNum],
									p1[LongColNum])
	if (p2[LongColNum] - p1[LongColNum]) < 0:
		a = - a

	b = getDistance(p2[LatColNum],
									p1[LongColNum],
									p1[LatColNum],
									p1[LongColNum])
	if (p2[LatColNum] - p1[LatColNum]) < 0:
		b = - b

	result = round(math.degrees(math.atan2(b, a)))
	return result

def points2cubes(myMat, distX, distY, distTime):
    # Algorithm 1 preprocessing in paper
    #   input: myMat, points sequence of a trajectory.
    #          distX, Epsilon_x in paper, longitude distance.
    #          distY, Epsilon_y in paper, latitude distance.
    #          distTime, Tau in paper, time distance.

    firstIndex = 0

    indexTop = firstIndex # orgi 1
    myStart = firstIndex  # origi 1

    n,c = myMat.shape

    indexLastRow = n - 1

    myMat2ColAmount = 14+1 #there is 0 index column
    mappingColAmount = 4+1 #there is 0 index column

    myMat2 = pandas.DataFrame(numpy.zeros((n,myMat2ColAmount),dtype=numpy.int))
    mapping = pandas.DataFrame(numpy.zeros((n, mappingColAmount),dtype=numpy.int))

    mapping.iloc[:,3] = list(range(firstIndex,n))
    mapping.iloc[firstIndex, 4] = indexTop

    minX = myMat.iloc[myStart, LongColNum]
    maxX = myMat.iloc[myStart, LongColNum]
    minY = myMat.iloc[myStart, LatColNum]
    maxY = myMat.iloc[myStart, LatColNum]
    minTime = myMat.iloc[myStart, TimeColNum]
    maxTime = myMat.iloc[myStart, TimeColNum]
    newMinX = minX
    newMaxX = maxX
    newMinY = minY
    newMaxY = maxY
    newMinTime = minTime
    newMaxTime = maxTime

    for i in range(firstIndex+1,n): #origi 2,n ，matlab是2,3,...,n，python是1,....,n-1
        #if i > 1000:
        #    print(i)
        flag = 1
        if (myMat.iloc[i, TimeColNum] - myMat.iloc[myStart, TimeColNum]) > distTime :
            flag = 0

        if flag:
            if myMat.iloc[i, LongColNum] > maxX:
                if (myMat.iloc[i, LongColNum] - minX) < distX :
                    newMaxX = myMat.iloc[i, LongColNum]
                else:
                    flag = 0
            elif myMat.iloc[i, LongColNum] < minX:
                if (maxX - myMat.iloc[i, LongColNum]) < distX :
                    newMinX = myMat.iloc[i, LongColNum]
                else:
                    flag = 0

        if flag:
             if myMat.iloc[i, LatColNum] > maxY :
                if (myMat.iloc[i, LatColNum] - minY) < distY:
                    newMaxY = myMat.iloc[i, LatColNum]
                else:
                    flag = 0
             elif myMat.iloc[i, LatColNum] < minY:
                 if (maxY - myMat.iloc[i, LatColNum]) < distY:
                     newMinY = myMat.iloc[i, LatColNum]
                 else:
                     flag = 0

        if flag:
             minX = newMinX
             maxX = newMaxX
             minY = newMinY
             maxY = newMaxY
             mapping.iloc[i,4] = indexTop
        else:
            myEnd = i - 1
            if myEnd == myStart:
                if myStart == firstIndex:
                    myEnd = firstIndex+1
                elif myStart < indexLastRow:
                    myEnd = i
            myMat2.iloc[indexTop, 0] = myEnd - myStart + 1
            myMat2.iloc[indexTop, 9] = myMat.iloc[myStart, 2]
            myMat2.iloc[indexTop, 10] = myMat.iloc[myEnd, 2]
            myMat2.iloc[indexTop, 11] = myMat.iloc[myStart, 3]
            myMat2.iloc[indexTop, 12] = myMat.iloc[myEnd, 3]
            myMat2.iloc[indexTop, 13] = myMat.iloc[myStart, 4]
            myMat2.iloc[indexTop, 14] = myMat.iloc[myEnd, 4]

            myMat2.iloc[indexTop, TimeColNum] = (myMat2.iloc[indexTop, 9] + myMat2.iloc[indexTop, 10]) // 2
            myMat2.iloc[indexTop, LongColNum] = (minX + maxX) / 2
            myMat2.iloc[indexTop, LatColNum] = (minY + maxY) / 2

            myMat2.iloc[indexTop, 6] = getDistance(myMat.iloc[myStart, LatColNum],
                                                  myMat.iloc[myEnd, LongColNum],
                                                  myMat.iloc[myStart, LatColNum],
                                                  myMat.iloc[myStart, LongColNum])
            if (myMat.iloc[myEnd, LongColNum] - myMat.iloc[myStart, LongColNum]) < 0:
                myMat2.iloc[indexTop, 6] = - myMat2.iloc[indexTop, 6]

            myMat2.iloc[indexTop, 7] = getDistance(myMat.iloc[myEnd, LatColNum],
                                                  myMat.iloc[myStart, LongColNum],
                                                  myMat.iloc[myStart, LatColNum],
                                                  myMat.iloc[myStart, LongColNum])
            if (myMat.iloc[myEnd, LatColNum] - myMat.iloc[myStart, LatColNum]) < 0:
                myMat2.iloc[indexTop, 7] = - myMat2.iloc[indexTop, 7]

            myMat2.iloc[indexTop, 8] = \
                round(math.degrees(math.atan2(myMat2.iloc[indexTop, 7],
                                              myMat2.iloc[indexTop, 6])))
            minX = myMat.iloc[i, LongColNum]
            maxX = myMat.iloc[i, LongColNum]
            minY = myMat.iloc[i, LatColNum]
            maxY = myMat.iloc[i, LatColNum]
            minTime = myMat.iloc[i, TimeColNum]
            maxTime = myMat.iloc[i, TimeColNum]
            newMinX = minX
            newMaxX = maxX
            newMinY = minY
            newMaxY = maxY
            indexTop = indexTop + 1
            mapping.iloc[i, 4] = indexTop
            myStart = i

    if (indexLastRow == myStart) and (myStart > firstIndex):
         myEnd = indexLastRow
         myStart = indexLastRow-1
    else:
         myEnd = indexLastRow

    myMat2.iloc[indexTop, 6] = getDistance(myMat.iloc[myStart, LatColNum],
																								myMat.iloc[myEnd, LongColNum],
																								myMat.iloc[myStart, LatColNum],
																								myMat.iloc[myStart, LongColNum])
    if (myMat.iloc[myEnd, LongColNum] - myMat.iloc[myStart, LongColNum]) < 0:
      myMat2.iloc[indexTop, 6] = - myMat2.iloc[indexTop, 6]

    myMat2.iloc[indexTop, 7] = getDistance(myMat.iloc[myEnd, LatColNum],
																								myMat.iloc[myStart, LongColNum],
																								myMat.iloc[myStart, LatColNum],
																								myMat.iloc[myStart, LongColNum])
    if (myMat.iloc[myEnd, LatColNum] - myMat.iloc[myStart, LatColNum]) < 0:
      myMat2.iloc[indexTop, 7] = - myMat2.iloc[indexTop, 7]

    #myMat2.iloc[indexTop, 6] = myMat.iloc[myEnd, LongColNum] - myMat.iloc[myStart, LongColNum]
    #myMat2.iloc[indexTop, 7] = myMat.iloc[myEnd, LatColNum] - myMat.iloc[myStart, LatColNum]
    myMat2.iloc[indexTop, 8] = round(math.degrees(math.atan2(myMat2.iloc[indexTop, 7], myMat2.iloc[indexTop, 6])))

    myMat2.iloc[indexTop, 9] = myMat.iloc[myStart, 2]
    myMat2.iloc[indexTop, 10] = myMat.iloc[myEnd, 2]
    myMat2.iloc[indexTop, 11] = myMat.iloc[myStart, 3]
    myMat2.iloc[indexTop, 12] = myMat.iloc[myEnd, 3]
    myMat2.iloc[indexTop, 13] = myMat.iloc[myStart, 4]
    myMat2.iloc[indexTop, 14] = myMat.iloc[myEnd, 4]

    myMat2.iloc[indexTop, 2] = (myMat2.iloc[indexTop, 9] + myMat2.iloc[indexTop, 10]) // 2

    myMat2.iloc[indexTop, 3] = (minX + maxX) / 2
    myMat2.iloc[indexTop, 4] = (minY + maxY) / 2
    myMat2.iloc[indexTop, 0] = myEnd - myStart + 1
    resultMat = myMat2.iloc[:(indexTop+1), :]

    return (resultMat,mapping)

#get distance by chord fomula from GPS coordinate
#return in meter
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

