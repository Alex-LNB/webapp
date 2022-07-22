class Config:
    SECRET_KEY = 'Llave_secreta_csrf'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/webapp_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ImplementConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/webapp_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development' : DevelopmentConfig,
    'implement' : ImplementConfig
}