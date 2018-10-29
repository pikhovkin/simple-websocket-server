from __future__ import print_function

import signal
import sys
import ssl
from optparse import OptionParser

from simple_websocket_server import WebSocket, WebSocketServer


class SimpleEcho(WebSocket):
    def handle(self):
        self.send_message(self.data)


class SimpleChat(WebSocket):
    def handle(self):
        for client in clients:
            if client != self:
                client.send_message(self.address[0] + u' - ' + self.data)

    def connected(self):
        print(self.address, 'connected')
        for client in clients:
            client.send_message(self.address[0] + u' - connected')
        clients.append(self)

    def handle_close(self):
        clients.remove(self)
        print(self.address, 'closed')
        for client in clients:
            client.send_message(self.address[0] + u' - disconnected')


if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options]', version='%prog 1.0')
    parser.add_option('--host', default='', type='string', action='store', dest='host', help='hostname (localhost)')
    parser.add_option('--port', default=8000, type='int', action='store', dest='port', help='port (8000)')
    parser.add_option('--example', default='echo', type='string', action='store', dest='example', help='echo, chat')
    parser.add_option('--ssl', default=0, type='int', action='store', dest='ssl', help='ssl (1: on, 0: off (default))')
    parser.add_option('--cert', default='./cert.pem', type='string', action='store', dest='cert',
                      help='cert (./cert.pem)')
    parser.add_option('--key', default='./key.pem', type='string', action='store', dest='key', help='key (./key.pem)')
    parser.add_option('--ver', default=ssl.PROTOCOL_TLSv1, type=int, action='store', dest='ver', help='ssl version')

    (options, args) = parser.parse_args()

    clients = []

    cls = SimpleEcho
    if options.example == 'chat':
        cls = SimpleChat

    sslopts = {}
    if options.ssl == 1:
        sslopts = dict(certfile=options.cert, keyfile=options.key, ssl_version=options.ver)

    server = WebSocketServer(options.host, options.port, cls, **sslopts)

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    server.serve_forever()
