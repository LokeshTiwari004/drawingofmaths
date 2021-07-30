from dom import *

fh = Handle_frames()
mm = MovieMaker(fh.name, fh.frame_sequence, movie_name='second')

# scene 1
sc = Canvas()
sc.createcp()

win = carsys2D(canvas=sc)

i = 99
while i < 201:
    win.drawgrid(skip_factor=(4, 4), color=(i, i, i), lw=1)
    win.drawaxis(color=(i, i, 0), lw=2)
    sc.savesc(fh.current_dir+'\\'+fh.name+'\\'+fh.nameit())
    i += 3

sc.clonesc()

t = np.linspace(0, 800*np.pi/399, 400)
radius = 50

i = 1
while i < 41:
    x = radius * np.cos(t[0:i*10])
    y = radius * np.sin(t[0:i*10])

    win.drawit(which='clone', array=win.truepos(x, y), thickness=2, color=(0, 160, 160))
    sc.savecl(fh.current_dir+'\\'+fh.name+'\\'+fh.nameit())

    i += 1

sc.fallback()
sc.createcp()

i = 0
while i < 400:
    win.bv1 = 10 * np.array([np.cos(t[i]), np.sin(t[i])])
    win.bv2 = 10 * np.array([np.cos(t[i]+np.pi/2), np.sin(t[i]+np.pi/2)])

    win.drawgrid(skip_factor=(4, 4))
    win.drawaxis()

    win.drawit(array=win.truepos(x, y), thickness=2, color=(0, 160, 160))

    sc.savesc(fh.current_dir + '\\' + fh.name + '\\' + fh.nameit())
    sc.fallback()
    sc.createcp()

    i += 1

sc.fallback()
sc.createcp()

i = 0
while i < 400:
    win.bv2 = 10 * np.array([np.cos(t[i] + np.pi / 2), np.sin(t[i] + np.pi / 2)])

    win.drawgrid(skip_factor=(4, 4))
    win.drawaxis()

    win.drawit(array=win.truepos(x, y), thickness=2, color=(0, 160, 160))

    sc.savesc(fh.current_dir + '\\' + fh.name + '\\' + fh.nameit())
    sc.fallback()
    sc.createcp()

    i += 1

mm.make_movie()
fh.del_img_seq()