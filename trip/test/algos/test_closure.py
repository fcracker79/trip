import unittest
from unittest import mock

from trip import domain
from trip.algos import closure


class TestClosure(unittest.TestCase):
    def test_diamond(self):
        node_a = mock.create_autospec(domain.VersionNode)
        node_b = mock.create_autospec(domain.VersionNode)
        node_c = mock.create_autospec(domain.VersionNode)
        node_d = mock.create_autospec(domain.VersionNode)
        node_a.name = 'node_a'
        node_b.name = 'node_b'
        node_c.name = 'node_c'
        node_d.name = 'node_d'
        node_a.dependencies = [node_b, node_c]
        node_b.dependencies = [node_d]
        node_c.dependencies = [node_d]
        node_d.dependencies = []
        self.assertEqual({node_a, node_b, node_c, node_d}, closure.get_closure(node_a))
        self.assertEqual({node_b, node_d}, closure.get_closure(node_b))
        self.assertEqual({node_c, node_d}, closure.get_closure(node_c))
        self.assertEqual({node_d}, closure.get_closure(node_d))
