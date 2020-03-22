import sqlite3
from typing import List


class Storage:
    def get(self, key: bytes) -> bytes:
        """Returns a key from whatever backend is used

        Args:
            key(str): string to be looked up

        Raises:
            KeyError: if the key was not found

        Returns:
            Union[str, None]: the value associated with the key.
                None if not found
        """
        raise NotImplemented

    def find(self, string: bytes) -> List[bytes]:
        """Returns a list of the keys whose value starts with `string`

        Args:
            string(str): string to be looked up among the values

        Returns:
            List[str]: List of keys. Empty list if none found
        """
        raise NotImplemented

    def store(self, key: bytes, value: bytes):
        """Store a key value pair

        Args:
            key(str): key to be inserted
            value(str): value to be inserted
        """
        raise NotImplemented


class SQLiteMock(Storage):
    def __init__(self):
        self.db = {}

    def get(self, key: bytes) -> bytes:
        return self.db[key]

    def find(self, string: bytes) -> List[bytes]:
        return [key for key, val in self.db.items() if val.startswith(string)]

    def store(self, key: str, value: str):
        self.db[key] = value


class SQLiteWrapper(Storage):
    def __init__(self, db_loc):
        self.db = sqlite3.connect(db_loc)
        c = self.db.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS vals (
                key TEXT PRIMARY KEY,
                value TEXT
            );""")
        self.db.commit()

    def get(self, key: bytes) -> bytes:
        c = self.db.cursor()
        c.execute("SELECT value FROM vals WHERE key=?", (key,))
        if result := c.fetchone() is not None:
            return result[0]
        else:
            raise KeyError("Key was not found in db")

    def find(self, string: bytes) -> List[bytes]:
        c = self.db.cursor()
        c.execute("SELECT key FROM vals WHERE value LIKE ?", (string + b'%',))
        return [x[0] for x in c]

    def store(self, key: bytes, value: bytes):
        c = self.db.cursor()
        c.execute(
            """INSERT INTO vals (key, value)
                   VALUES(?, ?) 
                   ON CONFLICT(key) 
                   DO UPDATE SET value=?;""",
            (key, value, value))
        self.db.commit()






