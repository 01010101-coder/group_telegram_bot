import aiosqlite


class EventsTable:
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
            CREATE TABLE IF NOT EXISTS Events (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT
            )
        ''')
        await connection.commit()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def add_event(self, dictin):
        try:
            connection = await self._connect()
            await connection.execute('''
                INSERT INTO Events(date, time, name, description)
                VALUES (?, ?, ?, ?)
            ''', (dictin["date"], dictin['time'], dictin['name'], dictin['description']))
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка добавления мероприятия: {e}")
            return False
