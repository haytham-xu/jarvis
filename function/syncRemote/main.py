
from service import testService, folderService
from facade import classifyFacade, categoryFacade, indexFacade, duplicateFacade, authFacade, randomFacade

def main():
    # testService.cleanEnvironment()
    folderService.rebuildFolderStructure()
    testService.initTestEnvironment()
    indexFacade.refreshRemoteIndex()
    classifyFacade.classify()
    categoryFacade.syncCategory()
    duplicateFacade.syncDuplicate()
    authFacade.syncAuth()
    randomFacade.generateRandom()

    # testService.checkRemoteCategory()
    # testService.checkLocalCategoryLn()
    # testService.checkLocalDuplicateLn()
    # testService.checkRemoteDuplicateLn()
    # testService.checkLocalAuthLn()
    # testService.checkRemoteAuthLn()

if __name__ == "__main__":
    main()
