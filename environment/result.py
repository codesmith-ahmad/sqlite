from sqlite3 import Error
from prettytable import PrettyTable

class Result:
    def __init__(
        self,
        error: Error = None,
        query: str = None,
        list_of_tables: list[str] = [],
        table_name: str = None,
        columns: list[str] = [],
        columns_type: list[str] = [],
        rows: list[list] = []
    ):
        self.error = error
        self.query = query
        self.list_of_tables = list_of_tables
        self.table_name = table_name
        self.columns = columns
        self.columns_type = columns_type
        self.rows = rows
        
    def has_error(self) -> bool:
        """Check if the result contains an error."""
        return self.error is not None
    
    def display(self) -> None:
        
        if self.has_error():
            print(self.error)
        # print(self.table_name.upper()) CANNOT BE DONE #TODO
    
        table = PrettyTable()
        table.field_names = self.columns
        table.add_rows(self.rows)
        table.set_style(15)
        print(table)

    def __str__(self):
        return (
            f"Error: {self.error}\n"
            f"List of Tables: {self.list_of_tables}\n"
            f"Table Name: {self.table_name}\n"
            f"Columns: {self.columns}\n"
            f"Columns Type: {self.columns_type}\n"
            f"Rows: {self.rows}"
        )
