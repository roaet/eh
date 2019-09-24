import mock
import unittest2 as unittest

from eh import constants
from eh import exceptions as exc
from eh.tests import base_test as base
from eh import topic as top


cheatsheet_header = """---
title: React.js
layout: 2017/sheet   # 'default' | '2017/sheet'

# Optional:
category: React
updated: 2017-08-30       # To show in the updated list
ads: false                # Add this to disable ads
weight: -5                # lower number = higher in related posts list
deprecated: true          # Don't show in related posts
deprecated_by: /enzyme    # Point to latest version
prism_languages: [vim]    # Extra syntax highlighting
intro: |
  This is some *Markdown* at the beginning of the article.
tags:
  - WIP
  - Featured
---"""

cheatsheet_invalid = cheatsheet_header[:-3] + """
# Special pages:
# (don't set these for cheatsheets)
type: home                # home | article | error
og_type: website          # opengraph type
---"""

cheatsheet_missing_title = """---
category: React
intro: |
  This is some *Markdown* at the beginning of the article.
tags:
  - WIP
  - Featured
---"""


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

    def test_parse_topic_contents_not_found_returns_nones(self):
        with mock.patch(
                'eh.topic.open',
                mock.mock_open(read_data=None)) as mock_open:
            mock_open.side_effect = IOError
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

    def test_cheatsheet_format_good(self):
        data = cheatsheet_header.split("\n")
        self.assertTrue(top.Topic.check_cheatsheet_format(data))
        data = cheatsheet_invalid.split("\n")
        self.assertFalse(top.Topic.check_cheatsheet_format(data))

    def test_cheatsheet_conversion(self):
        data = cheatsheet_header.split("\n")
        meta, summary, text = top.Topic.parse_cheatsheet_format(data)
        self.assertEqual(['WIP', 'Featured', "React"], meta)
        self.assertEqual(
            "This is some *Markdown* at the beginning of the article.",
            summary.strip())
        self.assertEqual("", text)

    def test_cheatsheet_title_missing(self):
        data = cheatsheet_missing_title.split("\n")
        self.assertFalse(top.Topic.check_cheatsheet_format(data))

    def test_determine_format(self):
        data = cheatsheet_header.split("\n")
        self.assertEqual("cheatsheet", top.Topic.determine_format(data))
        data = self.good_data.split("\n")
        self.assertEqual("eh", top.Topic.determine_format(data))
        with self.assertRaises(exc.TopicError):
            data = cheatsheet_missing_title.split("\n")
            top.Topic.determine_format(data)

