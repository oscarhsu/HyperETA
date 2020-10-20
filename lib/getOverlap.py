import math
import numpy
from pandas import DataFrame

from .angleDiff import angleDiff

def getOverlap(trajList ,distX,distY ,dtime,angDiffConst,withSameTrack):
	# Algorithm 2 hypercubes-intersection in paper.
	#   input: trajList, cubes.
	#          distX, Epsilon_x in paper, longitude distance.
	#          distY, Epsilon_y in paper, latitude distance.
	#          dtime, Tau in paper, time distance.
	#          angDiffConst, Theta in paper, direction difference threshold.
	#          withSameTrack, if two intersecting hypercubes were from the same trajectory, is it count?
	AREA_COL = 7
	n = trajList.shape[0]
	totalArea = DataFrame()
	trajList[9] = list(range(n))
	nt = numpy.unique(trajList[5])
	for i in nt:
		t1 = trajList[5] == i
		if withSameTrack:
			area2 = getOverlaySameTrack(i,trajList.loc[t1,:],dtime,distX,distY,angDiffConst)
			nArea2 = area2.shape[0]
			if nArea2 > 0:
				totalArea = totalArea.append(area2)
		trajList2 = trajList.loc[trajList[5] != i,]
		area = getOverlayAreaTime(i,trajList.loc[t1,],trajList2,dtime,distX,distY,angDiffConst)
		if area.empty:
			trajList = trajList2
			continue
		nArea = area.shape[0]
		totalArea = totalArea.append(area)
		trajList = trajList2
	return totalArea



def getOverlaySameTrack(trajNo,trajList,dtime,distX,distY,angDiffConst):
	n = trajList.shape[0]
	if n <= 1:
		return None
	area = DataFrame()
	for i in range(n-1):
		if angleDiff( trajList.loc[i,8], trajList.loc[i+1,8]) < angDiffConst:
			area1 = DataFrame([[0, trajNo, trajList(i,1), trajNo, trajList(i+1,1), trajList(i,9 ), trajList(i+1,9)] \
												 [0, trajNo, trajList(i+1,1), trajNo, trajList(i,1), trajList(i+1,9), trajList(i,9)]])
			area = area.append(area1, ignore_index=True)
	return area


def getOverlayAreaTime(trajNo,trajList1,trajList2,dtime,distX,distY,angDiffConst):
	maxTime = trajList1[2].iloc[-1] + dtime
	minTime = trajList1[2].iloc[0] - dtime

	trajList3 = trajList2.loc[(trajList2[2] > minTime) & (trajList2[2] < maxTime),]
	n = trajList1.shape[0]
	area = DataFrame()
	for i in range(n):
		trajList4 = trajList3.loc[abs(trajList3[2] - trajList1.iloc[i,2]) < dtime,]
		trajList4 = trajList4.loc[abs(trajList4[3] - trajList1.iloc[i,3]) < distX,]
		trajList4 = trajList4.loc[abs(trajList4[4] - trajList1.iloc[i,4]) < distY,]
		trajList4 = trajList4.loc[angleDiff(trajList4[8],trajList1.iloc[i,8]) < angDiffConst,]
		n1 = trajList4.shape[0]
		area1 = DataFrame(numpy.zeros((n1,6+1), dtype=int))
		area1[1] = trajNo
		area1[2] = i                    #trajNo軌的第幾cube
		area1[3] = trajList4[5].values  #其它軌
		area1[4] = trajList4[1].values  #其它軌第幾cube
		area1[5] = trajList1.iloc[i, 9] #trajNo軌此cube在總名單上第幾
		area1[6] = trajList4[9].values  #其它軌此cube在總名單上第幾
		area = area.append(area1, ignore_index=True)
	return area


