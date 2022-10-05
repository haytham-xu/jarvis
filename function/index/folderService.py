import re

from folderModel import Folder

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
