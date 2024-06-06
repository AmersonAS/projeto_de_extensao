import sqlite3

class DatabaseManager:
    def __init__(self, db_name='temperature_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS temperatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def insert_temperature(self, temperature):
        self.cursor.execute('''
            INSERT INTO temperatures (temperature)
            VALUES (?)
        ''', (temperature,))
        self.conn.commit()

    def get_all_temperatures(self):
        self.cursor.execute('SELECT * FROM temperatures')
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
