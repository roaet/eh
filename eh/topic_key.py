from fuzzywuzzy import fuzz

from eh import constants

class TopicKey(object):
    def __init__(self, conf, path, meta):
        self.path = path
        self.meta = [] if not meta else meta
        TopicKey.parse_topic_path(conf, self.path)
        self.keyparts = TopicKey.parse_topic_path(conf, self.path)

    def metascore(self, meta_string, summary):
        return TopicKey.get_key_metascore(self, meta_string, summary)

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

    @staticmethod
    def get_key_metascore(key, meta_string, summary):
        meta_parts = meta_string.split(constants.KEY_DIVIDE_CHAR)
        meta_str_spaced = meta_string.replace(
            constants.KEY_DIVIDE_CHAR, ' ')
        key_meta_spaced = ' '.join(key.meta)

        key_ratio = fuzz.ratio(meta_string, str(key))
        short_ratio = fuzz.ratio(meta_string, key.shortkey)
        meta_ratio = fuzz.token_set_ratio(meta_str_spaced, key_meta_spaced)
        summary_ratio = fuzz.token_set_ratio(meta_str_spaced, summary)
        MAX_MATCH = 100

        if key_ratio == MAX_MATCH:
            return MAX_MATCH
        SHORTKEY_WEIGHT = 0.4
        KEY_WEIGHT = 0.3
        META_WEIGHT = 0.2
        SUMMARY_WEIGHT = 0.1
        final = (
            short_ratio * SHORTKEY_WEIGHT +
            key_ratio * KEY_WEIGHT +
            meta_ratio * META_WEIGHT +
            summary_ratio * SUMMARY_WEIGHT)
        return final 

    def __repr__(self):
        return constants.KEY_DIVIDE_CHAR.join(self.keyparts)
