from myutils                import logging_config
from logging                import info, exception, error
from configparser           import ConfigParser
from os                     import system         as S
from environment            import environment    as E
from environment            import result         as R
from cutie                  import select         as select
from sqlite3                import connect        as connect
from prettytable            import PrettyTable    as PT
from prettytable            import SINGLE_BORDER
from prettytable.colortable import ColorTable

def main():
    exit = False
    while not exit:
        env = E.Environment()
        db = env.select_db() # Begin select menu
        r = env.connect(db)  # Connect and return results
            
        config = ConfigParser(interpolation=None)
        config.read('config.ini')
        for k,v in config['Databases'].items():
            cls.DB_OPTIONS[k] = v
        cls.SETTINGS = config['ViewSettings']

if __name__ == "__main__":
    main()