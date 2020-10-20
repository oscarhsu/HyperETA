import json
import pickle
import numpy
import pandas
from pandas import DataFrame
pandas.set_option('display.max_rows', 100)

import math
from math import cos
from math import sin
from math import radians
from math import asin

def getDistance(x,y):
	Long1,Lat1 = x
	Long2,Lat2 = y
	deltaX = cos(radians(Lat2))*cos(radians(Long2)) \
			 - cos(radians(Lat1)) * cos(radians(Long1))
	deltaY = cos(radians(Lat2))*sin(radians(Long2)) \
			 - cos(radians(Lat1)) * sin(radians(Long1))
	deltaZ = sin(radians(Lat2)) - sin(radians(Lat1))
	C = numpy.linalg.norm(numpy.array([deltaX, deltaY, deltaZ]))
	deltaSigma = 2 * asin(C/2)
	d = round( 6371 * 1000 * deltaSigma )
	return d


def ignoreBeginAndLastPoints(dist_gap):
	ratioOfMostGap = 0.2
	arrDist = numpy.array(dist_gap)
	arrDistGap = arrDist[1:]-arrDist[:-1]
	arrSortDistGap = numpy.sort(arrDistGap)
	iarr = math.ceil(arrDistGap.size * ratioOfMostGap)
	distDiffTop = arrSortDistGap[iarr]

	n = arrDistGap.size
	indexTop = 0
	for i in range(n):
		if arrDistGap[i] <= distDiffTop:
			print('ignore Begin Points found')
			indexTop += 1
		else:
			break
	indexEnd = n - 1
	for i in range(n-1, 0, -1):
		if arrDistGap[i] <= distDiffTop:
			print('ignore Last Points found')
			indexEnd -= 1
		else:
			break
	return (indexTop,indexEnd)



listJfTest = []
with open('data/TTE/test.json', 'r') as reader:
	for line in reader:
		jf = json.loads(line)
		n = len(jf['dist_gap'])
		(indexBegin,indexEnd) = ignoreBeginAndLastPoints(jf['dist_gap'])
		if indexBegin > 0:
			startValue = jf['dist_gap'][indexBegin]
			jf['dist_gap'] = numpy.array(jf['dist_gap'][indexBegin:(indexEnd+1)]) - startValue
			jf['dist_gap'] = jf['dist_gap'].tolist()
			startValue = jf['time_gap'][indexBegin]
			jf['time_gap'] = numpy.array(jf['time_gap'][indexBegin:(indexEnd+1)]) - startValue
			jf['time_gap'] = jf['time_gap'].tolist()
		else:
			jf['dist_gap'] = jf['dist_gap'][indexBegin:(indexEnd + 1)]
			jf['time_gap'] = jf['time_gap'][indexBegin:(indexEnd + 1)]
		jf['dist'] = jf['dist_gap'][-1]
		jf['time'] = jf['time_gap'][-1]
		jf['lats'] = jf['lats'][indexBegin:(indexEnd+1)]
		jf['states'] = jf['states'][indexBegin:(indexEnd+1)]
		jf['lngs'] = jf['lngs'][indexBegin:(indexEnd+1)]
		listJfTest.append(jf)

with open('data/TTE/testRemoveBeginLast', 'w') as writer:
	for x in listJfTest:
		line = json.dumps(x)
		print(line)
		writer.write(line+"\n")