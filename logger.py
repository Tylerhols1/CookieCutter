import logging
import os
from enum import Enum


class Info(Enum):
    CREATE = 1
    SAVE = 2
    ACCESS = 3
    RESENT = 4
    EXECUTE = 5
    INDEX = 6
    TEXT = 7


def initialize_log():
    logging.basicConfig(filename="info.log", filemode="w", level=logging.INFO)
    logger = logging.getLogger()
    return logger


def write_info(info_type, folder, logger, comic_image):
    if info_type == info_type.CREATE:
        logger.info("CREATED CROPPED_DIR")

    elif info_type == info_type.SAVE:
        logger.info("SAVED {}".format(os.path.basename(comic_image.get_name())))

    elif info_type == info_type.ACCESS:
        logger.info("ACCESSING {} file(s) in images/\n".format(folder.get_image_list_len()))

    elif info_type == info_type.RESENT:
        logger.info(
            "RESENT {} THROUGH THRESHOLD {} TIME(S)\n".format(os.path.basename(comic_image.get_name()),
                                                              comic_image.get_mask()))

    elif info_type == info_type.EXECUTE:
        None
        # TODO Replace None type with actual execution times
        # logger.info("PROGRAM EXECUTED IN {}".format(FINAL_TIME))
    elif info_type == info_type.INDEX:
        logger.error("WENT OUT OF INDEX")

