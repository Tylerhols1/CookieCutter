import os

class Folder():
    def __init__(self):
        self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.IMAGE_DIR = os.path.join(self.CURRENT_DIR, "images")
        self.IMAGE_LIST = os.listdir(self.IMAGE_DIR)
        self.CROPPED_DIR = os.path.join(self.CURRENT_DIR, "cropped")
        self.IMAGE_NAME = ""

    #TODO create os.isdir functions and stuff to get rid of os module in main