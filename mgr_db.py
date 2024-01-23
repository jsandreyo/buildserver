######################################################
## Author: John Andreyo
## Copyright: Copyright (c) 2024. All rights reserved.
## License: Please see LICENSE file in program's root.
## Version: 2.0
######################################################

""" DB MANAGER """

import pymysql as mysql
import g_

class DBManager:
    """ Manages functions related the MySQL database. """
        # pylint: disable=missing-function-docstring
        # pylint: disable=broad-exception-caught
        # pylint: disable=too-many-arguments

    def __init__(self):
        self.connection = None
        self.cursor = None
        g_.APP_LOGGER.info("DBManager instance initialized: %s", self)

    def get_connection(self):
        if not self.connection:
            self.connection = mysql.connect(
                unix_socket="/var/run/mysqld/mysqld.sock",
                user = "root",
                database = "db",
                port = 3360,
                passwd = "D3v0p$2"
            )
        return self.connection

    def get_cursor(self):
        if not self.cursor:
            self.cursor = self.get_connection().cursor()
        return self.cursor

    def handle_error(self, e):
        print(f"\nAn error occurred: {e}")
        g_.DB_LOGGER.error("An error occurred: %s", e)
        raise e

    def close_connection(self):
        if self.connection and self.connection.open \
        and self.connection.ping(reconnect=False):
            msg = "Closing connection."
            print(msg)
            g_.APP_LOGGER.info(msg)
            self.connection.close()

    def get_all_records(self):
        try:
            conn = self.get_connection()
            curs = self.get_cursor()
            msg = "Fetching records..."
            print(msg)
            g_.WEB_LOGGER.info(msg)
            conn.commit()
            curs.execute("SELECT BuildReqID, CommitID, " +\
                         "ProgramName, Status, RegistrationID " +\
                         "FROM Programs;")
            records = curs.fetchall()
            conn.commit()
            print(records)
            g_.WEB_LOGGER.info(records)
        except Exception as e: # if exception
            return self.handle_error(e)
        else: # if no exception
            return records
        finally:
            self.close_connection()

    def check_exists(self, commit_id, prog_name):
        try:
            conn = self.get_connection()
            curs = self.get_cursor()
            msg = "Checking records..."
            print(msg)
            g_.APP_LOGGER.info(msg)
            conn.commit()
            curs.execute(f"SELECT EXISTS(SELECT * from \
                Programs WHERE CommitID='{commit_id}' AND \
                ProgramName='{prog_name}');")
            result = curs.fetchone()[0]
            conn.commit()
        except Exception as e: # if exception
            return self.handle_error(e)
        else: # if no exception
            return result
        finally:
            self.close_connection()

    def insert_record(self, commit_id, prog_name, build_stat):
        try:
            conn = self.get_connection()
            curs = self.get_cursor()
            msg = "Inserting record..."
            print(msg)
            g_.APP_LOGGER.info(msg)
            sql = "INSERT INTO Programs (CommitID, ProgramName, Status)" + \
                 f"VALUES ('{commit_id}', '{prog_name}', '{build_stat}');"
            conn.commit()
            curs.execute(sql)
            conn.commit()
            row_count = curs.rowcount
        except Exception as e: # if exception
            return self.handle_error(e)
        else: # if no exception
            return row_count
        finally:
            self.close_connection()

    def update_record(self, commit_id, prog_name, build_stat, reg_id, bin_obj):
        try:
            conn = self.get_connection()
            curs = self.get_cursor()
            msg = "Updating record..."
            print(msg)
            g_.APP_LOGGER.info(msg)
            sql = "UPDATE Programs SET Status=%s, RegistrationID=%s, " + \
                  "BinaryObject=%s WHERE CommitID=%s AND ProgramName=%s"
            vals = (build_stat, reg_id, bin_obj, commit_id, prog_name)
            conn.commit()
            curs.execute(sql, vals)
            conn.commit()
            row_count = curs.rowcount
        except Exception as e: # if exception
            return self.handle_error(e)
        else: # if no exception
            return row_count
        finally:
            self.close_connection()

    def set_param(self, param_name, param_val):
        try:
            curs = self.get_cursor()
            conn = self.get_connection()
            self.connection.ping(reconnect=True) # fix for race condition
            sql = "UPDATE Params SET ParamValue=%s WHERE ParamName=%s;"
            vals = (param_val, param_name)
            conn.commit()
            curs.execute(sql, vals)
            conn.commit()
            row_count = curs.rowcount
        except Exception as e: # if exception
            return self.handle_error(e)
        else: # if no exception
            return row_count
        finally:
            self.close_connection()

    def get_param(self, param_name):
        try:
            conn = self.get_connection()
            curs = self.get_cursor()
            conn.ping(reconnect=True) # fix for race condition
            conn.commit()
            curs.execute("SELECT ParamValue FROM Params " + \
                         f"WHERE ParamName='{param_name}';")
            value = curs.fetchone()[0]
            conn.commit()
        except Exception as e: # if exception
            return self.handle_error(e)
        else: # if no exception
            return value
        finally:
            self.close_connection()

    def remove_incomplete_records(self):
        try:
            conn = self.get_connection()
            curs = self.get_cursor()
            conn.commit()
            curs.execute("DELETE FROM Programs WHERE " + \
                        f"Status='{g_.INIT_BUILD_STATUS}' OR " + \
                        f"Status='{g_.PRE_BUILD_STATUS}'")
            conn.commit()
            row_count = curs.rowcount
        except Exception as e: # if exception
            return self.handle_error(e)
        else: # if no exception
            return row_count
        finally:
            self.close_connection()
