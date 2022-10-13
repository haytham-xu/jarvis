
import time
import yaml
import re

from folderModel import Folder
# from utils import getConfigByKey

configPath = 'config.yaml'
configLogBasePathKey = 'logBasePath'
functionIndexKey = 'index'
functionIndexDuplicatedKey = 'duplicated'
functionIndexDeprecatedKey = 'deprecated'

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

def log(functionType, logCategory, logMessage):
    logFilePath = "{}/{}/{}.log".format(getConfigByKey(configLogBasePathKey), functionType, logCategory)
    f = open(logFilePath, "a")
    f.write(logMessage + "\n")
    f.close()

def logIndexDuplicated(folderName, currentPath, duplicatePath):
    curDate = time.strftime("%Y%m%d", time.localtime())
    logMessage = "{} | {} | {} | {}".format(curDate, folderName, currentPath, duplicatePath)
    log(functionIndexKey, functionIndexDuplicatedKey, logMessage)

def logIndexDeprecated(folderName, folderPath):
    curDate = time.strftime("%Y%m%d", time.localtime())
    logMessage = "{} | {} | {}".format(curDate, folderName, folderPath)
    log(functionIndexKey, functionIndexDeprecatedKey, logMessage)

def getFolderName(curPath, patentPath):
    return curPath.removeprefix(patentPath)[1:].replace('/', ' ')

def getFolder(folderName, folderpath):
    folder = Folder(folderName, folderpath)

    squareBracketsPattern = re.compile(r'\[.*?\]')
    chineseSquareBracketsPattern = re.compile(r'\【.*?\】')
    squareBracketsPathList = [i[1:-1] for i in squareBracketsPattern.findall(folderName) if i]
    squareBracketsPathList.extend([i[1:-1] for i in chineseSquareBracketsPattern.findall(folderName) if i])
    folder.setSquareBracketsPathList(squareBracketsPathList)
    folderName = squareBracketsPattern.sub("-", folderName)
    folderName = chineseSquareBracketsPattern.sub("-", folderName)

    bracketsPattern = re.compile(r'\(.*?\)')
    folder.setBracketsPathList([i[1:-1] for i in bracketsPattern.findall(folderName) if i])
    folderName = bracketsPattern.sub("-", folderName)

    folder.setPurePathList([i.strip() for i in re.split('-', folderName) if i and i != ' '])
    return folder
