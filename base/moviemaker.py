import subprocess
import pathlib


class MovieMaker:

    def __init__(self, frame_seq_path, movie_name, movie_location=None, movie_format='.mp4', framerate=30):
        self.framerate = framerate
        self.frame_seq_path = frame_seq_path
        if movie_location is None:
            self.output_file_path = str(pathlib.Path(__file__).parent.absolute().parent.absolute())\
                                    + '\\animations\\' + movie_name + movie_format
        else:
            self.output_file_path = movie_location + '\\' + movie_name + movie_format


    def make_movie(self, width=1920, height=1080, video_codec='libx264', crf=20):
        cmd = f'ffmpeg -r {self.framerate} -f image2 -s {width}x{height} -i "{self.frame_seq_path}" -vcodec {video_codec} -crf {crf} -pix_fmt yuv420p "{self.output_file_path}"'
        subprocess.check_output(cmd, shell=True)
