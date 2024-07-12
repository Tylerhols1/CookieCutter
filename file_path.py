import os
import logger as log
from logger import Info

class Folder:
    def __init__(self):
        self.curr_dir = os.path.dirname(os.path.realpath(__file__))
        self.image_dir = os.path.join(self.curr_dir, "images")
        self.image_list = os.listdir(self.image_dir)
        self.cropped_dir = os.path.join(self.curr_dir, "cropped")

    # TODO create os.isdir functions and stuff to get rid of os module in main
    # def create_cropped_dir(self, directory, logger):
    #     if not os.path.isdir(directory):
    #         os.mkdir(directory)
    #         log.write_info(Info.CREATE, self, logger, None)
    #     else:
    #         logger.info("THE DIRECTORY {} WAS ALREADY CREATED".format(directory))

    def get_curr_dir_path(self):
        return str(self.curr_dir)

    def get_image_dir_path(self):
        return str(self.image_dir)

    def get_image_list(self):
        return self.image_list

    def get_image_list_len(self):
        return len(self.image_list)

    def get_cropped_path(self):
        return str(self.cropped_dir)

    def set_cropped_path(self, cropped_dir):
        self.cropped_dir = cropped_dir
