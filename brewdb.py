#!/usr/bin/python3
import logging
import sys
from time import sleep
import mariadb as db

class BrewDB:

    def __init__(self):
        logging.info("brewdb.py-opening database")
        try:
            self.conn = db.connect(
                user='brewferm', password='barley', host='localhost', database='brewferm')
            self.cur = self.conn.cursor()
        except db.OperationalError as oe:
            logging.exception("brewdb.py-opening database- %s",oe)
        except Exception as inst:
            logging.exception(type(inst))    # the exception instance
            logging.error(inst.args)     # arguments stored in .args
            logging.error(inst)          # __str__ allows args to be printed directly,
                                # but may be overridden in exception subclasses
        except db.Error as e:          
            logging.exception("brewdb.py-Error connecting to database 'brewferm'- ", e)

    def add_data_point(self, beer_actual):
        try:
            if self.cur == None:
                __init__(self)
                
            self.cur.execute(
                "insert into history (beer_actual, state_actual) values (?, ?)", (beer_actual, 'paused'))
            self.conn.commit()
        except db.Warning as w:
            logging.warning("brewdb.py-inserting ", w)
        except Error as e:
            logging.exception("brewdb.py-inserting- ",e)

    def current_settings(self):
        try:
            logging.debug("retrieving current settings")
            self.cur.execute('select ts, beer_target, beer_p, beer_i, beer_d, chamber_p, chamber_i,chamber_d, hysteresis from settings order by ts desc limit 1')
            return db.rows
        except Error as e:
            logging.error("Error getting settings %s", e)

    def cleanup(self):
        try:
            logging.debug('closing db connection')
            self.conn.close()
        except Error as e:
            logging.error("Error closing databasde %s", e)

    def print_last(self, count):
        print(f"{count}")

if __name__ == "__main__":
    print(f"I'm just a module, not a main program!!")    


# MariaDB [brewferm]> desc history;
# +----------------+-------------------------------------+------+-----+----------------------+--------------------------------+
# | Field          | Type                                | Null | Key | Default              | Extra                          |
# +----------------+-------------------------------------+------+-----+----------------------+--------------------------------+
# | ts             | timestamp(6)                        | NO   |     | current_timestamp(6) | on update current_timestamp(6) |
# | beer_actual    | decimal(4,1)                        | YES  |     | NULL                 |                                |
# | beer_target    | decimal(4,1)                        | YES  |     | NULL                 |                                |
# | chamber_actual | decimal(4,1)                        | YES  |     | NULL                 |                                |
# | chamber_target | decimal(4,1)                        | YES  |     | NULL                 |                                |
# | state_actual   | enum('paused','cool','idle','heat') | YES  |     | NULL                 |                                |
# | state_target   | enum('paused','cool','idle','heat') | YES  |     | NULL                 |                                |
# | control_signal | decimal(4,1)                        | YES  |     | NULL                 |                                |
# | beer_p         | float                               | YES  |     | NULL                 |                                |
# | beer_i         | float                               | YES  |     | NULL                 |                                |
# | beer_d         | float                               | YES  |     | NULL                 |                                |
# | chamber_p      | float                               | YES  |     | NULL                 |                                |
# | chamber_i      | float                               | YES  |     | NULL                 |                                |
# | chamber_d      | float                               | YES  |     | NULL                 |                                |
# +----------------+-------------------------------------+------+-----+----------------------+--------------------------------+
# 14 rows in set

# MariaDB [brewferm]> desc changes;
# +-------------+--------------+------+-----+----------------------+--------------------------------+
# | Field       | Type         | Null | Key | Default              | Extra                          |
# +-------------+--------------+------+-----+----------------------+--------------------------------+
# | ts          | timestamp(6) | NO   |     | current_timestamp(6) | on update current_timestamp(6) |
# | beer_target | decimal(4,1) | YES  |     | NULL                 |                                |
# | beer_p      | float        | YES  |     | NULL                 |                                |
# | beer_i      | float        | YES  |     | NULL                 |                                |
# | beer_d      | float        | YES  |     | NULL                 |                                |
# | chamber_p   | float        | YES  |     | NULL                 |                                |
# | chamber_i   | float        | YES  |     | NULL                 |                                |
# | chamber_d   | float        | YES  |     | NULL                 |                                |
# | hysteresis  | float        | YES  |     | NULL                 |                                |
# +-------------+--------------+------+-----+----------------------+--------------------------------+
# 9 rows in set
