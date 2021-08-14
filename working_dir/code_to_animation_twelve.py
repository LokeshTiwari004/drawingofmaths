import numpy as np

from base.dom import *

fh = Handle_frames()
mm = MovieMaker(frame_seq_path=fh.frame_seq_path, movie_name='twelve',movie_location='C:\\Users\\USER\\Desktop')


screen = Canvas()
system = carsys3D(canvas=screen, center=[500, 540], bvbounds=(range(-25, 26), range(-35, 36), range(-25, 26)), bvscalings=(15, 15, 15))


system1 = carsys2D(canvas=screen, center=[1400, 185], bvbounds=(range(-30, 31), range(-14, 15)))
system1.label = 'XY'
system2 = carsys2D(canvas=screen, center=[1400, 540], bvbounds=(range(-30, 31), range(-14, 15)))
system2.label = 'YZ'
system3 = carsys2D(canvas=screen, center=[1400, 895], bvbounds=(range(-30, 31), range(-14, 15)))
system3.label = 'ZX'
system1.drawgrid()
system1.drawaxis()
system2.drawgrid()
system2.drawaxis()
system3.drawgrid()
system3.drawaxis()

system.drawaxis()
system.drawgrid(xy=False, yz=False, zx=True)


t = np.linspace(0, 2*np.pi, 600)

omega1 = 0
omega2 = 3
omega3 = 0

phi1 = 0
phi2 = 3
phi3 = 6

radius1 = 8
radius2 = 8
radius3 = 8


for i in range(1200):
    screen.createcp()

    a = radius1 * np.cos(omega1 * t)
    b = radius2 * np.cos(omega2 * t)
    c = radius3 * np.cos(omega3 * t)

    x = a * np.cos(phi1 * t) + b * np.sin(phi2 * t)
    y = b * np.cos(phi2 * t) + c * np.sin(phi3 * t)
    z = c * np.cos(phi3 * t) + a * np.sin(phi1 * t)

    system.drawwithcg(array=system.truepos(x, y, z), thickness=2)
    system1.drawwithcg(array=system1.truepos(x-3, y-3), thickness=2)
    system2.drawwithcg(array=system2.truepos(y-3, z-3), thickness=2)
    system3.drawwithcg(array=system3.truepos(z-3, x-3), thickness=2)

    screen.savesc(fh.nameit())
    screen.fallback()

    phi1 += 0.01
    phi2 += 0.01
    phi3 += 0.01

    omega1 += 0.01
    omega2 += 0.01
    omega3 += 0.01


mm.make_movie()
fh.del_img_seq()

