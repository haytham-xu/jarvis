
import sqlite3
from subprocess import call
from folderModel import Folder

class SqliteService:

    __sqlitePath = None
    __conn = None

    def __init__(self, sqlitePath):
        self.__sqlitePath = sqlitePath
        self.__conn = sqlite3.connect(self.__sqlitePath)

    def init(self):
        self.dropTable()
        self.createTable()
    
    def dropTable(self):
        c = self.__conn.cursor()
        c.execute("DROP TABLE folder")
        self.__conn.commit()

    def createTable(self):
        c = self.__conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS folder(
            code        CHAR(32) NOT NULL   PRIMARY KEY,
            name        TEXT     NOT NULL,
            path        TEXT     NOT NULL,
            pure_path_list    TEXT     NOT NULL,
            brackets_path_list    TEXT     NOT NULL,
            square_brackets_path_list    TEXT     NOT NULL,
            last_updated_time TIMESTAMP NOT NULL);
        ''')
        self.__conn.commit()

    def getByCode(self, code):
        c = self.__conn.cursor()
        sqlCommand = 'SELECT * FROM folder f WHERE f.code=\'%s\''% (code)
        cursor = c.execute(sqlCommand)
        folder = cursor.fetchone()
        res = Folder(folder[1], folder[2], folder[0])
        res.setPurePathListByString(folder[3])
        res.setBracketsPathListByString(folder[4])
        res.setSquareBracketsPathListByString(folder[5])
        res.setLastUpdatedTime(folder[6])
        return res

    def create(self, folder: Folder):
        c = self.__conn.cursor()
        insertQuery = 'INSERT INTO folder VALUES (?, ?, ?, ?, ?, ?, ?);'
        c.execute(insertQuery, (folder.getCode(), folder.getName(), folder.getPath(), folder.getPurePathListAsString(), folder.getBracketsPathListAsString(), folder.getSquareBracketsPathListAsString(), folder.getLastUpdatedTime()))
        c.close()
        self.__conn.commit()

    def close(self):
        self.__conn.close()
