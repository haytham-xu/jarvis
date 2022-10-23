
from service import configService, folderService, lnService

config = configService.Config()

def syncAuth():
    cleanAuthUselessLn()
    buildNewAuthLn()

def cleanAuthUselessLn():
    cleanUselessLn(config.localBasePath)
    cleanUselessLn(config.remoteBasePath)

def cleanUselessLn(basePath):
    authFolderAbsolutePathList = folderService.getFolderAbsolutePathRecursion(basePath + config.authBasePath)
    for authFolderAbsolutePath in authFolderAbsolutePathList:
        if folderService.isLink(authFolderAbsolutePath) and not folderService.isExist(folderService.readLink(authFolderAbsolutePath)):
            folderService.unLink(authFolderAbsolutePath)

def buildNewAuthLn():
    folderModelBelongToAuth = {}
    authMiddlePath = {}
    for authName in config.authDict.keys():
        folderModelBelongToAuth[authName] = []
        authMiddlePath[authName] = config.authBasePath + '/' + authName + '/'

    folderModelList = config.sqlService.getAll()
    for folderModel in folderModelList:
        for (authName, authNameAliasList) in config.authDict.items():
            for authNameAlias in authNameAliasList:
                if authNameAlias in folderModel.name:
                    folderModelBelongToAuth[authName].append(folderModel)

    for (authName, authMiddlePath) in authMiddlePath.items():
        if len(folderModelBelongToAuth[authName]) == 0:
            continue
        folderModelList = folderModelBelongToAuth[authName]
        localAuthAbsolutePath = config.localBasePath + authMiddlePath
        remoteAuthAbsolutePath = config.remoteBasePath + authMiddlePath
        cleanAndRebuild(localAuthAbsolutePath)
        cleanAndRebuild(remoteAuthAbsolutePath)
        
        for folderModel in folderModelList:
            localAbsolutePath = localAuthAbsolutePath + folderModel.name
            if folderService.isLink(localAbsolutePath):
                continue
            if not folderModel.hasParentFolder():
                lnService.buildLnLocally(localAbsolutePath, folderModel.getAbsolutePath())
                lnService.buildDuplicateRelativeLnRemote(config.remoteBasePath, authMiddlePath, folderModel.name, folderModel.getAbsolutePath())
                continue
            localParentAbsolutePath = localAuthAbsolutePath + folderModel.lnSuffixPath
            remoteParentAbsolutePath = folderModel.rootPath + folderModel.middlePath + folderModel.lnSuffixPath
            if not folderService.isExist(localParentAbsolutePath):
                lnService.buildLnLocally(localParentAbsolutePath, remoteParentAbsolutePath)
                lnService.buildDuplicateRelativeLnRemote(config.remoteBasePath, authMiddlePath, folderModel.lnSuffixPath, remoteParentAbsolutePath)

def cleanAndRebuild(path):
    folderService.removePath(path)
    folderService.makeDirs(path)
