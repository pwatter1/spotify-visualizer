import struct
import pyaudio
import sys
import numpy as np
from opensimplex import OpenSimplex
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui


class Terrain(object):

    def __init__(self):
        # setup the view window
        self.app = QtGui.QApplication(sys.argv)
        self.window = gl.GLViewWidget()
        self.window.setWindowTitle('Spotify Visualizer')
        self.window.setGeometry(0, 110, 1920, 1080)
        self.window.resize(1000, 600)
        self.window.setCameraPosition(distance=60, elevation=12)
        self.window.show()

        # constants/arrays
        self.nsteps = 1.3
        self.offset = 0
        self.ypoints = np.arange(-20, 20 + self.nsteps, self.nsteps)
        self.xpoints = np.arange(-20, 20 + self.nsteps, self.nsteps)
        self.nfaces = len(self.ypoints)

        self.RATE = 44100 # standard 4.1 khz
        self.CHUNK = len(self.xpoints) * len(self.ypoints)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )

        # perlin noise object
        self.noise = OpenSimplex()

        verts, faces, colors = self.mesh()

        self.mesh1 = gl.GLMeshItem(
            faces=faces,
            vertexes=verts,
            faceColors=colors,
            drawEdges=True,
            smooth=False,
        )
        self.mesh1.setGLOptions('additive')
        self.window.addItem(self.mesh1)


    def mesh(self, offset=0, height=2.5, wf_data=None):

        if wf_data is not None:
            wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
            wf_data = np.array(wf_data, dtype='b')[::2] + 128
            wf_data = np.array(wf_data, dtype='int32') - 128
            wf_data = wf_data * 0.04
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))
        else:
            wf_data = np.array([1] * 1024)
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

        faces = []
        colors = []

        # [x, y, wf_data[xid][yid] * (1.5 * self.noise.noise2d(x=xid / 5 + offset, y=yid / 5 + offset))] 


        verts = np.array([
            [x, y, wf_data[xid][yid] * (1.5 * self.noise.noise2d(x=(xid/5), y=(yid/5)))] 
			for xid, x in enumerate(self.xpoints) for yid, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        for yid in range(self.nfaces - 1):
            yoff = yid * self.nfaces
            for xid in range(self.nfaces - 1):
                faces.append([xid + yoff, xid + yoff + self.nfaces, xid + yoff + self.nfaces + 1])
                faces.append([xid + yoff, xid + yoff + 1, xid + yoff + self.nfaces + 1])
                colors.append([xid / self.nfaces, 1 - xid / self.nfaces, yid / self.nfaces, 0.1])
                colors.append([xid / self.nfaces, 1 - xid / self.nfaces, yid / self.nfaces, 0.11])

        faces = np.array(faces, dtype=np.uint32)
        colors = np.array(colors, dtype=np.float32)

        return verts, faces, colors


    def update(self):
        # update the mesh and shift the noise each time
        wf_data = self.stream.read(self.CHUNK)
        verts, faces, colors = self.mesh(offset=self.offset, wf_data=wf_data)
        self.mesh1.setMeshData(vertexes=verts, faces=faces, faceColors=colors)
        self.offset -= 0.05


    def start(self):
        # open graphics window and set it up
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


    def animation(self, frametime=10):
        # calls update method to run in a loop
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(frametime)
        self.start()


if __name__ == '__main__':
    t = Terrain()
    t.animation()