import numpy as np

from base.dom import *

fh = Handle_frames()
mm = MovieMaker(fh.frame_seq_path, 'sample', framerate=60)

sc = Canvas()

win = carsys2D(canvas=sc, bvscalings=(4, 4), bvbounds=(range(-3005, 3006), range(-3005, 3006)))
win.drawgrid(skip_factor=(25, 25))
win.drawaxis(lw=2)

t = 200

amp = np.arange(-int(t/2),int(t/2))/10
omega = np.random.randint(1, 11, t)

time = np.arange(0, 1000) / 100

x = amp[0] * np.cos(omega[0] * time)
y = amp[0] * np.sin(omega[0] * time)

for i in range(1, t):
    x += amp[i] * np.cos(omega[i] * time)
    y += amp[i] * np.sin(omega[i] * time)


for j in range(0, len(time)-1):
    win.drawit(array=win.truepos(x[j:j+2], y[j:j+2]), thickness=1, color=(100, 200, 200))
    sc.savesc(fh.nameit())


mm.make_movie()
fh.del_img_seq()
