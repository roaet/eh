import mock
import unittest2 as unittest

from eh import constants
from eh import exceptions as exc
from eh.tests import base_test as base
from eh import topic as top


class TestTopic(base.TestCase):
    def setUp(self):
        super(TestTopic, self).setUp()

        self.good_data = """[//]: # (testing) This is test contents
# Something about TESTING

Lorem ipsum something dolar emet. Yup.
"""
        self.conf = {}
        self.root_node = {}
        self.rootpath = '/home/place/'
        self.path = "parent/topic.md"
        self.meta = None
        open_name = 'eh.topic.open'
        self.patch1 = mock.patch(
            open_name, mock.mock_open(
                read_data=self.good_data))
        self.open_mock = self.patch1.start()
        self.topic = top.Topic(
            self.conf, self.root_node, self.rootpath, self.path)
        self.good_graph = {
            constants.PARENT_KEY: {
                "parent": { constants.TOPIC_KEY: ["poop"] }
            },
            "parent": { constants.TOPIC_KEY: ["poop"] }
        }
        self.good_graph_no_parents = {
            constants.PARENT_KEY: { },
            constants.TOPIC_KEY: ["poop"]
        }

    def tearDown(self):
        super(TestTopic, self).tearDown()
        mock.patch.stopall()

    def test_create_topic(self):
        self.assertIsNotNone(self.topic)

    def test_create_topic_removed_preamble(self):
        text_without_top_line = "\n".join(self.good_data.splitlines()[1:])
        self.assertEqual(len(self.topic.text), len(text_without_top_line))

    def test_create_topic_meta_correct(self):
        self.assertEqual(self.topic.meta[0], 'testing')

    def test_create_topic_subject_correct(self):
        self.assertEqual(self.topic.summary, 'This is test contents')

    def test_create_topic_key_exists(self):
        self.assertIsNotNone(self.topic.key)

    def test_create_topic_invalid_root_raises(self):
        with self.assertRaises(exc.TopicStoreInvalidRoot):
            topic = top.Topic(
                self.conf, None, self.rootpath, self.path)
        with self.assertRaises(exc.TopicStoreInvalidRoot):
            topic = top.Topic(
                self.conf, "poop", self.rootpath, self.path)
        with self.assertRaises(exc.TopicStoreInvalidRoot):
            topic = top.Topic(
                self.conf, 2, self.rootpath, self.path)
        with self.assertRaises(exc.TopicStoreInvalidRoot):
            topic = top.Topic(
                self.conf, 2.0, self.rootpath, self.path)
        with self.assertRaises(exc.TopicStoreInvalidRoot):
            topic = top.Topic(
                self.conf, 0, self.rootpath, self.path)
        with self.assertRaises(exc.TopicStoreInvalidRoot):
            topic = top.Topic(
                self.conf, ['asdf'], self.rootpath, self.path)
        with self.assertRaises(exc.TopicStoreInvalidRoot):
            topic = top.Topic(
                self.conf, ('asdf',), self.rootpath, self.path)

    def test_create_topic_invalid_rootpath_raises(self):
        with self.assertRaises(exc.TopicInvalidRootPath):
            topic = top.Topic(
                self.conf, {}, None, self.path)
        with self.assertRaises(exc.TopicInvalidRootPath):
            topic = top.Topic(
                self.conf, {}, 1.0, self.path)
        with self.assertRaises(exc.TopicInvalidRootPath):
            topic = top.Topic(
                self.conf, {}, 1, self.path)
        with self.assertRaises(exc.TopicInvalidRootPath):
            topic = top.Topic(
                self.conf, {}, 0, self.path)
        with self.assertRaises(exc.TopicInvalidRootPath):
            topic = top.Topic(
                self.conf, {}, ['asdf'], self.path)
        with self.assertRaises(exc.TopicInvalidRootPath):
            topic = top.Topic(
                self.conf, {}, {'asdf':'asdf'}, self.path)
        with self.assertRaises(exc.TopicInvalidRootPath):
            topic = top.Topic(
                self.conf, {}, ('asdf',), self.path)

    def test_is_topic(self):
        self.assertTrue(self.topic.is_topic('parent/topic'))
        self.assertFalse(self.topic.is_topic('topic'))
        self.assertFalse(self.topic.is_topic('parent topic'))
        self.assertFalse(self.topic.is_topic(None))

    def test_shortkey(self):
        self.assertTrue(self.topic.shortkey == 'topic')

    def test_remove_comment_preamble(self):
        text_top_line = self.good_data.splitlines()[0]
        self.assertEquals(
            top.Topic.remove_comment_preamble(text_top_line),
            text_top_line[len(constants.COMMENT_PREAMBLE)+1:])

    def test_split_meta_from_summary(self):
        text_top_line = self.good_data.splitlines()[0]
        cleaned = top.Topic.remove_comment_preamble(text_top_line)
        meta, summary = top.Topic.split_meta_from_summary(cleaned)

        self.assertEquals(['testing'], meta)
        self.assertEquals('This is test contents', summary)

    def test_check_comment_format(self):
        self.assertTrue(top.Topic.check_comment_format(self.good_data))
        self.assertFalse(top.Topic.check_comment_format(
            constants.COMMENT_PREAMBLE + " missing meta tags"))
        self.assertFalse(top.Topic.check_comment_format(
            constants.COMMENT_PREAMBLE + " (missing, summary)"))
        self.assertFalse(top.Topic.check_comment_format(
            constants.COMMENT_PREAMBLE + " () empty meta"))
        self.assertFalse(top.Topic.check_comment_format(None))

    def test_parse_topic_contents(self):
        with mock.patch(
                'eh.topic.open',
                mock.mock_open(read_data=self.good_data)) as mock_open:
            meta, summary, text = top.Topic.parse_topic_contents(
                self.conf, self.root_node, self.rootpath, self.path)
            self.assertEquals(['testing'], meta)
            self.assertEquals('This is test contents', summary)

            text_without_top_line = "\n".join(self.good_data.splitlines()[1:])
            self.assertEquals(text_without_top_line, text)

    @unittest.skip("TODO: learn to mock missing files")
    def test_parse_topic_contents_not_found(self):
        with mock.patch(
                'eh.topic.open',
                mock.mock_open(read_data=None)) as mock_open:
            meta, summary, text = top.Topic.parse_topic_contents(
                self.conf, self.root_node, self.rootpath, self.path)
            self.assertIsNone(meta)
            self.assertIsNone(summary)
            self.assertIsNone(text)

    def test_parse_topic_contents_invalid_preamble_raises(self):
        bad = """[/]: # (testing) This is test contents
# Something about TESTING

Lorem ipsum something dolar emet. Yup.
"""
        with mock.patch(
                'eh.topic.open',
                mock.mock_open(read_data=bad)) as mock_open:
            with self.assertRaises(exc.TopicError):
                top.Topic.parse_topic_contents(
                    self.conf, self.root_node, self.rootpath, self.path)

    def test_parse_topic_contents_missing_preamble_raises(self):
        bad = """(testing) This is test contents
# Something about TESTING

Lorem ipsum something dolar emet. Yup.
"""
        with mock.patch(
                'eh.topic.open',
                mock.mock_open(read_data=bad)) as mock_open:
            with self.assertRaises(exc.TopicError):
                top.Topic.parse_topic_contents(
                    self.conf, self.root_node, self.rootpath, self.path)

    def test_parse_topic_contents_missing_meta_raises(self):
        bad = """[//]: # This is test contents
# Something about TESTING

Lorem ipsum something dolar emet. Yup.
"""
        with mock.patch(
                'eh.topic.open',
                mock.mock_open(read_data=bad)) as mock_open:
            with self.assertRaises(exc.TopicError):
                top.Topic.parse_topic_contents(
                    self.conf, self.root_node, self.rootpath, self.path)

    def test_map_root(self):
        root = {}
        top.Topic.map_topic_path_to_root_node({}, root, self.path, 'poop')
        self.assertEquals(self.good_graph, root)

    def test_repr(self):
        self.assertEquals(
            "parent/topic 65 chars ['testing'] This is test contents",
            str(self.topic))

    def test_map_root(self):
        root = {}
        path = 'topic.md'
        top.Topic.map_topic_path_to_root_node({}, root, path, 'poop')
        self.assertEquals(self.good_graph_no_parents, root)
