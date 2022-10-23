
from service import configService
from service import folderService

config = configService.Config()

def classify():
    for middlePath in config.toCategoryPathList:
        categoryPathWithPrefixAndMiddle = config.localBasePath + middlePath
        folderPureNameList, _ = folderService.getNameOfFoldersAndFilesWithoutRecursion(categoryPathWithPrefixAndMiddle)
        for folderPureName in folderPureNameList:
            folderAbsolutePath = categoryPathWithPrefixAndMiddle + folderPureName
            innerFolderPureNameList, innerFilePureNameList = folderService.getNameOfFoldersAndFilesWithoutRecursion(folderAbsolutePath)
            folderNumer, fileNumber = folderService.getFolderAndFilesNumberRecursion(folderAbsolutePath, innerFolderPureNameList, innerFilePureNameList)
            targetPathTemplate = categoryPathWithPrefixAndMiddle + categoryPathWithPrefixAndMiddle[:-1].split('/')[-1]
            if fileNumber > 150 or folderNumer > 6:
                folderService.move(folderAbsolutePath, targetPathTemplate + '_l')
            elif (folderNumer == 0 and fileNumber in range(50, 150)) or folderNumer in range(3,6):
                folderService.move(folderAbsolutePath, targetPathTemplate + '_m')
            else:
                folderService.move(folderAbsolutePath, targetPathTemplate + '_s')

if __name__ == "__main__":
    classify()
