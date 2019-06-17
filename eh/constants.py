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
TOPIC_KEY = "_"
PARENT_KEY = "_parents"
STR_TOPIC_REPR = "%s %d chars %s %s" 

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
USERHOME = os.path.expanduser('~')
