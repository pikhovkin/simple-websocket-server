# coding: utf-8
from __future__ import print_function

from threading import Thread
from contextlib import contextmanager
import unittest

from websocket import create_connection, ABNF

from simple_websocket_server import WebSocketServer, WebSocket


class SimpleEcho(WebSocket):
    def handle(self):
        self.send_message(self.data)


class TestWebSocketServer(unittest.TestCase):
    @staticmethod
    @contextmanager
    def server(handler):
        server = WebSocketServer('localhost', 38200, handler)
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        yield server
        server.close()

    @staticmethod
    @contextmanager
    def client():
        ws = create_connection('ws://{}:{}'.format('localhost', 38200))
        yield ws
        ws.close()

    def test_echo(self):
        data = '$äüö^'
        with self.server(SimpleEcho):
            with self.client() as client:
                client.send(data)
                self.assertTrue(client.recv() == data)
