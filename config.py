import os


class Config:
    """Parent configuration class"""

    DEBUG = False
    SECRET = os.getenv("SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class DevelopmentConfig(Config):
    """Configuration for development"""

    DEBUG = True


class TestingConfig(Config):
    """Configuration for testing"""

    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production"""

    DEBUG = False
    TESTING = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
