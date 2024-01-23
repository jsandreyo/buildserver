######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" GCC MANAGER """

import os
import subprocess as sp
import g_

class GCCManager:
    """ Manages functions related to the GCC Compiler. """
        # pylint: disable=missing-function-docstring

    def __init__(self):
        g_.APP_LOGGER.info("GCCManager instance initialized: %s", self)

    # SHORTCUT: use of CLI for make rather than a Python API.
    def compile_program(self, path, subdir):
        prog_src_dir_path = os.path.join(path, subdir)
        compile_cmd = [f"make all -s -C {prog_src_dir_path} " + \
                       f"2>> {g_.GCC_ERR_LOG_FILE_PATH} " + \
                       f"1>> {g_.APP_OUT_LOG_FILE_PATH}"]
        compile_completed_proc = sp.run(compile_cmd, shell=True, check=False)
        return compile_completed_proc.returncode # let con't on error ---^

    def run_program(self, path, subdir):
        prog_src_dir_path = os.path.join(path, subdir)
        # SHORTCUT: subdir name doubles over as file name
        prog_file_path = os.path.join(prog_src_dir_path, subdir)
        run_cmd = [f"./{prog_file_path} " + \
                   f"2>> {g_.GCC_ERR_LOG_FILE_PATH} " + \
                   f"1>> {g_.APP_OUT_LOG_FILE_PATH}"]
        run_completed_proc = sp.run(run_cmd, shell=True, check=False)
        return run_completed_proc.returncode

    # SHORTCUT: use of CLI for make rather than a Python API.
    def clean_program(self, path, subdir):
        prog_src_dir_path = os.path.join(path, subdir)
        clean_cmd = [f"make clean -s -C {prog_src_dir_path} " + \
                     f"2>> {g_.GCC_ERR_LOG_FILE_PATH} " + \
                     f"1>> {g_.APP_OUT_LOG_FILE_PATH}"]
        clean_completed_proc = sp.run(clean_cmd, shell=True, check=False)
        return clean_completed_proc.returncode

    def clean_all_compiled_programs(self, path):
        for _root, dirs, _files in os.walk(path):
            for subdir in dirs:
                self.clean_program(path, subdir)
            break # only process first level of subdirs
