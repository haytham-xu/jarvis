

import sqlite3
from repository import folderModel

class SqliteService:

    sqlitePath = None
    conn = None

    def __init__(self, sqlitePath):
        self.sqlitePath = sqlitePath
        self.conn = sqlite3.connect(self.sqlitePath)

    def init(self):
        self.dropTable()
        self.createTable()

    def dropTable(self):
        c = self.conn.cursor()
        c.execute("DROP TABLE folder")
        self.conn.commit()

    def createTable(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS folder(
            code        CHAR(32) NOT NULL   PRIMARY KEY,
            name        TEXT     NOT NULL,
            rootPath    TEXT     NOT NULL,
            middlePath  TEXT     NOT NULL,
            lnSuffix_path TEXT     NOT NULL,
            pure_path_list    TEXT     NOT NULL,
            brackets_path_list    TEXT     NOT NULL,
            square_brackets_path_list    TEXT     NOT NULL);
        ''')
        self.conn.commit()

    def getByCode(self, code):
        c = self.conn.cursor()
        sqlCommand = 'SELECT * FROM folder f WHERE f.code=\'%s\''% (code)
        cursor = c.execute(sqlCommand)
        result = cursor.fetchone()
        if result:
            return self.buildFolder(result)
        else:
            return None

    def create(self, folder: folderModel.Folder):
        c = self.conn.cursor()
        insertQuery = 'INSERT INTO folder VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
        c.execute(insertQuery, (folder.code, folder.name, folder.rootPath, folder.middlePath ,folder.lnSuffixPath, folder.getPurePathListAsString(), folder.getBracketsPathListAsString(), folder.getSquareBracketsPathListAsString()))
        self.conn.commit()
        
    def getAll(self):
        c = self.conn.cursor()
        querySQL = 'SELECT * FROM folder'
        cursor = c.execute(querySQL)
        foldersInDB = cursor.fetchall()
        folderList = []
        for folder in foldersInDB:
            folderList.append(self.buildFolder(folder))
        return folderList

    def close(self):
        self.conn.close()

    def buildFolder(self, result):
        res = folderModel.Folder(result[1], result[2], result[3], result[0])
        res.setPurePathListByString(result[5])
        res.setBracketsPathListByString(result[6])
        res.setSquareBracketsPathListByString(result[7])
        return res
