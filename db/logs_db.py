import aiosqlite


class LogsTable:
    def __init__(self, dp_path='my_database.db'):
        self.db_path = dp_path
        self.connection = None

    async def _connect(self):
        if not self.connection:
            self.connection = await aiosqlite.connect(self.db_path)
        return self.connection

    async def initialize_table(self):
        connection = await self._connect()
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS Logs (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            time_spend INTEGER,
            is_success INTEGER
            )
        ''')
        await connection.commit()

    async def add_log(self, type, time_spend, is_success):
        try:
            connection = await self._connect()
            await connection.execute('''
                INSERT INTO Logs (type, time_spend, is_success)
                VALUES (?, ?, ?)
            ''', (type, time_spend, is_success))  # Убрана лишняя запятая
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка добавления log: {e}")
            return False

    async def close(self):
        if self.connection:
            await self.connection.close()
