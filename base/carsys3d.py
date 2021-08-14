import cv2
import numpy as np
from base.colormanager import Col_man

# (-np.pi/6, np.pi/2, np.pi/6)


# this class gives us a cartesian 2-dimensional system
class carsys3D:  # full form is cartesian System 2 dimensional

    def __init__(self, canvas, center=None, bvscalings=(10, 10, 10), bvangles=(np.arccos(1/(3**0.5)), np.arccos(1/(3**0.5)), np.arccos(1/(3**0.5))), bvbounds=(range(-40, 41), range(-42, 43), range(-40, 41))):
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
        self.alpha = bvangles[0]
        self.beta = bvangles[1]
        self.gamma = bvangles[2]

        self.a = np.cos(self.alpha)
        self.b = np.cos(self.beta)
        self.c = np.cos(self.gamma)

        self.theta = np.arccos(-(self.a * self.b) / np.sqrt((self.c ** 2 + self.b ** 2) * (self.c ** 2 + self.a ** 2)))
        self.phi = np.arccos(-(self.b * self.c) / np.sqrt((self.b ** 2 + self.a ** 2) * (self.a ** 2 + self.c ** 2)))

        self.axial_angle = 0

        self.scaling = bvscalings

        self.bv1 = self.scaling[0] * np.sin(self.alpha) * np.array([np.cos(np.pi/2 - self.theta + self.axial_angle), - np.sin(np.pi/2 - self.theta + self.axial_angle)])
        self.bv2 = self.scaling[1] * np.sin(self.beta) * np.array([np.cos(np.pi/2 + self.axial_angle), - np.sin(np.pi/2 + self.axial_angle)])
        self.bv3 = self.scaling[2] * np.sin(self.gamma) * np.array([np.cos(np.pi/2 + self.phi + self.axial_angle), - np.sin(np.pi/2 + self.phi + self.axial_angle)])

        # boundary is the extreme value that one can take in the direction of the basis vectors
        self.bv1bound = bvbounds[0]
        self.bv2bound = bvbounds[1]
        self.bv3bound = bvbounds[2]

        self.label = 'XYZ'

    def rotate(self, alpha, beta, gamma, axial_angle=0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.axial_angle = axial_angle

        self.a = np.cos(self.alpha)
        self.b = np.cos(self.beta)
        self.c = np.cos(self.gamma)

        self.theta = np.sign(self.c) * np.arccos(- (self.a * self.b) / np.sqrt((self.c ** 2 + self.b ** 2) * (self.c ** 2 + self.a ** 2)))
        self.phi = np.sign(self.a) * np.arccos(- (self.b * self.c) / np.sqrt((self.b ** 2 + self.a ** 2) * (self.a ** 2 + self.c ** 2)))

        self.bv1 = self.scaling[0] * np.sin(self.alpha) * np.array([np.cos(np.pi/2 - self.theta + self.axial_angle), - np.sin(np.pi/2 - self.theta + self.axial_angle)])
        self.bv2 = self.scaling[1] * np.sin(self.beta) * np.array([np.cos(np.pi/2 + self.axial_angle), - np.sin(np.pi/2 + self.axial_angle)])
        self.bv3 = self.scaling[2] * np.sin(self.gamma) * np.array([np.cos(np.pi/2 + self.phi + self.axial_angle), - np.sin(np.pi/2 + self.phi + self.axial_angle)])

    def rescale(self, x_scale, y_scale, z_scale):
        self.bv1bound = x_scale
        self.bv2bound = y_scale
        self.bv3bound = z_scale

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

    def drawwithcg(self, which='main', array=None, color=((200, 100, 50), (100, 200, 50)), thickness=1):
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

    def drawaxis(self, which='main', x=True, y=True, z=True, labelit=True, xc=(200, 200, 200), yc=(200, 200, 200), zc=(200, 200, 200), lw=2):
        if which == 'main' or which == 'clone':
            if x:
                self.drawit(which=which, array=self.truepos(np.array([min(self.bv1bound), max(self.bv1bound)]), np.array([0, 0]), np.array([0, 0])),
                            color=xc, thickness=lw)
                if labelit:
                    pos = self.truepos([max(self.bv1bound)+1], [0], [0])[0]
                    self.canvas.write(self.label[0], [int(pos[0]), int(pos[1])], which)
            if y:
                self.drawit(which=which, array=self.truepos(np.array([0, 0]), np.array([min(self.bv2bound), max(self.bv2bound)]), np.array([0, 0])),
                            color=yc, thickness=lw)
                if labelit:
                    pos = self.truepos([0], [max(self.bv2bound)+1], [0])[0]
                    self.canvas.write(self.label[1], [int(pos[0]), int(pos[1])], which)
            if z:
                self.drawit(which=which, array=self.truepos(np.array([0, 0]), np.array([0, 0]), np.array([min(self.bv3bound), max(self.bv3bound)])),
                            color=zc, thickness=lw)
                if labelit:
                    pos = self.truepos([0], [0], [max(self.bv3bound)+1])[0]
                    self.canvas.write(self.label[2], [int(pos[0]), int(pos[1])], which)
        else:
            NameError(f'{which} not found')

    def drawgrid(self, which='main', skip_factor=(4, 4, 4), xy=True, yz=True, zx=True, xyc=(150, 100, 50), yzc=(150, 100, 50), zxc=(150, 100, 50), lw=1):
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
