
from service import configService, folderService, loggingService, lnService
from repository import folderModel

config = configService.Config()

def syncDuplicate():
    cleanDuplicateUselessLn()
    buildLnforNewFolder()
    
def cleanDuplicateUselessLn():
    for duplicateMiddlePath in config.duplicatePathList:
        cleanUselessLn(config.localBasePath, duplicateMiddlePath)
        cleanUselessLn(config.remoteBasePath, duplicateMiddlePath)

def cleanUselessLn(basePath, middlePath):
    absolutePath = basePath + middlePath
    folderAbsolutePathList = folderService.getFolderAbsolutePathRecursion(absolutePath)
    for folderAbsolutePath in folderAbsolutePathList:
        if folderService.isLink(folderAbsolutePath):
            lnSourcePath = folderService.readLink(folderAbsolutePath)
            if not folderService.isExist(lnSourcePath):
                folderService.unLink(folderAbsolutePath)

def buildLnforNewFolder():
    for duplicateMiddlePath in config.duplicatePathList:
        localDuplicateAbsolutePath = config.localBasePath + duplicateMiddlePath
        localFolderAbsolutePathList = folderService.getFolderAbsolutePathRecursion(localDuplicateAbsolutePath)
        for localFolderAbsolutePath in localFolderAbsolutePathList:
            if folderService.isLink(localFolderAbsolutePath):
                continue
            folderName = localFolderAbsolutePath.removeprefix(localDuplicateAbsolutePath)
            aFolderModel = config.sqlService.getByCode(folderModel.getHashCode(folderName))
            if not aFolderModel:
                loggingService.logging.error("target folder not existing: " + config.errorLogTemplate.format(folderName))
                folderService.move(localFolderAbsolutePath, config.localBasePath + config.toCheckPath)
                continue
            if not aFolderModel.hasParentFolder():
                folderService.removePath(localFolderAbsolutePath)
                lnService.buildLnLocally(localFolderAbsolutePath, aFolderModel.getAbsolutePath())
                lnService.buildDuplicateRelativeLnRemote(config.remoteBasePath, duplicateMiddlePath, folderName, aFolderModel.getAbsolutePath())
                continue
            localParentFolderAbsolutePath = localDuplicateAbsolutePath + aFolderModel.lnSuffixPath
            remoteParentFolderAbsolutePath = aFolderModel.rootPath + aFolderModel.middlePath + aFolderModel.lnSuffixPath
            if not folderService.isLink(localParentFolderAbsolutePath):
                folderService.removePath(localParentFolderAbsolutePath)
                lnService.buildLnLocally(localParentFolderAbsolutePath, remoteParentFolderAbsolutePath)
                lnService.buildDuplicateRelativeLnRemote(config.remoteBasePath, duplicateMiddlePath, aFolderModel.lnSuffixPath, remoteParentFolderAbsolutePath)
