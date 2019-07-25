from ConfigObject import ConfigObject
import mock

from eh.tests import base_test as base
from eh import topic_manager as tm
from eh import topic_store as ts


class StoreMock(mock.Mock):
    def __init__(self, *args, **kwargs):
        super(StoreMock, self).__init__(*args, **kwargs)
        self.topic_name = 'topic'

    def has_topic(self, topic):
        if topic == 'pass':
            return True
        return False

    def get_topic(self, topic):
        if topic == 'pass':
            return self.topic_name
        return None

    def has_parent(self, parent):
        if parent == 'pass':
            return True
        return False

    def get_topics_for_parent(self, parent):
        if parent == 'pass' or parent == "":
            return [self.topic_name], ['parent']
        return [], []


class TestTopicManager(base.TestCase):
    def setUp(self):
        super(TestTopicManager, self).setUp()
        self.test_conf = ConfigObject()
        self.test_conf['topic_stores'] = {
            'thing': 'some/directory'
        }
        self.patch1 = mock.patch(
            'eh.topic_store.TopicStore', new_callable=StoreMock)
        self.store = self.patch1.start()
        self.store.topic_name = 'topic1'
        self.patch2 = mock.patch(
            'eh.topic_store.TopicStore', new_callable=StoreMock)
        self.store2 = self.patch2.start()
        self.store2.topic_name = 'topic2'

    def tearDown(self):
        mock.patch.stopall()

    def test_initialize_empty_conf_okay(self):
        manager = tm.TopicManager({})
        self.assertEqual(0, len(manager.topic_stores))

    def test_initialize_none_conf_okay(self):
        manager = tm.TopicManager(None)
        self.assertEqual(0, len(manager.topic_stores))

    def test_initialize_with_test_okay(self):
        manager = tm.TopicManager(self.test_conf)
        self.assertEqual(1, len(manager.topic_stores))

    def test_has_topic_matches_internal_store(self):
        manager = tm.TopicManager(self.test_conf)
        self.assertTrue(manager.has_topic('pass'))
        self.assertFalse(manager.has_topic('fail'))

    def test_has_topic_no_stores_has_no_match(self):
        manager = tm.TopicManager(self.test_conf)
        manager.topic_stores = []
        self.assertFalse(manager.has_topic('pass'))
        manager.topic_stores = [self.store]
        self.assertTrue(manager.has_topic('pass'))

    def test_get_topic_matches_internal_store(self):
        manager = tm.TopicManager(self.test_conf)
        self.assertIsNotNone(manager.get_topic('pass'))
        self.assertIsNone(manager.get_topic('fail'))

    def test_get_topic_no_stores_has_no_match(self):
        manager = tm.TopicManager(self.test_conf)
        manager.topic_stores = []
        self.assertIsNone(manager.get_topic('pass'))
        manager.topic_stores = [self.store]
        self.assertIsNotNone(manager.get_topic('pass'))

    def test_has_parent_matches_internal_store(self):
        manager = tm.TopicManager(self.test_conf)
        self.assertTrue(manager.has_parent('pass'))
        self.assertFalse(manager.has_parent('fail'))

    def test_has_parent_no_stores_has_no_match(self):
        manager = tm.TopicManager(self.test_conf)
        manager.topic_stores = []
        self.assertFalse(manager.has_parent('pass'))
        manager.topic_stores = [self.store]
        self.assertTrue(manager.has_parent('pass'))

    def test_get_topics_for_parent_matches_internal_store(self):
        manager = tm.TopicManager(self.test_conf)
        ret, pret = manager.get_topics_for_parent('pass')
        self.assertEqual(1, len(ret))
        self.assertEqual(1, len(pret))

    def test_get_topics_for_parent_no_store(self):
        manager = tm.TopicManager(self.test_conf)
        manager.topic_stores = []
        ret, pret = manager.get_topics_for_parent('pass')
        self.assertEqual(0, len(ret))
        self.assertEqual(0, len(pret))

        manager.topic_stores = [self.store]
        ret, pret = manager.get_topics_for_parent('pass')
        self.assertEqual(1, len(ret))
        self.assertEqual(1, len(pret))

    def test_get_topics_for_parent_multiple_stores(self):
        manager = tm.TopicManager(self.test_conf)
        manager.topic_stores = [self.store, self.store2]
        ret, pret = manager.get_topics_for_parent('pass')
        self.assertEqual(2, len(ret))
        self.assertEqual(2, len(pret))

    def test_get_root_list(self):
        manager = tm.TopicManager(self.test_conf)
        manager.topic_stores = [self.store, self.store2]
        ret, pret = manager.get_root_list()
        self.assertEqual(2, len(ret))
        self.assertEqual(2, len(pret))

    def test_get_root_list_empty_with_no_stores(self):
        manager = tm.TopicManager(self.test_conf)
        manager.topic_stores = []
        ret, pret = manager.get_root_list()
        self.assertEqual(0, len(ret))
        self.assertEqual(0, len(pret))
