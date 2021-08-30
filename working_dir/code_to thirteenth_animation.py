import numpy as np

from base.dom import *

screen = Canvas()
system = carsys2D(screen, bvbounds=(range(0, 8), (-3, 4)), center=[1550, 300], bvscalings=(25, 25))
system2 = carsys2D(screen, bvbounds=(range(-4, 5), (-4, 5)), center=[900, 540], bvscalings=(80, 80))

fh = Handle_frames()
mm = MovieMaker(fh.frame_seq_path, 'thirteen')

integer = np.vectorize(int)
x = list(integer(system2.truepos([[-35, 40]])[0]))
screen.write('experimenting', list(x), fontScale=2, thickness=2)

t = np.linspace(0, 2 * np.pi, 400)
a, b, c = 1, 4, 7
y = np.sin(a * t + b) + np.sin(b * t + c) + np.sin(c * t + a)
x = np.cos(a * t + b) + np.cos(b * t + c) + np.cos(c * t + a)

system.drawaxis(color=(200, 200, 200), lw=1)
system2.drawgrid(color=(150, 150, 50), lw=1, skip_factor=(1, 1))
system2.drawaxis(color=(200, 200, 200), lw=2)

screen.createcp()
system.drawwithcg(array=system.truepos(t, y), thickness=2)
screen.savesc(fh.nameit())
screen.fallback()

for i in range(1, 31):
    screen.createcp()

    system.drawwithcg(array=system.truepos(t, y), thickness=2)
    system.drawwithcg(array=system.truepos(t, y - (i/2)), thickness=2)


    screen.savesc(fh.nameit())
    screen.fallback()


for i in range(1, 399):
    screen.createcp()

    system.drawwithcg(array=system.truepos(t, y), thickness=2)
    system.drawwithcg(array=system.truepos(t[i:], y[i:] - 15), thickness=2)
    system2.drawwithcg(array=system2.truepos(x[:i+1], y[:i+1]), thickness=2)
    system2.drawit(array=system2.truepos([0, x[i]], [0, y[i]]), color=(0, 150, 150), thickness=2)

    screen.savesc(fh.nameit())
    screen.fallback()

for i in range(600):
    screen.createcp()

    a += 0.01
    b += 0.01
    c -= 0.01

    y = np.sin(a * t + b) + np.sin(b * t + c) + np.sin(c * t + a)
    x = np.cos(a * t + b) + np.cos(b * t + c) + np.cos(c * t + a)

    system2.drawwithcg(array=system2.truepos(x, y), thickness=2)
    system.drawwithcg(array=system.truepos(t, y), thickness=2)

    screen.savesc(fh.nameit())
    screen.fallback()



mm.make_movie()
fh.del_img_seq()
