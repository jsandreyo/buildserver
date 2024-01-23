######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" LOG HANDLER """

import logging

class LogsHandler:
    """ Provides means for configuration of logging. """
        # pylint: disable=too-few-public-methods

    formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s %(message)s")

    @staticmethod
    def get_logger(logger_name, log_file_path, log_level):
        """ sets up logging to a file """
        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(LogsHandler.formatter)
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger.addHandler(handler)
        return logger
