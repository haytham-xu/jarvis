
import sqlite3
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
        result = cursor.fetchone()
        c.close()
        if result:
            return self.buildFolder(result)
        else:
            raise Exception('{} not exist'.format(code))

    def create(self, folder: Folder):
        c = self.__conn.cursor()
        insertQuery = 'INSERT INTO folder VALUES (?, ?, ?, ?, ?, ?, ?);'
        try:
            c.execute(insertQuery, (folder.getCode(), folder.getName(), folder.getPath(), folder.getPurePathListAsString(), folder.getBracketsPathListAsString(), folder.getSquareBracketsPathListAsString(), folder.getLastUpdatedTime()))
        except Exception as err:
            raise err
        else:
            self.__conn.commit()
        finally:
            c.close()
        

    def getAll(self):
        # c = self.__conn.cursor()
        # sqlCommand = 'SELECT * FROM folder;'
        # print(c.execute(sqlCommand).fetchall())
        # c.close()
        pass

    def close(self):
        self.__conn.close()

    def buildFolder(self, result):
        res = Folder(result[1], result[2], result[0])
        res.setPurePathListByString(result[3])
        res.setBracketsPathListByString(result[4])
        res.setSquareBracketsPathListByString(result[5])
        res.setLastUpdatedTime(result[6])
        return res
