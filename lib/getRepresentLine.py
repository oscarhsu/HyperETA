import numpy
from numpy import ones
from numpy import cos
from numpy import sin
from numpy import arctan2
from numpy import radians
from numpy import degrees
from pandas import DataFrame
import pandas
from scipy.sparse import coo_matrix

def getRepresentLine( area,trajHur ,perc):
	# Algorithm 3 common sub-trajectories clustering in paper.
	#   Input: area, cube-intersection information.
	#          trajHur, cubes.
	#          perc, p in paper.
	result = DataFrame()
	spRow = area[5].to_list() + area[6].to_list()
	spCol = area[6].to_list() + area[5].to_list()
	spData = area[3].to_list() + area[1].to_list()
	df = DataFrame({0:spRow,1:spData})
	df.drop_duplicates(inplace=True)
	sumSP = df[0].value_counts(sort=False).sort_index()
	#SP1 = coo_matrix((ones(df.shape[0]),(df[0],df[1])))
	#sumSP = SP1.sum(axis=1)
	m = sumSP.max()
	#icc = sumSP.argmax()
	icc = sumSP.idxmax()

	if perc >= 1:
		minIsec = 0
	else:
		minIsec = getPerc(sumSP,perc)

	SP = DataFrame({0:spRow, 1:spCol, 2:spData})
	SP.drop_duplicates(inplace=True)

	while m >= minIsec:
		spIccOne = (SP.loc[SP[0] == icc,])[1].to_list() #icc.cube的row，的col(交集cube index)
		a = trajHur.loc[spIccOne,]
		result = result.append(getOne(a), ignore_index=True)

		#把SP第一欄和第二欄，有spIccOne裡所列cube號碼的，列刪除
		SP.drop(SP.loc[ SP[1].isin( spIccOne) | SP[0].isin(spIccOne) ,: ].index, inplace=True)
		if SP.size == 0:
			break
		SP2 = SP.drop_duplicates(subset=[0,2])[0]
		sumSP2 = SP2.value_counts(sort=False).sort_index()
		m = sumSP2.max()
		icc = sumSP2.idxmax()
	return result

import matplotlib

def getPerc(coreCount, perc):
	m = coreCount.max()
	countHist = coreCount.value_counts(sort=False)
	countHist = countHist.sort_index()
	sumCount = countHist.sum()
	countHistCumsum = countHist.cumsum()
	perc2 = 1-perc
	sumCount2 = sumCount * perc2
	countHistCumsum2 = countHistCumsum.loc[countHistCumsum >= sumCount2]
	minIsec = countHistCumsum2.index[0]
	return minIsec


def getOne(trajHur):
	result = {0:0,
						1:trajHur[9].mean(),
						2:trajHur[3].mean(),
						3:trajHur[4].mean(),
						4:avgAngle(trajHur[8]),
						5:len(trajHur[8]),
						6:trajHur[10].mean()}
	return result


def avgAngle(angles):
	y = sin(radians(angles)).sum()
	x = cos(radians(angles)).sum()
	result = round(degrees(arctan2(y,x)))
	return result
