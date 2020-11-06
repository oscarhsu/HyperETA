import json
import numpy
from lib import getTraj

class trajModel:
	listJf = None
	ratioOfMostGap = 0.8
	multiplier = 5
	epLat = None
	epLng = None
	epTime = None
	traj = None
	trajOri = None
	mapping = None

	def __init__(self,config):
		ratioOfMostGap = config['ratioOfMostGap']
		multiplier = config['multiplier']

	def inputTraj(self,filename):
		listJf = []
		with open(filename, 'r') as reader:
				for line in reader:
					jf = json.loads(line)
					listJf.append(jf)
		if (self.epLat == None) | (self.epLng == None) | (self.epTime == None):
			self.getEpslon(listJf)
		print('Transform trajectories into hypercubes....')
		traj, trajOri, mapping = getTraj(listJf, self.epLng, self.epLat, self.epTime)
		print('Finished')
		trajOri = self.getPostTime(trajOri, listJf)
		self.traj = traj
		self.trajOri = trajOri
		self.mapping = mapping
		self.listJf = listJf

	def getPostTime(self,trajTrainOri,listJf):
			trajTrainOri['TrackNo'] = 0
			trajTrainOri['preDist'] = 0
			trajTrainOri['postDist'] = 0
			trajTrainOri['preTime'] = 0
			trajTrainOri['postTime'] = 0
			indexTop = 0
			indexEnd = 0
			TrackNo = 0
			jf = None
			for jf in listJf:
				TrackNo += 1
				lenDistGap = len(jf['dist_gap'])
				indexEnd = indexTop + lenDistGap - 1
				arrDistGap = numpy.array(jf['dist_gap'])
				arrTimeGap = numpy.array(jf['time_gap'])
				result = arrDistGap[1:] - arrDistGap[:-1]
				resultTime = arrTimeGap[1:] - arrTimeGap[:-1]
				trajTrainOri.loc[indexTop:indexEnd, 'TrackNo'] = TrackNo
				trajTrainOri.loc[(indexTop + 1):indexEnd, 'preDist'] = result
				trajTrainOri.loc[indexTop:(indexEnd - 1), 'postDist'] = result
				trajTrainOri.loc[(indexTop + 1):indexEnd, 'preTime'] = resultTime
				trajTrainOri.loc[indexTop:(indexEnd - 1), 'postTime'] = resultTime
				indexTop += lenDistGap
			return trajTrainOri

	def getEpslon(self,listJf):
		mostLatsGap = self.getAvgGap(listJf, 'lats', self.ratioOfMostGap)
		self.epLat = mostLatsGap * self.multiplier
		mostLngsGap = self.getAvgGap(listJf, 'lngs', self.ratioOfMostGap)
		self.epLng = mostLngsGap * self.multiplier
		mostTimeGap = self.getAvgGap(listJf, 'time_gap', self.ratioOfMostGap)
		self.epTime = mostTimeGap * self.multiplier

	def getAvgGap(self,listJf,colName,ratioOfMostGap):
		lats = []
		for i in range(len(listJf)):
			temp = numpy.array(listJf[i][colName][1:]) - numpy.array(listJf[i][colName][:-1])
			lats += abs(temp).tolist()
		hist = numpy.histogram(lats,bins=100)
		iarr = numpy.where((hist[0].cumsum() / hist[0].sum())>ratioOfMostGap)[0][0]
		mostLatGap = hist[1][iarr] #包含大部份的lats間隔值
		return mostLatGap

if __name__ == '__main__':
	listFileName = ['data/TTE/train_00','data/TTE/train_01','data/TTE/train_02','data/TTE/train_03','data/TTE/train_04']
	oTrajModel = trajModel()
	oTrajModel.inputTraj(listFileName)
