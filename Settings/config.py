import os

class Common(object):
    MYSQL_IP_ADDRESS = os.getenv('MYSQL_IP_ADDRESS')
    MYSQL_PORT = os.getenv('MYSQL_PORT')

class Dev(Common):
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

class Production(Common):
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')