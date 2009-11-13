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
        route1 = Route('/test')
        route2 = Route('/:test')
        route3 = Route('/no-match/:test')
        route4 = Route('/te:match')
        map(router.connect, (route1, route2, route3, route4))
        matches = tuple(router('/test'))
        self.assertEqual(len(matches), 3)
        self.assertEqual(matches[0].route, route1)
        self.assertEqual(matches[1].route, route2)
        self.assertEqual(matches[2].route, route4)

class RouteCase(unittest.TestCase):
    def test_asterisk(self):
        from otto.router import Route
        route1 = Route('static*subpath')
        match1 = route1.match('/static/style/helper.css')
        self.assertTrue(match1 is not None)
        self.assertEqual(match1['subpath'], (u'style', u'helper.css'))

    def test_asterisk_and_name(self):
        from otto.router import Route
        route1 = Route("/repr/*/:name")
        match1 = route1.match('/repr/math/pi')
        self.assertTrue(match1 is not None)
        self.assertEqual(match1['*'], (u'math',))
        self.assertEqual(match1['name'], u'pi')
