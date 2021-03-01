#!/usr/bin/python
import os
import sys
from nlpsim.nlpsim_api import *


if __name__ == '__main__':
    print('Calling API')
    initialise(os.path.dirname(os.path.realpath(__file__)))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=False)