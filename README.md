# A simple WebSocket server

[![CircleCI](https://img.shields.io/circleci/project/github/pikhovkin/simple-websocket-server.svg)](https://circleci.com/gh/pikhovkin/simple-websocket-server)
[![PyPI](https://img.shields.io/pypi/v/simple-websocket-server.svg)](https://pypi.org/project/simple-websocket-server/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple-websocket-server.svg)
[![PyPI - License](https://img.shields.io/pypi/l/simple-websocket-server.svg)](./LICENSE)

Based on [simple-websocket-server](https://github.com/dpallot/simple-websocket-server).

- RFC 6455 (All latest browsers)
- TLS/SSL out of the box
- Passes Autobahns Websocket Testsuite
- Support for Python 2 and 3

#### Installation

    pip install simple-websocket-server

#### Echo Server Example

`````python
from simple_websocket_server import WebSocketServer, WebSocket


class SimpleEcho(WebSocket):
    def handle(self):
        # echo message back to client
        self.send_message(self.data)

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()
`````

Open *tests/websocket.html* and connect to the server.

#### Chat Server Example

`````python
from simple_websocket_server import WebSocketServer, WebSocket


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


clients = []

server = WebSocketServer('', 8000, SimpleChat)
server.serve_forever()
`````
Open multiple *tests/websocket.html* and connect to the server.

#### Want to get up and running faster?

There is an example which provides a simple echo and chat server

Echo Server

    python tests/example_server.py --example echo

Chat Server (open up multiple *tests/websocket.html* files)

    python tests/example_server.py --example chat

#### TLS/SSL Example

1) Generate a certificate with key

        openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

2) Run the secure TSL/SSL server (in this case the cert.pem file is in the same directory)

        python tests/example_server.py --example chat --ssl 1

3) Offer the certificate to the browser by serving *tests/websocket.html* through https.
The HTTPS server will look for cert.pem in the local directory.
Ensure the *tests/websocket.html* is also in the same directory to where the server is run.

        python tests/simple_https_server.py

4) Open a web browser to: *https://localhost:443/tests/websocket.html*

5) Change *ws://localhost:8000/* to *wss://localhost:8000* and click connect.

Note: if you are having problems connecting, ensure that the certificate is added in your browser against the exception *https://localhost:8000* or whatever host:port pair you want to connect to.

#### For the Programmers

connected: called when handshake is complete
 - self.address: TCP address port tuple of the endpoint

handle_close: called when the endpoint is closed or there is an error
 - self.address: TCP address port tuple of the endpoint

handle: gets called when there is an incoming message from the client endpoint
 - self.address: TCP address port tuple of the endpoint
 - self.opcode: the WebSocket frame type (STREAM, TEXT, BINARY)
 - self.data: bytearray (BINARY frame) or unicode string payload (TEXT frame)  
 - self.request: HTTP details from the WebSocket handshake (refer to BaseHTTPRequestHandler)

send_message: send some text or binary data to the client endpoint
 - sending data as a unicode object will send a TEXT frame
 - sending data as a bytearray object will send a BINARY frame

close: send close frame to endpoint

### Licensing

MIT
