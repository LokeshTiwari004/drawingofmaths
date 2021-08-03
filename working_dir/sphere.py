from base.dom import *


class DrawSphere:


    def __init__(self, system3d, radius=30, steps=100, smoothness=400, color=((200, 100, 100), (100, 200, 100))):

        self.system = system3d
        self.radius = radius

        self.interval = np.linspace(0, 2 * smoothness * np.pi/(smoothness-1), smoothness)

        self.steps = steps

        self.cm = Col_man()  # cm means color manager
        # cg means color gradient
        self.cg = self.cm.color_gradient(start=color[0], stop=color[1],
                                         rateofcahnge=((color[1][0]-color[0][0])/steps, (color[1][1]-color[0][1])/steps, (color[1][2]-color[0][2])/steps),
                                         steps=steps)


    def drawit(self, along_x=False, along_y=False, along_z=False, axis=True, grid=True, bound=False, lw=1):

        if axis:
            self.system.drawaxis(x=along_x, y=along_y, z=along_z)
        if grid:
            self.system.drawgrid(xy=along_z, yz=along_x, zx=along_y)

        for i in range(0, 200, int(200 / self.steps)):

            x_val = self.radius * np.sin(self.interval[i]) * np.cos(self.interval)
            y_val = self.radius * np.sin(self.interval[i]) * np.sin(self.interval)
            z_val = np.array([self.radius * np.cos(self.interval[i])] * 400)

            if along_z:
                self.system.drawit(array=self.system.truepos(x_val, y_val, z_val, bound), color=self.cm.color, thickness=lw)
            if along_y:
                self.system.drawit(array=self.system.truepos(x_val, z_val, y_val, bound), color=self.cm.color, thickness=lw)
            if along_x:
                self.system.drawit(array=self.system.truepos(z_val, x_val, y_val, bound), color=self.cm.color, thickness=lw)

            self.cg.__next__()


if __name__ == '__main__':
    screen = Canvas()
    sys3d = carsys3D(screen, bvbounds=(range(-30, 31), range(-30, 0), range(-35, 36)))

    DrawSphere(sys3d, steps=100).drawit(along_y=True, bound=True, lw=1)

    screen.savesc('sphere1.png')
