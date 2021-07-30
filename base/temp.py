from dom import *

fh = Handle_frames()
mm = MovieMaker(fh.name, fh.frame_sequence, movie_name='third', framerate=30)

screen = Canvas()
screen.createcp()

center1 = carsys3D(screen)

center1.drawgrid(which='main', skip_factor=(6, 6, 6), zxc=(80, 80, 8), lw=1, xy=False, yz=False)
center1.drawaxis(which='main', xc=(180, 180, 180), yc=(180, 180, 180), zc=(180, 180, 180), lw=2)


t = np.linspace(0, 800*np.pi/399, 400)
radius = 30

i = 0
while i < 200:

    x = radius * np.sin(t[i]) * np.cos(t)
    y = radius * np.sin(t[i]) * np.sin(t)
    z = [radius * np.cos(t[i])]*400

    center1.drawit(which='main', array=center1.truepos(x, y, z), color=(200, 200, 0), thickness=1)
    # center1.drawit(which='main', array=center1.truepos(x, z, y), color=(66, 147, 168), thickness=1)
    screen.savesc(fh.current_dir + '\\' + fh.name + '\\' + fh.nameit())

    i += 1

mm.make_movie()
fh.del_img_seq()
