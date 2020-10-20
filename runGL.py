from lib.getTraj import getTraj
from lib.getOverlap import getOverlap

def runGL(angDiffConst = None,distX = None,distY = None,distTime = None,p = None):
	#Geolife user 3
	angDiffConst = 30 # Theta, direction difference 30 degree
	distX = 0.00117   # Epsilon_x, Long distance 100 meters
	distY = 0.0009    # Epsilon_y, Lat distance 100 meters
	distTime = 3600   # Tau, time difference 3600 seconds
	p = 0.1           # p
	is2Ddraw = True   # draw on 2D plot to clearly see arrow.

	dictionary = 'data/geolife/'

	traj,trajOri = getTraj( dictionary, distX, distY , distTime )
	areaHur = getOverlap( traj.copy(),distX,distY ,distTime,angDiffConst,False)
	return (traj, areaHur)
		# cubes = getRepresentLine2( areaHur,traj,p );
		# cubes = get2points(cubes,distX,distY);
		# if is2Ddraw
		# 		draw2D(cubes,trajOri,'Geolife user 3');
		# else
		# 		draw3D(cubes,trajOri,'Geolife user 3');
		#end
		#saveas(gcf, '../results/figGL.png')


if __name__ == '__main__':
	(traj, areaHur) = runGL(30,0.00117,0.0009,3600,0.1)