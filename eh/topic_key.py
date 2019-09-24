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
    def _key_metascore(lookup, key):
        s = fuzz.ratio(lookup, str(key))
        if lookup == str(key):
            s = constants.MATCH
        return s, s * constants.KEY_WEIGHT

    @staticmethod
    def _shortkey_metascore(lookup, key):
        s = fuzz.ratio(lookup, key.shortkey)
        if lookup == key.shortkey:
            s = constants.MATCH
        return s, s * constants.SHORTKEY_WEIGHT

    @staticmethod
    def _meta_metascore(lookup, key):
        l = lookup.replace(constants.KEY_DIVIDE_CHAR, ' ')
        s = fuzz.token_set_ratio(l, ' '.join(key.meta))
        if lookup == ','.join(key.meta):
            s = constants.MATCH
        return s, s * constants.META_WEIGHT

    @staticmethod
    def _summary_metascore(lookup, summary):
        l = lookup.replace(constants.KEY_DIVIDE_CHAR, ' ')
        s = fuzz.token_set_ratio(l, summary)
        if lookup == summary:
            s = constants.MATCH
        return s, s * constants.SUMMARY_WEIGHT

    @staticmethod
    def get_key_metascore(key, lookup, summary):
        key_score, key_ratio = TopicKey._key_metascore(lookup, key)
        short_score, short_ratio = TopicKey._shortkey_metascore(lookup, key)
        meta_score, meta_ratio = TopicKey._meta_metascore(lookup, key)
        summary_score, summary_ratio = TopicKey._summary_metascore(
            lookup, summary)

        if key_score == constants.MATCH:
            return constants.MATCH
        final = short_ratio + key_ratio + meta_ratio + summary_ratio
        return final 

    def __repr__(self):
        return constants.KEY_DIVIDE_CHAR.join(self.keyparts)
