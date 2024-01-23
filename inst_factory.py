######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" INSTANCE FACTORY """

from mgr_git import GitManager
from mgr_zip import ZipManager
from mgr_gcc import GCCManager
from mgr_db import DBManager
from registrar import Registrar
from g_ import APP_LOGGER

class InstanceFactory:
    """ Produces instances of various classes. """
        # pylint: disable=missing-function-docstring

    def __init__(self):
        self.repo_mgr_inst = None
        self.zip_mgr_inst = None
        self.gcc_mgr_inst = None
        self.db_mgr_inst = None
        self.registrar_inst = None
        APP_LOGGER.info("InstanceFactory instance initialized: %s", self)

    def get_repo_mgr(self):
        if not self.repo_mgr_inst:
            self.repo_mgr_inst = GitManager()
            APP_LOGGER.info("GitManager instance created! %s", self.repo_mgr_inst)
        return self.repo_mgr_inst

    def get_zip_mgr(self):
        if not self.zip_mgr_inst:
            self.zip_mgr_inst = ZipManager()
            APP_LOGGER.info("ZipManager instance created! %s", self.zip_mgr_inst)
        return self.zip_mgr_inst

    def get_gcc_mgr(self):
        if not self.gcc_mgr_inst:
            self.gcc_mgr_inst = GCCManager()
            APP_LOGGER.info("GCCManager instance created! %s", self.gcc_mgr_inst)
        return self.gcc_mgr_inst

    def get_db_mgr(self):
        if not self.db_mgr_inst:
            self.db_mgr_inst = DBManager()
            APP_LOGGER.info("DBManager instance created! %s", self.db_mgr_inst)
        return self.db_mgr_inst

    def get_registrar(self):
        if not self.registrar_inst:
            self.registrar_inst = Registrar(
                self.get_repo_mgr(), self.get_zip_mgr(),
                self.get_gcc_mgr(), self.get_db_mgr())
            APP_LOGGER.info("Registrar instance created! %s", self.registrar_inst)
        return self.registrar_inst
