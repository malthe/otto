import unittest

class RouterCase(unittest.TestCase):

    def test_empty_routes(self):
        from otto.router import Router
        router = Router()
        match = router('/path').next
        self.assertRaises(StopIteration, match)

    def test_iteration(self):
        from otto.router import Router
        from otto.router import Route
        router = Router()

        route1 = router.connect(Route('/test'))
        route2 = router.connect(Route('/:test'))
        route3 = router.connect(Route('/no-match/:test'))
        route4 = router.connect(Route('/te:match'))

        matches = tuple(router('/test'))
        self.assertEqual(len(matches), 3)

        self.assertEqual(matches[0].route, route1)
        self.assertEqual(matches[1].route, route2)
        self.assertEqual(matches[2].route, route4)
