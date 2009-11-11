import unittest

class RouterCase(unittest.TestCase):

    def test_empty_routes(self):
        from otto.router import Router
        router = Router()
        match = router('/path').next
        self.assertRaises(StopIteration, match)
