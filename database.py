import sqlite3

DB_NAME = "characters.db"

class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def AddCharacter(self, character, base64_image):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {character} (image TEXT)")
        cursor.execute(f"INSERT INTO {character} VALUES (?)", (base64_image,))
        conn.commit()
        conn.close()

    def GetCharacter(self, character):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT image FROM {character}")
        result = cursor.fetchall()
        conn.close()
        return result
    
    def GetAllCharacters(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        response =  cursor.fetchall()
        conn.close()
        return [character[0] for character in response]