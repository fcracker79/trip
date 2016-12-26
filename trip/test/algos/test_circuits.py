import unittest
from unittest import mock

from trip import domain
from trip.algos import circuits


class TestCircuits(unittest.TestCase):
    def test_simple(self):
        node_a = mock.create_autospec(domain.VersionNode)
        node_b = mock.create_autospec(domain.VersionNode)
        node_c = mock.create_autospec(domain.VersionNode)
        node_a.name = 'node_a'
        node_b.name = 'node_b'
        node_c.name = 'node_c'
        node_a.dependencies = [node_b]
        node_b.dependencies = [node_c]
        node_c.dependencies = [node_a]
        result = circuits.find_circuits(node_a)
        self.assertEqual(1, len(result))
        self.assertEqual([node_a, node_b, node_c, node_a], result[0])
        result = circuits.find_circuits(node_b)
        self.assertEqual(1, len(result))
        self.assertEqual([node_b, node_c, node_a, node_b], result[0])

    def test_no_cycle(self):
        node_a = mock.create_autospec(domain.VersionNode)
        node_b = mock.create_autospec(domain.VersionNode)
        node_c = mock.create_autospec(domain.VersionNode)
        node_a.name = 'node_a'
        node_b.name = 'node_b'
        node_c.name = 'node_c'
        node_a.dependencies = [node_b]
        node_b.dependencies = [node_c]
        node_c.dependencies = []
        result = circuits.find_circuits(node_a)
        self.assertEqual(0, len(result))

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
        for n in (node_a, node_b, node_c, node_d):
            result = circuits.find_circuits(n)
            self.assertEqual(0, len(result))
        result = circuits.find_circuits(node_a, node_b, node_c, node_d)
        self.assertEqual(0, len(result))
