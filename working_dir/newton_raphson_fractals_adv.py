import numpy as np
import cv2


height = 720
width = 1080

img = np.zeros((height, width, 3), np.uint8)

n = 8
factor = 0.01

k1 = 3
k2 = 4
k3 = -1

p1 = 4
p2 = 3


def polynomial(z):
    return k1 * z ** p1 + k2 * z ** p2 + k3


def derivative(z):
    return k1 * p1 * z ** (p1 - 1) + k2 * p2 * z ** (p2 - 1)


for i in range(height):
    for y in range(width):
        z = complex((y - width/2) * factor, (height/2 - i) * factor)
        for f in range(14):
            if z != (0 + 0j):
                n = polynomial(z)
                d = derivative(z)
                if d != (0 + 0j):
                    z -= polynomial(z)/derivative(z)
                else:
                    z = (0 - 1j)
                    break
            else:
                break

        if z.real != 0:
            theta = np.arctan(z.imag/z.real) / np.pi + 1/2
        else:
            if z.imag < 0:
                theta = 0
            else:
                theta = 1

        b, g, r = 50, 10, 70
        br, gr, rr = 100, 90, 40
        img[i, y] = [b + br * theta, g + gr * theta, r + rr * theta]


cv2.imwrite('newton_fractal17.png', img)