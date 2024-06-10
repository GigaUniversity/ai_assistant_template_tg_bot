import os
from datetime import datetime, timedelta, timezone
import logging.config

from source.config import Config

# Установка часового пояса
moscow_tz = timezone(timedelta(hours=3), name='MSC')
now = datetime.now(tz=moscow_tz)

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
        'tg_bot': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'reaction': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
}


# Инициализация логгера
logging.config.dictConfig(logger_config)
logger = logging.getLogger('tg_bot')
reaction_logger = logging.getLogger('reaction')
