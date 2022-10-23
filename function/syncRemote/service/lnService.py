
import subprocess
import os

def buildLnLocally(localPath, remotePath):
    buildLn(localPath, remotePath)

def buildDuplicateRelativeLnRemote(remoteBasePath, lnRelativeMiddlePath, folderName, folderRemoteAbsolutePath):
    remoteDuplicatePath = remoteBasePath + lnRelativeMiddlePath
    backNumber = len(lnRelativeMiddlePath.split('/')) - 1
    relativeLinkPath = "../"*backNumber + folderRemoteAbsolutePath.removeprefix(remoteBasePath)
    currentcwd = os.getcwd()
    os.chdir(remoteDuplicatePath)
    buildLn(folderName, relativeLinkPath)
    os.chdir(currentcwd)

def buildLn(localPath, remotePath):
    subprocess.call(["ln", "-s", remotePath, localPath])

