import numpy as np

from dom import *

fh = Handle_frames()
mm = MovieMaker(fh.name, fh.frame_sequence, movie_name='anim', framerate=15)

screen = Canvas()
screen.createcp()

center1 = carsys3D(screen)

center1.drawgrid(which='main', skip_factor=(6, 6, 6), zxc=(80, 80, 8), lw=1, xy=False, yz=False)
center1.drawaxis(which='main', xc=(180, 180, 180), yc=(180, 180, 180), zc=(180, 180, 180), lw=2)


t = np.linspace(0, 800*np.pi/399, 400)
radius = 30

cm = Col_man()
rc = cm.color_gradient()

i = 1
while i < 200:

    x = radius * np.sin(t[i]) * np.cos(t)
    y = radius * np.sin(t[i]) * np.sin(t)
    z = np.array([radius * np.cos(t[i])]*400)

    center1.drawit(which='main', array=center1.truepos(x, y, z), color=rc.__next__(), thickness=1)
    screen.savesc(fh.current_dir + '\\' + fh.name + '\\' + fh.nameit())
    i += 1


# screen.savesc('lok.png')
mm.make_movie()
fh.del_img_seq()
