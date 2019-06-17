from eh import constants
from eh import topic_store as ts


class TopicManager(object):
    def __init__(self, conf):
        self.topic_stores = self._gather_topics(conf)

    def _gather_topics(self, conf):
        out = []
        for t in conf.get(constants.CONF_TOPIC_STORE, []):
            t_store = ts.TopicStore(conf, t)
            out.append(t_store)
        return out

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
