
import yaml

def getConfig(configPath):
    with open(configPath, 'rb') as conf:
        configs = yaml.safe_load(conf)
        with open(configs['currentConfig'], 'rb') as curConf:
            curConfigs = yaml.safe_load(curConf)
            return curConfigs['dbPath'], curConfigs['topLevelFolderPath'], curConfigs['subFolderSuffix']
