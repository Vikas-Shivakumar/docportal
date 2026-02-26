import sys
import traceback
from logger.custom_logger import customLogger

logger = customLogger().get_logger(__file__)

class customException(Exception):
    def __init__(self, error_msg, error_details):
        _,_,exc_tb = error_details.exc_info()
        self.filename = exc_tb.tb_frame.f_code.co_filename
        self.lineno = exc_tb.tb_lineno
        self.error_msg = str(error_msg)
        self.traceback_str = "".join(traceback.format_exception(*error_details.exc_info()))

    def __str__(self):
        return f"""
        Error in [{self.filename}] at line [{self.lineno}]
        Message : {self.error_msg}
        Traceback " {self.traceback_str}
        """
    
if __name__ == "__main__":
    try:
        a=1/0
        print(a)
    except Exception as e:
        exc_error = customException(e, sys)
        logger.error(exc_error)
        raise exc_error
        

