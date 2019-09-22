import os

COMMENT_PREAMBLE = '[//]: #'
META_START_CHAR = '('
META_END_CHAR = ')'
META_DIVIDE_CHAR = ','
CR_CHAR = '\n'
KNOWN_EXT = ['.md']
KEY_DIVIDE_CHAR = os.sep
EMPTY = ''
CONF_TOPIC_STORE = 'topic_stores'
CONF_DIR_NAME = '.eh'
CONF_NAME = 'eh.ini'
TOPIC_KEY = "_"
PARENT_KEY = "_parents"
STR_TOPIC_REPR = "%s %d chars %s %s" 

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
DEFAULT_STORE = os.path.join(ROOT_DIR, 'contrib/subjects/')
PACKAGE_DIR = os.path.join(ROOT_DIR)
USERHOME = os.path.expanduser('~')
CONF_DIR = os.path.join(USERHOME, CONF_DIR_NAME)
CONF_FILE = os.path.join(CONF_DIR, CONF_NAME)
DEFAULT_CONF = os.path.join(PACKAGE_DIR, 'default_conf.ini')
