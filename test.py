try:
    import unittest2 as unittest
except ImportError:
    import unittest

from app import health

class SimpleTest(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(health(), 'healthy')
