
from service import configService, folderService, loggingService, lnService
from repository import folderModel

config = configService.Config()

def syncCategory():
    cleanLocalCategoryLn()
    uploadLocalCategory()
    buildLocalCategoryLn()

def cleanLocalCategoryLn():
    for categoryMiddlePath in config.categoryPathList:
        localCategoryAbsolutePath = config.localBasePath + categoryMiddlePath
        localFolderPureNameList,_ = folderService.getNameOfFoldersAndFilesWithoutRecursion(localCategoryAbsolutePath)
        for localFolderPureName in localFolderPureNameList:
            localFolderAbsolutePath = localCategoryAbsolutePath + localFolderPureName
            if folderService.isLink(localFolderAbsolutePath):
                folderService.unLink(localFolderAbsolutePath)

def uploadLocalCategory():
    for categoryMiddlePath in config.categoryPathList:
        localCategoryAbsolutePath = config.localBasePath + categoryMiddlePath
        remoteCategoryAbsolutePath = config.remoteBasePath + categoryMiddlePath
        localFolderAbsolutePathList = folderService.getFolderAbsolutePathRecursion(localCategoryAbsolutePath)
        for localFolderAbsolutePath in localFolderAbsolutePathList:
            remoteFolderAbsolutePath = remoteCategoryAbsolutePath + localFolderAbsolutePath.removeprefix(localCategoryAbsolutePath)
            aFolderModel = folderModel.Folder(localFolderAbsolutePath.removeprefix(localCategoryAbsolutePath), config.remoteBasePath, categoryMiddlePath)
            if config.sqlService.getByCode(aFolderModel.code):
                loggingService.logging.error(config.duplicateLogTemplate.format(localFolderAbsolutePath, remoteFolderAbsolutePath))
                folderService.move(localFolderAbsolutePath, config.localBasePath + config.toCheckPath)
                return
            folderService.copyFolder(localFolderAbsolutePath, remoteFolderAbsolutePath)
            if folderService.getFolderAndFilesNumberRecursion(localFolderAbsolutePath) == folderService.getFolderAndFilesNumberRecursion(remoteFolderAbsolutePath):
                folderService.removePath(localFolderAbsolutePath)
                config.sqlService.create(aFolderModel)
            if aFolderModel.hasParentFolder():
                parentAbsolutePath = localCategoryAbsolutePath + aFolderModel.lnSuffixPath
                parentFolderRemainingFolderNumber,_ = folderService.getFolderAndFilesNumberRecursion(parentAbsolutePath)
                if parentFolderRemainingFolderNumber == 0:
                    folderService.removePath(parentAbsolutePath)
                
def buildLocalCategoryLn():
    folderModelList = config.sqlService.getAll()
    for folderModel in folderModelList:
        if not folderModel.hasParentFolder():
            remoteAbsolutePath = folderModel.getAbsolutePath()
            localAbsolutePath = config.localBasePath + remoteAbsolutePath.removeprefix(config.remoteBasePath)
            lnService.buildLnLocally(localAbsolutePath, remoteAbsolutePath)
            continue
        remoteAbsolutePath = folderModel.rootPath + folderModel.middlePath + folderModel.lnSuffixPath
        localAbsolutePath = config.localBasePath + remoteAbsolutePath.removeprefix(config.remoteBasePath)
        if not folderService.isExist(localAbsolutePath):
            lnService.buildLnLocally(localAbsolutePath, remoteAbsolutePath)