

import logging, time
from service import configService

config = configService.Config()

logging.basicConfig(filename= config.logBasePath + '/' + time.strftime("%Y%m%d", time.localtime()) +'.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)
