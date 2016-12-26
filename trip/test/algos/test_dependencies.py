import unittest
from unittest import mock

from trip import domain
from trip.algos import dependencies


class TestDependencies(unittest.TestCase):
    def _new_node(self, version_name: str, version_number: str, dependencies: list=None):
        node = mock.create_autospec(domain.VersionNode)
        node.version_name = version_name
        node.version_number = version_number
        if dependencies:
            node.dependencies = dependencies
        return node

    def test(self):
        lib_a_1_0_0 = self._new_node('lib_a', '1.0.0')
        lib_a_2_0_0 = self._new_node('lib_a', '2.0.0')
        lib_a_3_0_0 = self._new_node('lib_a', '3.0.0')

        lib_b_1_0_0 = self._new_node('lib_b', '1.0.0')
        lib_b_2_0_0 = self._new_node('lib_b', '2.0.0')
        lib_b_3_0_0 = self._new_node('lib_b', '3.0.0')

        lib_c_1_0_0 = self._new_node('lib_c', '1.0.0')
        lib_c_2_0_0 = self._new_node('lib_c', '2.0.0')
        lib_c_3_0_0 = self._new_node('lib_c', '3.0.0')

        lib_a_1_0_0.dependencies = [lib_b_1_0_0, lib_b_2_0_0]
        lib_a_2_0_0.dependencies = [lib_b_3_0_0]
        lib_a_3_0_0.dependencies = [lib_b_3_0_0]

        lib_b_1_0_0.dependencies = [lib_c_1_0_0]
        lib_b_2_0_0.dependencies = [lib_c_2_0_0, lib_c_3_0_0]
        lib_b_3_0_0.dependencies = [lib_c_2_0_0, lib_c_3_0_0]

        lib_c_1_0_0.dependencies = []
        lib_c_2_0_0.dependencies = []
        lib_c_3_0_0.dependencies = []

        requirements = {
            'lib_a':  [lib_a_1_0_0, lib_a_2_0_0, lib_a_3_0_0],
            'lib_b': [lib_b_1_0_0, lib_b_2_0_0],
            'lib_c': [lib_c_3_0_0]
        }
        final_dependencies = dependencies.get_dependencies(requirements)
        for x in final_dependencies:
            print([y.version_name + '-' + y.version_number for y in x])
