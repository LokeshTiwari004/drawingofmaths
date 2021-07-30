import subprocess
import pathlib


class MovieMaker:

    def __init__(self, img_seq_folder, frame_squence, movie_name, movie_location=None, movie_format='.mp4', framerate=30):
        self.framerate = framerate
        self.current_dir = str(pathlib.Path(__file__).parent.absolute())
        self.img_seq_path = self.current_dir + f'\\{img_seq_folder}\\' + str(frame_squence)
        if movie_location is None:
            self.output_file_path = str(pathlib.Path(__file__).parent.absolute().parent.absolute())\
                                    + '\\animations\\' + movie_name + movie_format
        else:
            self.output_file_path = movie_location + '\\' + movie_name + movie_format
        self.img_seq_folder = img_seq_folder


    def make_movie(self, width=1920, height=1080, video_codec='libx264', crf=20):
        cmd = f'ffmpeg -r {self.framerate} -f image2 -s {width}x{height} -i "{self.img_seq_path}" -vcodec {video_codec} -crf {crf} -pix_fmt yuv420p "{self.output_file_path}"'
        print(cmd)
        subprocess.check_output(cmd, shell=True)
