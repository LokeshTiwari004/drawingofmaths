import os
import subprocess
import pathlib


class Handle_frames:

    def __init__(self, name='anim', scene=1, padding_digits=6, img_format='.png'):
        self.img_format = img_format
        self.name = name
        self.scene = str(scene)
        self.universal_dir = pathlib.Path(__file__).parent.absolute().parent.absolute()

        os.makedirs(str(self.universal_dir) + '\\' + self.name)
        self.frame_seq_folder = str(self.universal_dir) + "\\" + self.name

        if len(self.scene) == 1:
            self.scene = '00' + self.scene
        elif len(self.scene) == 2:
            self.scene = '0' + self.scene

        self.padding_digits = padding_digits

        self.frame_num = 0
        self.frame_skeleton = self.name + '.' + self.scene + '.'
        self.frame_name = self.frame_skeleton + (self.padding_digits - 1) * '0' + str(self.frame_num) + self.img_format

        self.frame_seq_path = self.frame_seq_folder + '\\' + self.name + '.' + str(self.scene) + '.' + '%' + '0' + str(self.padding_digits) + 'd' + self.img_format

    def nameit(self, with_location=True):
        self.frame_num += 1
        digits_in_frame_num = len(str(self.frame_num))
        self.frame_name = self.frame_skeleton + (self.padding_digits - digits_in_frame_num) * '0' + str(self.frame_num) + self.img_format
        if with_location:
            return self.frame_seq_folder + "\\" + self.frame_name
        else:
            return self.frame_name

    def del_img_seq(self):
        subprocess.check_output('rmdir /s /q ' + str(self.frame_seq_folder), shell=True)
