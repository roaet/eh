import os

from eh import constants
from eh import exceptions as exc
from eh import topic

class TopicStore(object):
    """
    The TopicStore class contains the root node of the topic graph.

    All topics can be mapped from the root node. The code to produce the graph
    is in the Topic module.

    The graph structure is used to store the parent/child relationships in
    topics. It allows for easy lookup and display of options.

    The root node is a dict. It looks like this:

        root = {
            constants.PARENT_KEY: ["parent"],
            constants.TOPIC_KEY: ["topic1"],
            "parent": { constants.TOPIC_KEY: ["topic2"] }
        }

    - constants.PARENT_KEY provides a list of all parents within the graph
    - constants.TOPIC_KEY provides all topics on the same level (in this case
      root)
    - every key afterwards is the parent and its value is a dict with the same
      structure relative to the same level (in this case root) except they will
      not have the PARENT_KEY

    self._topics is a flattened list of all topic objects in this store

    """
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
        """
        Given paths locate files with known extensions and return as list.

        This method is recursive and will search subdirectories.

        On initial call mainpath and filepath will likely be the same. The 
        mainpath will be the root of the topic store, and the filepath will
        hold the current subdirectory being searched.

        All files will have their paths returned relative to mainpath (this
        means that mainpath shouldn't be in the return).
        """
        found_topics = []
        if not conf or not mainpath or not filepath:
            return found_topics
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
        """
        Produce all topic objects given a list of paths and store in graph
        structure whose root is represented by root_node.

        rootpath: is a common path shared by everything in the store and is
        not used for topic 'keying' (the absolute path leading up to where
        the topic store begins)

        topic_paths: is a list of topic_paths starting from rootpath. this path
        is used for topic 'keying'

        returns: a list of all topic objects created during this process
        """
        topics = []
        for p in topic_paths:
            try:
                t = topic.Topic(conf, root_node, rootpath, p)
                topics.append(t)
            except exc.TopicError:
                continue
        return topics

    def _parents(self):
        """
        Return a list of all parents for this store.

        All parents (subdirectories) encountered are stored in a list on the
        root node.
        """
        return self.root_node[constants.PARENT_KEY]

    def topic_count(self):
        return len(self._topics)

    def has_topic(self, topic):
        for t in self._topics:
            if t.is_topic(topic):
                return True
        return False

    def has_parent(self, parent):
        return parent in self._parents()

    def get_topic(self, path):
        """
        Return the topic object given a path.

        Locate the specific topic object by traversing the graph using the
        path. It walks the path until it reaches the 'level' where the topic
        node should be.
        """
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
        """
        Given a parent, the root if parent is None, return topics and subtopics
        """
        p = self.root_node
        if parent:
            p = self._parents().get(parent, None)
        if p is None:
            return None, None
        return p.get(
            constants.TOPIC_KEY, []), TopicStore.get_filtered_parent_keys(p)

    @staticmethod
    def get_filtered_parent_keys(parent_node):
        """
        Produces a list of keys (sub-directories and topics) for a parent.
        """
        drop_list = [constants.PARENT_KEY, constants.TOPIC_KEY]
        try:
            return [k for k in parent_node.keys() if k not in drop_list]
        except AttributeError:
            raise exc.InvalidValue(
                "Provided parent node is invalid (expected a dict)")
