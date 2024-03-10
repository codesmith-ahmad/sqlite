from configparser import ConfigParser
from myutils import type_library as T
from myutils import file_module as F
from logging import info
from cutie import select

class Environment:
    """Environment to this SQLite console"""
    
    MODELS_FOLDER = "models"
    
    def __init__(self) -> T.Self:
        info("Intializing Environment")
        self.config = self.load_settings()  # Parse config.ini
        self.menu_dict = self.load_menu()        # Read list of DBs from config
        self.models = self.load_models()    # Load models (DTOs)
        
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
        db_names = list(self.menu_dict.keys())
        db_filepaths = list(self.menu_dict.values())
        print("\n\033[?mSelect database\n\033[0m:\n")
        index = select(
            options= db_names + ["\033[0m"],
            caption_indices=[len(db_names) - 1],
            deselected_prefix="\033[0m   ",
            selected_prefix=" \033[92m>\033[7m\033[0m \033[7m" # 92 = green, 7 = reverse
            )
        return db_filepaths[index]
    
    def start(cls) -> None:
        cls.initialize()
        print("Select database:\n")
        list_of_options = list(cls.DB_OPTIONS.keys())
        idx = select(list_of_options,deselected_prefix="\033[0m   ",selected_prefix=" \033[92m> \033[7m")
        selected_option = list_of_options[idx]
        selected_database = cls.DB_OPTIONS[selected_option]
        command = ConnectionCommand(selected_database)
        report = Receiver.execute(command)
        cls.consume(report)
        cls.main_loop()       

    @classmethod
    def load_banner(cls):
        info("loading banner")
        banner = open(cls.SETTINGS['banner']).read()
        color = cls.SETTINGS['banner_color']
        cls.BANNER = f"\033[{color}m{banner}\033[0m"
         
    @classmethod
    def banner(cls) -> None:
        """Prints the banner"""
        print(cls.BANNER)
        
    @classmethod
    def menu_dict(cls):
        """Prints the menu"""
        print(cls.MENU)
        
    # @classmethod
    # def main_loop(cls):
    #     over = False
    #     cls.banner()
    #     cls.menu()
    #     while not over:
    #         user_input = input("> ")
    #         command = cls.process(user_input)
    #         report = Receiver.execute(command)
    #         system('cls')
    #         cls.banner()
    #         cls.consume(report)
    
    @classmethod
    def process(cls, raw_input):
        """
        Take raw input, refine it, creates command
        """
        try:
            refined_input = raw_input.strip().lower().split()
            if cls.mode == 'SQL' and refined_input[0] in cls.tables:
                command = SelectionCommand(
                    target=refined_input[0],
                    columns=['*']
                    )
        except Exception as e:
            exception(f"ERROR: SEEK HELP ||| {e}")
        finally:
            return command
        
    # @classmethod
    # def consume(cls, repor):
    #     match report.TYPE_OF_REPORT:
    #         case Operation.CONNECTION:
    #             return cls.consume_connection_report(report)
    #         case Operation.SELECTION:
    #             return cls.consume_selection_report(report)
    #         case Operation.INSERTION:
    #             return cls.consume_insertion_report(report)
    #         case Operation.ALTERATION:
    #             return cls.consume_alteration_report(report)
    #         case Operation.DELETION:
    #             return cls.consume_deletion_report(report)
    #         case Operation.GENERIC:
    #             exception("\033[31mUNKNOWN REPORT TYPE\033[0m")
    #             raise ValueError
    
    @classmethod
    def consume_connection_report(cls,report) -> None:
        cls.tables = report.list_of_tables
        msg = f"Success! Connected to SQLite version {report.sqlite_version}"
        info(msg)
        
    @classmethod
    def consume_selection_report(cls,report) -> None:
        table = report.table # string
        columns = report.headers # list of strings
        rows = report.query_results # list of list of strings and int
 
        table = PrettyTable()
        table.field_names = columns
        table.add_rows(rows)
        table.set_style(15)

        print(table)

    @classmethod
    def __str__(cls):
        """
        String representation of the class.
        """
        return f"{cls}"