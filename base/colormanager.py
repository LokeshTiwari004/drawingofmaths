import numpy as np


class Col_man:  # color manager

    def __init__(self):
        self.r = 0
        self.b = 0
        self.g = 0

        self.color = self.b, self.g, self.r

        self.roc_b = None
        self.roc_g = None
        self.roc_r = None

        self.range_r = None
        self.range_b = None
        self.range_g = None


    def color_gradient(self, start=(255, 100, 50), stop=(155, 200, 150), rateofcahnge=(-0.5, 0.5, 0.5), steps=200):

        self.roc_b = rateofcahnge[0]
        self.roc_g = rateofcahnge[1]
        self.roc_r = rateofcahnge[2]

        self.b = start[0]
        self.g = start[1]
        self.r = start[2]

        self.color = self.b, self.g, self.r

        self.range_b = min(start[0], stop[0]), max(start[0], stop[0])
        self.range_g = min(start[1], stop[1]), max(start[1], stop[1])
        self.range_r = min(start[2], stop[2]), max(start[2], stop[2])

        for i in range(steps):

            self.b += self.roc_b
            self.g += self.roc_g
            self.r += self.roc_r

            self.b = self.manage_boundary(self.b, minimum=self.range_b[0], maximum=self.range_b[1])
            self.g = self.manage_boundary(self.g, minimum=self.range_g[0], maximum=self.range_g[1])
            self.r = self.manage_boundary(self.r, minimum=self.range_r[0], maximum=self.range_r[1])

            self.color = int(self.b), int(self.g), int(self.r)

            yield self.color

    @staticmethod
    def manage_boundary(inp, minimum=0, maximum=255):
        if inp < minimum:
            return minimum
        elif inp > maximum:
            return maximum
        else:
            return inp

    @classmethod
    def giverancol(cls):  # give random color
        return tuple(np.random.randint(0, 256, 3))
