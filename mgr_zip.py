######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" ZIP MANAGER """

import os
from zipfile import ZipFile
import shutil
import g_

class ZipManager:
    """ Manages functions related to the processing of zip file. """
        # pylint: disable=missing-function-docstring

    def __init__(self):
        g_.APP_LOGGER.info("ZipManager instance initialized: %s", self)

    def unzip_file(self, zip_file_path):
        with ZipFile(zip_file_path, "r") as zip_file:
            zip_file.extractall(path=g_.ZIP_FILE_DIR)

    def copy_unzipped_dir(self, from_path, to_path, unzipped_dir_name):
        source_subdir_path = os.path.join(from_path, unzipped_dir_name)
        target_subdir_path = os.path.join(to_path, unzipped_dir_name)
        if os.path.isdir(source_subdir_path):
            shutil.copytree(source_subdir_path, target_subdir_path, dirs_exist_ok=True)

    def remove_obj(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    def remove_all_unzipped_objs(self, path):
        for obj in os.scandir(path):
            if (obj.name != ".git") and (not obj.name.endswith(".zip")):
                self.remove_obj(obj)

    def remove_all_objs(self, path):
        for obj in os.scandir(path):
            self.remove_obj(obj)

    def remove_file(self, file_path):
        os.remove(file_path)
        print("Removed:", file_path)

    def remove_all_zip_files(self, path):
        for _root, _dirs, files in os.walk(path):
            for zip_file_name in files:
                prog_zip_file_path = os.path.join(path, zip_file_name)
                self.remove_file(prog_zip_file_path)
            break # only process first level of subdirs
