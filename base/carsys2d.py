import cv2
import numpy as np
from base.colormanager import Col_man


# this class gives us a cartesian 2-dimensional system
class carsys2D:  # full form is cartesian System 2 dimensional

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
        self.bv1 = np.array([10, 0])
        self.bv2 = np.array([0, -10])

        # boundary is the extreme value that one can in the direction of the basis vectors
        self.bv1bound = range(-98, 99)
        self.bv2bound = range(-53, 54)

    def truepos(self, arr, y=None, bindit=False):  # full form of this function name is true position

        """ this function does scaling and provides true position on screen of points
            this takes input as an two dimensional array of co-ordinates
            and return n x 2 array of true position on screen of those points"""

        arr = np.array(arr)
        if y is not None:
            y = np.array(y)

        if len(arr.shape) == 1 and y is not None:
            if len(arr) == len(y):
                if bindit:
                    arr = arr[arr > min(self.bv1bound) - 1]
                    arr = arr[arr < max(self.bv1bound) + 1]

                    y = y[y > min(self.bv1bound) - 1]
                    y = y[y < max(self.bv1bound) + 1]

                answer = np.array([self.center + arr[0] * self.bv1 + y[0] * self.bv2])

                for i in range(1, len(arr)):
                    answer = np.vstack((answer, self.center + arr[i] * self.bv1 + y[i] * self.bv2))

                return answer
            else:
                RuntimeError('length of both arrays are different')

        elif len(arr.shape) == 1 and y is None:
            RuntimeError('please specify y values')

        elif len(arr.shape) == 2 and y is None:
            if arr.shape[1] == 2:
                answer = np.array([self.center + arr[0, 0] * self.bv1 + arr[0, 1] * self.bv2])
                for i in range(1, len(arr)):
                    answer = np.vstack((answer, [self.center + arr[i, 0] * self.bv1 + arr[i, 1] * self.bv2]))
                return answer
            elif arr.shape[0] == 2:
                answer = np.array([self.center + arr[0, 0] * self.bv1 + arr[1, 0] * self.bv2])
                for i in range(1, len(arr)):
                    answer = np.vstack((answer, [self.center + arr[0, i] * self.bv1 + arr[1, i] * self.bv2]))
                return answer
            else:
                RuntimeError('This is cartesian system 2 dimensional')
        else:
            RuntimeError('this is cartesian system 2 dimensional')

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

    def drawwithcg(self, which='main', array=None, color=((255, 0, 0), (0, 255, 0)), thickness=1):
        if array is not None:
            array = array.reshape((-1, 1, 2))
            array = np.array(np.rint(array), dtype='int32')
            steps = len(array)-1
            cm = Col_man()
            cg = cm.color_gradient(start=color[0], stop=color[1], rateofcahnge=((color[1][0]-color[0][0])/steps, (color[1][1]-color[0][1])/steps, (color[1][2]-color[0][2])/steps), steps=steps)
            if which == 'main':
                for i in range(len(array)-1):
                    self.canvas.main = cv2.polylines(self.canvas.main, [array[i:i+2]], False, cg.__next__(), thickness)
            elif which == 'clone':
                for i in range(len(array)-1):
                    self.canvas.clone = cv2.polylines(self.canvas.clone, [array[i:i+2]], False, cg.__next__(), thickness)
            else:
                NameError(f'{which} not available')
        else:
            RuntimeError('please specify array of points')

    def drawaxis(self, which='main', color=(200, 200, 0), lw=2):
        if which == 'main' or which == 'clone':
            self.drawit(which=which, array=self.truepos([min(self.bv1bound), max(self.bv1bound)], [0, 0]),
                        color=color, thickness=lw)
            self.drawit(which=which, array=self.truepos([0, 0], [min(self.bv2bound), max(self.bv2bound)]),
                        color=color, thickness=lw)
        else:
            NameError(f'{which} not found')

    def drawgrid(self, skip_factor=(5, 5), which='main', color=(200, 200, 200), lw=1):
        if which == 'main' or which == 'clone':
            val = np.array([0, 0])
            updw = [min(self.bv2bound), max(self.bv2bound)]
            lfrg = [min(self.bv1bound), max(self.bv1bound)]
            for g in range(0, int(max(self.bv1bound)), skip_factor[0]):
                self.drawit(which=which, array=self.truepos(val + np.array([g, g]), updw), color=color,
                            thickness=lw)
                self.drawit(which=which,array=self.truepos(val - np.array([g, g]), updw), color=color, thickness=lw)
            for g in range(0, int(max(self.bv2bound)), skip_factor[1]):
                self.drawit(which=which, array=self.truepos(lfrg, val + np.array([g, g])), color=color, thickness=lw)
                self.drawit(which=which, array=self.truepos(lfrg, val - np.array([g, g])), color=color, thickness=lw)
        else:
            NameError(f'{which} not found')
