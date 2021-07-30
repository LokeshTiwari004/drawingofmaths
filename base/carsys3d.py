import cv2
import numpy as np


# this class gives us a cartesian 2-dimensional system
class carsys3D:  # full form is cartesian System 2 dimensional

    def __init__(self, canvas, center=None):
        self.canvas = canvas

        # this provides the center aka origin for system 2 dimensional
        if center is None:
            self.center = np.array([self.canvas.width / 2, self.canvas.height / 2])
        else:
            if type(center) is list:
                self.center = np.array(center)
            else:
                RuntimeError('center must be "list" of two real numbers')

        # these are the default orthogonal basis vectors
        self.bv1 = np.array([10 * np.cos(99*np.pi/50), -10 * np.sin(99*np.pi/50)])
        self.bv2 = np.array([0, -10])
        self.bv3 = np.array([4 * np.cos(np.pi/6), -4 * np.sin(np.pi/6)])

        # boundary is the extreme value that one can in the direction of the basis vectors
        self.bv1bound = range(-40, 41)
        self.bv2bound = range(-40, 41)
        self.bv3bound = range(-40, 41)

    def truepos(self, x=None, y=None, z=None):  # full form of this function name is true position

        """ this function does scaling and provides true position on screen of points
            this takes input as an array of co-ordinates
            and return n x 2 array of true position on screen of those points"""
        if x is not None:
            x = np.array(x)
        if y is not None:
            y = np.array(y)
        if z is not None:
            z = np.array(z)

        if len(x) == len(y) and len(x) == len(y):
            x = x[x > min(self.bv1bound) - 1]
            x = x[x < max(self.bv1bound) + 1]

            y = y[y > min(self.bv1bound) - 1]
            y = y[y < max(self.bv1bound) + 1]

            answer = np.array([self.center + x[0] * self.bv1 + y[0] * self.bv2 + z[0] * self.bv3])

            for i in range(1, len(x)):
                answer = np.vstack((answer, self.center + x[i] * self.bv1 + y[i] * self.bv2 + z[i] * self.bv3))

            return answer
        else:
            RuntimeError('array length must be equal')

    def drawit(self, which='main', array=None, isClosed=False, color=(200, 200, 200), thickness=1, pointsonly=False):
        if array is not None:
            array = array.reshape((-1, 1, 2))
            array = np.array(np.rint(array), dtype='int32')
            if which == 'main':
                if pointsonly:
                    self.canvas.main = cv2.polylines(self.canvas.main, array, isClosed, color, thickness)
                else:
                    self.canvas.main = cv2.polylines(self.canvas.main, [array], isClosed, color, thickness)
            elif which == 'clone':
                if pointsonly:
                    self.canvas.clone = cv2.polylines(self.canvas.clone, array, isClosed, color, thickness)
                else:
                    self.canvas.clone = cv2.polylines(self.canvas.clone, [array], isClosed, color, thickness)
            else:
                NameError(f'{which} not available')
        else:
            RuntimeError('please specify array of points')

    def drawaxis(self, which='main', x=True, y=True, z=True, xc=(200, 200, 0), yc=(200, 200, 0), zc=(200, 200, 0), lw=2):
        if which == 'main' or which == 'clone':
            if x:
                self.drawit(which=which, array=self.truepos([min(self.bv1bound), max(self.bv1bound)], [0, 0], [0, 0]),
                            color=xc, thickness=lw)
            if y:
                self.drawit(which=which, array=self.truepos([0, 0], [min(self.bv2bound), max(self.bv2bound)], [0, 0]),
                            color=yc, thickness=lw)
            if z:
                self.drawit(which=which, array=self.truepos([0, 0], [0, 0], [min(self.bv3bound), max(self.bv3bound)]),
                            color=zc, thickness=lw)
        else:
            NameError(f'{which} not found')

    def drawgrid(self, which='main', skip_factor=(4, 4, 4), xy=True, yz=True, zx=True, xyc=(100, 100, 100), yzc=(100, 100, 100), zxc=(100, 100, 100), lw=1):
        val = np.array([0, 0])

        updw = [min(self.bv2bound), max(self.bv2bound)]
        lfrg = [min(self.bv1bound), max(self.bv1bound)]
        zupdw = [min(self.bv3bound), max(self.bv3bound)]

        if xy:

            for g in range(0, int(max(self.bv1bound)), skip_factor[0]):
                self.drawit(which=which, array=self.truepos(val + np.array([g, g]), updw, [0, 0]),
                            color=xyc, thickness=lw)
                self.drawit(which=which, array=self.truepos(val - np.array([g, g]), updw, [0, 0]),
                            color=xyc, thickness=lw)

            for g in range(0, int(max(self.bv2bound)), skip_factor[1]):
                self.drawit(which=which, array=self.truepos(lfrg, val + np.array([g, g]), [0, 0]),
                            color=xyc, thickness=lw)
                self.drawit(which=which, array=self.truepos(lfrg, val - np.array([g, g]), [0, 0]),
                            color=xyc, thickness=lw)
        if yz:

            for g in range(0, int(max(self.bv1bound)), skip_factor[0]):
                self.drawit(which=which, array=self.truepos([0, 0], val + np.array([g, g]), zupdw),
                            color=yzc, thickness=lw)
                self.drawit(which=which, array=self.truepos([0, 0], val - np.array([g, g]), zupdw),
                            color=yzc, thickness=lw)

            for g in range(0, int(max(self.bv2bound)), skip_factor[1]):
                self.drawit(which=which, array=self.truepos([0, 0], lfrg, val + np.array([g, g])),
                            color=yzc, thickness=lw)
                self.drawit(which=which, array=self.truepos([0, 0], lfrg, val - np.array([g, g])),
                            color=yzc, thickness=lw)
        if zx:

            for g in range(0, int(max(self.bv1bound)), skip_factor[0]):
                self.drawit(which=which, array=self.truepos(val + np.array([g, g]), [0, 0], zupdw),
                            color=zxc, thickness=lw)
                self.drawit(which=which, array=self.truepos(val - np.array([g, g]), [0, 0], zupdw),
                            color=zxc, thickness=lw)

            for g in range(0, int(max(self.bv2bound)), skip_factor[1]):
                self.drawit(which=which, array=self.truepos(updw, [0, 0], val + np.array([g, g])),
                            color=zxc, thickness=lw)
                self.drawit(which=which, array=self.truepos(updw, [0, 0], val - np.array([g, g])),
                            color=zxc, thickness=lw)
