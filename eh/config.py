import os
import shutil

from ConfigObject import ConfigObject

from eh import constants


def is_true(value):
    return value.upper() in ['TRUE', 'T', 'YES']


def open_config():
    if not os.path.exists(constants.CONF_DIR):
        os.mkdir(constants.CONF_DIR)
    if not os.path.exists(constants.CONF_FILE):
        shutil.copyfile(
            constants.DEFAULT_CONF,
            constants.CONF_FILE)
    return ConfigObject(filename=constants.CONF_FILE)
