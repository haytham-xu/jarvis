
import os, shutil
from service import configService

config = configService.Config()

def isExist(path):
    return os.path.exists(path)

def removePath(path):
    shutil.rmtree(path)

def makeDirs(path):
    os.makedirs(path)

def copyFolder(sourcePath, targetPath):
    shutil.copytree(sourcePath, targetPath)

def listFoldersAndFiles(path):
    return os.listdir(path)

def isFolder(path):
    return os.path.isdir(path)

def move(sourcePath, targetPath):
    shutil.move(sourcePath, targetPath)

def isLink(path):
    return os.path.islink(path)

def unLink(path):
    return os.unlink(path)

def readLink(path):
    return os.readlink(path)


def rebuildFolderStructure():
    paths = []
    paths.extend(config.folderTree)
    paths.extend(config.categoryPathList)
    paths.extend(config.duplicatePathList)
    paths.append(config.randomPath)
    for authName in config.authDict.keys():
        paths.append(config.authBasePath + '/' + authName)
    for folderPath in paths:
        localPath = config.localBasePath + folderPath
        remotePath = config.remoteBasePath + folderPath
        checkOrCreate(localPath)
        checkOrCreate(remotePath)
    checkOrCreate(config.localBasePath + config.toCheckPath)

def checkOrCreate(path):
    if not isExist(path):
        makeDirs(path)

def getNameOfFoldersAndFilesWithoutRecursion(path):
    
    path = path if path.endswith('/') else path + '/'
    folder, files = [], []
    allItems = listFoldersAndFiles(path)
    for item in allItems:
        if isFolder(path + item):
            folder.append(item)
        else:
            files.append(item)
    folder = list(set(folder) - config.ignoreFolder)
    files = list(set(files) - config.ignoreFile)
    return folder, files

def getFolderAbsolutePathRecursion(path):
    path = path if path.endswith('/') else path + '/'
    allFolders = []
    allItems = listFoldersAndFiles(path)
    for item in allItems:
        itemAbsolutePath = path + item
        if isFolder(itemAbsolutePath):
            innerFolderNumber, _ = getFolderAndFilesNumberRecursion(itemAbsolutePath)
            if innerFolderNumber == 0:
                allFolders.append(itemAbsolutePath)
            else:
                allFolders.extend(getFolderAbsolutePathRecursion(itemAbsolutePath))
    return allFolders

def getFolderAndFilesNumberRecursion(path, folderPureNameList=None, filePureNameList=None):
    path = path if path.endswith('/') else path + '/'
    if(folderPureNameList == None and filePureNameList == None):
        folderPureNameList, filePureNameList = getNameOfFoldersAndFilesWithoutRecursion(path)
        return getFolderAndFilesNumberRecursion(path, folderPureNameList, filePureNameList)
    if len(folderPureNameList) == 0:
        return 0, len(filePureNameList)
    else:
        folderNumber = len(folderPureNameList)
        fileNumber = len(filePureNameList)
        for folderPureName in folderPureNameList:
            innerPath = path + folderPureName
            innerFolderPureNameList, innerFilePureNameList = getNameOfFoldersAndFilesWithoutRecursion(innerPath)
            innerFolderNumber, innerFileNumber = getFolderAndFilesNumberRecursion(innerPath, innerFolderPureNameList, innerFilePureNameList)
            folderNumber += innerFolderNumber
            fileNumber += innerFileNumber
        return folderNumber, fileNumber