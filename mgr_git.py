######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" REPO MANAGER """

import os
import subprocess as sp
import git
from git import Git
from git import Repo
import g_

class GitManager:
    """ Manages functions related to Git. """
        # pylint: disable=missing-function-docstring

    def __init__(self):
        g_.APP_LOGGER.info("GitManager instance initialized: %s", self)

    def do_shallow_clone(self, git_url, path):
        print(f"Cloning {git_url} into {path}...")
        Git().clone(git_url, path, depth=1, kill_after_timeout=60) # shallow clone

    def get_zip_files_using_git(self, git_url, path, zip_mgr):
        # SHORTCUT: same directory is used regardless repo specified;
        # ideally each would be cloned to its own subdir.
        dot_git_path = os.path.join(path, ".git")
        if not os.path.exists(dot_git_path) \
            and not os.path.isdir(dot_git_path):
            # discard any files added locally by wget, then
            # clone from remote repo to current working dir.
            print(f"Removing any zip files from {path} not added by Git...")
            zip_mgr.remove_all_zip_files(path)
            self.do_shallow_clone(git_url, path)
        else:
            repo = Repo(path)
            if git_url == repo.remotes.origin.url:
                # fetch current state from remote origin of current repo,
                # undo any local changes made by wget, then pull from
                # remote origin of current repo into current working dir.
                print(f"Resetting any local changes in {path} not made by Git...")
                repo.remotes.origin.fetch()
                repo.git.reset('--hard','origin')
                print(f"Pulling {repo.remotes.origin.url} into {path}...")
                repo.remotes.origin.pull()
                #Git(path).pull(git_url, kill_after_timeout=60) # alternative
            else:
                # discard all objects associated with previous repo,
                # then clone from new remote repo to current working dir.
                zip_mgr.remove_all_objs(path)
                self.do_shallow_clone(git_url, path)

    # SHORTCUT: use of CLI for wget rather than a Python API.
    def get_zip_file_using_wget(self, git_zip_url, path):
        print(f"Downloading {git_zip_url} into {path}...")
        wget_cmd = ["wget --timestamping --no-if-modified-since " + \
                    f"--quiet --directory-prefix={path} {git_zip_url} " + \
                    f"2>> {g_.GIT_ERR_LOG_FILE_PATH} " + \
                    f"1>> {g_.APP_OUT_LOG_FILE_PATH}"]
        return sp.getoutput(wget_cmd)

    def get_zip_files(self, url, path, zip_mgr):
        try:
            if url.endswith(".git"):
                print("Inputted URL ends in .git, will use gitpython to retrieve file(s).")
                self.get_zip_files_using_git(url, path, zip_mgr)
            elif url.endswith(".zip"):
                print("Inputted URL ends in .zip, will use wget to retrieve file.")
                self.get_zip_file_using_wget(url, path)
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"\nAn error occurred: {e}")
            g_.GIT_LOGGER.error("An error occurred: %s", e)
            raise e

    def get_commit_id_with_lib(self, path, subdir):
        prog_src_dir_path = os.path.join(path, subdir)
        repo = git.Repo(path=prog_src_dir_path)
        short_sha = None
        if os.path.exists(prog_src_dir_path) \
            and os.path.isdir(prog_src_dir_path):
            short_sha = repo.git.rev_parse(repo.head.commit.hexsha, short=7)
        return short_sha
