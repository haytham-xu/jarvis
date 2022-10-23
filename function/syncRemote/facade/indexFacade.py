from service import configService, folderService
from repository import folderModel

config = configService.Config()

def refreshRemoteIndex():
    config.sqlService.init()
    for categoryMiddlePath in config.categoryPathList:
        remoteCategoryAbsolutePath = config.remoteBasePath + categoryMiddlePath
        remoteFolderAbsulotePathList = folderService.getFolderAbsolutePathRecursion(remoteCategoryAbsolutePath)
        for remoteFolderAbsulotePath in remoteFolderAbsulotePathList:
            aFolder = folderModel.Folder(remoteFolderAbsulotePath.removeprefix(remoteCategoryAbsolutePath), config.remoteBasePath, categoryMiddlePath)
            config.sqlService.create(aFolder)
