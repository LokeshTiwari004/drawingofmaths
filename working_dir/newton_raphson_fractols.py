import numpy as np
import cv2


height = 720
width = 1080

img = np.zeros((height, width, 3), np.uint8)

n = 8
factor = 0.0025


for i in range(height):
    for y in range(width):
        z = complex((y - width/2) * factor, (height/2 - i) * factor)
        for f in range(20):
            if z != (0 + 0j):
                z = ((n-1)*z + z**(1-n))/3
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


cv2.imwrite('newton_fractal14.png', img)