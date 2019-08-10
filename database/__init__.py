from sqlite3 import connect
from os import path
from shutil import copyfile
from hashlib import sha512

from keyring import set_password, delete_password, set_keyring
from keyring.errors import PasswordDeleteError
from keyring.backends import Windows


set_keyring(Windows.WinVaultKeyring())
# determine if user launches app for the first time, if yes - create game DB
if not path.exists('db/user.db'):
    try:
        delete_password(sha512('config_db'.encode('utf-8')).hexdigest(),
                        sha512('config_db'.encode('utf-8')).hexdigest())
    except PasswordDeleteError:
        pass

    with open('db/config.db', 'rb') as f1, open('db/default.db', 'rb') as f2:
        set_password(sha512('config_db'.encode('utf-8')).hexdigest(), sha512('config_db'.encode('utf-8')).hexdigest(),
                     sha512((f1.read() + f2.read())[::-1]).hexdigest())

    copyfile('db/default.db', 'db/user.db')
    try:
        delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    except PasswordDeleteError:
        pass

    with open('db/user.db', 'rb') as f1:
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(f1.read()[::-1]).hexdigest())

# create database connections and cursors
USER_DB_CONNECTION = connect('db/user.db')
USER_DB_CURSOR = USER_DB_CONNECTION.cursor()
_config_db_connection = connect('db/config.db')
CONFIG_DB_CURSOR = _config_db_connection.cursor()


def on_commit():
    delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    USER_DB_CONNECTION.commit()
    with open('db/user.db', 'rb') as f:
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(f.read()[::-1]).hexdigest())


def on_recalculate_config_db():
    delete_password(sha512('config_db'.encode('utf-8')).hexdigest(), sha512('config_db'.encode('utf-8')).hexdigest())
    with open('db/config.db', 'rb') as x, open('db/default.db', 'rb') as y:
        set_password(sha512('config_db'.encode('utf-8')).hexdigest(), sha512('config_db'.encode('utf-8')).hexdigest(),
                     sha512((x.read() + y.read())[::-1]).hexdigest())
