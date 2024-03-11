import sqlite3
import datetime
from configparser import ConfigParser
from prettytable import PrettyTable
from myutils import type_library as T
from myutils import file_module as F
from logging import info
from cutie import select
from sqlite3 import Connection, connect
from sqlite3 import Cursor
from sqlite3 import Error # TODO
from environment.result import Result

class Environment:
    """Environment to this SQLite console"""
    
    MODELS_FOLDER = "models"
    
    def __init__(self) -> T.Self:
        info("Intializing Environment")
        configure_sqlite3()
        self.config = self.load_settings()  # Parse config.ini
        self.menu_dict = self.load_menu()   # Read list of DBs from config
        self.models = self.load_models()    # Load models (DTOs)
        self.connection: Connection = None
        # self.cursor: Cursor = None          Superfluous
        
    def load_settings(self) -> ConfigParser:
        """Parses config.ini and loads it up in Environment"""
        info("Loading config")
        config = ConfigParser(interpolation=None)
        config.read('config.ini')
        return config
        
    def load_menu(self) -> dict[str,str]:
        """Returns a dictionary of databases from config.ini"""
        info("Loading menu")
        items_view = self.config['Databases'].items()
        databases = {}
        for k,v in items_view:
            databases[k] = v
        return databases
        
    def load_models(self) -> list[T.ClassObject]:
        info("Loading models")
        return F.get_classes_from_folder(self.MODELS_FOLDER)
    
    def select_db(self) -> str:
        """Returns filepath of selected database"""
        db_names = list(self.menu_dict.keys()) + ["\033[0m"] # secretly adding caption to reset ansi styles #TODO Use myutils instead
        db_filepaths = list(self.menu_dict.values())         #   |
        print("\n\033[33mSelect database\033[0m:")           #   |
        index = select(                                      #   |
            options= db_names,                               #   V
            caption_indices=[len(db_names) - 1], # last is caption, does not count
            deselected_prefix="\033[0m   ",
            selected_prefix=" \033[92m>\033[7m\033[0m \033[7m" # 92 = green, 7 = reverse
            )
        # TODO
        # if position is last option
        return db_filepaths[index]
    
    def connect(self,data_source:str) -> None:
        info(f"Connecting to {data_source}...")
        con = connect(
            database=data_source,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        con.row_factory = sqlite3.Row # .execute() will now return Rows instead of tuples. Rows work similar to dict
        self.connection = con
        # self.cursor = self.connection.cursor() Superfluous
        info(f"Successfully connected to SQLite version {con.execute("SELECT sqlite_version()").fetchone()[0]}")
        
    def fetch_tables(self) -> Result:
        r = Result()
        query = r"""
            SELECT name FROM sqlite_master
            WHERE
            type = 'table' AND
            name NOT LIKE '$%' AND
            name NOT LIKE 'sqlite%';
            """
        tuples = self.cursor.execute(query).fetchall()
        for v in tuples:
                r.list_of_tables += [v[0]]
        return r
    
    def execute(self,query:str) -> Result:
        try:
            r = Result()
            c = self.cursor # Get cursor for reuse
            meta = c.execute(f"{query} LIMIT 0").description # See https://stackoverflow.com/questions/37495497/sql-query-with-limit-0
            data = c.execute(query)
            r.query = query
            r.columns = [column[0] for column in meta]
            r.rows = data.fetchall()
        except Error as e:
            r.error = e
        except Exception as e:
            r.error = e
        finally:
            return r
        
    def __str__(self):
        """
        String representation of the class.
        """
        return f"{self}"

#TODO Move this to another my file **************************************

#TODO Refer to https://docs.python.org/3/library/sqlite3.html#adapter-and-converter-recipes

def configure_sqlite3(self):
    sqlite3.register_adapter(datetime.date, adapt_date_iso)
    sqlite3.register_adapter(datetime.time, adapt_time_iso)
    sqlite3.register_adapter(datetime.datetime, adapt_datetime)
    sqlite3.register_adapter(MyFileObject, adapt_file)
    sqlite3.register_adapter(MyYAMLObject, adapt_yaml)
    sqlite3.register_converter("date", convert_date)
    sqlite3.register_converter("time", convert_time)
    sqlite3.register_converter("datetime", convert_datetime)
    sqlite3.register_converter("file", convert_file)
    sqlite3.register_converter("yaml", convert_yaml)

class MyFileObject:
    pass

class MyYAMLObject:
    pass

def adapt_date_iso(val):
    pass

def adapt_time_iso(val):
    pass

def adapt_datetime(val):
    pass

def adapt_file(val):
    pass

def adapt_yaml(val):
    pass

def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())

def convert_time(val):
    """Convert 24-hr time to datetime.time object."""
    iso_time_string = self.convert_to_iso(val) # TODO 2359 --> T23:59:00Z or sum like that
    return datetime.time.fromisoformat()

def convert_to_iso(val):
    raise NotImplementedError()

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())

def convert_file(val):
    pass

def convert_yaml(val):
    pass
