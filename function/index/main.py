import os


from dbService import SqliteService
from folderService import getFolder, getFolderName
from utils import getConfig

configPath = 'config.yaml'

def main():
    dbPath, topLevelFolderPath, subFolderSuffix = getConfig()
    syncIndex(dbPath, topLevelFolderPath, subFolderSuffix)

def syncIndex(dbPath, topLevelFolderPath, subFolderSuffix):
    sqlService = SqliteService(dbPath)
    # sqlService.init()
    for top in topLevelFolderPath:
        for suffix in subFolderSuffix:
            targetFolderPath = top + '/' + top.split('/')[-1]  + "_" + suffix
            for curFolder, folders, _ in os.walk(targetFolderPath):  
                if(folders == []):
                    curFolderName = getFolderName(curFolder, targetFolderPath)
                    folder = getFolder(curFolderName, curFolder)
                    sqlService.create(folder)    
    sqlService.close()

if __name__ == "__main__":
    main()
