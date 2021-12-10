import os
import errno
import json


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



class outputUtil:
    def dataToExl(symbol_name,strategy,data):
            filename = "output_{}_{}.xlsx".format(strategy,symbol_name)
            data.to_excel(filename)