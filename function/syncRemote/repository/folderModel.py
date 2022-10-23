
import string, hashlib, re

folderModelStringTemplate = '''
code: %s
name: %s
middlePath: %s
lnSuffixPath: %s
rootPath: %s
absolutePath: %s
purePathList: %s
bracketsPathList: %s
squareBracketsPathList: %s
'''

class Folder:
    code = None
    name = None
    rootPath = None
    middlePath = None
    lnSuffixPath = None
    purePathList = None
    bracketsPathList = None
    squareBracketsPathList = None

    def __init__(self, name, rootPath, middlePath, code = None):
        if not code:
            self.code = getHashCode(name)
        else:
            self.code = code
        self.name = name
        self.rootPath = rootPath
        self.middlePath = middlePath if middlePath[-1] == '/' else middlePath + '/'
        self.lnSuffixPath = name.split('/')[0] if '/' in name else name
        self.squareBracketsPathList = initSquareBracketsPathList(name)
        self.bracketsPathList = initBracketsPathList(name)
        self.purePathList = initPurePathList(name)

    def hasParentFolder(self):
        return self.lnSuffixPath != self.name

    def getAbsolutePath(self):
        return self.rootPath + self.middlePath + self.name

    def getBracketsPathListAsString(self):
        return ",".join(self.bracketsPathList)

    def getPurePathListAsString(self):
        return ",".join(self.purePathList)

    def getSquareBracketsPathListAsString(self):
        return ",".join(self.squareBracketsPathList)
    
    def getPathList(self):
        pathList = []
        if(self.purePathList):
            pathList.extend(self.purePathList)
        if(self.bracketsPathList):
            pathList.extend(self.bracketsPathList)
        if(self.squareBracketsPathList):
            pathList.extend(self.squareBracketsPathList)
        return pathList

    def getPathListAsString(self):
        return str(self.getPathList())

    def setPurePathListByString(self, purePathListString:string):
        self.purePathList = purePathListString.split(',')

    def setBracketsPathListByString(self, bracketsPathListString:string):
        self.bracketsPathList = bracketsPathListString.split(',')

    def setSquareBracketsPathListByString(self, squareBracketsPathListString:string):
        self.squareBracketsPathList = squareBracketsPathListString.split(',')

    def toString(self):
        return folderModelStringTemplate % (self.code, self.name, self.middlePath, self.lnSuffixPath, self.rootPath,  self.getAbsolutePath(), self.purePathList, self.bracketsPathList, self.squareBracketsPathList)

def initSquareBracketsPathList(name):
    squareBracketsPattern = re.compile(r'\[.*?\]')
    chineseSquareBracketsPattern = re.compile(r'\【.*?\】')
    squareBracketsPathList = list(set([i[1:-1] for i in squareBracketsPattern.findall(name) if i]))
    squareBracketsPathList.extend(list(set([i[1:-1] for i in chineseSquareBracketsPattern.findall(name) if i])))
    return squareBracketsPathList

def initBracketsPathList(name):
    bracketsPattern = re.compile(r'\(.*?\)')
    return list(set([i[1:-1] for i in bracketsPattern.findall(name) if i]))

def initPurePathList(name):
    templateSplitSign = "--"
    squareBracketsPattern = re.compile(r'\[.*?\]')
    chineseSquareBracketsPattern = re.compile(r'\【.*?\】')
    bracketsPattern = re.compile(r'\(.*?\)')
    name = squareBracketsPattern.sub(templateSplitSign, name)
    name = chineseSquareBracketsPattern.sub(templateSplitSign, name)
    name = bracketsPattern.sub(templateSplitSign, name)
    name = templateSplitSign.join(name.split('/'))
    return list(set([i.strip() for i in re.split(templateSplitSign, name) if i and i != ' ']))

def getHashCode(sourceString):
    md5 = hashlib.md5()
    md5.update(sourceString.encode('utf-8'))
    return md5.hexdigest()