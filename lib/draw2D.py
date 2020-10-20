from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def draw2D(m1):
	#m1：原始traj點
	plt.figure(1)
	# plt.clf()
	#
	# plt.title(thisTitle)
	plt.xlabel('Longitude')
	plt.ylabel('Latitude')
	plt.quiver(m1[11],m1[13],m1[12]-m1[11],m1[14]-m1[13])
	#
	# plt.plot(m1[3],m1[4],'.g')
	#
	#
	# plt.show()

	# fig = plt.figure()
	# ax = plt.gca(projection='3d')
	# ax.scatter(m1[3],m1[4], m1[2], c='r', marker='.')
	# ax.set_xlabel('X Label')
	# ax.set_ylabel('Y Label')
	# ax.set_zlabel('Z Label')
	# #plt.show()
