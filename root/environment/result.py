from sqlite3 import Error
import prettytable
from prettytable import PrettyTable, DOUBLE_BORDER, PLAIN_COLUMNS

class Result:
    
    MAX_TABLE_WIDTH = 150 # Terminal default is 120 columns
    MIN_CELL_WIDTH = 4
    
    def __init__(
        self,
        error: Error = None,
        query: str = None,
        table_name: str = None,
        columns: list[str] = [],
        rows: list[list] = []
    ):
        self.error = error
        self.query = query
        self.table = table_name
        self.columns = columns
        self.rows = rows
        
    def has_error(self) -> bool:
        """Check if the result contains an error."""
        return self.error is not None
    
    def display(self) -> None:
        if self.error == 0:
            error = "Query OK"
            table_name = self.table.upper()
        else:
            error = self.error
            table_name = "\033[31mERROR\033[0m"
    
        table = PrettyTable()
        table.set_style(DOUBLE_BORDER)
        table.max_table_width = self.MAX_TABLE_WIDTH
        table.min_width = self.MIN_CELL_WIDTH 
        table.custom_format['notes'] = self.truncate_and_remove_newlines # make notes smaller but #TODO need a way to get the text by itself
        table.custom_format['subjects'] = self.truncate_and_remove_newlines
        table.print_empty = True
        table.field_names = self.columns
        table.add_rows(self.rows)
        print(table_name)
        print(error)
        print(table)

    # Custom format function to remove new lines and truncate text
    def truncate_and_remove_newlines(self, field_name, value):
        MAX_LENGTH = 40  # Maximum length for the column
        # Remove carriage return and new lines
        cleaned_value = str(value).replace('\r\n', ';')
        # Truncate the text if it's too long
        truncated_value = (cleaned_value[:MAX_LENGTH - 3] + '...') if len(cleaned_value) > MAX_LENGTH else cleaned_value

        return truncated_value
    
    def __str__(self):
        return (
            f"Error: {self.error}\n"
            f"List of Tables: {self.list_of_tables}\n"
            f"Table Name: {self.table}\n"
            f"Columns: {self.columns}\n"
            f"Columns Type: {self.columns_type}\n"
            f"Rows: {self.rows}"
        )
