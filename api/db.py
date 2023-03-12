import sqlite3
import os

class DBHandle:
    def __init__(self, file_path):
        self.db_file_path = file_path

        os.makedirs(os.path.dirname(self.db_file_path), exist_ok = True)

        self.db_handle = sqlite3.connect(file_path)
        self.db_cursor = self.db_handle.cursor()

        self.get_already_exist_tables()
    
    def get_already_exist_tables(self):
        self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name !='sqlite_sequence'")
        table_names = [i[0] for i in self.db_cursor.fetchall()]

        self.db_tables = {}

        for table_name in table_names:
            self.db_cursor.execute(f"SELECT * FROM {table_name}")
            columns = [column_data[0] for column_data in self.db_cursor.description]
            columns.remove("ORDER_ID")

            self.db_tables[table_name] = {}
            self.db_tables[table_name]["columns"] = tuple(columns)
    
    def refresh_existing_tables(self):
        return self.get_already_exist_tables()

    def create_table(self, table_name, columns: list):
        self.db_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, {', '.join(columns)})")
        self.db_handle.commit()

        self.db_tables[table_name] = {}
        self.db_tables[table_name]["columns"] = tuple(i.split()[0] for i in columns)

    def insert_value(self, table_name, values):
        if not values:
            return

        self.db_cursor.execute(f"INSERT INTO {table_name} " + 
                               f"VALUES (NULL, {', '.join(['?' for i in range(len(values))])})",
                               values)
        self.db_handle.commit()

    def read_value(self, table_name, columns = "*", many = 0, sort_reverse = False):
        self.db_cursor.execute(f"SELECT {columns if columns == '*' else ', '.join(columns)} " +
                               f"FROM {table_name} " +
                               f"{'ORDER BY ORDER_ID DESC' if sort_reverse else ''}")
        return self.db_cursor.fetchmany(many)
    
    def close(self):
        self.db_handle.close()
