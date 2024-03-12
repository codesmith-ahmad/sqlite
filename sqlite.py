from myutils                import logging_config
from os                     import system         as S
from environment            import environment    as E
from environment            import result         as R
from cutie                  import select         as select
from sqlite3                import connect        as connect
from prettytable            import PrettyTable    as PT
from prettytable            import SINGLE_BORDER
from prettytable.colortable import ColorTable

def main():
    env = E.Environment()
    main_menu(env) # loop

def main_menu(e: E.Environment):
    exit_flag = 0
    while exit_flag == 0:
        filepath = e.select_db() # Begin select menu #TODO MOVE select_db outside Environement. initialzie Env only when filepath acquired
        e.connect(filepath)      # Connect to selected db
        e.fetch_tables()         # Extract all tables to know whats available
        exit_flag = sql_loop(e)
        r = R.Result()

def sql_loop(e: E.Environment) -> int:
    exit_flag = 0
    print("DO NOT FORGET TO COMMIT UPDATES")
    while exit_flag == 0:
        q = input(r"SQL> ")
        query = q.strip().lower()
        match query:
            case 'exit': 
                e.connection.close()
                return 1
            case 'close':
                e.connection.close()
                return 0
            case 'help':
                print_tables(e.tables)
            case _:
                r = e.execute(query)
                r.display()

def print_tables(tables):
    separator = "------------"
    print(separator + "\033[33m")
    for table in tables:
        print(table)
    print("\033[0m" + separator)

if __name__ == "__main__":
    main()
