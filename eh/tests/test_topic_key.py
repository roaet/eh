import mock

from eh import constants
from eh import exceptions as exc
from eh.tests import base_test as base
from eh import topic_key as tk
from eh.topic_key import TopicKey


class TestTopicKey(base.TestCase):
    def setUp(self):
        super(TestTopicKey, self).setUp()
        self.conf = {}
        self.path = "parent/topic.md"
        self.meta = None

    def tearDown(self):
        super(TestTopicKey, self).tearDown()
        mock.patch.stopall()

    def test_create_key(self):
        key = tk.TopicKey(self.conf, self.path, self.meta)
        self.assertIsNotNone(key)

    def test_metascore_does_not_raise(self):
        key = tk.TopicKey(self.conf, self.path, self.meta)
        self.assertNotEqual(0, key.metascore(self.path, ""))
        key = tk.TopicKey({}, "", None)
        self.assertEqual(0, key.metascore(self.path, ""))

    def test_matches(self):
        key = tk.TopicKey(self.conf, self.path, self.meta)
        self.assertTrue(key.matches('parent/topic'))
        self.assertFalse(key.matches('topic'))
        self.assertFalse(key.matches('parent'))
        self.assertFalse(key.matches('topic/parent'))

    def test_short_key(self):
        key = tk.TopicKey(self.conf, self.path, self.meta)
        self.assertEqual('topic', key.shortkey)
        self.assertNotEqual('parent', key.shortkey)
        self.assertNotEqual('parent/topic', key.shortkey)

    def test_parse_topic_path(self):
        keyparts = tk.TopicKey.parse_topic_path(self.conf, "simple")
        self.assertIsNotNone(keyparts)
        self.assertEquals(1, len(keyparts))
        self.assertEquals("simple", keyparts[0])

        keyparts = tk.TopicKey.parse_topic_path(self.conf, "parent/simple")
        self.assertIsNotNone(keyparts)
        self.assertEquals(2, len(keyparts))
        self.assertEquals("parent", keyparts[0])
        self.assertEquals("simple", keyparts[1])

        with mock.patch('eh.constants.KNOWN_EXT', ['.ext']) as mock_ext:
            keyparts = tk.TopicKey.parse_topic_path(self.conf, "simple.ext")
            self.assertIsNotNone(keyparts)
            self.assertEquals(1, len(keyparts))
            self.assertEquals("simple", keyparts[0])

    def test_parse_topic_paths_ignore_internal_extension(self):
        with mock.patch('eh.constants.KNOWN_EXT', ['.ext']) as mock_ext:
            keyparts = tk.TopicKey.parse_topic_path(self.conf, "whoa.ext.ext")
            self.assertIsNotNone(keyparts)
            self.assertEquals(1, len(keyparts))
            self.assertEquals("whoa.ext", keyparts[0])

    def test_topic_key_repr(self):
        key = tk.TopicKey(self.conf, self.path, self.meta)
        self.assertTrue(key.matches('parent/topic'))
        self.assertTrue('parent/topic', str(key))

    def test_get_key_metascore_precedence(self):
        key = tk.TopicKey(self.conf, "parent/foo", ["parent", "foo"])
        summary = "parent/foo"
        lookup = "parent/foo"

        ks, kr = TopicKey._key_metascore(lookup, key)
        ss, sr = TopicKey._shortkey_metascore(lookup, key)
        ms, mr = TopicKey._meta_metascore(lookup, key)
        sums, sumr = TopicKey._summary_metascore(lookup, summary)
        print(ks, ss, ms, sums)
        print(kr, sr, mr, sumr)
        self.assertEqual(kr, max([kr, sr, mr, sumr]))
        self.assertTrue(kr > sr and sr > mr and mr > sumr)
