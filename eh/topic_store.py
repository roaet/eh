import os

from eh import constants
from eh import exceptions
from eh import topic

class TopicStore(object):
    def __init__(self, conf, filepath):
        self.root_node = {}
        self.root_node[constants.PARENT_KEY] = {}
        self.filepath = filepath
        self.topic_paths = self._gather_topics(conf, filepath, filepath)
        self._topics = self._parse_topics(
            conf, self.root_node, self.filepath, self.topic_paths)

    def update(self):
        pass

    def _gather_topics(self, conf, mainpath, filepath):
        found_topics = []
        for f in os.listdir(filepath):
            full_path = os.path.join(filepath, f)
            if (
                    not os.path.isdir(full_path) and 
                    f.lower().endswith(tuple(constants.KNOWN_EXT))):
                found_topics.append(full_path)
            if os.path.isdir(full_path):
                found_topics.extend(self._gather_topics(
                    conf, mainpath, full_path))
        found_topics = [
            p.replace(mainpath, constants.EMPTY) for p in found_topics]
        return found_topics

    def _parse_topics(self, conf, root_node, rootpath, topic_paths):
        topics = []
        for p in topic_paths:
            try:
                t = topic.Topic(conf, root_node, rootpath, p)
                topics.append(t)
            except exceptions.TopicError:
                continue
        return topics

    def _parents(self):
        return self.root_node[constants.PARENT_KEY]

    def has_topic(self, topic):
        for t in self._topics:
            if t.is_topic(topic):
                return True
        return False

    def has_parent(self, parent):
        return parent in self._parents()

    def get_topic(self, path):
        path_parts = path.split(constants.KEY_DIVIDE_CHAR)
        node = self.root_node
        if len(path_parts) > 1:
            for k in path_parts[:-1]:
                node = node[k]

        for topic in node[constants.TOPIC_KEY]:
            if topic.is_topic(path):
                return topic
        return None
    
    def get_topics_for_parent(self, parent):
        p = self.root_node
        if parent:
            p = self._parents().get(parent, None)
        if p is None:
            return None, None
        return p.get(
            constants.TOPIC_KEY, []), TopicStore.get_filtered_parent_keys(p)

    @staticmethod
    def get_filtered_parent_keys(parent_node):
        drop_list = [constants.PARENT_KEY, constants.TOPIC_KEY]
        return [k for k in parent_node.keys() if k not in drop_list]
