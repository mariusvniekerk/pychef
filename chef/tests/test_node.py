from unittest2 import TestCase, skip

from chef import Node
from chef.exceptions import ChefError
from chef.node import NodeAttributes
from chef.tests import ChefTestCase

class NodeAttributeTestCase(TestCase):
    def test_getitem(self):
        attrs = NodeAttributes([{'a': 1}])
        self.assertEqual(attrs['a'], 1)
    
    def test_setitem(self):
        data = {'a': 1}
        attrs = NodeAttributes([data], write=data)
        attrs['a'] = 2
        self.assertEqual(attrs['a'], 2)
        self.assertEqual(data['a'], 2)

    def test_getitem_nested(self):
         attrs = NodeAttributes([{'a': {'b': 1}}])
         self.assertEqual(attrs['a']['b'], 1)
    
    def test_set_nested(self):
        data = {'a': {'b': 1}}
        attrs = NodeAttributes([data], write=data)
        attrs['a']['b'] = 2
        self.assertEqual(attrs['a']['b'], 2)
        self.assertEqual(data['a']['b'], 2)
    
    def test_search_path(self):
        attrs = NodeAttributes([{'a': 1}, {'a': 2}])
        self.assertEqual(attrs['a'], 1)
    
    def test_search_path_nested(self):
        data1 = {'a': {'b': 1}}
        data2 = {'a': {'b': 2}}
        attrs = NodeAttributes([data1, data2])
        self.assertEqual(attrs['a']['b'], 1)
    
    def test_read_only(self):
        attrs = NodeAttributes([{'a': 1}])
        with self.assertRaises(ChefError):
            attrs['a'] = 2

class NodeTestCase(ChefTestCase):
    def setUp(self):
        super(NodeTestCase, self).setUp()
        self.node = Node('test_1')

    @skip('default and override attrs from roles not being sent')
    def test_default_attr(self):
        self.assertEqual(self.node.default['test_attr'], 'default')

    def test_normal_attr(self):
        self.assertEqual(self.node.normal['test_attr'], 'normal')

    @skip('default and override attrs from roles not being sent')
    def test_override_attr(self):
        self.assertEqual(self.node.override['test_attr'], 'override')

    # Switch these back to override later
    def test_composite_attr(self):
        self.assertEqual(self.node.attributes['test_attr'], 'normal')

    def test_getitem(self):
        self.assertEqual(self.node['test_attr'], 'normal')
