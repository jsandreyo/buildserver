######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" REGISTRAR """

import os
import uuid
from time import sleep
import g_

class Registrar:
    """ Main controlling module for registering C program
        files via this build server. Registration process
        includes the download, deployment, compiling, and
        cataloging of associated objects and data. """
        # pylint: disable=missing-function-docstring

    def __init__(self, git_mgr_inst, zip_mgr_inst,
                        gcc_mgr_inst, db_mgr_inst):
        self.git_mgr_inst = git_mgr_inst
        self.zip_mgr_inst = zip_mgr_inst
        self.gcc_mgr_inst = gcc_mgr_inst
        self.db_mgr_inst = db_mgr_inst
        g_.APP_LOGGER.info("Registrar instance initialized: %s", self)

    def register_programs(self, url):
        # SHORTCUT: batch style processing is used also for just a single zip file;
        # ideally, the singular forms of the methods below would be used directly.
        # SHORTCUT: in some cases where unexpected processing errors occur for
        # a given program, processing of remaining programs is skipped; ideally
        # processing of remaining programs would always continue.S
        print("--- CLEANING UP PROGRAMS ---")
        self.cleanup_programs()

        print("--- PULLING PROGRAMS ---")
        self.pull_programs(url, g_.ZIP_FILE_DIR_PATH, self.zip_mgr_inst)

        print("--- DEPLOYING PROGRAMS ---")
        self.deploy_programs(g_.ZIP_FILE_DIR_PATH, g_.SRC_CODE_DIR_PATH)

        print("--- PROCESSING PROGRAMS ---")
        self.process_programs(g_.SRC_CODE_DIR_PATH)

        print("--- RUNNING PROGRAMS ---")
        self.run_programs(g_.SRC_CODE_DIR_PATH)

        print("--- CLEANING UP PROGRAMS ---")
        self.cleanup_programs()

    def pull_programs(self, url, path, zip_mgr):
        self.git_mgr_inst.get_zip_files(url, path, zip_mgr)

    def submit_initial_info(self, path, subdir):
        shorthash = self.git_mgr_inst.get_commit_id_with_lib(path, subdir)
        self.db_mgr_inst.insert_record(shorthash, subdir, g_.INIT_BUILD_STATUS)
        sleep(3) # allow user to see changes of state

    def deploy_program(self, from_path, file_name, to_path):
        try:
            file_path = os.path.join(from_path, file_name)
            if file_name.endswith(".zip"):
                self.zip_mgr_inst.unzip_file(file_path)
                unzipped_dir_name = os.path.splitext(file_name)[0] # file name prefix
                shorthash = self.git_mgr_inst.get_commit_id_with_lib(from_path, unzipped_dir_name)
                result = self.db_mgr_inst.check_exists(shorthash, unzipped_dir_name)
                if result == 0 and shorthash != "": # id not yet exists in db and is not undefined
                    self.zip_mgr_inst.copy_unzipped_dir(from_path, to_path, unzipped_dir_name)
                    self.submit_initial_info(from_path, unzipped_dir_name)
                else:
                    print(f"Already processed commit {shorthash} for {unzipped_dir_name}. " + \
                        "No work to do.")
            else:
                print(f"Removing non-zip file: {file_path}")
                self.zip_mgr_inst.remove_file(file_path)
        except Exception: # pylint: disable=broad-exception-caught
            print(f"Removing invalid zip file: {file_path}")
            self.zip_mgr_inst.remove_file(file_path)
            #raise e # use this if global failure-rollback behavior is desired.

    def deploy_programs(self, from_path, to_path):
        for _root, _dirs, files in os.walk(from_path):
            for file_name in files:
                self.deploy_program(from_path, file_name, to_path)
            break # only process first level of subdirs

    def submit_prebuild_info(self, subdir, shorthash):
        self.db_mgr_inst.update_record(shorthash, subdir,
                                       g_.PRE_BUILD_STATUS,
                                       None, None)
        sleep(3) # allow user to see changes of state

    def submit_postbuild_info(self, result, path, subdir, shorthash):
        prog_name = subdir
        commit_id = shorthash
        build_stat = "N/A"
        reg_id = None
        if result == 0:
            reg_id = uuid.uuid4()
            build_stat = g_.POST_BUILD_STATUS_SUCCESS
            binary_obj = bytearray()
            bin_obj_rel_file_path = os.path.join(path, subdir, prog_name)
            with open(bin_obj_rel_file_path, "rb") as file:
                binary_obj = file.read()
            self.db_mgr_inst.update_record(commit_id, prog_name,
                                           build_stat, reg_id, binary_obj)
        else:
            build_stat = g_.POST_BUILD_STATUS_FAILURE

            self.db_mgr_inst.update_record(commit_id, prog_name,
                                           build_stat, None, None)
        sleep(3) # allow user to see changes of state

    def process_program(self, path, subdir):
        shorthash = self.git_mgr_inst.get_commit_id_with_lib(path, subdir)
        self.submit_prebuild_info(subdir, shorthash)
        result = self.gcc_mgr_inst.compile_program(path, subdir)
        self.submit_postbuild_info(result, path, subdir, shorthash)

    def process_programs(self, path):
        for _root, dirs, _files in os.walk(path):
            for subdir in dirs:
                self.process_program(path, subdir)
            break # only process first level of subdirs

    def run_program(self, path, subdir):
        self.gcc_mgr_inst.run_program(path, subdir)

    def run_programs(self, path):
        for _root, dirs, _files in os.walk(path):
            for subdir in dirs:
                self.run_program(path, subdir)
            break # only process first level of subdirs

    def cleanup_programs(self):
        self.gcc_mgr_inst.clean_all_compiled_programs(g_.SRC_CODE_DIR_PATH)
        self.zip_mgr_inst.remove_all_unzipped_objs(g_.ZIP_FILE_DIR_PATH)
        self.zip_mgr_inst.remove_all_unzipped_objs(g_.SRC_CODE_DIR_PATH)
