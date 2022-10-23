
import random
from service import configService, folderService, lnService

config = configService.Config()

def generateRandom():
    folderModelList = config.sqlService.getAll()
    mhRandomNumber = config.randomMHNumber if config.randomMHNumber < len(folderModelList) else len(folderModelList)
    randomIndexList = random.sample(range(len(folderModelList)), mhRandomNumber)
    localRandomPath = config.localBasePath + config.randomPath + '/'
    remoteRandomPath = config.remoteBasePath + config.randomPath + '/'
    cleanAndRebuild(localRandomPath)
    cleanAndRebuild(remoteRandomPath)
    for index in randomIndexList:
        folderModel = folderModelList[index]
        if not folderModel.hasParentFolder():
            lnService.buildLnLocally(localRandomPath + folderModel.name, folderModel.getAbsolutePath())
            lnService.buildDuplicateRelativeLnRemote(config.remoteBasePath, config.randomPath + '/', folderModel.name, folderModel.getAbsolutePath())
            continue
        localParentAbsolutePath = localRandomPath + folderModel.lnSuffixPath
        remoteParentAbsolutepath = folderModel.rootPath + folderModel.middlePath + folderModel.lnSuffixPath
        if not folderService.isExist(localParentAbsolutePath):
            lnService.buildLnLocally(localParentAbsolutePath, remoteParentAbsolutepath)
            lnService.buildDuplicateRelativeLnRemote(config.remoteBasePath, config.randomPath + '/', folderModel.lnSuffixPath, remoteParentAbsolutepath)
        

def cleanAndRebuild(path):
    folderService.removePath(path)
    folderService.makeDirs(path)
