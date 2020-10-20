from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def draw3Darrow(m1):
	fig = plt.figure()
	ax = plt.gca(projection='3d')
	ax.scatter(m1[3],m1[4], m1[2], c='r', marker='.')
	#ax.quiver(m1[11],m1[13],m1[9],m1[12]-m1[11],m1[14]-m1[13],m1[10]-m1[9],length=0.1,arrow_length_ratio=0.1)
	ax.set_xlabel('Longitude')
	ax.set_ylabel('Latitude')
	ax.set_zlabel('Time(s)')
	#plt.show()
