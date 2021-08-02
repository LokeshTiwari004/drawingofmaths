from dom import *

fh = Handle_frames()
mm = MovieMaker(fh.name, fh.frame_sequence, movie_name='ninth', framerate=30)

sc = Canvas()
sc.createcp()


win = carsys3D(canvas=sc)


t = np.linspace(0, 800*np.pi/399, 400)
radius = 30

win.drawgrid(which='main', skip_factor=(4, 4, 4), zxc=(100, 60, 30), xyc=(30, 100, 50), yzc=(60, 30, 100), lw=1,
             zx=True, xy=False, yz=False)
win.drawaxis(which='main', xc=(180, 100, 100), yc=(100, 180, 100), zc=(100, 100, 180), lw=2)

cm = Col_man()
rc = cm.color_gradient()


# scene 1 drawing the 3d structure


i = 1
while i < 200:

    x = radius * np.sin(t[i]) * np.sin(t) * np.cos(t[i])
    y = radius * np.sin(t[i]) * np.sin(t)
    z = np.array([radius * np.cos(t[i])]*400)

    win.drawit(which='main', array=win.truepos(x, y, z), color=rc.__next__(), thickness=1)

    sc.savesc(fh.current_dir + '\\' + fh.name + '\\' + fh.nameit())
    i += 1




# scene 2 changing view

w1 = -np.pi/600

a1 = -np.pi / 6
a2 = np.pi / 6
a3 = np.pi/2

factor1 = 1.0
factor2 = 1.0

i = 1
while i <= 200:

    sc.fallback()
    sc.createcp()

    win.bv1 = np.array([10 * np.cos(a1), -10 * np.sin(a1)])
    win.bv2 = np.array([0, -10])
    win.bv3 = np.array([10 * np.cos(a2), -10 * np.sin(a2)])


    cm = Col_man()
    rc = cm.color_gradient()

    j = 1
    while j < 200:
        x = radius * np.sin(t[j]) * np.sin(t) * np.cos(t[j])
        y = radius * np.sin(t[j]) * np.sin(t)
        z = np.array([radius * np.cos(t[j])] * 400)
        win.drawit(which='main', array=win.truepos(x, y, z), color=rc.__next__(), thickness=1)
        j += 1

    win.drawgrid(which='main', skip_factor=(4, 4, 4), zxc=(60, 30, 20), xyc=(20, 60, 30), yzc=(30, 20, 60), lw=1,
                 zx=True, xy=True, yz=True)
    win.drawaxis(which='main', xc=(180, 100, 100), yc=(100, 180, 100), zc=(100, 100, 180), lw=2)

    sc.savesc(fh.current_dir + '\\' + fh.name + '\\' + fh.nameit())

    a1 -= w1
    a2 += w1


    i += 1


w2 = np.pi/600

i = 1
while i <= 200:

    sc.fallback()
    sc.createcp()

    win.bv1 = np.array([10 * np.cos(a1), -10 * np.sin(a1)])
    win.bv2 = np.array([0, -10])
    win.bv3 = np.array([10 * np.cos(a2), -10 * np.sin(a2)])


    cm = Col_man()
    rc = cm.color_gradient()

    j = 1
    while j < 200:
        x = radius * np.sin(t[j]) * np.sin(t) * np.cos(t[j])
        y = radius * np.sin(t[j]) * np.sin(t)
        z = np.array([radius * np.cos(t[j])] * 400)
        win.drawit(which='main', array=win.truepos(x, y, z), color=rc.__next__(), thickness=1)
        j += 1

    win.drawgrid(which='main', skip_factor=(4, 4, 4), zxc=(60, 30, 20), xyc=(20, 60, 30), yzc=(30, 20, 60), lw=1,
                 zx=True, xy=True, yz=True)
    win.drawaxis(which='main', xc=(180, 100, 100), yc=(100, 180, 100), zc=(100, 100, 180), lw=2)

    sc.savesc(fh.current_dir + '\\' + fh.name + '\\' + fh.nameit())

    a1 += 2 * w2
    a2 += w2


    i += 1


mm.make_movie()
fh.del_img_seq()

