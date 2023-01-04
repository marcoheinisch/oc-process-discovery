import sqlite3
import pandas as pd

class SqlLiteConnection():
    db_path = "sap_tables.sqlite"
    conn = None    
    
    def push_tables(self, tables: dict) -> None:
        """Pushes a dictionary of tables with dataframes to the database"""
        self.conn = sqlite3.connect(self.db_path)  
        for table, df in tables.items():
            table_name = str(table).upper()
            df.to_sql(table_name, self.conn, if_exists='replace')
        self.conn.close()
    
    def get_table(self, table_name: str) -> pd.DataFrame:
        """Returns a dataframe of the table if stored in sqlite database"""
        self.conn = sqlite3.connect(self.db_path)  
        df = pd.read_sql(f"SELECT * FROM {table_name.upper()}", self.conn)
        self.conn.close()
        return df
    
    def get_tables(self) -> dict:
        """Returns a dict with all dataframes stored in sqlite database"""
        self.conn = sqlite3.connect(self.db_path)  
        dfs = {}
        res = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res.fetchall():
            name = name[0].upper()
            df = df = pd.read_sql(f"SELECT * FROM {name.upper()}", self.conn)
            dfs[name] = df
        self.conn.close()
        return dfs
