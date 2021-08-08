from base.dom import *
from sphere import DrawSphere


fh = Handle_frames()
mm = MovieMaker(fh.frame_seq_path, 'tenth', 'C:\\Users\\USER\\Desktop', framerate=30)


screen = Canvas()
sys3d = carsys3D(screen, bvbounds=(range(-60, 61), range(-80, 81), range(-60, 61)))


alpha = np.pi / 6
beta = np.pi / 3
gamma = np.pi / 2


t = np.pi / 150
b = 1 - np.cos(beta) ** 2

for i in range(0, 100):
    screen.createcp()

    sys3d.rotate(alpha, beta, gamma)
    sys3d.drawaxis()
    DrawSphere(sys3d, steps=100).drawit(along_x=True, axis=False, grid=True, bound=False, lw=1)

    screen.savesc(fh.nameit())
    screen.fallback()

    alpha += t
    gamma = np.arccos(np.sqrt(b - np.cos(alpha) ** 2))


for i in range(0, 99):
    alpha -= t
    gamma = np.arccos(np.sqrt(b - np.cos(alpha) ** 2))

    screen.createcp()

    sys3d.rotate(alpha, beta, np.pi - gamma)
    sys3d.drawaxis()
    DrawSphere(sys3d, steps=100).drawit(along_x=True, axis=False, grid=True, bound=False, lw=1)

    screen.savesc(fh.nameit())
    screen.fallback()




mm.make_movie()
fh.del_img_seq()