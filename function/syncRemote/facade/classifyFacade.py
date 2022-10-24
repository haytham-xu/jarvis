
from service import configService
from service import folderService

config = configService.Config()

def classify():
    for middlePath in config.toCategoryPathList:
        categoryPathWithPrefixAndMiddle = config.localBasePath + middlePath
        folderPureNameList, _ = folderService.getNameOfFoldersAndFilesWithoutRecursion(categoryPathWithPrefixAndMiddle)
        for folderPureName in folderPureNameList:
            localFolderAbsolutePath = categoryPathWithPrefixAndMiddle + folderPureName
            innerFolderPureNameList, innerFilePureNameList = folderService.getNameOfFoldersAndFilesWithoutRecursion(localFolderAbsolutePath)
            folderNumer, fileNumber = folderService.getFolderAndFilesNumberRecursion(localFolderAbsolutePath, innerFolderPureNameList, innerFilePureNameList)
            targetPathTemplate = categoryPathWithPrefixAndMiddle + categoryPathWithPrefixAndMiddle[:-1].split('/')[-1]
            print("classify: ", localFolderAbsolutePath)
            if fileNumber > 150 or folderNumer > 6:
                folderService.move(localFolderAbsolutePath, targetPathTemplate + '_l')
            elif (folderNumer == 0 and fileNumber in range(50, 150)) or folderNumer in range(3,6):
                folderService.move(localFolderAbsolutePath, targetPathTemplate + '_m')
            else:
                folderService.move(localFolderAbsolutePath, targetPathTemplate + '_s')
    config.sqlService.close()

if __name__ == "__main__":
    classify()
