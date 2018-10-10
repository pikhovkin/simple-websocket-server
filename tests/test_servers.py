# coding: utf-8
from __future__ import print_function

import sys
from threading import Thread
from contextlib import contextmanager
import unittest

VER = sys.version_info[0]
if VER >= 3:
    from queue import Queue
else:
    from Queue import Queue

from websocket import create_connection

from simple_websocket_server import WebSocketServer, WebSocket


HOST = 'localhost'
PORT = 38200


class SimpleEcho(WebSocket):
    def handle(self):
        self.send_message(self.data)


class WSServer(WebSocketServer):
    request_queue_size = 1000


class TestWebSocketServer(unittest.TestCase):
    @staticmethod
    @contextmanager
    def server(server_cls, handler_cls):
        server = server_cls(HOST, PORT, handler_cls)
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        yield server
        server.close()

    def test_load(self):
        class Worker(Thread):
            def __init__(self, q_input, q_output):
                self.q_input = q_input
                self.q_output = q_output

                super(Worker, self).__init__()

            def run(self):
                tasks = self.q_input.get()
                while tasks > 0:
                    tasks -= 1

                    ws = create_connection('ws://{}:{}'.format(HOST, PORT))
                    ws.send('$äüö^')

                    self.q_output.put(ws.recv())

                    ws.close()

                self.q_input.task_done()

        q_input = Queue()
        q_output = Queue()

        CLIENTS = 500
        MESSAGES = 10

        for r in range(CLIENTS):
            q_input.put(MESSAGES)

        with self.server(WSServer, SimpleEcho):
            for r in range(CLIENTS):
                w = Worker(q_input, q_output)
                w.setDaemon(True)
                w.start()

            q_input.join()
