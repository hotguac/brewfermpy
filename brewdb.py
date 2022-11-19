import mariadb as db

from logger import BrewfermLogger


"""
Creates a rotating log
"""
logger = BrewfermLogger('brewdb.py').getLogger()


class BrewDB:
    def __init__(self):
        logger.info("opening database")
        try:
            self.conn = db.connect(
                user='brewferm',
                password='barley',
                host='localhost',
                database='brewferm')

            self.cur = self.conn.cursor()
        except db.OperationalError as oe:
            logger.exception("brewdb.py-opening database- %s", oe)
        except Exception as inst:
            logger.exception(type(inst))
        except db.Error as e:
            logger.exception(
                "brewdb.py-Error connecting to database 'brewferm'- ", e)

    def add_data_point(self, beer_actual):
        try:
            self.cur.execute(
                ('insert into history (beer_actual, state_actual) '
                    'values (?, ?)', (beer_actual, 'paused')))
            self.conn.commit()
        except db.Warning as w:
            logger.warning("brewdb.py-inserting ", w)
        except Exception as e:
            logger.exception("brewdb.py-inserting- ", e)

    def current_settings(self):
        try:
            logger.debug("retrieving current settings")
            self.cur.execute(
                ('select ts, beer_target, beer_p, beer_i, beer_d, '
                    'chamber_p, chamber_i,chamber_d, hysteresis '
                    'from settings order by ts desc limit 1'))
            return db.rows
        except Exception as e:
            logger.error("Error getting settings %s", e)

    def cleanup(self):
        try:
            logger.debug('closing db connection')
            self.conn.close()
        except Exception as e:
            logger.error("Error closing databasde %s", e)

    def print_last(self, count):
        print(f"{count}")


if __name__ == "__main__":
    print("I'm just a module, not a main program!!")
