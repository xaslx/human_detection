import sqlite3
from datetime import date

from src.repositories.base import BaseRepository


class SqliteRepository(BaseRepository):
    
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)

    def save(self, obj: dict) -> None:
        with self.connection as conn:
            conn.execute('INSERT INTO photos (filename, timestamp) VALUES (?, ?)', (obj['filename'], obj['timestamp']))

    def get(self, obj_id: int) -> dict | None:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM photos WHERE id = ?', (obj_id,))
        row = cursor.fetchone()
        return {'id': row[0], 'filename': row[1], 'timestamp': row[2]} if row else None

    def get_all(self) -> list[dict] | None:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM photos')
        rows = cursor.fetchall()
        return [{'id': row[0], 'filename': row[1], 'timestamp': row[2]} for row in rows]

    def get_by_date(self, start_date: date, end_date: date) -> list[dict] | None:
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM photos WHERE date(timestamp) BETWEEN ? AND ?', (start_date, end_date))
        rows = cursor.fetchall()
        return [{'id': row[0], 'filename': row[1], 'timestamp': row[2]} for row in rows]

    def close(self):
        self.connection.close()
