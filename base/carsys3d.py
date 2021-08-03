import cv2
import numpy as np


# this class gives us a cartesian 2-dimensional system
class carsys3D:  # full form is cartesian System 2 dimensional

    def __init__(self, canvas, center=None, bvscalings=(10, 10, 10), bvangles=(-np.pi/6, np.pi/2, np.pi/6), bvbounds=(range(-40, 41), range(-42, 43), range(-40, 41))):
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
        self.xangle = bvangles[0]
        self.yangle = bvangles[1]
        self.zangle = bvangles[2]

        self.scaling = bvscalings

        self.bv1 = np.array([self.scaling[0] * np.cos(self.xangle), -self.scaling[0] * np.sin(self.xangle)])
        self.bv2 = np.array([self.scaling[1] * np.cos(self.yangle), -self.scaling[1] * np.sin(self.yangle)])
        self.bv3 = np.array([self.scaling[2] * np.cos(self.zangle), -self.scaling[2] * np.sin(self.zangle)])

        # boundary is the extreme value that one can take in the direction of the basis vectors
        self.bv1bound = bvbounds[0]
        self.bv2bound = bvbounds[1]
        self.bv3bound = bvbounds[2]

    def truepos(self, x=None, y=None, z=None, bind=False):  # full form of this function name is true position

        """ this function does scaling and provides true position on screen of points
            this takes input as an array of co-ordinates
            and return n x 2 array of true position on screen of those points"""

        if bind:
            x = x[x > min(self.bv1bound) - 1]
            x = x[x < max(self.bv1bound) + 1]

            y = y[y > min(self.bv2bound) - 1]
            y = y[y < max(self.bv2bound) + 1]

            z = z[z > min(self.bv3bound) - 1]
            z = z[z < max(self.bv3bound) + 1]

        length_of_x = len(x)

        if length_of_x != 0:
            if length_of_x == len(y):
                if length_of_x == len(z):
                    answer = np.array([self.center + x[0] * self.bv1 + y[0] * self.bv2 + z[0] * self.bv3])

                    for i in range(1, len(x)):
                        answer = np.vstack((answer, self.center + x[i] * self.bv1 + y[i] * self.bv2 + z[i] * self.bv3))

                    return answer
        else:
            return np.array([0, 0])

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
                self.drawit(which=which, array=self.truepos(np.array([min(self.bv1bound), max(self.bv1bound)]), np.array([0, 0]), np.array([0, 0])),
                            color=xc, thickness=lw)
            if y:
                self.drawit(which=which, array=self.truepos(np.array([0, 0]), np.array([min(self.bv2bound), max(self.bv2bound)]), np.array([0, 0])),
                            color=yc, thickness=lw)
            if z:
                self.drawit(which=which, array=self.truepos(np.array([0, 0]), np.array([0, 0]), np.array([min(self.bv3bound), max(self.bv3bound)])),
                            color=zc, thickness=lw)
        else:
            NameError(f'{which} not found')

    def drawgrid(self, which='main', skip_factor=(4, 4, 4), xy=True, yz=True, zx=True, xyc=(100, 100, 100), yzc=(100, 100, 100), zxc=(100, 100, 100), lw=1):
        val = np.array([0, 0])

        updw = np.array([min(self.bv2bound), max(self.bv2bound)])
        lfrg = np.array([min(self.bv1bound), max(self.bv1bound)])
        zupdw = np.array([min(self.bv3bound), max(self.bv3bound)])

        if xy:

            for g in range(max(0, int(min(self.bv1bound))), int(max(self.bv1bound)) + 1, skip_factor[0]):
                self.drawit(which=which, array=self.truepos(np.array([g, g]), updw, val),
                            color=xyc, thickness=lw)
            for g in range(min(0, int(max(self.bv1bound))),int(min(self.bv1bound)) - 1, -skip_factor[0]):
                self.drawit(which=which, array=self.truepos(np.array([g, g]), updw, val),
                            color=xyc, thickness=lw)

            for g in range(max(0, int(min(self.bv2bound))), int(max(self.bv2bound)) + 1, skip_factor[0]):
                self.drawit(which=which, array=self.truepos(lfrg, np.array([g, g]), val),
                            color=xyc, thickness=lw)
            for g in range(min(0, int(max(self.bv2bound))), int(min(self.bv2bound)) - 1, -skip_factor[0]):
                self.drawit(which=which, array=self.truepos(lfrg, np.array([g, g]), val),
                            color=xyc, thickness=lw)
        if yz:

            for g in range(max(0, int(min(self.bv2bound))), int(max(self.bv2bound)) + 1, skip_factor[2]):
                self.drawit(which=which, array=self.truepos(val, np.array([g, g]), zupdw),
                            color=yzc, thickness=lw)
            for g in range(min(0, int(max(self.bv2bound))), int(min(self.bv2bound)) - 1, -skip_factor[2]):
                self.drawit(which=which, array=self.truepos(val, np.array([g, g]), zupdw),
                            color=yzc, thickness=lw)

            for g in range(max(0, int(min(self.bv3bound))), int(max(self.bv3bound)) + 1, skip_factor[2]):
                self.drawit(which=which, array=self.truepos(val, updw, np.array([g, g])),
                            color=yzc, thickness=lw)
            for g in range(min(0, int(max(self.bv3bound))),int(min(self.bv3bound)) - 1, -skip_factor[2]):
                self.drawit(which=which, array=self.truepos(val, updw, np.array([g, g])),
                            color=yzc, thickness=lw)
        if zx:

            for g in range(max(0, int(min(self.bv3bound))), int(max(self.bv3bound)) + 1, skip_factor[2]):
                self.drawit(which=which, array=self.truepos(lfrg, val, np.array([g, g])),
                            color=zxc, thickness=lw)
            for g in range(min(0, int(max(self.bv3bound))), int(min(self.bv3bound)) - 1, -skip_factor[2]):
                self.drawit(which=which, array=self.truepos(lfrg, val, np.array([g, g])),
                            color=zxc, thickness=lw)

            for g in range(max(0, int(min(self.bv1bound))), int(max(self.bv1bound)) + 1, skip_factor[2]):
                self.drawit(which=which, array=self.truepos(np.array([g, g]), val, zupdw),
                            color=zxc, thickness=lw)
            for g in range(min(0, int(max(self.bv1bound))), int(min(self.bv1bound)) - 1, -skip_factor[2]):
                self.drawit(which=which, array=self.truepos(np.array([g, g]), val, zupdw),
                            color=zxc, thickness=lw)
