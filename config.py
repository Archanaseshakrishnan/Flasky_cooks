import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'archana_encryption_key'
  MAIL_SERVER = os.environ.get('MAIL_SERVER', 'aseshakr@asu.edu') 
  MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  FLASKY_MAIL_SECRET_PREFIX = '[Flasky]'
  FLASKY_MAIL_SENDER = 'Flasky Admin <aseshakr@asu.edu>'
  FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' 

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
  'development' : DevelopmentConfig,
  'testing' : TestingConfig,
  'production' : ProductionConfig,
  'default' : DevelopmentConfig
}
