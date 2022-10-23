import sys
from service import folderService
from service import configService

toRemovePath = ["game", "sp", "duplicate", "mh", "ln", "tocheck"]
localFolderNameList = ["[square(bracketInSquare)]test1(bracket)", "[square(bracketInSquare)]test2(bracket)"]
remoteFolderNameList = ["[square(bracketInSquare)]test1(bracket)"]
testFolderMiddlePath = ".testFolder/"
testCategoryMPathWithoutSufffix = "mh/mh_yb/mh_yb_np/"
testCategoryMPath = "mh/mh_yb/mh_yb_np/mh_yb_np_s/"
testDuplocayeMPath = "duplicate/duplicate_np/"
testAuthMPath = "ln/auth/test/"

utResultTemplat = "{} - {} - {}"

config = configService.Config()

def cleanEnvironment():
    for path in toRemovePath:
        localPath = config.localBasePath + path
        remotePath = config.remoteBasePath + path
        if folderService.isExist(localPath):
            folderService.removePath(localPath)
        if folderService.isExist(remotePath):
            folderService.removePath(remotePath)

def initTestEnvironment():
    folderService.rebuildFolderStructure()
    for folderName in localFolderNameList:
        folderPath = config.localBasePath + testFolderMiddlePath + folderName
        localTargetFolder = config.localBasePath + testCategoryMPathWithoutSufffix
        duplicateFolder = config.localBasePath + testDuplocayeMPath
        folderService.copyFolder(folderPath, localTargetFolder + folderName)
        folderService.copyFolder(folderPath, duplicateFolder + folderName)
    for folderName in remoteFolderNameList:
        folderPath = config.localBasePath + testFolderMiddlePath + folderName
        remoteTargetFolder = config.remoteBasePath + testCategoryMPath
        folderService.copyFolder(folderPath, remoteTargetFolder + folderName)

def checkRemoteCategory():
    for folderName in localFolderNameList:
        remoteMHFolderPath = config.remoteBasePath + testCategoryMPath + folderName
        print(utResultTemplat.format(folderService.isExist(remoteMHFolderPath), folderName, sys._getframe().f_code.co_name))

def checkLocalCategoryLn():
    for folderName in localFolderNameList:
        remoteMHFolderPath = config.remoteBasePath + testCategoryMPath + folderName
        localMHFolderPath = config.localBasePath + testCategoryMPath+ folderName
        print(utResultTemplat.format(folderService.isExist(localMHFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.isLink(localMHFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.readLink(localMHFolderPath) == remoteMHFolderPath, folderName, sys._getframe().f_code.co_name))

def checkLocalDuplicateLn():
    for folderName in localFolderNameList:
        remoteMHFolderPath = config.remoteBasePath + testCategoryMPath + folderName
        localDuplicateFolderPath = config.localBasePath + testDuplocayeMPath + folderName
        print(utResultTemplat.format(folderService.isExist(localDuplicateFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.isLink(localDuplicateFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.readLink(localDuplicateFolderPath) == remoteMHFolderPath, folderName, sys._getframe().f_code.co_name))

def checkRemoteDuplicateLn():
     for folderName in localFolderNameList:
        remoteMHFolderPath = config.remoteBasePath + testCategoryMPath + folderName
        remoteDuplicateFolderPath = config.remoteBasePath + testDuplocayeMPath + folderName
        print(utResultTemplat.format(folderService.isExist(remoteDuplicateFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.isLink(remoteDuplicateFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(len(folderService.listFoldersAndFiles(remoteDuplicateFolderPath)) == len(folderService.listFoldersAndFiles(remoteMHFolderPath)), folderName, sys._getframe().f_code.co_name))

def checkLocalAuthLn():
    for folderName in localFolderNameList:
        remoteMHFolderPath = config.remoteBasePath + testCategoryMPath + folderName
        localAuthFolderPath = config.localBasePath + testAuthMPath + folderName
        print(utResultTemplat.format(folderService.isExist(localAuthFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.isLink(localAuthFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.readLink(localAuthFolderPath) == remoteMHFolderPath, folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(len(folderService.listFoldersAndFiles(localAuthFolderPath)) == len(folderService.listFoldersAndFiles(remoteMHFolderPath)), folderName, sys._getframe().f_code.co_name))

def checkRemoteAuthLn():
    for folderName in localFolderNameList:
        remoteMHFolderPath = config.remoteBasePath + testCategoryMPath + folderName
        remoteAuthFolderPath = config.remoteBasePath + testAuthMPath + folderName
        print(utResultTemplat.format(folderService.isExist(remoteAuthFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(folderService.isLink(remoteAuthFolderPath), folderName, sys._getframe().f_code.co_name))
        print(utResultTemplat.format(len(folderService.listFoldersAndFiles(remoteAuthFolderPath)) == len(folderService.listFoldersAndFiles(remoteMHFolderPath)), folderName, sys._getframe().f_code.co_name))

