from base.dom import *

fh = Handle_frames()
mm = MovieMaker(fh.frame_seq_path, 'eleventh')

sc = Canvas()
win = carsys2D(canvas=sc)

win.bv1 = np.array([80, 0])
win.bv2 = np.array([0, -80])
win.bv1bound = range(-12, 13)
win.bv2bound = range(-6, 7)


t = np.linspace(0, 800*np.pi/399, 600) - 12

for i in range(360):
    sc.createcp()

    if i < 200:
        win.drawaxis(color=(200 - i, 200 - i, 200 - i))
        win.drawgrid(skip_factor=(1, 1), color=(200 - i, 200 - i, 200 - i))

    win.drawwithcg(which='main', array=win.truepos(t, 1.2 * np.sin(t)), thickness=2)
    t += 0.05

    sc.savesc(fh.nameit())
    sc.fallback()


mm.make_movie()
fh.del_img_seq()
