from sqlite3 import connect
from os import path, makedirs
from shutil import copyfile
from hashlib import sha512

from keyring import set_password, delete_password, set_keyring
from keyring.errors import PasswordDeleteError
from keyring.backends import Windows
from pyglet.resource import get_settings_path


set_keyring(Windows.WinVaultKeyring())
# determine if user launches app for the first time, if yes - create game DB
USER_DB_LOCATION = get_settings_path(sha512('rssim'.encode('utf-8')).hexdigest())
if not path.exists(USER_DB_LOCATION):
    makedirs(USER_DB_LOCATION)

if not path.exists(path.join(USER_DB_LOCATION, 'user.db')):
    copyfile('db/default.db', path.join(USER_DB_LOCATION, 'user.db'))
    try:
        delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    except PasswordDeleteError:
        pass

    with open(path.join(USER_DB_LOCATION, 'user.db'), 'rb') as f1:
        data = f1.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data[::3] + data[1::3] + data[2::3]).hexdigest())

# create database connections and cursors
USER_DB_CONNECTION = connect(path.join(USER_DB_LOCATION, 'user.db'))
USER_DB_CURSOR = USER_DB_CONNECTION.cursor()
__config_db_connection = connect('db/config.db')
CONFIG_DB_CURSOR = __config_db_connection.cursor()


def on_commit():
    delete_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest())
    USER_DB_CONNECTION.commit()
    with open(path.join(USER_DB_LOCATION, 'user.db'), 'rb') as f:
        data1 = f.read()[::-1]
        set_password(sha512('user_db'.encode('utf-8')).hexdigest(), sha512('user_db'.encode('utf-8')).hexdigest(),
                     sha512(data1[::3] + data1[1::3] + data1[2::3]).hexdigest())
