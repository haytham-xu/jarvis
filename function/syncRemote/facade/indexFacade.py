from service import configService, folderService, loggingService
from repository import folderModel

config = configService.Config()

def refreshRemoteIndex():
    config.sqlService.init()
    for categoryMiddlePath in config.categoryPathList:
        remoteCategoryAbsolutePath = config.remoteBasePath + categoryMiddlePath
        remoteFolderAbsulotePathList = folderService.getFolderAbsolutePathRecursion(remoteCategoryAbsolutePath)
        for remoteFolderAbsulotePath in remoteFolderAbsulotePathList:
            remoteFolderModel = folderModel.Folder(remoteFolderAbsulotePath.removeprefix(remoteCategoryAbsolutePath), config.remoteBasePath, categoryMiddlePath)
            existingFolderModel = config.sqlService.getByCode(remoteFolderModel.code)
            if existingFolderModel:
                loggingService.logging.error(config.duplicateLogTemplate.format(remoteFolderModel.getAbsolutePath(), existingFolderModel.getAbsolutePath()))
                folderService.move(remoteFolderModel.getAbsolutePath(), config.remoteBasePath + config.toCheckPath)
                continue
            print("create index: ", remoteFolderAbsulotePath)
            config.sqlService.create(remoteFolderModel)
    config.sqlService.close()
