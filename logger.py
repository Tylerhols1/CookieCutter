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

def initialize_log():
    logging.basicConfig(filename="info.log", filemode="w", level=logging.INFO)
    logger = logging.getLogger()
    return logger

def write_info(Info, folder, logger):
        if Info == Info.CREATE:
            logger.info("CREATED CROPPED_DIR")
        
        elif Info == Info.SAVE:
            logger.info("SAVED {}".format(os.path.basename(folder.NEW_FILE_NAME)))
        
        elif Info == Info.ACCESS:
            logger.info("ACCESSING {} file(s)\n".format(len(folder.IMAGE_LIST)))
        
        elif Info == Info.RESENT:
            logger.info("RESENT {} THROUGH THRESHOLD {} TIME(S)\n".format(os.path.basename(folder.IMAGE_NAME), folder.NEW_MASK))
        
        elif Info == Info.EXECUTE:
            logger.info("PROGRAM EXECUTED IN {}".format(FINAL_TIME))

        elif Info == Info.INDEX:
            logger.error("WENT OUT OF INDEX, INDEXING IS OUT OF {} TIME(S)".format(len(sorted_contours)))
   