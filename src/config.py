
class config():
    SECRET_KEY = "carolina"

class DevelopmentConfig(config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = "travel_quotes"

config = {
    'development': DevelopmentConfig
}

