from tempfile import TemporaryDirectory
from unittest import mock

from django.test import TestCase

from documents.parsers import get_parser_class


class TestParserDiscovery(TestCase):

    @mock.patch("documents.parsers.document_consumer_declaration.send")
    def test__get_parser_class_1_parser(self, m, *args):
        class DummyParser(object):
            pass

        m.return_value = (
            (None, lambda _: {"weight": 0, "parser": DummyParser}),
        )

        self.assertEqual(
            get_parser_class("doc.pdf"),
            DummyParser
        )

    @mock.patch("documents.parsers.document_consumer_declaration.send")
    def test__get_parser_class_n_parsers(self, m, *args):

        class DummyParser1(object):
            pass

        class DummyParser2(object):
            pass

        m.return_value = (
            (None, lambda _: {"weight": 0, "parser": DummyParser1}),
            (None, lambda _: {"weight": 1, "parser": DummyParser2}),
        )

        self.assertEqual(
            get_parser_class("doc.pdf"),
            DummyParser2
        )

    @mock.patch("documents.parsers.document_consumer_declaration.send")
    def test__get_parser_class_0_parsers(self, m, *args):
        m.return_value = ((None, lambda _: None),)
        with TemporaryDirectory() as tmpdir:
            self.assertIsNone(
                get_parser_class("doc.pdf")
            )
