import aiosqlite


class UsersTable:
    def __init__(self, db_path='my_database.db'):
        self.db_path = db_path
        self.connection = None

    async def _connect(self):
        """Создание подключения к базе данных, если его нет."""
        if not self.connection:
            self.connection = await aiosqlite.connect(self.db_path)
        return self.connection

    async def initialize_table(self):
        """Инициализация таблицы Users."""
        connection = await self._connect()
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tg_id BIGINT NOT NULL,
                tg_username TEXT,
                rank BIT NOT NULL DEFAULT 0
            )
        ''')
        await connection.commit()

    async def get_user_by_tg_id(self, tg_id):
        """Получение пользователя по tg_id."""
        connection = await self._connect()
        cursor = await connection.execute('SELECT * FROM Users WHERE tg_id = ?', (tg_id,))
        return await cursor.fetchone()

    async def add_user(self, name, tg_id, tg_username):
        """Добавление нового пользователя."""
        try:
            connection = await self._connect()
            await connection.execute('''
                INSERT INTO Users (name, tg_id, tg_username, rank) 
                VALUES (?, ?, ?, 0)
            ''', (name, tg_id, tg_username))
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка добавления пользователя: {e}")
            return False

    async def update_rank(self, tg_id, rank):
        """Обновление ранга пользователя."""
        try:
            connection = await self._connect()
            await connection.execute('UPDATE Users SET rank = ? WHERE tg_id = ?', (rank, tg_id))
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка обновления ранга: {e}")
            return False

    async def get_users_by_rank(self, rank):
        """Получение всех пользователей с определенным рангом."""
        connection = await self._connect()
        cursor = await connection.execute('SELECT * FROM Users WHERE rank = ?', (rank,))
        return await cursor.fetchall()

    async def close(self):
        """Закрытие соединения с базой данных."""
        if self.connection:
            await self.connection.close()

    async def delete_user(self, tg_id):
        """Удаление пользователя по tg_id."""
        try:
            connection = await self._connect()
            await connection.execute('DELETE FROM Users WHERE tg_id = ?', (tg_id,))
            await connection.commit()
            return True
        except aiosqlite.Error as e:
            print(f"Ошибка удаления пользователя: {e}")
            return False
