from sqlite3 import connect
from os import path
from shutil import copyfile

# determine if user launches app for the first time, if yes - create game DB
if not path.exists('db/user.db'):
    copyfile('db/default.db', 'db/user.db')

# create database connections and cursors
USER_DB_CONNECTION = connect('db/user.db')
USER_DB_CURSOR = USER_DB_CONNECTION.cursor()
_config_db_connection = connect('db/config.db')
CONFIG_DB_CURSOR = _config_db_connection.cursor()
