from Settings.config import Dev, Production
import os

config_space = os.getenv('CONFIG_SPACE', 'DEV')
if config_space:
    if config_space == 'DEV':
        auto_config = Dev
    elif config_space == 'PRODUCTION':
        auto_config = Production
    else:
        auto_config = None
        raise EnvironmentError(f'CONFIG_SPACE is unexpected value: {config_space}')
else:
    raise EnvironmentError('CONFIG_SPACE environment variable is not set!')