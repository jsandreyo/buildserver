######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.1
######################################################

""" GLOBAL CONSTANTS """

import os
from utilities import Utilities

##################################################################################
# DIRECTORIES

PROJ_ROOT_PATH = ""

ZIP_FILE_DIR_NAME = "c_programs_zip"
SRC_CODE_DIR_NAME = "c_programs_src"

Utilities.create_working_dir(ZIP_FILE_DIR_NAME)
Utilities.create_working_dir(SRC_CODE_DIR_NAME)

ZIP_FILE_DIR = f"./{ZIP_FILE_DIR_NAME}"
SRC_CODE_DIR = f"./{SRC_CODE_DIR_NAME}"

ZIP_FILE_DIR_PATH = os.path.join(PROJ_ROOT_PATH, ZIP_FILE_DIR_NAME)
SRC_CODE_DIR_PATH = os.path.join(PROJ_ROOT_PATH, SRC_CODE_DIR_NAME)

##################################################################################
# LOGGERS

ERROR_LOGS_DIR_NAME = "error-logs"
OUTPUT_LOGS_DIR_NAME = "output-logs"

Utilities.create_working_dir(ERROR_LOGS_DIR_NAME)
Utilities.create_working_dir(OUTPUT_LOGS_DIR_NAME)

ERROR_LOGS_DIR = f"./{ERROR_LOGS_DIR_NAME}"
OUTPUT_LOGS_DIR = f"./{OUTPUT_LOGS_DIR_NAME}"

ZIP_ERR_LOG_FILE_NAME = "error-zip.log"
GIT_ERR_LOG_FILE_NAME = "error-git.log"
GCC_ERR_LOG_FILE_NAME = "error-gcc.log"
DB_ERR_LOG_FILE_NAME = "error-db.log"
WEB_OUT_LOG_FILE_NAME = "output-web.log"
APP_OUT_LOG_FILE_NAME = "output-app.log"

ZIP_ERR_LOG_FILE_PATH = os.path.join(ERROR_LOGS_DIR, ZIP_ERR_LOG_FILE_NAME)
GIT_ERR_LOG_FILE_PATH = os.path.join(ERROR_LOGS_DIR, GIT_ERR_LOG_FILE_NAME)
GCC_ERR_LOG_FILE_PATH = os.path.join(ERROR_LOGS_DIR, GCC_ERR_LOG_FILE_NAME)
DB_ERR_LOG_FILE_PATH = os.path.join(ERROR_LOGS_DIR, DB_ERR_LOG_FILE_NAME)
WEB_OUT_LOG_FILE_PATH = os.path.join(OUTPUT_LOGS_DIR, WEB_OUT_LOG_FILE_NAME)
APP_OUT_LOG_FILE_PATH = os.path.join(OUTPUT_LOGS_DIR, APP_OUT_LOG_FILE_NAME)

LOG_FORMAT = "[%(asctime)s] %(name)s %(levelname)s %(message)s"

ZIP_LOGGER = Utilities.get_logger("ZipManager", ZIP_ERR_LOG_FILE_PATH, "INFO", LOG_FORMAT)
GIT_LOGGER = Utilities.get_logger("GitManager", GIT_ERR_LOG_FILE_PATH, "INFO", LOG_FORMAT)
GCC_LOGGER = Utilities.get_logger("GCCManager", GCC_ERR_LOG_FILE_PATH, "INFO", LOG_FORMAT)
DB_LOGGER = Utilities.get_logger("DBManager", DB_ERR_LOG_FILE_PATH, "INFO", LOG_FORMAT)
WEB_LOGGER = Utilities.get_logger("WebLogger", WEB_OUT_LOG_FILE_PATH, "INFO", LOG_FORMAT)
APP_LOGGER = Utilities.get_logger("AppLogger", APP_OUT_LOG_FILE_PATH, "INFO", LOG_FORMAT)

##################################################################################
# STATUSES

INIT_BUILD_STATUS = "Queued"
PRE_BUILD_STATUS =  "Building..."
POST_BUILD_STATUS_SUCCESS = "SUCCESS"
POST_BUILD_STATUS_FAILURE = "FAILURE"
#CANCELED_BUILD_STATUS = "CANCELED"

##################################################################################
# MESSAGES

OD_IN_USE_MSG = "Another instance of this application in on-demand mode " + \
                "already running!  Please wait for it to complete or abort " + \
                "it before starting a new one."

AU_IN_USE_MSG = "Another instance of this application in auto mode already " + \
                "running!  Please abort it before starting a new one."

DONE_MSG = "\n******************* Build cycle complete *******************\n\r"

##################################################################################
# DEFAULTS

DEFAULT_INTERVAL_SECONDS = 180

DEFAULT_BUILD_CYCLE_MODE = "a" # automated mode

# e.g. https://github.com/<user>/<repo>/archive/<branch>.git
DEFAULT_GIT_REPO_URL = "https://github.com/jsandreyo/repo_b.git"
