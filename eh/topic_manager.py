import os

from eh import constants
from eh import topic_store as ts
from eh import git_store as gs


class TopicManager(object):
    def __init__(self, conf):
        self.topic_stores = self._gather_topics(conf)

    def _topic_store_path(self, name):
        return os.path.join(constants.CONF_DIR, name)

    def _gather_topics(self, conf):
        out = []
        if not conf:
            return out
        for name, location in conf.items(constants.CONF_TOPIC_STORE):
            if location.startswith('https://github.com/'):
                t_store = gs.GitTopicStore(
                    conf, location, self._topic_store_path(name))
            else:
                t_store = ts.TopicStore(conf, location)
            t_store.initialize(conf)
            out.append(t_store)
        return out

    def update(self):
        for s in self.topic_stores:
            s.update()

    def has_topic(self, topic):
        for s in self.topic_stores:
            if s.has_topic(topic):
                return True
        return False

    def get_topic(self, topic):
        for s in self.topic_stores:
            if s.has_topic(topic):
                return s.get_topic(topic)
        return None

    def has_parent(self, parent):
        for s in self.topic_stores:
            if s.has_parent(parent):
                return True
        return False

    def get_topics_for_parent(self, parent):
        ret = []
        pret = []
        for s in self.topic_stores:
            topics, parents = s.get_topics_for_parent(parent)
            if topics:
                ret.extend(topics)
            if parents:
                pret.extend(parents)
        return ret, pret

    def get_root_list(self):
        return self.get_topics_for_parent("")
