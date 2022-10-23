
import yaml

from repository import dbRepository

configPath = 'config.yaml'

dbPathKey = "dbPath"
localBasePathKey = "localBasePath"
remoteBasePathKey = "remoteBasePath"
folderTreeKey = "folderTree"
categoryPathKey = "categoryPath"
duplicatePathKey = "duplicatePath"
authDictKey = "authDict"
authBasePathKey = "authBasePath"
trBasePathKey = "trBasePath"
randomPathKey = "randomPath"
randomMHNumberKey = "randomMHNumber"
randomSPNumberKey = "randomSPNumber"
ignoreFileKey = "ignoreFile"
logBasePathKey = "logBasePath"
toCheckPathKey = "toCheckPath"

def getConfigByKey(key):
    return getAllConfig()[key]

def getAllConfig():
    allConfigs = {}
    with open(configPath, 'r') as config:
        allConfigs.update(yaml.safe_load(config))
        currentProfile = allConfigs['profile']
        profileConfigPath = './envvar/{}.yaml'.format(currentProfile)
        with open(profileConfigPath, 'r') as currentProfileConfig:
            allConfigs.update(yaml.safe_load(currentProfileConfig))
    return allConfigs

def mergedPath(prefixPathList, suffixPathList):
    r = []
    if prefixPathList == []:
        return suffixPathList
    for prefixPath in prefixPathList:
        for suffixPath in suffixPathList:
            mergedSuffixPath = "_".join((prefixPath.split('/')[-1], suffixPath))
            r.append("/".join((prefixPath, mergedSuffixPath)))
    return r

def getMergedPath(pathlist):
    mergedPatgList = []
    for innerPath in pathlist:
        mergedPatgList = mergedPath(mergedPatgList, innerPath)
    return [path + '/' for path in mergedPatgList]

class Config:
    localBasePath = None
    remoteBasePath = None
    folderTree = None
    categoryPathList = None
    toCategoryPathList = None
    dbPath = None
    sqlService = None
    duplicatePathList = None
    authDict = None
    authBasePath = None
    trBasePath = None
    randomPath = None
    randomMHNumber = None
    randomSPNumber = None
    ignoreFile = None
    ignoreFolder = None
    logBasePath = None
    toCheckPath = None
    duplicateLogTemplate = "Duplicate: {} -> {}"
    successLogTemplate = "Success: {} -> {}"
    errorLogTemplate = "Error: {}"

    def __init__(self):
        self.toCheckPath = getConfigByKey(toCheckPathKey)
        self.localBasePath = getConfigByKey(localBasePathKey)
        self.remoteBasePath = getConfigByKey(remoteBasePathKey)
        self.folderTree = getConfigByKey(folderTreeKey)
        self.categoryPathList = getMergedPath(getConfigByKey(categoryPathKey))
        self.toCategoryPathList = getMergedPath(getConfigByKey(categoryPathKey)[:-1])
        self.dbPath = self.remoteBasePath + getConfigByKey(dbPathKey)
        self.duplicatePathList = getMergedPath(getConfigByKey(duplicatePathKey))
        self.authDict = getConfigByKey(authDictKey)
        self.authBasePath = getConfigByKey(authBasePathKey)
        self.trBasePath = getConfigByKey(trBasePathKey)
        self.randomPath = getConfigByKey(randomPathKey)
        self.randomMHNumber = getConfigByKey(randomMHNumberKey)
        self.randomSPNumber = getConfigByKey(randomSPNumberKey)
        self.logBasePath = getConfigByKey(logBasePathKey)
        self.ignoreFile = set(getConfigByKey(ignoreFileKey))
        self.ignoreFolder = set([p.split('/')[-2] for p in self.categoryPathList])
        self.sqlService = dbRepository.SqliteService(self.dbPath)
