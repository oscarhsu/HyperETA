import numpy
import pandas
from pandas import DataFrame
from .points2cubes import points2cubes

from os import listdir
from os.path import isfile, join

def getTraj2( aList, distX, distY , distTime ,isTest = False):
	myMat = DataFrame()
	mapping = DataFrame()
	trajsOri = DataFrame()
	j = 0
	for obj in aList:
			print("ID：", j)
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

