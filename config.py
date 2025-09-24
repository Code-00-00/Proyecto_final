# config.py
import os

class Config:
    # Configuración de MySQL para XAMPP
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/final_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'tu_clave_secreta_aqui_cambiala'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True
    }

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}