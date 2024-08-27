import sqlite3

class UsersTable:
    def __init__(self):
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()

        # Создание таблицы Users, если она не существует
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        tg_id BIGINT NOT NULL,
        tg_username TEXT NOT NULL,
        rank BIT NOT NULL DEFAULT 0
        )
        ''')

        self.connection.commit()

    def get_cell(self, by="", id=""):
        """Получить данные пользователя по id или другому полю."""
        query = f"SELECT name, tg_id, tg_username, rank FROM Users WHERE {by} = ?"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            return list(result)
        return None

    def paste_cell(self, info=[]):
        """Добавить новую запись в таблицу Users."""
        try:
            self.cursor.execute('''
            INSERT INTO Users (name, tg_id, tg_username, rank) 
            VALUES (?, ?, ?, ?)
            ''', info)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления записи: {e}")
            return False

    def get_all(self):
        """Получить все записи из таблицы Users."""
        self.cursor.execute("SELECT * FROM Users")
        result = self.cursor.fetchall()
        return [list(row) for row in result]

    def update_cell(self, by="", id="", new_data={}):
        """Обновить конкретную запись по id или другому полю."""
        try:
            set_clause = ", ".join([f"{key} = ?" for key in new_data.keys()])
            values = list(new_data.values()) + [id]
            query = f"UPDATE Users SET {set_clause} WHERE {by} = ?"
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка обновления записи: {e}")
            return False

    def delete_cell(self, by="", id=""):
        """Удалить запись из таблицы Users по id или другому полю."""
        try:
            self.cursor.execute(f"DELETE FROM Users WHERE {by} = ?", (id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка удаления записи: {e}")
            return False

    def __del__(self):
        """Закрытие соединения при уничтожении объекта."""
        if self.connection:
            self.connection.close()
