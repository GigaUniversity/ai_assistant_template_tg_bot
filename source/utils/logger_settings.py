import os
from datetime import datetime
import logging.config

from source.config import Config


now = datetime.now()

# Создание папки логов, если её нет
path_to_logs = os.path.join(Config.PROJECT_DIR, 'logs')
os.makedirs(path_to_logs, exist_ok=True)

file_name = f'{path_to_logs}/{Config.UNI_ID}_{now.strftime("%d_%m_%Y_time_%H_%M_%S")}.log'


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': file_name,
            'mode': "w"
        }
    },
    'loggers': {
        'TG_BOT': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'REACTION': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
}


# Инициализация логгера
logging.config.dictConfig(logger_config)
logger = logging.getLogger('TG_BOT')
reaction_logger = logging.getLogger('REACTION')