import os

class Folder:
    def __init__(self):
        self.CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.IMAGE_DIR = os.path.join(self.CURRENT_DIR, "images")
        self.IMAGE_LIST = os.listdir(self.IMAGE_DIR)
        self.CROPPED_DIR = os.path.join(self.CURRENT_DIR, "cropped")
        self.IMAGE_NAME = ""
        self.NEW_FILE_NAME = ""

        ## may move this to a mask class or something to separate the two 
        self.NEW_MASK = 0
    
    #TODO create os.isdir functions and stuff to get rid of os module in main