#!/usr/bin/env python

import os
import sys
from  wsgiref import simple_server

def run():
    here = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, here)
    from fluxbin import app
    simple_server.make_server('', 8080, app).serve_forever()

if __name__ == '__main__':
    run()
