# https://www.jianshu.com/p/da28160541ce
import os
from datetime import timedelta


class BaseConfig:
    VERSION = os.popen("git rev-parse --short HEAD").read()

    # JWT TOKEN Config
    TOKEN_EXPIRES_IN = 3600


class DevelopmentConfig(BaseConfig):
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=5)


class TestingConfig(BaseConfig):
    SERVER_NAME = "vm.dutbit.com"


class ProductionConfig(BaseConfig):
    SERVER_NAME = "www.dutbit.com"


dictConfig = {"development": DevelopmentConfig, "testing": TestingConfig, "production": ProductionConfig}
