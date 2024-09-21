import aiosqlite
import json

from datetime import datetime

pairs_time = {
    1: "8:15",
    2: "9:45",
    3: "11:15",
    4: "13:00",
    5: "14:30"
}

class SkipTable:
    def __init__(self, db_path='my_database.db'):
        self.db_path = db_path
        self.connection = None

    async def _connect(self):
        if not self.connection:
            self.connection = await aiosqlite.connect(self.db_path)
        return self.connection

    async def initialize_table(self):
        connection = await self._connect()
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS SkipHistory (
                id INTEGER PRIMARY KEY,
                tg_id BIGINT NOT NULL,
                date TEXT NOT NULL,
                pairs TEXT NOT NULL,
                description TEXT,
                approved BIT NOT NULL DEFAULT 1
            )
        ''')
        await connection.commit()

    async def add_skip(self, tg_id, date, pairs, description):
        try:
            pairs = json.dumps(pairs)
        except:
            print("Error dumping")
            return False

        try:
            connection = await self._connect()
            await connection.execute('''
                INSERT INTO SkipHistory(tg_id, date, pairs, description, approved)
                VALUES (?, ?, ?, ?, 1)
            ''', (tg_id, date, pairs, description))
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка добавления записи: {e}")
            return False

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def delete_skip(self, tg_id, date):
        try:
            connection = await self._connect()
            await connection.execute('DELETE FROM SkipHistory WHERE tg_id = ? AND date = ?', (tg_id, date, ))
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка удаление записи: {e}")
            return False

    async def update_approved(self, id, value):
        try:
            connection = await self._connect()
            await connection.execute('UPDATE SkipHistory SET approved = ? WHERE id = ?', (value, id,))
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка обновления approved: {e}")
            return False

    async def get_absent_students_by_date(self, date):
        # Подключение к базе данных и выполнение запроса
        connection = await aiosqlite.connect('events.db')
        async with connection.execute("SELECT tg_id, pairs, description FROM SkipHistory WHERE date = ?", (date,)) as cursor:
            rows = await cursor.fetchall()
            return [{'tg_id': row[0], 'pairs': row[1], 'description': row[2]} for row in rows]

#     Добавить обновление пар, если один и тот же пользователь
#     отмечает отсутствие на один и тот же день
