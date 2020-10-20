import json
import pickle
import numpy
import pandas
from pandas import DataFrame
pandas.set_option('display.max_rows', 100)

epLat = 0.012160099999998054
epLng = 0.014610749999992125
epTime = 255

with open('trajTrain.pickle', 'rb') as f:
  trajTrainDict = pickle.load(f)
  trajTrain = trajTrainDict['trajTrain']
  trajTrainOri = trajTrainDict['trajTrainOri']
  mappingTrain = trajTrainDict['mappingTrain']

with open('trajTest.pickle', 'rb') as f:
    trajTrainDict = pickle.load(f)
    trajTest = trajTrainDict['trajTest']
    trajTestOri = trajTrainDict['trajTestOri']
    mappingTest = trajTrainDict['mappingTest']


def getOverlayOneCubeWithPointAmount(trajList1, trajList2, dtime, distX, distY, angDiffConst, pointAmountRatio=0):
    maxTime = trajList1[9] + dtime
    minTime = trajList1[9] - dtime
    trajList3 = trajList2.loc[(trajList2[9] > minTime) & (trajList2[9] < maxTime),]
    trajList4 = trajList3.loc[abs(trajList3[9] - trajList1[9]) < dtime,]
    trajList4 = trajList4.loc[abs(trajList4[3] - trajList1[3]) < distX,]
    trajList4 = trajList4.loc[abs(trajList4[4] - trajList1[4]) < distY,]
    trajList4 = trajList4.loc[angleDiff(trajList4[8], trajList1[8]) < angDiffConst,]
    while pointAmountRatio > 0:
      trajList5 = trajList4.loc[abs(trajList4[0] - trajList1[0]) < (trajList1[0] * (1 - pointAmountRatio)),]
      if trajList5.size > 0:
        trajList4 = trajList5
        break
      pointAmountRatio -= 0.1
    if trajList4.size <= 0:
      return None
    n1 = trajList4.shape[0]
    area1 = DataFrame(numpy.zeros((n1, 3), dtype=int))
    area1[0] = trajList4[5].values  # 其它軌
    area1[1] = trajList4[1].values  # 其它軌第幾cube
    area1[2] = trajList4.index.values  # 其它軌此cube在總名單上第幾
    return area1

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


def ignoreBeginOrLastOnePointCube(traj, trajOri, mapping):
  hist = numpy.bincount(mapping[4])
  hist2 = numpy.bincount(hist)
  ratioOfMostGap = 0.2
  lessGap = numpy.where((hist2.cumsum() / hist2.sum()) <= ratioOfMostGap)[0][-1]
  # get lessGap
  n = hist.__len__()
  indexTop = 0
  indexTop2 = 0
  for i in range(n):
    if hist[i] <= lessGap:
      indexTop += 1
      indexTop2 += 1
    else:
      break
  indexEnd = traj.shape[0] - 1
  indexEnd2 = trajOri.shape[0] - 1
  for i in range(n - 1, 0, -1):
    if hist[i] <= lessGap:
      indexEnd -= 1
      indexEnd2 -= 1
    else:
      break
  return (traj.iloc[indexTop:(indexEnd + 1), :].copy(), trajOri.iloc[indexTop2:(indexEnd2 + 1), :].copy())

from math import cos
from math import sin
from math import radians
from math import asin
import numpy

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

from dtw import accelerated_dtw

def getDTWeachRow(row,x,mappingTrain,trajTrainOri):
    tempTrajOriNo = mappingTrain.loc[
            (mappingTrain[2] == row[5]) &
            (mappingTrain[4] == row[1])
            ,3].to_list()
    y = trajTrainOri.loc[
            (trajTrainOri[5] == row[5]) &
            (trajTrainOri[1].isin( tempTrajOriNo ))
            ,[3,4]].to_numpy()
    d, cost_matrix, acc_cost_matrix, path = accelerated_dtw(x,y,getDistance)
    return d


def getTimeByMinDtw(targetNo,
                    area,
                    targetTrajOri,
                    targetMapping,
                    trajTrain,
                    trajTrainOri,
                    mappingTrain):
  trajTrainCubesIndex = area[2]

  targetTrajOriResetIndex = targetTrajOri.set_index(1)
  x = targetTrajOriResetIndex.loc[
    targetMapping.loc[targetMapping[4] == targetNo, 3],
    [3, 4]
  ].to_numpy()

  # result = []
  dfTrajNoWiCubeNo = trajTrain.loc[trajTrainCubesIndex, [5, 1]]
  n = dfTrajNoWiCubeNo.shape[0]
  result = dfTrajNoWiCubeNo.apply(getDTWeachRow, axis=1, args=(x, mappingTrain, trajTrainOri))
  minIndex = result.idxmin()
  minTrajTrain = trajTrain.loc[minIndex,]
  commonTime = trajTrain.loc[minIndex, 10] - trajTrain.loc[minIndex, 9]
  return (commonTime,minIndex)

def getTrainNext(trajTrain,minIndex):
  nextIndex = minIndex+1
  preIndex = minIndex-1



  if (nextIndex in trajTrain.index) & \
     (trajTrain.loc[minIndex,5] == trajTrain.loc[nextIndex,5]):
    nextPointTime = trajTrain.loc[nextIndex,9] - trajTrain.loc[minIndex,10]
  else:
    nextPointTime = -1

  if (preIndex in trajTrain.index) & \
     (trajTrain.loc[minIndex,5] == trajTrain.loc[preIndex,5]):
    prePointTime = trajTrain.loc[minIndex,9] - trajTrain.loc[preIndex,10]
  else:
    prePointTime = -1

  return (nextPointTime,prePointTime)

# 2020/06/23
import math


def getTestResult4OneTarget2(targetTrajNo,
                             trajTest,
                             trajTestOri,
                             mappingTest,
                             trajTrain,
                             trajTrainOri,
                             mappingTrain,
                             epLng, epLat):
  targetTraj = trajTest.loc[trajTest[5] == targetTrajNo,].copy()
  targetTrajOri = trajTestOri.loc[trajTestOri[5] == targetTrajNo,].copy()
  targetMapping = mappingTest.loc[mappingTest[2] == targetTrajNo,].copy()
  targetNew, targetOriNew = ignoreBeginOrLastOnePointCube(targetTraj, targetTrajOri, targetMapping)
  targetNew2 = targetNew.copy()
  realTime = targetNew.iloc[-1, 10] - targetNew.iloc[0, 9]
  realTime2 = realTime
  totalTime = 0
  n = targetNew.shape[0]
  commonTime = 0

  ratioOfMostGap = 0.9
  timeDiff = targetTrajOri[2].iloc[1:].to_numpy() - targetTrajOri[2].iloc[:-1].to_numpy()
  timeDiff = timeDiff.astype('int')
  timeDiff = numpy.sort(timeDiff)
  iarr = math.ceil(timeDiff.size * ratioOfMostGap)
  timeDiffTop = timeDiff[iarr] * 2

  tempExpResult = numpy.zeros((n, 3), dtype='int')
  tempExpResult[:, 0] = targetNew.iloc[:, 10] - targetNew.iloc[:, 9]
  listArea = []
  nextPointTime = 0
  prePointTime = 0
  preCubeTimeDiff = 0
  preNextPointTime = 0
  for i2 in range(n):
    # print(i2)

    if i2 > 0:
      targetNew.iloc[i2, 9] = targetNew.iloc[i2 - 1, 9] + commonTime
    area = getOverlayOneCubeWithPointAmount(targetNew.iloc[i2,],
                                            trajTrain,
                                            3600,
                                            epLng,
                                            epLat,
                                            10, 0.7)
    if area is None:
      print('ERROR: index=', i2, ' area is None')
      continue
    commonTime,minIndex = getTimeByMinDtw(targetNew.iloc[i2, 1],
                                 area,
                                 targetOriNew,
                                 targetMapping,
                                 trajTrain,
                                 trajTrainOri,
                                 mappingTrain)

    nextPointTime, prePointTime = getTrainNext(trajTrain, minIndex)
    if (preNextPointTime == -1) & (prePointTime > -1) & (preCubeTimeDiff < timeDiffTop):
      tempExpResult[i2-1, 2] += prePointTime
      totalTime += prePointTime
      targetNew.iloc[i2, 9] += prePointTime
    tempExpResult[i2, 1] = commonTime
    if i2 < (n - 1):
      cubeTimeDiff = targetNew2.iloc[i2 + 1, 9] - targetNew2.iloc[i2, 10]
      preCubeTimeDiff = cubeTimeDiff
      if cubeTimeDiff > timeDiffTop:
        realTime2 -= cubeTimeDiff
        nextPointTime = 0
      elif nextPointTime > -1:
        commonTime += nextPointTime
      #else:
      #  commonTime = getFullTime(commonTime, targetNew.iloc[i2,], targetNew.iloc[i2 + 1,])
    preNextPointTime = nextPointTime
    tempExpResult[i2, 2] = commonTime
    totalTime += commonTime
  return (totalTime, realTime, realTime2, tempExpResult)

def getFullTime(trajTrain,trajTrainOri,mappingTrain):
    dist = getDistance((cube1[11], cube1[13]),
                       (cube1[12], cube1[14]))
    dist2 = getDistance((cube1[11], cube1[13]),
                        (cube2[11], cube2[13]))
    return math.ceil(commonTime / dist * dist2)

targetTrajNo = 4
totalTime,realTime,realTime2,tempExpResult = \
    getTestResult4OneTarget2(targetTrajNo,
                            trajTest,
                            trajTestOri,
                            mappingTest,
                            trajTrain,
                            trajTrainOri,
                            mappingTrain,
                            epLng,epLat)