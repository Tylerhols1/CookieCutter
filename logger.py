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
    match Info: 
        case Info.CREATE:
            logger.info("CREATED CROPPED_DIR")
        
        case Info.SAVE:
            logger.info("SAVED {}".format(os.path.basename(folder.NEW_FILE_NAME)))
        
        case Info.ACCESS:
            logger.info("ACCESSING {} file(s)\n".format(len(folder.IMAGE_LIST)))
        
        case Info.RESENT:
            logger.info("RESENT {} THROUGH THRESHOLD {} TIME(S)\n".format(os.path.basename(folder.IMAGE_NAME), folder.NEW_MASK))
        
        case Info.EXECUTE:
            logger.info("PROGRAM EXECUTED IN {}".format(FINAL_TIME))

        case Info.INDEX:
            logger.error("WENT OUT OF INDEX, INDEXING IS OUT OF {} TIME(S)".format(len(sorted_contours)))
   