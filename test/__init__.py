from __future__ import unicode_literals

from splinter import Browser
from unittest import TestCase
from multiprocessing import Process
from werkzeug.serving import make_server
from web import app


class TestSlowSplinter(TestCase):
    def setUp(self):
        server = make_server('0.0.0.0', 65432, app)
        thread = Process(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        self.browser = Browser()

    def tearDown(self):
        self.browser.quit()

    def test_slow_splinter(self):
        for x in xrange(1, 4):
            self.browser.visit('http://localhost:65432/')
