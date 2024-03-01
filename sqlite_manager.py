import json
import sqlite3


class FacebookRepository:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect('facebook.db')
        self.cursor = self.connection.cursor()
        self.create_search_jobs_table()

    def create_search_jobs_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL,
                is_done BOOLEAN,
                response TEXT,
                deleted BOOLEAN
            )
        ''')

    def create_new_search(self, payload):
        self.cursor.execute('''
            INSERT INTO search_jobs(payload, is_done, deleted)
            VALUES(?, FALSE, FALSE)
        ''', (json.dumps(payload),))
        return self.cursor.lastrowid

    def finish_search(self, search_id, result):
        self.cursor.execute('''
            UPDATE search_jobs
            SET response = ?, is_done = TRUE
            WHERE id = ?
        ''', (json.dumps(result), search_id))

    def read_by_id(self, search_id):
        return self.cursor.execute('SELECT * FROM search_jobs WHERE id = ?', search_id)

    def finish(self):
        self.connection.commit()
        self.connection.close()