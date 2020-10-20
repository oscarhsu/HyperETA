import json
listJf = []
with open('data/TTE/test.json' , 'r') as reader:
	for line in reader:
		jf = json.loads(line)
		listJf.append(jf)
		#print(jf['driverID'])

from lib.draw2D import draw2D
#x = list(zip(listJf[0]['lngs'],listJf[0]['lats']))
draw2D([],(listJf[1]['lngs'],listJf[1]['lats']),'TTE')

import numpy
lats = []
for i in range(len(listJf)):
	temp = numpy.array(listJf[i]['lats'][1:]) - numpy.array(listJf[i]['lats'][:-1])
	lats += abs(temp).tolist()
hist = numpy.histogram(lats,bins=100)
ratioOfMostGap = 0.8
iarr = numpy.where((hist[0]. cumsum() / hist[0].sum())>ratioOfMostGap)[0][0]
mostLatGap = hist[1][iarr] #包含大部份的lats間隔值
epLat = mostLatGap * 10

aList = []
for i in range(len(listJf)):
	temp = numpy.array(listJf[i]['lngs'][1:]) - numpy.array(listJf[i]['lngs'][:-1])
	aList += abs(temp).tolist()
hist = numpy.histogram(aList,bins=100)
iarr = numpy.where((hist[0].cumsum() / hist[0].sum())>ratioOfMostGap)[0][0]
mostLngGap = hist[1][iarr] #包含大部份的lats間隔值
epLng = mostLngGap * 10

aList = []
for i in range(len(listJf)):
	temp = numpy.array(listJf[i]['time_gap'][1:]) - numpy.array(listJf[i]['time_gap'][:-1])
	aList += abs(temp).tolist()
hist = numpy.histogram(aList,bins=100)
iarr = numpy.where((hist[0].cumsum() / hist[0].sum())>ratioOfMostGap)[0][0]
mostTimeGap = hist[1][iarr] #包含大部份的lats間隔值
epTime = mostTimeGap * 10

