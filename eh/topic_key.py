from eh import constants

class TopicKey(object):
    def __init__(self, conf, path, meta):
        self.path = path
        self.meta = meta
        TopicKey.parse_topic_path(conf, self.path)
        self.keyparts = TopicKey.parse_topic_path(conf, self.path)

    def matches(self, topic_string):
        if topic_string == str(self):
            return True
        return False

    @property
    def shortkey(self):
        return self.keyparts[-1]

    @staticmethod
    def parse_topic_path(conf, path):
        key = path
        for ext in constants.KNOWN_EXT:
            if key.endswith(ext):
                key = "".join(key.rsplit(ext, 1))
        keyparts = key.split(constants.KEY_DIVIDE_CHAR)
        return keyparts

    def __repr__(self):
        return constants.KEY_DIVIDE_CHAR.join(self.keyparts)

