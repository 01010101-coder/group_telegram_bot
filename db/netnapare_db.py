import aiosqlite


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
                date DATE NOT NULL,
                description TEXT
            )
        ''')
        await connection.commit()
