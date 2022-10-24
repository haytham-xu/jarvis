
from service import testService, folderService
from facade import classifyFacade, categoryFacade, indexFacade, duplicateFacade, authFacade, randomFacade

def main():
    # testService.cleanEnvironment()
    folderService.rebuildFolderStructure()
    # testService.initTestEnvironment()
    print("---refreshRemoteIndex start---")
    indexFacade.refreshRemoteIndex()
    print("---classify start---")
    classifyFacade.classify()
    print("---syncCategory start---")
    categoryFacade.syncCategory()
    print("---syncDuplicate start---")
    duplicateFacade.syncDuplicate()
    print("---syncAuth start---")
    authFacade.syncAuth()
    print("---generateRandom start---")
    randomFacade.generateRandom()

    # testService.checkRemoteCategory()
    # testService.checkLocalCategoryLn()
    # testService.checkLocalDuplicateLn()
    # testService.checkRemoteDuplicateLn()
    # testService.checkLocalAuthLn()
    # testService.checkRemoteAuthLn()

if __name__ == "__main__":
    main()
