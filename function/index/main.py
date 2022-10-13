import os

from dbService import SqliteService
from utils import getConfigByKey, logIndexDuplicated, getFolder, getFolderName

functionType = 'index'

def main():
    dbPath = getConfigByKey('dbPath')
    topLevelFolderPath = getConfigByKey('topLevelFolderPath')
    subFolderSuffix = getConfigByKey('subFolderSuffix')
    syncIndex(dbPath, topLevelFolderPath, subFolderSuffix)

def syncIndex(dbPath, topLevelFolderPath, subFolderSuffix):
    sqlService = SqliteService(dbPath)
    sqlService.init()
    for top in topLevelFolderPath:
        for suffix in subFolderSuffix:
            targetFolderPath = top + '/' + top.split('/')[-1]  + "_" + suffix
            for curFolder, folders, _ in os.walk(targetFolderPath):  
                if(folders == []):
                    curFolderName = getFolderName(curFolder, targetFolderPath)
                    print(curFolderName)
                    folder = getFolder(curFolderName, curFolder)
                    try:
                        sqlService.create(folder)
                    except Exception:
                        existingFolder = sqlService.getByCode(folder.getCode())
                        logIndexDuplicated(folder.getName(), existingFolder.getPath(), folder.getPath())
    sqlService.close()

if __name__ == "__main__":
    main()
