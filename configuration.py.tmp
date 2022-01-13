import os
import yaml

# from strategies.utils import is_file, create_directory
from Util import is_file, create_directory


class Configuration:
    """
    Module for working with configuration file.
    """

    # By default user’s home location ./eth-wallet directory is where to save config file
    config_dir = os.path.expanduser('~') + '/.algo'
    config_file = '/config.yaml'
    # print ("Configuration file",config_dir,config_file)
    # Default configuration yaml file will be created from this dictionary
    initial_test_config = dict(
        keystore_location=config_dir,
        # keystore_filename='/keystore'
        td_consumer_key='',

        client_id = '',
        account_id = '',
        refresh_token = '',
    )

    initial_dev_config = dict(
        keystore_location=config_dir,
        # keystore_filename='/keystore',
        td_consumer_key='',

        client_id='',
        account_id='',
        refresh_token='',
    )

    initial_config=initial_test_config #initial_dev_config

    def __init__(self,
                 config_dir=config_dir,
                 config_file=config_file,
                 initial_config=initial_config):

        # default class paths can be override in test within constructor
        self.config_dir = config_dir
        self.config_file = config_file
        self.config_path = config_dir + config_file
        self.initial_config = initial_config

        # Variables from configuration file. They will be initialized after load_configuration() call
        # self.keystore_filename = ''


    def is_configuration(self):
        """Checks if exists configuration on default path"""
        if is_file(self.config_path):
            return True
        else:
            return False

    def load_configuration(self):
        """Load bot configuration from .yaml file"""
        if not is_file(self.config_path):
            self.create_empty_configuration()
            self.load_configuration()
        else:
            with open(self.config_path, 'r') as yaml_file:
                file = yaml.safe_load(yaml_file)
            for key, value in file.items():
                setattr(self, key, value)
        return self

    def create_empty_configuration(self):
        """
        Creates and initialize empty configuration file
        :return: True if config file created successfully
        """
        create_directory(self.config_dir)
        with open(self.config_path, 'w+') as yaml_file:
            yaml.dump(self.initial_config, yaml_file, default_flow_style=False)

        return True


    def __update_configuration(self, parameter_name, parameter_value):
        """
        Updates configuration file.
        :param parameter_name: parameter name to change or append
        :param parameter_value: value to parameter_key
        :return: True if config file updated successfully
        """
        with open(self.config_path, 'r') as yaml_file:
            file = yaml.safe_load(yaml_file)

        file[parameter_name] = parameter_value

        create_directory(self.config_dir)
        with open(self.config_path, 'w+') as yaml_file:
            yaml.dump(file, yaml_file, default_flow_style=False)

        return True
