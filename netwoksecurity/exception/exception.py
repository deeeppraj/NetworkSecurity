import sys
from netwoksecurity.logging.logger import logging
'''
In oreder to test both my custom exception class and logger together
'''
 
 
class CustomException(Exception):
    def __init__(self,error,error_detail:sys):
        _,_,error_tb = error_detail.exc_info()
        self.error = error

        self.file_name = error_tb.tb_frame.f_code.co_filename
        self.line_no =  error_tb.tb_lineno

    def __str__(self):
            error_message = f"Error occured in {self.file_name} ,  line number {self.line_no} , {str(self.error)}"
            return error_message
    