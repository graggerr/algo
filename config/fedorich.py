import json
import os
from configparser import ConfigParser

import td
from td.client import TDClient
from tda.auth import client_from_token_file, __token_loader
from tda.auth import client_from_login_flow
from selenium import webdriver
from config.Util import get_project_root

#


token_path = 'token.pickle'

from selenium.webdriver import Safari

def is_file(path):
    """
    Checks if path is file.
    :param path: path with filename
    :return: True if file exists
    """
    return os.path.isfile(path)

# driver = Safari()

config = ConfigParser()
CONFIG_PATH = os.path.join(get_project_root(), 'config/config.ini')  # requires `import os`
config.read(CONFIG_PATH)
CLIENT_ID = config.get('main', 'CLIENT_ID')
api_key="{}{}".format(CLIENT_ID,'@AMER.OAUTHAP')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
redirect_uri=REDIRECT_URI
CREDENTIALS_PATH = "{}{}".format(get_project_root(),config.get('main', 'JSON_PATH'))
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')


if is_file(token_path):
    client = client_from_token_file(token_path, api_key)
else:
    driver = webdriver.Chrome(executable_path=r"/usr/local/bin/chromedriver")
    client = client_from_login_flow(driver, api_key, redirect_uri, token_path,)

tl=__token_loader(token_path)
token_dict=tl()
print(   token_dict['token'])
tdclient=TDClient(client_id=api_key, redirect_uri=redirect_uri, credentials_path="current_session.json", _do_init = False)


tdclient._token_save(token_dict=token_dict['token'],includes_refresh=True)