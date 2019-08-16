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
    copyfile('db/default.db', 'db/user.db')
    try:
        delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    except PasswordDeleteError:
        pass

    with open('db/user.db', 'rb') as f1:
        data = f1.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data[::3] + data[1::3] + data[2::3]).hexdigest())

# create database connections and cursors
USER_DB_CONNECTION = connect('db/user.db')
USER_DB_CURSOR = USER_DB_CONNECTION.cursor()
_config_db_connection = connect('db/config.db')
CONFIG_DB_CURSOR = _config_db_connection.cursor()


def on_commit():
    delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    USER_DB_CONNECTION.commit()
    with open('db/user.db', 'rb') as f:
        data1 = f.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data1[::3] + data1[1::3] + data1[2::3]).hexdigest())
