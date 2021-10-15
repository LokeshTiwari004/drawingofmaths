import numpy as np
import cv2
from base.dom import *

fh = Handle_frames()
mm = MovieMaker(fh.frame_seq_path, 'newton_fractals')

height = 400
width = 400

img = np.zeros((height, width, 3), np.uint8)

r1 = (4 + 0j)
r2 = (-5 + 3j)
r3 = (-5 - 3j)
# r4 = (-1 - 3j)
# r5 = (1 - 3j)



def polynomial(r):
    return (r - r1) * (r - r2) * (r - r3) # * (r - r4) * (r - r5)


def distance_squared(num):
    return num.real ** 2 + num.imag ** 2


def inverse_of_derivative(r):
    # u = (r - r1) * (r - r2) * (r - r3) * (r - r4) + (r - r1) * (r - r2) * (r - r3) * (r - r5) + (r - r1) * (r - r2) * (r - r4) * (r - r5) + (r - r1) * (r - r3) * (r - r4) * (r - r5) + (r - r2) * (r - r3) * (r - r4) * (r - r5)
    u = (r - r1) * (r - r2) + (r - r1) * (r - r3) + (r - r3) * (r - r2)

    k = distance_squared(u)
    u = complex(u.real, - u.imag)
    if k != 0:
        return u/k
    else:
        return u


def closest_root(num):
    # my_arr = np.array([distance_squared(num - r1),distance_squared(num - r2),distance_squared(num - r3),distance_squared(num - r4),distance_squared(num - r5)])
    my_arr = np.array([distance_squared(num - r1), distance_squared(num - r2), distance_squared(num - r3)])
    h = np.where(my_arr == np.amin(my_arr))[0][0]
    if h == 1:
        return [36, 201, 179]
    elif h == 2:
        return [79, 35, 184]
    # elif h == 3:
    #     return [196, 201, 36]
    # elif h == 4:
    #     return [141, 201, 36]
    elif h == 0:
        return [201, 36, 122]



# for s in range(360):
s = 0
factor = 0.1 - s/359 * 0.09
for i in range(height):
    for y in range(width):
        num = complex((y - width/2) * factor, (height/2 - i) * factor)
        for f in range(10):
            num = num - polynomial(num) * inverse_of_derivative(num)
        img[i, y] = closest_root(num)

cv2.imwrite('newton_fractal.png', img)

    # cv2.imwrite(fh.nameit(), img)

# mm.make_movie()
