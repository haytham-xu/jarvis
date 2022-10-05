
import hashlib
import datetime
import string

class Folder:
    __code = None
    __name = None
    __path = None
    __purePathList = None
    __bracketsPathList = None
    __squareBracketsPathList = None
    __lastUpdatedTime = None

    def __init__(self):
        pass

    def __init__(self, name: str, path: str, code: str = None, purePathList: list = None, bracketsPathList: list = None, squareBracketsPathList: list = None, lastUpdatedTime: datetime = None):
        if not code:
            md5 = hashlib.md5()
            md5.update(name.encode('utf-8'))
            self.__code = md5.hexdigest()
        else:
            self.__code = code
        self.__name = name
        self.__path = path
        self.__purePathList = purePathList
        self.__bracketsPathList = bracketsPathList
        self.__squareBracketsPathList = squareBracketsPathList
        if lastUpdatedTime:
            self.__lastUpdatedTime = lastUpdatedTime
        else:
            self.__lastUpdatedTime = datetime.datetime.now()

    def getCode(self):
        return self.__code
    
    def getName(self):
        return self.__name
    
    def getPath(self):
        return self.__path

    def getPurePathList(self):
        return self.__purePathList

    def getBracketsPathList(self):
        return self.__bracketsPathList

    def getSquareBracketsPathList(self):
        return self.__squareBracketsPathList

    def getLastUpdatedTime(self):
        return self.__lastUpdatedTime

    def getBracketsPathListAsString(self):
        return ",".join(self.getBracketsPathList())

    def getPurePathListAsString(self):
        return ",".join(self.getPurePathList())

    def getSquareBracketsPathListAsString(self):
        return ",".join(self.getSquareBracketsPathList())
    
    def getPathList(self):
        pathList = []
        if(self.__purePathList):
            pathList.extend(self.__purePathList)
        if(self.__bracketsPathList):
            pathList.extend(self.__bracketsPathList)
        if(self.__squareBracketsPathList):
            pathList.extend(self.__squareBracketsPathList)
        return pathList

    def getPathListAsString(self):
        return str(self.getPathList())

    def setCode(self, id):
        self.__code = id

    def setName(self, name):
        self.__name = name
    
    def setPath(self, path):
        self.__path = path

    def setPurePathList(self, purePathList):
        self.__purePathList = purePathList

    def setBracketsPathList(self, bracketsPathList):
        self.__bracketsPathList = bracketsPathList

    def setSquareBracketsPathList(self, squareBracketsPathList):
        self.__squareBracketsPathList = squareBracketsPathList

    def setPurePathListByString(self, purePathListString:string):
        self.__purePathList = purePathListString.split(',')

    def setBracketsPathListByString(self, bracketsPathListString:string):
        self.__bracketsPathList = bracketsPathListString.split(',')

    def setSquareBracketsPathListByString(self, squareBracketsPathListString:string):
        self.__squareBracketsPathList = squareBracketsPathListString.split(',')

    def setLastUpdatedTime(self, lastUpdatedTime):
        self.__lastUpdatedTime = lastUpdatedTime

    def toString(self):
        return " ".join([self.__code, self.__name, self.__path, self.getPathListAsString(), self.__lastUpdatedTime])
