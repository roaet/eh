import mock

from eh import constants
from eh import exceptions as exc
from eh.tests import base_test as base
from eh import topic_store as ts


class TopicMock(mock.Mock):
    def __init__(self, *args, **kwargs):
        super(TopicMock, self).__init__(*args, **kwargs)
        self.topic = 'topic'

    def is_topic(self, topic_key):
        return topic_key == self.topic


class TestTopicStore(base.TestCase):
    def setUp(self):
        super(TestTopicStore, self).setUp()
        self.conf = {
            "stuff": True
        }
        self.topics = {
            "topic1": {},
            "parent": {
                "topic2": {},
                "topic3": {},
            }
        }
        self.topic2 = TopicMock()
        self.topic2.topic = "parent/topic2"
        self.topic1 = TopicMock()
        self.topic1.topic = "topic1"
        self.root = {
            constants.PARENT_KEY: ["parent"],
            constants.TOPIC_KEY: [self.topic1],
            "parent": { constants.TOPIC_KEY: [self.topic2] }
        }

    def tearDown(self):
        super(TestTopicStore, self).tearDown()
        mock.patch.stopall()

    def test_create_store(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())

    def test_invalid_topic_format_continues(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        with mock.patch('eh.topic.Topic.parse_topic_contents') as mock_parse:
            mock_parse.side_effect = exc.TopicError
            store._parse_topics({}, {}, "/", ['a', 'b'])

    def test_get_topic_valid_path(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        store.root_node = self.root
        topic = store.get_topic('parent/topic2')
        self.assertIsNotNone(topic)

    def test_get_topic_simple_path(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        store.root_node = self.root
        topic = store.get_topic('topic1')
        self.assertIsNotNone(topic)

    def test_get_topic_invalid_path(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        store.root_node = self.root
        topic = store.get_topic('topic2')
        self.assertIsNone(topic)

    def test_default_store_does_not_update(self):
        store = ts.TopicStore({}, "", 'test_store')
        ret = store.update()
        self.assertIsNone(ret)

    def test_gather_topics_empty_dir(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        with mock.patch('os.listdir', return_value=[]) as list_mock:
            topics = store._gather_topics(self.conf, '/', '/')
            self.assertEquals(0, len(topics))
            self.assertEquals(0, store.topic_count())
            self.assertIsNotNone(topics)

    def test_gather_topics_one_item_no_ext(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        with mock.patch('os.listdir', return_value=["thing"]) as list_mock:
            topics = store._gather_topics(self.conf, '/', '/')
            self.assertEquals(0, len(topics))
            self.assertIsNotNone(topics)

    def test_gather_topics_one_item_with_ext(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        with mock.patch('os.listdir', return_value=["thing.md"]) as list_mock:
            topics = store._gather_topics(self.conf, '/', '/')
            self.assertEquals(1, len(topics))
            self.assertIsNotNone(topics)

    def test_gather_topics_removes_mainpath(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        with mock.patch('os.listdir', return_value=["thing.md"]) as list_mock:
            topics = store._gather_topics(self.conf, '/a/b/c', '/a/b/c/d')
            self.assertEquals(1, len(topics))
            self.assertIsNotNone(topics)
            self.assertTrue('/a/b/c' not in topics[0])

    def test_gather_topics_mixed_items(self):
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        mixed_list = ["poop", "thing.md"]
        with mock.patch('os.listdir', return_value=mixed_list) as list_mock:
            topics = store._gather_topics(self.conf, '/', '/')
            self.assertEquals(1, len(topics))
            self.assertIsNotNone(topics)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    def test_gather_topics_with_directory(
            self, mock_listdir, mock_isdir):
        mixed_list = ["a_dir", "thing.md"]
        mock_isdir.side_effect = lambda x : x == '/a_dir'
        mock_listdir.side_effect = (
            lambda x : mixed_list if x != 'a_dir' else 'thing2.md')
        store = ts.TopicStore({}, "", 'test_store')
        self.assertEquals(0, store.topic_count())

        topics = store._gather_topics(self.conf, '/', '/')
        self.assertEquals(2, len(topics))
        self.assertIsNotNone(topics)

    @mock.patch('eh.topic.Topic', new_callable=TopicMock)
    def test_parse_topics_returned_topics_equals_paths(
            self, mock_topic):
        store = ts.TopicStore(self.conf, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        root = {}
        main_path = '/'
        paths = [
            'path1',
            'path2'
        ]
        topics = store._parse_topics(self.conf, root, main_path, paths)
        self.assertEquals(len(paths), len(topics))
        self.assertEquals(len(paths), mock_topic.call_count)

    @mock.patch('eh.topic.Topic', new_callable=TopicMock)
    def test_parse_topics_empty_paths_okay(
            self, mock_topic):
        store = ts.TopicStore(self.conf, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        root = {}
        main_path = '/'
        paths = []
        topics = store._parse_topics(self.conf, root, main_path, paths)
        self.assertEquals(len(paths), len(topics))
        self.assertEquals(len(paths), mock_topic.call_count)

    @mock.patch('eh.topic.Topic.parse_topic_contents')
    def test_parse_topics_invalid_root_fails(self, mock_ptc):
        mock_ptc.return_value = (None, None, None)
        store = ts.TopicStore(self.conf, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        main_path = '/'
        paths = [
            'path1',
            'path2'
        ]
        for _t in [None, "", []]:
            with self.assertRaises(exc.TopicStoreInvalidRoot):
                topics = store._parse_topics(self.conf, _t, main_path, paths)

    def test_parse_topics_invalid_path_fails(self):
        store = ts.TopicStore(self.conf, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        root = {}
        paths = [
            'path1',
            'path2'
        ]
        for _t in [None, "", [], {}]:
            with self.assertRaises(exc.TopicInvalidRootPath):
                topics = store._parse_topics(self.conf, root, _t, paths)

    def test_get_filtered_parent_keys(self):
        parent_node = {
            constants.PARENT_KEY: "something",
            constants.TOPIC_KEY: "something else",
            "Some key": "another something",
        }
        filtered = ts.TopicStore.get_filtered_parent_keys(parent_node)
        self.assertEquals(1, len(filtered))
        self.assertFalse(constants.PARENT_KEY in filtered)
        self.assertFalse(constants.TOPIC_KEY in filtered)
        self.assertTrue("Some key" in filtered)

    def test_get_filtered_parent_keys_empty_dict_okay(self):
        parent_node = {}
        filtered = ts.TopicStore.get_filtered_parent_keys(parent_node)
        self.assertEquals(0, len(filtered))

    def test_get_filtered_parent_keys_weird_values(self):
        for _t in [None, [], "asdf"]:
            with self.assertRaises(exc.InvalidValue):
                ts.TopicStore.get_filtered_parent_keys(_t)

    def test_get_topics_for_parent_returns_root_with_none(self):
        store = ts.TopicStore(self.conf, "", 'test_store')
        store.root_node = self.root
        self.assertEquals(0, store.topic_count())
        with mock.patch('eh.topic_store.TopicStore._parents') as mock_parents:
            mock_parents.return_value = {}
            root_ret = store.get_topics_for_parent(None)
            self.assertEquals(([self.topic1], ['parent']), root_ret)

    def test_get_topics_for_parent_returns_none_when_not_found(self):
        store = ts.TopicStore(self.conf, "", 'test_store')
        self.assertEquals(0, store.topic_count())
        with mock.patch('eh.topic_store.TopicStore._parents') as mock_parents:
            mock_parents.return_value = {}
            ret = store.get_topics_for_parent("woo")
            self.assertEquals((None, None), ret)

    def test_has_parent(self):
        store = ts.TopicStore(self.conf, "", 'test_store')
        store.root_node = self.root
        self.assertTrue(store.has_parent("parent"))
        self.assertFalse(store.has_parent("topic1"))
        self.assertFalse(store.has_parent("nothing"))

    def test_parents(self):
        store = ts.TopicStore(self.conf, "", 'test_store')
        store.root_node = self.root
        self.assertIsNotNone(store._parents())
        self.assertEquals(1, len(store._parents()))

    @mock.patch('eh.topic.Topic.is_topic')
    def test_has_topic(self, mock_is_topic):
        store = ts.TopicStore(self.conf, "", 'test_store')
        t1 = TopicMock()
        t1.topic = 'poo'

        store._topics = [t1]
        self.assertTrue(store.has_topic('poo'))
        self.assertFalse(store.has_topic('foo'))
