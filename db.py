import sqlite3
from config_db import name_db

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(name_db)
        self.conn.row_factory = sqlite3.Row
        self.create_tab_db()

#----------------------------------------------------------------------------------------------------------------------
# Creating tables and small functions

# Creating tables
    def create_tab_db(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS printers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ip_address TEXT NOT NULL UNIQUE,
                model TEXT,
                location TEXT
            )
        ''')

        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS cartridges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_code TEXT,
                color_name TEXT NOT NULL CHECK(color_name IN ('black', 'cyan', 'magenta', 'yellow')),
                quantity INTEGER NOT NULL DEFAULT 0,
                is_color BOOLEAN NOT NULL,
                printer_model TEXT NOT NULL,
                UNIQUE(printer_model, color_name)
            )
        ''')

        self.conn.commit()

# List tab
    def get_tab(self) -> list[str]:
        cur = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        return [row[0] for row in cur.fetchall()]

# Checking tables
    def check_tab(self, name_tab: str) -> bool:
        tab = self.get_tab()
        if not name_tab in tab:
            return False
        else:
            return True

# The list of columns in the table
    def get_columns(self, name_tab: str) -> list[str]:
        if not self.check_tab(name_tab):
            return []

        cur  = self.conn.execute(f"PRAGMA table_info({name_tab})")
        return [row[1] for row in cur.fetchall()]

#----------------------------------------------------------------------------------------------------------------------
# Basic table operations (reading the database, adding, deleting, and modifying data in the database)

# Reading the table
    def read_db(self, name_tab:str) -> list[dict]:
        if not self.check_tab(name_tab):
            return []

        cur = self.conn.execute(f'SELECT * FROM {name_tab}')
        return [dict(row) for row in cur.fetchall()]

# Adding data to a table
    def add_data(self, name_tab: str, data: dict) -> bool:
        if not self.check_tab(name_tab):
            return False

        columns = self.get_columns(name_tab)
        writable_columns = [col for col in columns if col != 'id']

        valid_data = {
            k: v for k, v in data.items()
            if k in writable_columns
        }

        cols = ', '.join(f'`{col}`' for col in valid_data.keys())
        placeholders = ', '.join('?' * len(valid_data))

        query = f"INSERT INTO `{name_tab}` ({cols}) VALUES ({placeholders})"

        self.conn.execute(query, list(valid_data.values()))
        self.conn.commit()
        return True

# Deleting data from a table
    def delete_data(self, name_tab: str, number_id: int) -> bool:
        if not self.check_tab(name_tab):
            return False

        with self.conn:
            self.conn.execute('DELETE FROM printers WHERE id = ?', (number_id,))
            return True

# Updating the data in the table
    def update_data(self, name_tab: str, number_id: int, data: dict) -> bool:
        if not self.check_tab(name_tab):
            return False

        columns = self.get_columns(name_tab)
        writable_columns = [col for col in columns if col != 'id']

        valid_data = {
            k: v for k, v in data.items()
            if k in writable_columns
        }
        set_clause = ', '.join(f'`{col}` = ?' for col in valid_data.keys())

        query = f"UPDATE `{name_tab}` SET {set_clause} WHERE `id` = ?"

        self.conn.execute(query, list(valid_data.values()) + [number_id])
        self.conn.commit()
        return True

# Deleting a table
    def drop_tab(self) -> bool:
        self.conn.execute(f"DROP TABLE cartridges;")
        self.conn.commit()
        return True
