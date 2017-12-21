import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from opensimplex import OpenSimplex


class Terrain(object):
	def __init__(self):	
		self.app = QtGui.QApplication([])
		self.window = gl.GLViewWidget()	
		self.window.resize(1000,600)
		self.window.setWindowTitle("Terrain")
		self.window.setCameraPosition(distance=30, elevation=8)
		
		grid = gl.GLGridItem()
		grid.scale(2,2,2)
		self.window.addItem(grid)
		
		self.window.show()

		self.numSteps = 1 # distance between each vertex
		self.ypoints = range(-20, 22, self.numSteps)
		self.xpoints = range(-20, 22, self.numSteps)
		self.numFaces = len(self.ypoints)

		vertices = np.array([
				[ x, y, 0 ]
				for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
		], dtype=np.float32)
		
		

	def start(self):
		if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
			QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
	t = Terrain()
	t.start()
