import unittest

class DispatcherCase(unittest.TestCase):
    def test_prefetch(self):
        from otto.publisher import Dispatcher

        test = []
        class Mapper(object):
            def __init__(self, id=None):
                test.append(id)

            def resolve(self, path):
                test.append(path)

        def controller(*args):
            test.extend(*args)

        dispatcher = Dispatcher("/:id/*/:name", controller=controller, mapper=Mapper)
        matchdict = {'': 'boo', 'id': 'foo', 'name': 'bar'}
        controller = dispatcher.dispatch(matchdict)
        self.assertEqual(test, ['foo', 'boo'])
        self.assertEqual(matchdict, {'name': 'bar'})
