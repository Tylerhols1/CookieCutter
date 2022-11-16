import logging

class Logger():
    def __init__(self):
        logging.basicConfig(filename="info.log", filemode="w", level=logging.INFO)
        self = logging.getLogger()
        