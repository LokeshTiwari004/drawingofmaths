import cv2
import numpy as np


# generate screen
class Canvas:

    def __init__(self, width=1980, height=1080):
        self.width = width
        self.height = height
        self.main = np.zeros((height, width, 3), np.uint8)
        self.clone = None
        """ this checkpoint is just an extra property to hold a particular state of clone (exclusive)or main in case
            we want a branch but
            work on the current clone (exclusive)or main is incomplete"""
        self.checkpoint = None

    # this gives you a clone of the main screen
    def clonesc(self):
        self.clone = self.main.copy()

    # this gives you a checkpoint of the clone (exclusive)or main
    def createcp(self, which="main"):
        if which == 'clone':
            self.checkpoint = self.clone.copy()
        elif which == 'main':
            self.checkpoint = self.main.copy()
        else:
            RuntimeError(f'{which} is not available')

    # this put the clone (exclusive)or main(by default) to its last checkpoint
    def fallback(self, which="main"):
        if which == 'clone':
            self.clone = self.checkpoint.copy()
            self.checkpoint = None
        elif which == 'main':
            self.main = self.checkpoint.copy()
            self.checkpoint = None
        else:
            RuntimeError(f'{which} is not available')

    # save screen
    def savesc(self, img_name):
        cv2.imwrite(img_name, self.main)

    # save clone
    def savecl(self, img_name):
        cv2.imwrite(img_name, self.clone)

    # this is to show screen
    def showsc(self):
        cv2.imshow('MAIN SCREEN', self.main)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # this is to show clone
    def showcl(self):
        cv2.imshow('CLONE', self.clone)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
