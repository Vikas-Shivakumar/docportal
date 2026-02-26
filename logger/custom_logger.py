import logging
import os
from datetime import datetime

class customLogger:
    def __init__(self, log_dir='logs_dir'):
        self.log_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        log_file_path = os.path.join(self.log_dir, log_file)

        logging.basicConfig(
            filename=log_file_path,
            level = logging.INFO

        )

    def get_logger(self,name=__file__):
        return logging.getLogger(os.path.basename(name))
    

if  __name__ == "__main__":
    logger = customLogger()
    logger = logger.get_logger(__file__)
    logger.info("custom logger is initialized")