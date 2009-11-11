import unittest

class RouterCase(unittest.TestCase):

    def test_empty_routes(self):
        from otto.router import Router
        router = Router()
        match = router('/path').next
        self.assertRaises(StopIteration, match)

    def test_iteration(self):
        from otto.router import Router
        router = Router()

        def controller(environ, start_response):
            pass

        route1 = router.connect('/test', controller)
        route2 = router.connect('/:test', controller)
        route3 = router.connect('/no-match/:test', controller)
        route4 = router.connect('/te:match', controller)

        matches = tuple(router('/test'))
        self.assertEqual(len(matches), 3)

        self.assertEqual(matches[0].route, route1)
        self.assertEqual(matches[1].route, route2)
        self.assertEqual(matches[2].route, route4)
