import numpy as np
import pandas
from pandas import DataFrame
from .points2cubes import points2cubes

from os import listdir
from os.path import isfile, join

def getTraj( dictionary, distX, distY , distTime ,isTest = False):
	files = listdir(dictionary) # 取得所有檔案與子目錄名稱
	sorted(files)
	if isTest:
		# files = ['20081023124523.plt',
		# 				 '20081024000805.plt',
		# 				 '20081025010205.plt',
		# 				 '20081026024152.plt' ]
		files = files[:100]

	myMat = DataFrame()
	trajsOri = DataFrame()
	j = 0
	for f in files:
		if f[0] == '.':
			continue
		fullpath = join(dictionary, f) # 產生檔案的絕對路徑
		if isfile(fullpath): # 判斷 fullpath 是檔案還是資料夾
			print("檔案：", f)
			df = pandas.read_csv(fullpath,
						 header=None,
						 names=[1,2,3,4],
						 dtype={1:np.int, 2:np.int, 3:np.float, 4:np.float})
			if df.shape[0] <= 1:
				continue
			resultCheckOvernight = checkOvernight(df)
			if resultCheckOvernight == -1:
				continue
			elif resultCheckOvernight != None:
				df1 = df.iloc[:resultCheckOvernight,].copy()
				df1.insert(0, 0, 0)
				tempMat = points2cubes(df1, distX, distY, distTime)
				j = j + 1
				tempMat[5] = j  # add traj number
				df1[5] = j  # add traj number
				n2 = tempMat.shape[0]
				tempMat[1] = list(range(n2))
				myMat = myMat.append(tempMat, ignore_index=True)
				trajsOri = trajsOri.append(df1, ignore_index=True)
				df = df.iloc[resultCheckOvernight:,].reset_index(drop=True)
				df[1] = df.index.values
			df.insert(0,0,0)
			tempMat = points2cubes(df, distX, distY, distTime)
			j = j + 1
			tempMat[5] = j # add traj number
			df[5] = j # add traj number
			n2 = tempMat.shape[0]
			tempMat[1] = list(range(n2))
			myMat    = myMat.append(tempMat, ignore_index=True)
			trajsOri = trajsOri.append(df, ignore_index=True)
	myMat[1] = myMat[1].astype(dtype=np.int)
	myMat[6] = myMat[6].astype(dtype=np.int)
	myMat[7] = myMat[7].astype(dtype=np.int)
	return (myMat,trajsOri)


def checkOvernight(df):
	arr = df[2].to_numpy(dtype=np.int32)
	arr2 = arr[1:] - arr[:-1]
	whereTheValue = np.where(arr2 < 0)[0]
	lenWhereTheValue = whereTheValue.__len__()
	if lenWhereTheValue == 0:
		return None
	elif lenWhereTheValue == 1:
		return whereTheValue[0]+1 #第二天開始的位置
	else:
		return -1
