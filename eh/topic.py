import os
import yaml

from eh import constants
from eh import exceptions as exc
from eh import topic_key as tk

class Topic(object):
    def __init__(self, conf, root_node, rootpath, path):
        self.path = path
        if root_node is None or not isinstance(root_node, dict):
            raise exc.TopicStoreInvalidRoot()
        self.root_node = root_node
        if rootpath is None or not isinstance(rootpath, str) or not rootpath:
            raise exc.TopicInvalidRootPath()
        self.rootpath = rootpath
        self.meta, self.summary, self.text = (
            Topic.parse_topic_contents(conf, root_node, rootpath, path))
        self.key = tk.TopicKey(conf, self.path, self.meta)
        Topic.map_topic_path_to_root_node(conf, root_node, path, self)

    def meta_match(self, meta_string):
        return self.key.metascore(meta_string, self.summary)

    def is_topic(self, topic):
        if self.key.matches(topic):
            return True
        return False
    
    @property
    def shortkey(self):
        return self.key.shortkey

    def __repr__(self):
        return constants.STR_TOPIC_REPR % (
            self.key, len(self.text), self.meta, self.summary)

    @staticmethod
    def map_topic_path_to_root_node(conf, root_node, path, node):
        path_parts = path.split(constants.KEY_DIVIDE_CHAR)
        current_node = root_node
        if constants.PARENT_KEY not in root_node:
            root_node[constants.PARENT_KEY] = {}
        for i in range(len(path_parts)):
            if i == len(path_parts) - 1:  # leaf nodes
                if constants.TOPIC_KEY not in current_node:
                    current_node[constants.TOPIC_KEY] = []
                current_node[constants.TOPIC_KEY].append(node)
            else:
                p = path_parts[i]
                if p not in current_node:
                    current_node[p] = {}
                current_node = current_node[p]
                parent_path = constants.KEY_DIVIDE_CHAR.join(path_parts[0:i+1])
                if parent_path not in root_node[constants.PARENT_KEY]:
                    root_node[constants.PARENT_KEY][parent_path] = current_node

    @staticmethod
    def get_cheatsheet_parts(data):
        data_copy = data[:]
        data_copy.pop(0)
        header = []
        end_header_found = False
        while not end_header_found:
            line = data_copy.pop(0)
            if line == '---':
                end_header_found = True
                break
            header.append(line)
        yaml_text = constants.CR_CHAR.join(header)
        header_object = yaml.load(yaml_text, Loader=yaml.FullLoader)
        return header_object, constants.CR_CHAR.join(data_copy)

    @staticmethod
    def check_cheatsheet_format(data):
        header_object, text = Topic.get_cheatsheet_parts(data)
        valid_attributes = [
            'title', 'layout', 'category', 'updated', 'ads', 'weight',
            'deprecated', 'deprecated_by', 'prism_languages', 'intro',
            'tags', 'type', 'home']
        required_attributes = ['title']
        for attribute in header_object.keys():
            if attribute not in valid_attributes:
                return False
        for required in required_attributes:
            if required not in header_object.keys():
                return False
        return True

    @staticmethod
    def determine_format(data):
        data_copy = data[:]
        top_line = data_copy.pop(0)
        if top_line == '---':  # possibly cheatsheet format
            if Topic.check_cheatsheet_format(data):
                return 'cheatsheet'
        if not Topic.check_comment_format(top_line):
            raise exc.TopicError("Missing expected preamble")
        return 'eh'

    @staticmethod
    def parse_eh_format(data):
        data_copy = data[:]
        top_line = data_copy.pop(0)
        text = constants.CR_CHAR.join(data_copy)
        meta, summary = Topic.split_meta_from_summary(top_line)
        return meta, summary, text

    @staticmethod
    def parse_cheatsheet_format(data):
        data_copy = data[:]
        header_object, text = Topic.get_cheatsheet_parts(data_copy)
        meta = header_object.get('tags', [])
        meta.extend(header_object.get('category', []))
        summary = header_object.get('intro', "")
        return meta, summary, text

    @staticmethod
    def parse_topic_contents(conf, root_node, root, path):
        fullpath = os.path.join(root, path)
        try:
            with open(fullpath, 'r') as myfile:
                data = myfile.read().splitlines()
                file_format = Topic.determine_format(data)
                if file_format == 'eh':
                    return Topic.parse_eh_format(data)
                if file_format == 'cheatsheet':
                    return Topic.parse_cheatsheet_format(data)
        except IOError:
            pass
        return None, None, None

    @staticmethod
    def remove_comment_preamble(text):
        """
        Removes the comment preamble from a single line of text and returns
        the rest.
        """
        return text.replace(
            constants.COMMENT_PREAMBLE, constants.EMPTY).strip()

    @staticmethod
    def split_meta_from_summary(text):
        """
        Returns the meta tags and summary as tuple from comment line

        Input such as:
            (tag1, tag2) Summary...

        Would return:
            (["tag1", "tag2"]), "Summary..."
        """
        text = Topic.remove_comment_preamble(text)
        meta = text[0:text.index(constants.META_END_CHAR)+1]
        text = text.replace(meta, constants.EMPTY).strip()
        meta = meta.replace(constants.META_END_CHAR, constants.EMPTY).replace(
            constants.META_START_CHAR, constants.EMPTY)
        meta_list = [m.strip() for m in meta.split(constants.META_DIVIDE_CHAR)]
        return meta_list, text

    @staticmethod
    def check_comment_format(text):
        """
        Checks a single line to see if it satisfies requirements to be a real
        comment
        """
        if not text or not isinstance(text, str):
            return False
        if not text or not text.startswith(constants.COMMENT_PREAMBLE):
            return False
        text = Topic.remove_comment_preamble(text)
        if (
                not text.startswith(constants.META_START_CHAR)
                or constants.META_END_CHAR not in text):
            return False
        meta, text = Topic.split_meta_from_summary(text)
        return any(meta) and (text)
