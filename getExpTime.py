import json
import pickle
import numpy
import pandas
from pandas import DataFrame

epLat = 0.012160099999998054
epLng = 0.014610749999992125

def getOverlayOneCube(trajList1,trajList2,dtime,distX,distY,angDiffConst):
	maxTime = trajList1[9] + dtime
	minTime = trajList1[9] - dtime
	trajList3 = trajList2.loc[(trajList2[9] > minTime) & (trajList2[9] < maxTime),]
	trajList4 = trajList3.loc[abs(trajList3[9] - trajList1[9]) < dtime,]
	trajList4 = trajList4.loc[abs(trajList4[3] - trajList1[3]) < distX,]
	trajList4 = trajList4.loc[abs(trajList4[4] - trajList1[4]) < distY,]
	trajList4 = trajList4.loc[angleDiff(trajList4[8],trajList1[8]) < angDiffConst,]
	n1 = trajList4.shape[0]
	area1 = DataFrame(numpy.zeros((n1,3), dtype=int))
	area1[0] = trajList4[5].values  #其它軌
	area1[1] = trajList4[1].values  #其它軌第幾cube
	area1[2] = trajList4.index.values  #其它軌此cube在總名單上第幾
	return area1

def angleDiff(a ,b):
	result = abs(a - b)
	result = result.values
	if len(a) > 1:
		index = result > 180
		result[index] = 360 - result[index]
	else:
		if result > 180:
			result = 360 - result
	return result

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


with open('trajTrain.pickle','rb') as f:
    trajTrainDict = pickle.load(f)
    trajTrain = trajTrainDict['trajTrain']
    trajTrainOri = trajTrainDict['trajTrainOri']
    
with open('trajTest.pickle','rb') as f:
    trajTrainDict = pickle.load(f)
    trajTest = trajTrainDict['trajTest']
    trajTestOri = trajTrainDict['trajTestOri']

startTestTraj = 12000    
intervalNum = 1000

trajNoList = numpy.unique(trajTest[5])
expResult = numpy.zeros((trajNoList.size+1,2),dtype='int') #expResult[0]無用
for targetTrajNo in trajNoList[startTestTraj:(startTestTraj+intervalNum)]:
    print(targetTrajNo)
    targetTraj = trajTest.loc[trajTest[5] == targetTrajNo,].copy()
    realTime = targetTraj.iloc[-1,10]-targetTraj.iloc[0,9]
    expResult[targetTrajNo,0] = realTime
    totalTime = 0
    n = targetTraj.shape[0]
    commonTime = 0
    for i2 in range(n):
        if i2 > 0:
            targetTraj.iloc[i2,9] = targetTraj.iloc[i2-1, 9] + commonTime
        area = getOverlayOneCube(targetTraj.iloc[i2,],
                                 trajTrain,
                                 3600,
                                 epLng,
                                 epLat,
                                 50)
        commonTime = getMaxGroup(trajTrain.loc[area[2],])
        totalTime += commonTime
    expResult[targetTrajNo,1] = totalTime

with open('expResult'+str(startTestTraj)+'-'+str(startTestTraj+intervalNum)+'.pickle','wb') as f:
	pickle.dump(expResult, f)











