from numpy import radians
from numpy import tan

def get2points( cubes, distX, distY ):
	distX = distX / 2
	distY = distY / 2
	n,c = cubes.shape
	cubes[c] = 0
	cubes[c+1] = 0
	cubes[c+2] = 0
	cubes[c+3] = 0
	for i in range(n):
		p = [0, 0, 0, 0, 0]
		if cubes.iloc[i,4] == 0:
			p[1] = cubes.iloc[i,2] - distX
			p[2] = cubes.iloc[i,3]
			p[3] = cubes.iloc[i,2] + distX
			p[4] = cubes.iloc[i,3]
		elif (45 > cubes.iloc[i,4]) and (cubes.iloc[i,4] > 0):
			d = distX * tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] - distX
			p[2] = cubes.iloc[i,3] - d
			p[3] = cubes.iloc[i,2] + distX
			p[4] = cubes.iloc[i,3] + d
		elif cubes.iloc[i,4] == 45:
			p[1] = cubes.iloc[i,2] - distX
			p[2] = cubes.iloc[i,3] - distY
			p[3] = cubes.iloc[i,2] + distX
			p[4] = cubes.iloc[i,3] + distY
		elif 90 > cubes.iloc[i,4] and cubes.iloc[i,4] > 45:
			d = distY / tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] - d
			p[2] = cubes.iloc[i,3] - distY
			p[3] = cubes.iloc[i,2] + d
			p[4] = cubes.iloc[i,3] + distY
		elif cubes.iloc[i,4] == 90:
			p[1] = cubes.iloc[i,2]
			p[2] = cubes.iloc[i,3] - distY
			p[3] = cubes.iloc[i,2]
			p[4] = cubes.iloc[i,3] + distY
		elif 135 > cubes.iloc[i,4] and cubes.iloc[i,4] > 90:
			d = distY / tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] - d
			p[2] = cubes.iloc[i,3] - distY
			p[3] = cubes.iloc[i,2] + d
			p[4] = cubes.iloc[i,3] + distY
		elif cubes.iloc[i,4] == 135 :
			p[1] = cubes.iloc[i,2] + distX
			p[2] = cubes.iloc[i,3] - distY
			p[3] = cubes.iloc[i,2] - distX
			p[4] = cubes.iloc[i,3] + distY
		elif 180 > cubes.iloc[i,4] and cubes.iloc[i,4] > 135:
			d = distX * tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] + distX
			p[2] = cubes.iloc[i,3] + d
			p[3] = cubes.iloc[i,2] - distX
			p[4] = cubes.iloc[i,3] - d
		elif cubes.iloc[i,4] == 180 or cubes.iloc[i,4] == -180:
			p[1] = cubes.iloc[i,2] + distX
			p[2] = cubes.iloc[i,3]
			p[3] = cubes.iloc[i,2] - distX
			p[4] = cubes.iloc[i,3]
		elif -135 > cubes.iloc[i,4] and cubes.iloc[i,4] > -180:
			d = distX * tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] + distX
			p[2] = cubes.iloc[i,3] + d
			p[3] = cubes.iloc[i,2] - distX
			p[4] = cubes.iloc[i,3] - d
		elif cubes.iloc[i,4] == -135:
			p[1] = cubes.iloc[i,2] + distX
			p[2] = cubes.iloc[i,3] + distY
			p[3] = cubes.iloc[i,2] - distX
			p[4] = cubes.iloc[i,3] - distY
		elif -90 > cubes.iloc[i,4] and cubes.iloc[i,4] > -135:
			d = distY / tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] + d
			p[2] = cubes.iloc[i,3] + distY
			p[3] = cubes.iloc[i,2] - d
			p[4] = cubes.iloc[i,3] - distY
		elif cubes.iloc[i,4] == -90:
			p[1] = cubes.iloc[i,2]
			p[2] = cubes.iloc[i,3] + distY
			p[3] = cubes.iloc[i,2]
			p[4] = cubes.iloc[i,3] - distY
		elif -45 > cubes.iloc[i,4] and cubes.iloc[i,4] > -90:
			d = distY / tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] + d
			p[2] = cubes.iloc[i,3] + distY
			p[3] = cubes.iloc[i,2] - d
			p[4] = cubes.iloc[i,3] - distY
		elif cubes.iloc[i,4] == -45:
			p[1] = cubes.iloc[i,2] - distX
			p[2] = cubes.iloc[i,3] + distY
			p[3] = cubes.iloc[i,2] + distX
			p[4] = cubes.iloc[i,3] - distY
		elif 0 > cubes.iloc[i,4] and cubes.iloc[i,4] > -45:
			d = distX * tan(radians(cubes.iloc[i,4]))
			p[1] = cubes.iloc[i,2] - distX
			p[2] = cubes.iloc[i,3] - d
			p[3] = cubes.iloc[i,2] + distX
			p[4] = cubes.iloc[i,3] + d
		else:
			print('ERROR')
			continue
		cubes.iloc[i,7:11] = p[1:]
	#return cubes

