######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" BUILD SERVER """

import os
import sys
import signal
import argparse
import time
from time import sleep
from flask import Flask
import inst_factory
import g_

factory = inst_factory.InstanceFactory()
g_.APP_LOGGER.info("InstanceFactory instance created (pid: %s): %s", os.getpid(), factory)

class BusinessLayer:
    """ Encompasses entry point logic for build server CLI,
    processes user inputs, and performs application cycling. """

    @staticmethod
    def wait_for_process_timer(proc_param, proc_title, registrar):
        """ Displays timer and waiting msg until given param is true. """
        proc_was_in_prog = False
        start = time.perf_counter_ns()
        while registrar.db_mgr_inst.get_param(proc_param):
            print(f"\rWaiting for {proc_title} to finish..." + \
                f"{(time.perf_counter_ns() - start) / 10**9}s" + \
                "\033[?25l", end="", flush=True) # print timer in place; hide cursor.
            proc_was_in_prog = True
        if proc_was_in_prog:
            print("\n")

    @staticmethod
    def _perform_on_demand_mode_build_cycle(registrar, args):
        """ Performs on-demand mode build cycle and related processes. """
        print("\nStarting one-off build...\r\n")
        proc_to_wait_for_param = "is_a_cycle_in_prog"
        proc_to_wait_for_title = "auto mode build cycle"
        BusinessLayer.wait_for_process_timer(proc_to_wait_for_param,
                                             proc_to_wait_for_title,
                                             registrar)
        registrar.db_mgr_inst.set_param("is_o_mode_in_use", 1)
        registrar.register_programs(args.url)
        registrar.db_mgr_inst.set_param("is_o_mode_in_use", 0)
        print(g_.DONE_MSG)

    @staticmethod
    def _perform_auto_mode_build_cycle(registrar, args):
        """ Performs auto mode build cycle and related processes. """
        print("Starting intermittent build...\n")
        sleep(2)
        proc_to_wait_for_param = "is_o_mode_in_use"
        proc_to_wait_for_title = "on-demand mode build cycle"
        BusinessLayer.wait_for_process_timer(proc_to_wait_for_param,
                                             proc_to_wait_for_title,
                                             registrar)
        registrar.db_mgr_inst.set_param("is_a_cycle_in_prog", 1)
        registrar.register_programs(args.url)
        registrar.db_mgr_inst.set_param("is_a_cycle_in_prog", 0)
        print(g_.DONE_MSG)

    @staticmethod
    def clean_up_dirty(args, registrar):
        """ Resets parameters representing states of respective processes. """
        print("\nReverting to clean state...")
        if args.mode in ("o", "on-demand"):
            registrar.db_mgr_inst.set_param("is_o_mode_in_use", 0)
        if args.mode in ("a", "auto"):
            registrar.db_mgr_inst.set_param("is_a_mode_in_use", 0)
            registrar.db_mgr_inst.set_param("is_a_cycle_in_prog", 0)
        registrar.cleanup_programs()
        registrar.db_mgr_inst.remove_incomplete_records()
        print("Graceful termination complete.")

    @staticmethod
    def signal_handler(sig, frame): # pylint: disable=unused-argument
        """ Captures Ctrl-C signal and exits gracefully. """
        BusinessLayer.clean_up_dirty(BusinessLayer.args, BusinessLayer.registrar)
        print("\nCtrl-C detected! Exiting...")
        sys.exit()

    def main(): # pylint: disable=no-method-argument
        """ Entry point into Python app (BIZ). """
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mode",
                            dest = "mode",
                            default = g_.DEFAULT_BUILD_CYCLE_MODE,
                            help="Mode: [a]uto specifies continuous build cycles; [o]n-demand " + \
                                 "specifies a single build cycle.  Defaults to auto mode if " + \
                                 "not specified.")
        parser.add_argument("-u", "--url",
                            dest = "url",
                            default = g_.DEFAULT_GIT_REPO_URL,
                            help="Url: the address of remote repository hosting self-" + \
                                 "contained C programs.  Defaults to " + \
                                 "https://github.com/jsandreyo/repo_b.git if not specified.")
        parser.add_argument("-i", "--interval",
                            dest = "seconds",
                            default = g_.DEFAULT_INTERVAL_SECONDS,
                            help="Interval: the number of seconds between continuous build " + \
                                 "cycles.  Defaults to 180 seconds if not specified. Ignored " + \
                                 "if specified with on-demand mode.")

        BusinessLayer.args = parser.parse_args()
        BusinessLayer.registrar = factory.get_registrar()

        def _start_on_demand(registrar, args):
            if not registrar.db_mgr_inst.get_param("is_o_mode_in_use"):
                BusinessLayer._perform_on_demand_mode_build_cycle(registrar, args)
            else:
                print(g_.OD_IN_USE_MSG)
                sys.exit()

        def _start_auto(registrar, args):
            if not registrar.db_mgr_inst.get_param("is_a_mode_in_use"):
                registrar.db_mgr_inst.set_param("is_a_mode_in_use", 1)
                s = int(args.seconds)
                print(f"\nBuild cycles will occur every {s / 60} " + \
                    "minute(s) upon completion of previous.\n")
                sleep(2)
                while True:
                    for i in reversed(range(s)):
                        if i == s - 1:
                            BusinessLayer._perform_auto_mode_build_cycle(registrar, args)
                        print(f"\rNext build cycle starts in [{i:02d}] seconds.",
                            end="\r", flush=True) # print countdown in place;
                        sleep(1)
                        if i == 0: print("\n") # pylint: disable=multiple-statements
            else:
                print(g_.AU_IN_USE_MSG)
                sys.exit()

        try:
            if BusinessLayer.args.mode in ("o", "on-demand"):
                _start_on_demand(BusinessLayer.registrar, BusinessLayer.args)
            elif BusinessLayer.args.mode in ("a", "auto"):
                _start_auto(BusinessLayer.registrar, BusinessLayer.args)
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"\nAn error occurred: {e}")
            g_.APP_LOGGER.error("An error occurred: %s", e)
            BusinessLayer.clean_up_dirty(BusinessLayer.args, BusinessLayer.registrar)
        finally:
            sys.exit()

def set_project_path(module_file_name):
    """ Determines absolute path leading to base directory of project. """
    g_.PROJ_ROOT_PATH = os.path.dirname(module_file_name)

if __name__ == "__main__":
    set_project_path(sys.modules[__name__].__file__)
    g_.APP_LOGGER.info("Project root: %s\n", g_.PROJ_ROOT_PATH)
    signal.signal(signal.SIGINT, BusinessLayer.signal_handler)
    BusinessLayer.main()

#################################################################

if __name__ != "__main__":
    buildserver_con = Flask(__name__)
    init_msg = f"Flask buildserver_con initialized: {buildserver_con}\n" + \
                "Waiting for client to connect..."
    print(init_msg)
    g_.WEB_LOGGER.info(init_msg)

class PresentationLayer: # pylint: disable=too-few-public-methods
    """ Encompasses entry point logic for build server GUI and
    composes a web page for displaying information related to
    the building and registration of C programs performed by
    the CLI. """

    @staticmethod
    def _build_html():
        """ Dynamically builds web page content in the
            form of HTML based on retrieved data records. """
        html = ""
        records = factory.get_db_mgr().get_all_records()
        if records:
            msg = "Converting records..."
            print(msg)
            g_.WEB_LOGGER.info(msg)
            for row in records:
                html = html + "<tr>"
                for col in row:
                    html = html + "<td>" + str(col) + "</td>"
                html = html + "</tr>"
        return html

    @staticmethod
    def _fill_template(html):
        """ Reads in a templated HTML file, dynamically formats
            it with dynamic content, then returns it as a string
            to be routed to a designated URL by Flask. """
        msg = "Building webpage..."
        print(msg)
        g_.WEB_LOGGER.info(msg)
        with open(file="./static/template.html", mode="r",
                  encoding="utf-8") as template:
            return template.read().format(content=html)

    # pylint: disable=no-method-argument
    @buildserver_con.route("/")
    def send_webpage():
        """ Entry point into Flask app (GUI). """
        records = PresentationLayer._build_html()
        webpage = PresentationLayer._fill_template(records)
        msg = "Serving webpage..."
        print(msg)
        g_.WEB_LOGGER.info(msg)
        return webpage
