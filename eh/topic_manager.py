import os

from eh import constants
from eh import topic_store as ts
from eh import git_store as gs


class TopicManager(object):
    def __init__(self, conf, repos=[], min_score=30):
        self.repos = repos
        self.min_score = min_score
        self._topic_stores = self._gather_topics(conf)

    @property
    def topic_stores(self):
        out = []
        if len(self.repos) == 0:
            return self._topic_stores
        for s in self._topic_stores:
            if s.name in self.repos:
                out.append(s)
        return out

    def _topic_store_path(self, name):
        return os.path.join(constants.CONF_DIR, name)

    def _gather_topics(self, conf):
        out = []
        if not conf:
            return out
        for name, location in conf.items(constants.CONF_TOPIC_STORE):
            if len(self.repos) > 0 and name not in self.repos:
                continue
            if location.startswith('https://github.com/'):
                t_store = gs.GitTopicStore(
                    conf, location, self._topic_store_path(name), name)
            else:
                t_store = ts.TopicStore(conf, location, name)
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

    def meta_search(self, meta_string):
        out = []
        for s in self.topic_stores:
            meta_results = s.meta_search(meta_string)
            if len(meta_results) > 0:
                out.extend([
                    r for r in meta_results if r[0] > self.min_score])
        out_sort = sorted(out, key=lambda x: x[0], reverse=True)
        return out_sort

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

    def get_all_topics(self):
        out = []
        for s in self.topic_stores:
            out.extend([(s.name, t) for t in s.get_all_topics()])
        return out

    def get_root_list(self):
        return self.get_topics_for_parent("")
