#!/usr/bin/env python3

import unittest
import app


class TestHello(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_hello(self):
        response = self.app.get('/')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.data, b'Hello World!\n')

    def test_hello_hello(self):
        response = self.app.get('/hello/')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.data, b'Hello World!\n')

    def test_hello_name(self):
        name = 'Simon'
        response = self.app.get(f'/hello/{name}')
        self.assertEqual(response.status, '200 OK')
        self.assertIn(bytearray(name, 'utf-8'), response.data)

    def test_new_route(self):
        name = 'Simon'
        response = self.app.get(f'/feature/{name}')
        self.assertEqual(response.status, '200 OK')


if __name__ == '__main__':
    unittest.main()
