######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.1
######################################################

""" UTILITIES """

import os
import logging

class Utilities:
    """ Provides top level utility functions. """
        # pylint: disable=too-few-public-methods

    @staticmethod
    def create_working_dir(working_dir):
        """ dynamically creates an empty working directory 
        (otherwise a placeholder file would be needed in order 
        for directory to be committed to Git, which would 
        interfere with this application's file operations) """
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

    @staticmethod
    def get_logger(logger_name, log_file_path, log_level, log_format):
        """ sets up logging to a file """
        handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger.addHandler(handler)
        return logger
