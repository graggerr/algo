import os
import errno
import json
from pathlib import Path

def is_configuration(config_path):
    """Checks if exists configuration on default path"""
    if is_file(config_path):
        return True
    else:
        return False


def is_file(path):
    """
    Checks if path is file.
    :param path: path with filename
    :return: True if file exists
    """
    return os.path.isfile(path)


def is_directory(path):
    """
    Checks if path is directory.
    :param path: path with directory
    :return: True if is directory, False if directory doesn't exist
    """
    if os.path.exists(path):
        return True
    return False


def create_directory(dirname):
    """
    Crete directory if doesn't already exist.
    :param dirname: path with new directory
    :return: path with directory
    """
    if not is_directory(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def get_project_root():
    return Path(__file__).parent.parent

class outputUtil:
    def dataToExl(name_ext1,name_ent2,data):
            filename = "output_{}_{}.xlsx".format(name_ext1,name_ent2)
            data.to_excel(filename)